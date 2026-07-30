"""Download a small set of public WHO topic pages as text (best-effort).

WHY WHO topic pages (not bulk UNGA PDFs) for v1:
  - Bilingual, public-health relevant, short enough for a laptop demo
  - Clear provenance URLs for your README / interview story
  - Avoids brittle scraping of huge resolution archives

For production-scale work you would use WHO IRIS / UN Digital Library APIs
with proper rate limits and PDF pipelines. This script is intentionally small.

Usage:
  python -m scripts.download_corpus
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import RAW_DIR

# Curated bilingual pairs, public WHO health-topic pages
CORPUS = [
    {
        "doc_id": "who_web_mental_health_en",
        "title": "WHO: Mental health (web)",
        "language": "en",
        "url": "https://www.who.int/health-topics/mental-health",
    },
    {
        "doc_id": "who_web_mental_health_fr",
        "title": "OMS: Santé mentale (web)",
        "language": "fr",
        "url": "https://www.who.int/fr/health-topics/mental-health",
    },
    {
        "doc_id": "who_web_uhc_en",
        "title": "WHO: Universal health coverage (web)",
        "language": "en",
        "url": "https://www.who.int/health-topics/universal-health-coverage",
    },
    {
        "doc_id": "who_web_uhc_fr",
        "title": "OMS: Couverture sanitaire universelle (web)",
        "language": "fr",
        "url": "https://www.who.int/fr/health-topics/universal-health-coverage",
    },
]


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = False
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self._skip = False
        if tag in {"p", "li", "h1", "h2", "h3", "br", "div"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> None:
    """Download curated WHO topic pages into data/raw/ with provenance sidecars."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "multilingual-rag-assistant/0.1 (portfolio demo)"}
    for item in CORPUS:
        print(f"Fetching {item['url']} ...")
        try:
            resp = requests.get(item["url"], headers=headers, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"  SKIP: request failed, {exc}")
            continue
        text = html_to_text(resp.text)
        if len(text) < 200:
            print(f"  WARNING: short extract ({len(text)} chars), page may be JS-heavy.")
        out = RAW_DIR / f"{item['doc_id']}.txt"
        try:
            out.write_text(text, encoding="utf-8")
            meta = {
                "doc_id": item["doc_id"],
                "title": item["title"],
                "language": item["language"],
                "source_url": item["url"],
                "organization": "WHO",
            }
            (RAW_DIR / f"{item['doc_id']}.txt.meta.json").write_text(
                json.dumps(meta, indent=2), encoding="utf-8"
            )
        except OSError as exc:
            print(f"  SKIP: write failed, {exc}")
            continue
        print(f"  Wrote {out} ({len(text)} chars)")
    print("Done. Rebuild index with: python -m scripts.build_index")


if __name__ == "__main__":
    main()
