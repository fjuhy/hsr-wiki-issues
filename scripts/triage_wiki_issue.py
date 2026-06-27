#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from typing import Any

TYPE_LABELS = {
    "content-error": "official-evidence-required",
    "typo": "copy-edit",
    "source-needed": "official-evidence-required",
    "site-bug": "frontend-check",
    "search": "search-index-check",
    "mobile": "mobile-smoke-check",
    "abuse": "moderation-review",
}


def classify_issue(title: str, labels: list[str]) -> dict[str, Any]:
    actions = sorted({TYPE_LABELS[label] for label in labels if label in TYPE_LABELS}) or ["needs-info"]
    match = re.search(r"([a-z0-9]+(?:-[a-z0-9]+)+)", title.lower())
    return {
        "actions": actions,
        "affected_page": match.group(1) if match else "",
        "requires_official_source_check": "official-evidence-required" in actions,
        "never_apply_without_verification": True,
        "public_comment_policy": "Do not paste private raw evidence, local paths, or full raw source dumps.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--labels", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    print(json.dumps(classify_issue(args.title, labels), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
