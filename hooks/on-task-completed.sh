#!/bin/bash
# Tivoo hook: on task completed
# Sends emotion preset to Tivoo screen + TTS announcement

INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject // "task"')

# Run in background so hook returns immediately
(
  python3 /Users/didi/Projects/tivoo-control/tivoo_macos.py preset happy --set luna --loop 1 2>/dev/null
  say -v Tingting "任务完成：${TASK_SUBJECT}" 2>/dev/null
) &

exit 0
