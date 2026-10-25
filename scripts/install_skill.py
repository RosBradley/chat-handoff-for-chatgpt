#!/usr/bin/env python3
"""Copy the skill into a Codex discovery directory."""
from __future__ import annotations
import argparse
import hashlib
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def inventory(folder: Path) -> dict[str, str]:
    result = {}
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError(f"Not a regular skill directory: {folder}")
    for p in sorted(folder.rglob("*")):
        if p.is_symlink():
            raise ValueError(f"Symlink not allowed: {p}")
        if p.is_file():
            result[p.relative_to(folder).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def install(source: Path, destination: Path, replace: bool = False) -> tuple[str, Path | None]:
    source = source.resolve()
    destination = destination.absolute()
    if destination.name != "chat-handoff":
        raise ValueError("Destination must end in chat-handoff")
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError("Destination or parent is a symlink")
    if destination.resolve() == source or destination.resolve().is_relative_to(source) or source.is_relative_to(destination.resolve()):
        raise ValueError("Destination overlaps the maintained source")
    src = inventory(source)
    if "SKILL.md" not in src:
        raise ValueError("Source has no SKILL.md")
    backup = None
    if destination.exists():
        if inventory(destination) == src:
            return "Already current", None
        if not replace:
            raise ValueError("Destination differs; review it, then use --replace to back it up and install")
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".handoff-stage-", dir=destination.parent))
    try:
        shutil.copytree(source, stage / "chat-handoff")
        if inventory(stage / "chat-handoff") != src:
            raise ValueError("Copy verification failed")
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = destination.parent.parent / "chat-handoff-backups" / stamp
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
        try:
            (stage / "chat-handoff").rename(destination)
        except BaseException:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    return "Installed", backup


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("repo", "user"), default="repo")
    parser.add_argument("--project", type=Path, help="Repository root; only with --scope repo")
    parser.add_argument("--replace", action="store_true", help="Back up a differing installation before replacing it")
    args = parser.parse_args()
    if args.scope == "user" and args.project:
        parser.error("--project is only valid with --scope repo")
    parent = Path.home() if args.scope == "user" else (args.project or ROOT).absolute()
    destination = parent / ".agents" / "skills" / "chat-handoff"
    try:
        status, backup = install(ROOT / "skills" / "chat-handoff", destination, args.replace)
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
    print(f"{status}: {destination}")
    if backup:
        print(f"Previous copy preserved: {backup}")
    print("Use $chat-handoff in Codex. If not discovered, restart Codex.")
