"""Keep the 001 website copy in sync with the approved book chapter."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "book/crypto-season-01/001-blind-signatures.md"
WEB_COPY = ROOT / "site/app/cards/content/001.json"


def section(document, heading):
    match = re.search(r"(?m)^## " + re.escape(heading) + r"\n(.*?)(?=\n## |\Z)", document, re.S)
    if not match:
        raise ValueError(f"Missing chapter section: {heading}")
    return match.group(1).strip()


def chapter_content():
    document = CHAPTER.read_text(encoding="utf-8")
    story = section(document, "The story").split("\n\n")
    clues = []
    for line in section(document, "Hidden in the artwork").splitlines():
        match = re.fullmatch(r"\d+\. \*\*(.*?)\*\* (.*)", line)
        if not match:
            raise ValueError(f"Unrecognised clue: {line}")
        clues.append({"title": match.group(1), "text": match.group(2)})
    note = section(document, "Source and art note").split("\n\n")[0]
    if len(story) != 4 or len(clues) != 4:
        raise ValueError("001 must have four story paragraphs and four clues")
    return {"story": story, "eggs": clues, "sourceNote": note}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the published copy differs from the book")
    args = parser.parse_args()
    content = json.dumps(chapter_content(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not WEB_COPY.exists() or WEB_COPY.read_text(encoding="utf-8") != content:
            raise SystemExit("001 website copy differs from the approved book chapter. Run sync_001.py.")
        print("001 website copy matches the approved book chapter")
    else:
        WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
        WEB_COPY.write_text(content, encoding="utf-8")
        print(WEB_COPY)


if __name__ == "__main__":
    main()
