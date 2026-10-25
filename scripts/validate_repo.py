#!/usr/bin/env python3
"""Validate the maintained manifests, skill, source inventory and links."""
import json
from repo_tools import validate
if __name__ == "__main__":
    try:
        print(json.dumps(validate(), indent=2))
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit(f"Validation failed: {exc}")
