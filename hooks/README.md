# Claude Code Hooks for Tivoo

Configure [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) to show animated presets on your Tivoo pixel screen when Claude Code events fire.

## Quick Start

```bash
# Apply default hooks (Chinese TTS)
./configure-hooks.sh

# Apply default hooks (English TTS)
./configure-hooks.sh --lang en

# Enable all 13 events
./configure-hooks.sh --all

# Preview without applying
./configure-hooks.sh --dry-run

# Use Luna emotion presets
./configure-hooks.sh --luna

# Custom selection
./configure-hooks.sh --events Stop,Notification,Elicitation

# Remove all hooks
./configure-hooks.sh --reset
```

## Event → Preset Mapping

### Default Enabled (6 events)

These fire when Claude stops or needs user action:

| Event | Preset | Loop | 中文 TTS | English TTS |
|-------|--------|------|----------|-------------|
| **Stop** | `done` | 3 | 完成啦，等待指示 | Done, awaiting instructions |
| **StopFailure** | `error` | 3 | 出错了，快来看看 | Error, come take a look |
| **Notification** | `star` | 5 | 通知来啦 | Heads up |
| **PermissionRequest** | `waiting` | 5 | 等待授权 | Approval needed |
| **Elicitation** | `coding` | 5 | 等待输入 | Input needed |
| **TeammateIdle** | `idle` | 5 | 队友闲置 | Teammate idle |

### Opt-in Events (7 events)

Enable with `--all` or `--events`:

| Event | Preset | Loop | 中文 TTS | English TTS |
|-------|--------|------|----------|-------------|
| UserPromptSubmit | `searching` | 2 | — | — |
| TaskCreated | `building` | 2 | — | — |
| TaskCompleted | `check` | 2 | 子任务完成 | Task done |
| SubagentStart | `working` | 2 | — | — |
| SubagentStop | `check` | 2 | — | — |
| PostToolUseFailure | `cross` | 2 | — | — |
| PermissionDenied | `cross` | 2 | — | — |

### Excluded Events (13 events)

These are not included (too noisy, too niche, or not useful for screen notifications):

| Event | Reason |
|-------|--------|
| PreToolUse | Fires before every tool call, too frequent |
| PostToolUse | Fires after every tool call, too frequent |
| FileChanged | Filesystem watcher, noise |
| CwdChanged | Directory changes, noise |
| ConfigChange | Rarely fires |
| InstructionsLoaded | Rarely fires |
| WorktreeCreate / WorktreeRemove | Worktree-specific, niche |
| ElicitationResult | Immediately follows Elicitation, redundant |
| PreCompact / PostCompact | Context compaction, not user-actionable |
| SessionStart / SessionEnd | Session lifecycle, not actionable |

## Options

| Flag | Description |
|------|-------------|
| `--lang cn\|en` | TTS language: `cn` (Tingting) or `en` (Samantha). Default: `cn` |
| `--dry-run` | Print config without writing to settings.json |
| `--all` | Enable all 13 events (not just defaults) |
| `--events E1,E2,...` | Enable only specified events |
| `--tts E1,E2,...` | Enable TTS only for specified events |
| `--no-tts` | Disable all TTS announcements |
| `--luna` | Use Luna emotion presets via `--load` |
| `--reset` | Remove all Tivoo hooks from settings |
| `-h, --help` | Show help and full event list |

## Files

- `configure-hooks.sh` — Configuration script
- `generated/` — Auto-generated hook scripts (created by configure-hooks.sh, gitignored)
