# Card 091 book build

The two-page PDF uses the established HISTROVE 090 renderer at repository commit 42081088eafd1882ab22332bb53c71d140a4d22d. Page geometry, DejaVu typography, colors, columns and the full-artwork proportional fit are unchanged. The first page contains the approved raw artwork; the facing page contains the story, four detail explanations and linked sources. The four closeups are separate pixel-exact crops, as in the original template.

## Rebuild

From this master directory, run:

    python3 build_book.py
    python3 verify_book.py

Dependencies: reportlab, Pillow and PyMuPDF. The two DejaVu font files are included. No network access is needed to rebuild. Use `python3 build_book.py --content-only` to regenerate only the chapter Markdown, reader JSON and sources JSON.

## Editable inputs

- `authoring-content.json`: the three story paragraphs, four detail explanations, source links and art note.
- `crop-input.json`: four native raw-art crop boxes in top-left-origin pixel coordinates.
- `art.png`: the unmodified, approved 1060 x 1484 artwork. It must match the SHA256 in `art-provenance.json`.
- `build_book.py`: the complete editable renderer.
- `source/layout-reference.json`: immutable template and font provenance.
- `source/template-090-build_book.py`: the untouched 090 source renderer retained for comparison.

## Outputs and limitations

The build writes the two-page A4 PDF, both page PNGs, a spread PNG, reader JSON, chapter Markdown, sources JSON, four detail PNGs, normalized crop coordinates and technical QA. It does not alter the artwork or publish anything. Rebuilding resets the visual-review field to pending; inspect both rendered page PNGs before release.

The artwork is fitted proportionally at approximately 128.21 effective PPI. No higher native resolution or physical print acceptance is claimed. The reference photograph's attribution and license are recorded in the reader source note; that reference license is not treated as independent commercial-rights clearance for the final illustration.
