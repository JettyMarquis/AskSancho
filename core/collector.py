"""
collector.py — Claude Code transcript collector

Watches ~/.claude/projects/*/conversations/ for new conversation files
and queues them for indexing by indexer.py.

Status: TODO (High Version Phase A)
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

TRANSCRIPT_BASE = Path.home() / ".claude" / "projects"
COLLECTED_LOG = Path(__file__).parent.parent / ".collected.json"


def find_transcript_dirs():
    """Find all Claude Code project conversation directories."""
    pattern = str(TRANSCRIPT_BASE / "*" / "conversations")
    return glob.glob(pattern)


def load_collected() -> set:
    """Load set of already-collected conversation file paths."""
    if not COLLECTED_LOG.exists():
        return set()
    with open(COLLECTED_LOG) as f:
        return set(json.load(f))


def save_collected(collected: set):
    with open(COLLECTED_LOG, "w") as f:
        json.dump(list(collected), f, indent=2)


def collect_new_transcripts() -> list[dict]:
    """Return list of new conversation entries not yet indexed."""
    collected = load_collected()
    new_entries = []

    for conv_dir in find_transcript_dirs():
        for jsonl_file in glob.glob(os.path.join(conv_dir, "*.jsonl")):
            if jsonl_file in collected:
                continue
            try:
                messages = []
                with open(jsonl_file) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            messages.append(json.loads(line))
                new_entries.append({
                    "file": jsonl_file,
                    "messages": messages,
                    "collected_at": datetime.now().isoformat(),
                })
                collected.add(jsonl_file)
            except Exception as e:
                print(f"[collector] Warning: could not read {jsonl_file}: {e}")

    save_collected(collected)
    return new_entries


if __name__ == "__main__":
    entries = collect_new_transcripts()
    print(f"[collector] Collected {len(entries)} new conversation(s)")
    for e in entries:
        print(f"  {e['file']} ({len(e['messages'])} messages)")
