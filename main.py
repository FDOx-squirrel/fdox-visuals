#!/usr/bin/env python3
"""fdox-visuals orchestrator — the only entry point.

    python main.py                  all steps, in order
    python main.py --list           print steps and exit
    python main.py --only pattern   one step
    python main.py --from pattern   this step and everything after
    python main.py --skip fdo-meta  everything but this
    python main.py --dry-run        print the plan, run nothing
    python main.py --strict         warnings become errors (this is what CI runs)

Step modules are imported lazily so `--list` and `--dry-run` stay instant
and free of resvg-py/Pillow.
"""

from __future__ import annotations

import argparse
import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "py"))

# (id, description, module name under py/)
STEPS = [
    ("pattern", "Four-step documentation pattern banner + 4 icon badges", "step_pattern"),
    ("purpose", "FDOx purpose banner ('What does FDOx do?') + 4 icon badges", "step_purpose"),
    ("fdo-meta", "FAIR Digital Object meta-graphic (Data/Metadata/PID) + standalone sphere", "step_fdo_meta"),
    ("architecture", "fdo-squirrel architecture diagram", "step_architecture"),
    ("md-cff-schema", "MD.cff schema class diagram", "step_md_cff_schema"),
    ("citation-cff-schema", "CITATION.cff schema diagram", "step_citation_cff_schema"),
    ("talk-process", "Talk slides: the four-step pattern, one real slide each", "step_talk_process"),
    ("talk-purpose", "Talk slides: the four-outcome pattern, one real slide each", "step_talk_purpose"),
]


def _select(args: argparse.Namespace) -> list[tuple[str, str, str]]:
    ids = [s[0] for s in STEPS]
    if args.only:
        if args.only not in ids:
            sys.exit(f"unknown step '{args.only}' — choices: {', '.join(ids)}")
        return [s for s in STEPS if s[0] == args.only]
    if args.frm:
        if args.frm not in ids:
            sys.exit(f"unknown step '{args.frm}' — choices: {', '.join(ids)}")
        i = ids.index(args.frm)
        return STEPS[i:]
    if args.skip:
        if args.skip not in ids:
            sys.exit(f"unknown step '{args.skip}' — choices: {', '.join(ids)}")
        return [s for s in STEPS if s[0] != args.skip]
    return list(STEPS)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the fdox-visuals graphics.")
    ap.add_argument("--list", action="store_true", help="print steps and exit")
    ap.add_argument("--only", metavar="ID", help="run exactly one step")
    ap.add_argument("--from", dest="frm", metavar="ID", help="run this step and everything after")
    ap.add_argument("--skip", metavar="ID", help="run everything but this step")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    ap.add_argument("--strict", action="store_true", help="warnings become errors")
    args = ap.parse_args()

    if args.list:
        for sid, desc, _ in STEPS:
            print(f"{sid:10s} {desc}")
        return 0

    selected = _select(args)

    if args.dry_run:
        print("plan:")
        for sid, desc, _ in selected:
            print(f"  {sid:10s} {desc}")
        return 0

    timings: list[tuple[str, float]] = []
    report_lines: list[str] = []
    had_error = False

    for sid, desc, modname in selected:
        print(f"== {sid} — {desc} ==")
        t0 = time.time()
        try:
            mod = importlib.import_module(modname)
            for line in mod.run(strict=args.strict):
                print(f"  {line}")
                report_lines.append(f"[{sid}] {line}")
        except Exception as exc:  # noqa: BLE001 — surfaced to the user, not swallowed
            had_error = True
            print(f"  ERROR: {exc}")
            report_lines.append(f"[{sid}] ERROR: {exc}")
            if args.strict:
                break
        timings.append((sid, time.time() - t0))

    total = sum(t for _, t in timings)
    print("\ntiming:")
    for sid, t in timings:
        share = (t / total * 100) if total else 0
        print(f"  {sid:10s} {t:6.2f}s  ({share:4.1f}%)")
    print(f"  {'total':10s} {total:6.2f}s")

    report_path = ROOT / "img" / "pipeline_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
