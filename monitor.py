import hashlib
import json
import sys
from pathlib import Path

BASELINE = Path("integrity.json")


def scan(root):
    result = {}
    for path in Path(root).rglob("*"):
        if path.is_file() and path.resolve() != BASELINE.resolve():
            digest = hashlib.sha256()
            with path.open("rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    digest.update(chunk)
            result[str(path.relative_to(root))] = digest.hexdigest()
    return result


if len(sys.argv) != 3 or sys.argv[1] not in {"snapshot", "check"}:
    raise SystemExit("Usage: python monitor.py snapshot|check DIRECTORY")

mode, directory = sys.argv[1], Path(sys.argv[2])
if not directory.is_dir():
    raise SystemExit(f"Not a directory: {directory}")
current = scan(directory)
if mode == "snapshot":
    BASELINE.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"Saved hashes for {len(current)} files to {BASELINE}.")
else:
    if not BASELINE.exists():
        raise SystemExit(f"No baseline at {BASELINE}; run snapshot first.")
    saved = json.loads(BASELINE.read_text(encoding="utf-8"))
    added = sorted(current.keys() - saved.keys())
    removed = sorted(saved.keys() - current.keys())
    changed = sorted(name for name in current.keys() & saved.keys() if current[name] != saved[name])
    for label, names in (("ADDED", added), ("CHANGED", changed), ("REMOVED", removed)):
        for name in names:
            print(f"{label}: {name}")
    if not (added or removed or changed):
        print("No changes detected.")
    else:
        print(f"Summary: {len(added)} added, {len(changed)} changed, {len(removed)} removed.")
