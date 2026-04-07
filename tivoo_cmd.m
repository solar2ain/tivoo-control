#import <Foundation/Foundation.h>
#import <IOBluetooth/IOBluetooth.h>

@interface TivooDelegate : NSObject <IOBluetoothRFCOMMChannelDelegate> {
    @public NSMutableData *responseData;
}
@end

@implementation TivooDelegate

- (instancetype)init {
    self = [super init];
    responseData = [NSMutableData new];
    return self;
}

- (void)rfcommChannelData:(IOBluetoothRFCOMMChannel *)rfcommChannel data:(void *)dataPointer length:(NSUInteger)dataLength {
    [responseData appendBytes:dataPointer length:dataLength];
    NSMutableString *hex = [NSMutableString new];
    const unsigned char *bytes = (const unsigned char *)dataPointer;
    for (NSUInteger i = 0; i < dataLength; i++) [hex appendFormat:@"%02X ", bytes[i]];
    NSLog(@"RX: %@", hex);
}

- (void)rfcommChannelOpenComplete:(IOBluetoothRFCOMMChannel *)rfcommChannel status:(IOReturn)error {
    NSLog(@"RFCOMM %@ (err=%d)", error == 0 ? @"OK" : @"FAIL", (int)error);
}

- (void)rfcommChannelClosed:(IOBluetoothRFCOMMChannel *)rfcommChannel {
    NSLog(@"RFCOMM closed");
}

@end

static NSData *buildPacket(NSData *payload) {
    NSUInteger pl = [payload length];
    NSUInteger totalLen = pl + 2;
    uint8_t lLow = totalLen & 0xFF;
    uint8_t lHigh = (totalLen >> 8) & 0xFF;
    uint16_t crc = lLow + lHigh;
    const uint8_t *pb = [payload bytes];
    for (NSUInteger i = 0; i < pl; i++) crc += pb[i];

    NSMutableData *pkt = [NSMutableData dataWithCapacity:pl + 7];
    uint8_t s = 0x01; [pkt appendBytes:&s length:1];
    [pkt appendBytes:&lLow length:1];
    [pkt appendBytes:&lHigh length:1];
    [pkt appendData:payload];
    uint8_t cl = crc & 0xFF, ch = (crc >> 8) & 0xFF;
    [pkt appendBytes:&cl length:1];
    [pkt appendBytes:&ch length:1];
    s = 0x02; [pkt appendBytes:&s length:1];
    return pkt;
}

static NSData *hexToData(NSString *hex) {
    NSMutableData *d = [NSMutableData new];
    NSString *clean = [[hex stringByReplacingOccurrencesOfString:@" " withString:@""] uppercaseString];
    for (NSUInteger i = 0; i + 1 < [clean length]; i += 2) {
        unichar c1 = [clean characterAtIndex:i];
        unichar c2 = [clean characterAtIndex:i+1];
        uint8_t val = 0;
        if (c1 >= '0' && c1 <= '9') val = (c1 - '0') << 4;
        else if (c1 >= 'A' && c1 <= 'F') val = (c1 - 'A' + 10) << 4;
        if (c2 >= '0' && c2 <= '9') val |= (c2 - '0');
        else if (c2 >= 'A' && c2 <= 'F') val |= (c2 - 'A' + 10);
        [d appendBytes:&val length:1];
    }
    return d;
}

static void runLoopFor(NSTimeInterval t) {
    [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:t]];
}

static void sendAndRecv(IOBluetoothRFCOMMChannel *ch, NSData *payload, NSTimeInterval wait) {
    NSData *pkt = buildPacket(payload);
    NSMutableString *hex = [NSMutableString new];
    const uint8_t *b = [pkt bytes];
    for (NSUInteger i = 0; i < [pkt length]; i++) [hex appendFormat:@"%02X ", b[i]];
    NSLog(@"TX: %@", hex);

    [ch writeSync:(void *)[pkt bytes] length:[pkt length]];
    runLoopFor(wait);
}

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        if (argc < 2) {
            NSLog(@"用法: tivoo_cmd [-s] <hex_payload> [hex_payload2] ...");
            NSLog(@"  -s    会话模式：保持连接，发送多个 payload（用 -- 分隔）");
            NSLog(@"");
            NSLog(@"  示例: tivoo_cmd 74 64           (亮度 100%%)");
            NSLog(@"        tivoo_cmd -s 74 64 -- 45 00 00  (先设亮度再切时钟)");
            return 1;
        }

        BOOL sessionMode = NO;
        int startArg = 1;

        if (argc > 1 && strcmp(argv[1], "-s") == 0) {
            sessionMode = YES;
            startArg = 2;
        }

        // 收集所有 payload（用 -- 分隔多个命令）
        NSMutableArray<NSData *> *payloads = [NSMutableArray new];
        NSMutableString *currentHex = [NSMutableString new];

        for (int i = startArg; i < argc; i++) {
            if (strcmp(argv[i], "--") == 0) {
                if ([currentHex length] > 0) {
                    [payloads addObject:hexToData(currentHex)];
                    [currentHex setString:@""];
                }
            } else {
                if ([currentHex length] > 0) [currentHex appendString:@" "];
                [currentHex appendString:[NSString stringWithUTF8String:argv[i]]];
            }
        }
        if ([currentHex length] > 0) {
            [payloads addObject:hexToData(currentHex)];
        }

        if ([payloads count] == 0) {
            NSLog(@"无效的 hex 数据");
            return 1;
        }

        IOBluetoothDevice *dev = [IOBluetoothDevice deviceWithAddressString:@"11:75:58:8C:5B:0C"];
        if (!dev) { NSLog(@"设备未找到"); return 1; }

        if (![dev isConnected]) {
            [dev openConnection];
            runLoopFor(1.0);
        }

        TivooDelegate *delegate = [[TivooDelegate alloc] init];
        IOBluetoothRFCOMMChannel *channel = nil;
        IOReturn err = [dev openRFCOMMChannelSync:&channel withChannelID:1 delegate:delegate];

        if (err != kIOReturnSuccess || !channel) {
            NSLog(@"RFCOMM 连接失败: %d", (int)err);
            return 1;
        }
        runLoopFor(0.3);

        // 发送所有 payload
        for (NSUInteger i = 0; i < [payloads count]; i++) {
            NSData *payload = [payloads objectAtIndex:i];
            if ([payload length] == 0) continue;

            NSTimeInterval wait = (i == [payloads count] - 1) ? 0.8 : 0.05;
            sendAndRecv(channel, payload, wait);
        }

        [channel closeChannel];
    }
    return 0;
}
