# Claude Code Hooks for Tivoo

Configure [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) to show animated Claude emotions on your Tivoo pixel screen when Claude Code events fire.

Uses Claude-specific emotion presets (`--load claude`) by default for fine-grained expressive animations. TTS (text-to-speech) is only enabled for Notification events — other events communicate through emotion animations alone.

## Quick Start

```bash
# Apply default hooks (Notification has English TTS)
./configure-claude-hooks.sh

# Chinese TTS for Notification
./configure-claude-hooks.sh -l zh

# Enable all 13 events
./configure-claude-hooks.sh --all

# Preview without applying
./configure-claude-hooks.sh --dry-run

# Use generic presets instead of Claude emotions
./configure-claude-hooks.sh --no-load

# Custom selection
./configure-claude-hooks.sh --events Stop,Notification,Elicitation

# Remove all hooks
./configure-claude-hooks.sh --reset
```

## Event → Claude Emotion Mapping

### Default Enabled (6 events)

These fire when Claude stops or needs user action:

| Event | Claude Emotion | Loop | TTS |
|-------|---------------|------|-----|
| **Stop** | `done` | 5 | — |
| **StopFailure** | `oops` | 5 | — |
| **Notification** | `notify` | 5 | 通知来啦 / Heads up + message |
| **PermissionRequest** | `question` | 5 | — |
| **Elicitation** | `question` | 5 | — |
| **TeammateIdle** | `standby` | 5 | — |

### Opt-in Events (7 events)

Enable with `--all` or `--events`:

| Event | Claude Emotion | Loop |
|-------|---------------|------|
| UserPromptSubmit | `working` | 2 |
| TaskCreated | `tasklist` | 2 |
| TaskCompleted | `taskdone` | 2 |
| SubagentStart | `subagent` | 2 |
| SubagentStop | `taskdone` | 2 |
| PostToolUseFailure | `oops` | 2 |
| PermissionDenied | `oops` | 2 |

### Excluded Events

These are not included (too noisy, too niche, or not useful for screen notifications):

| Event | Reason |
|-------|--------|
| PreToolUse / PostToolUse | Fires on every tool call, too frequent |
| FileChanged / CwdChanged | Filesystem watcher, noise |
| ConfigChange / InstructionsLoaded | Rarely fires |
| WorktreeCreate / WorktreeRemove | Worktree-specific, niche |
| ElicitationResult | Immediately follows Elicitation, redundant |
| PreCompact / PostCompact | Context compaction, not user-actionable |
| SessionStart / SessionEnd | Session lifecycle, not actionable |

## Options

| Flag | Description |
|------|-------------|
| `-l, --lang en\|zh` | TTS language: `en` (Samantha) or `zh` (Tingting). Default: `en` |
| `--dry-run` | Print config without writing to settings.json |
| `--all` | Enable all 13 events (not just defaults) |
| `--events E1,E2,...` | Enable only specified events |
| `--tts E1,E2,...` | Enable TTS for extra events beyond Notification |
| `--no-tts` | Disable all TTS (including Notification) |
| `--no-load` | Use generic presets instead of Claude emotions |
| `--reset` | Remove all Tivoo hooks from settings |
| `-h, --help` | Show help and full event list |

## Files

- `configure-claude-hooks.sh` — Configuration script for Claude Code
- `generated-claude/` — Auto-generated hook scripts (created by configure-claude-hooks.sh)
