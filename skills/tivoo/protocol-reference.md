# Divoom Tivoo Bluetooth Protocol Reference

## Device Info

- **Model**: Divoom Tivoo
- **MAC Address**: `11:75:58:8C:5B:0C`
- **Connection**: Classic Bluetooth RFCOMM (Port 1)
- **Screen**: 16x16 RGB pixels

### Bluetooth Structure

| Name | Type | Purpose |
|------|------|---------|
| `tivoo-light` | BLE (Low Energy) | Device discovery / broadcast |
| `tivoo-audio` | Classic Bluetooth RFCOMM | **Actual control channel** |

## Packet Format

```
[0x01][len_lo][len_hi][command][params...][crc_lo][crc_hi][0x02]
```

- **Start**: Fixed `0x01`
- **Length**: Payload bytes + 2 (CRC takes 2 bytes), little-endian 16-bit
- **Command + Params**: Protocol payload
- **Checksum**: `sum(len_lo + len_hi + command + all params)` & 0xFFFF, little-endian
- **End**: Fixed `0x02`

### Example: Brightness 100%

```
Raw command: 0x74 0x64
Packed:      01 04 00 74 64 D8 00 02

Breakdown:
  01        Start
  04 00     Length = 2(payload) + 2(crc) = 4
  74        Command: set brightness
  64        Parameter: 100
  D8 00     CRC: 0x04+0x00+0x74+0x64 = 0xD8
  02        End
```

## Command Table

### 0x74 — Set Brightness

| Parameter | Description |
|-----------|-------------|
| `[brightness]` | 0-100 |

```
100%: 74 64
0%:   74 00
```

### 0x45 — Set View Mode

**Clock mode:**

```
45 00 [24h] [style] 01 [weather] [temp] [calendar] [R] [G] [B]
```

| Field | Values | Description |
|-------|--------|-------------|
| 24h | 0x00/0x01 | 12/24 hour format |
| style | 0x00-0x06 | Clock style |
| weather | 0x00/0x01 | Show weather |
| temp | 0x00/0x01 | Show temperature |
| calendar | 0x00/0x01 | Show calendar |
| R, G, B | 0x00-0xFF | Color |

Clock styles: 0=fullscreen, 1=rainbow, 2=boxed, 3=square, 4=fullscreen-inv, 5=round, 6=wide

**Light effect mode:**

```
45 01 [R] [G] [B] 64 00 01 00 00 00
```

Example — Red light: `45 01 FF 00 00 64 00 01 00 00 00`

### 0x46 — Request Device Status

No parameters. Device returns a status packet.

```
46
```

### 0x44 — Send Static Image

```
44 00 0A 0A 04 [frame_data]
```

See "Image Frame Encoding" below for frame_data structure.

### 0x49 — Send Animation Frame

```
49 [total_lo] [total_hi] [chunk_index] [chunk_data...]
```

- total: Total bytes of all frame data (little-endian 16-bit)
- chunk_index: Chunk sequence number (starting from 0)
- chunk_data: Up to 200 bytes per chunk

Multi-frame animations require keeping the Bluetooth connection open (session mode), sending all chunks sequentially.

## Image Frame Encoding

### Frame Format

```
[0xAA] [frame_size_lo] [frame_size_hi] [timecode_lo] [timecode_hi]
[0x00] [num_colors] [palette...] [pixel_data...]
```

| Field | Description |
|-------|-------------|
| 0xAA | Frame start marker |
| frame_size | Total frame size (including marker and size bytes) |
| timecode | Per-frame display duration in milliseconds |
| 0x00 | Palette flag: reset |
| num_colors | Number of colors (0 means 256) |
| palette | `[R,G,B]` x num_colors |
| pixel_data | Bit-packed pixel indices |

### Pixel Bit-Packing

1. Build a palette (deduplicated color list)
2. Each pixel records its index in the palette
3. `bits_per_pixel = ceil(log2(num_colors))`
4. For each index, take the low `bits_per_pixel` bits, **reverse bit order**
5. Concatenate all bits, **reverse each 8-bit group** before packing into a byte
6. Pad to multiple of 8 bits

### Python Implementation Reference

See `encode_image()` and `build_image_frame()` in `tivoo_macos.py`.

## References

- [esp32-divoom](https://github.com/d03n3rfr1tz3/esp32-divoom) — Most complete protocol reference implementation
- [pixoo-client](https://github.com/virtualabs/pixoo-client) — Python Linux RFCOMM implementation
- [node-divoom-timebox-evo](https://github.com/RomRider/node-divoom-timebox-evo) — Node.js implementation
- Divoom REST API: http://doc.divoom-gz.com/web/ (Wi-Fi Pixoo series)
