# HISTROVE family photo archive

Saved on 3 November 2026 at Dan’s request. These are the supplied latest family-photo assets, preserved byte-for-byte.

This archive is separate from the website and card-release branches. It does not install a banner, change live pages, or publish a new card. The website strip remains an archived layout, not a deployed site change.

![Family photo website strip](HISTROVE-Family-Website-Strip-v1.png)

## Files

- [Family-Art-v6.png](Family-Art-v6.png): Raw thirteen-character family illustration, 2172 × 724.
- [HISTROVE-Family-Header-Source-v4.zip, stored in two lossless parts](source-zip-parts/): X-header source package, including SVG, logo and reference images.
- [HISTROVE-Family-Header-v4.png](HISTROVE-Family-Header-v4.png): X header, 1500 × 500.
- [HISTROVE-Family-Website-Strip-Source-v1.zip](HISTROVE-Family-Website-Strip-Source-v1.zip): Website-strip source package.
- [HISTROVE-Family-Website-Strip-v1.png](HISTROVE-Family-Website-Strip-v1.png): Website-strip layout, 2400 × 600; archive only, not installed on the site.
- [HISTROVE-Family-Website-Strip-v1.svg](HISTROVE-Family-Website-Strip-v1.svg): Website-strip source assembly with embedded raster illustration.

The source packages are preserved unchanged. The larger X-header ZIP is stored in two lossless parts because it exceeds the transfer-size limit. The X-header SVG is included in its source ZIP. SVG assemblies contain the raster artwork; they are not wholly vector illustrations.

## Verification

PNG files decode successfully. Both ZIPs pass integrity checks. File byte counts, SHA-256 hashes and Git blob identities are recorded in [archive-manifest.json](archive-manifest.json).

## Restore the X-header source ZIP

Download this archive directory, including `source-zip-parts/`, then run:

```sh
python3 restore-header-source.py
```

The script checks each part and recreates `HISTROVE-Family-Header-Source-v4.zip` byte-for-byte. It will not replace a different existing file. Expected SHA-256:

```text
e15056bed07a8a2987ddcdf194da1246140334e204674bbb20e97df6e229d7e7
```

No artwork is regenerated or recompressed during restoration. The website-strip ZIP is available as a single file.
