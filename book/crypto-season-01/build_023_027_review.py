"""Build the five canonical two-page spreads and combine them for editorial review."""
from pathlib import Path
import subprocess
import sys

from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
CHAPTERS = (
    ("023", "doge-goes-to-sochi"),
    ("024", "mt-gox"),
    ("025", "monero-launches"),
    ("026", "quantum"),
    ("027", "the-bitcoin-auction"),
)
OUT = HERE / "proofs/023-027-full-art-spreads-review-v1.pdf"


def main():
    writer = PdfWriter()
    for number, slug in CHAPTERS:
        subprocess.run([sys.executable, str(HERE / f"sync_{number}.py"), "--check"], check=True)
        subprocess.run([sys.executable, str(HERE / f"build_{number}_spread.py")], check=True)
        path = HERE / f"proofs/{number}-{slug}-full-art-spread-v1.pdf"
        if len(PdfReader(path).pages) != 2:
            raise ValueError(f"{number} must contain exactly two pages")
        writer.append(str(path))
    writer.add_metadata({
        "/Title": "LORE Crypto Season One - Cards 023 to 027 - Book review spreads",
        "/Author": "LORE",
        "/Subject": "Five two-page editorial spreads with exact approved illustrations and matching canonical stories",
    })
    writer.page_layout = "/TwoPageLeft"
    with OUT.open("wb") as stream:
        writer.write(stream)
    if len(PdfReader(OUT).pages) != 10:
        raise ValueError("The combined review must contain exactly ten pages")
    print(OUT)


if __name__ == "__main__":
    main()
