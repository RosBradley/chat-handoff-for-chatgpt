#!/usr/bin/env python3
"""Build archives without publishing."""
import argparse
from pathlib import Path
from repo_tools import ROOT, build
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for path in build(args.output.resolve()):
        print(path)
