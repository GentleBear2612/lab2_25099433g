import os
import sys
import datetime
import argparse


def append_entry(action: str, details: str) -> None:
    """Append a timestamped entry to lab2_writeup.md in the repository root.

    action: short action title
    details: markdown-formatted details (string)
    """
    repo_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    writeup_path = os.path.join(repo_root, 'lab2_writeup.md')
    ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    entry_lines = ["\n### Entry - " + ts, f"- Action: {action}", "- Details:", "", details.strip(), ""]
    entry = "\n".join(entry_lines)

    with open(writeup_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def _main(argv=None):
    parser = argparse.ArgumentParser(description='Append an activity entry to lab2_writeup.md')
    parser.add_argument('--action', '-a', required=True, help='Short action title')
    parser.add_argument('--details', '-d', required=True, help='Detailed markdown text')
    args = parser.parse_args(argv)
    append_entry(args.action, args.details)


if __name__ == '__main__':
    _main()
