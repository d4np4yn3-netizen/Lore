# Rebuild 038

The source artwork is immutable; every builder asserts its SHA-256. Run build_038_final_front.py and build_038_spread.py from any directory. The local chapter is 038-cryptopunks.md beside art.png; the book builder also supports the canonical repository book path. Source fonts are bundled. System dependencies: Inkscape and Poppler pdftoppm. Python packages are listed in requirements.txt.

Render the print PDF with pdftoppm -png -r 300 -singlefile to qa/card-pdf-300dpi.png and the book at 130 DPI to qa/book-1.png and qa/book-2.png. The web preview is a separate 600×837 derivative of the print trim (36,36,780,1074). Run qa_038_assets.py after rendering; the original approved proof inputs are required for copy and pixel regression checks.

Only the QR and its caption changed on the card. The book lost two review labels and otherwise preserves approved wording, layout and native image pixels. Physical print, physical QR scan and A4 reproduction approval remain outstanding; the native book art is approximately 127 PPI.
