# Logo Design

This article covers the brand assets in [`design/`](../../design/): what exists, how the variants relate to each other, and the rules for using them.

A freshly generated project ships a placeholder logo: an open book with the name of its language written across the pages. It is generic on purpose, so that the read me, the documentation website, the favicon, and the package icon all work from the first commit. Replace it with the project's own logo whenever there is one, and rewrite this article to match (see [replacing the placeholder](#replacing-the-placeholder)).

## Concept

A library is a book of reusable code, so the mark is an open book. The pages carry the name of the language, `C` on the left page and `#` on the right, which ties the mark to C# beyond its color.

## Color

The palette is built around `#178600`, the color the repository host uses for C# in its language statistics, so the mark reads as C# rather than as .NET in general. Each token has a light value, for a light background, and a dark value, for a dark background. The dark accent is lighter than the light one, so that both keep their contrast on their own background:

| Token  | Light     | Dark      | Used for                            |
| ------ | --------- | --------- | ----------------------------------- |
| Ink    | `#1c2a1f` | `#e2efe3` | The outlines of the pages           |
| Accent | `#1a7f1a` | `#6fd36a` | The cover and the two glyphs        |
| Paper  | `#ffffff` | `#20331f` | The fill of the pages               |
| Ground | `#ffffff` | `#111a13` | The rounded square behind the badge |
| Edge   | `#d5dfd6` | `#2c3d2e` | The outline of the badge's square   |

The documentation website uses the light accent as its primary color, and the dark accent for its links in the dark palette (see [documentation website](tooling/documentation-website.md)).

## Typography

The mark has no typeface. The two glyphs are drawn as strokes rather than set in a font, so the files depend on no installed font. Wherever the mark appears together with the product name, the name is plain text set by the surrounding page, never part of an image, because the name differs from project to project while the images do not.

## The Mark

All files share a 64 by 64 viewbox:

- **The cover** is a single filled shape behind the pages: `M4 20 L4 52 C14 49 24 50 32 54 C40 50 50 49 60 52 L60 20 Z`, in the accent.
- **The pages** are two mirrored shapes that meet at the spine, `M32 18 C24 13 14 13 8 16 L8 48 C14 45 24 45 32 50 Z` and its mirror image at `x = 32`, filled with paper and outlined with ink at a stroke width of `2.5` with round joins.
- **The glyphs** are strokes in the accent at a stroke width of `3` with round caps. The `C` is an arc of radius `7.5` around `(21.1, 30.2)`, open to the right between `-45°` and `45°`. The `#` consists of two slanted strokes from `y = 23.5` to `y = 37` and two horizontal strokes at `y = 26.8` and `y = 33.6`, from `x = 38.5` to `x = 49.5`.
- **Centering:** the bounding box of each glyph is centered on the interior of its page, which runs from `x = 9.25` to `x = 30.75` and from `x = 33.25` to `x = 54.75`, and, over the width of the glyphs, from `y = 15.7` to `y = 44.7`, so both glyphs are centered at `y = 30.2`.
- **The badge** puts the mark, scaled by `0.796875`, on a rounded square with a corner radius of `14`, translated by `(6.5, 5.3)` so that the book is centered in it.

## Variants and Files

Vector masters live in [`design/`](../../design/) and are the source of truth. The copies the read me and the documentation website reference live in [`docs/assets/`](../assets/README.md). Nothing regenerates the copies automatically, so update them by hand whenever a master changes:

- **The mark**, `mark-light.svg` and `mark-dark.svg`, for the read me header and the favicon.
- **The badge**, `badge-light.svg` and `badge-dark.svg`, for the header of the documentation website and the package icon, where the mark needs a ground of its own to stand out against a colored header bar or an unknown background.

The copies are the masters with a fixed size added (`header-logo-*.svg` at 56 pixels, `logo-*.svg` at 48 pixels), and the favicon SVGs are the mark as it is. Two files have to be raster images, because their formats leave no choice: `docs/assets/images/package-icon.png`, which NuGet requires as a PNG or JPEG, baked from the light badge at 128 by 128 pixels, and `docs/assets/favicon/favicon.ico`, baked from the light mark at 16, 32, and 48 pixels. With `rsvg-convert` and ImageMagick installed:

```shell
rsvg-convert -w 128 -h 128 design/badge-light.svg -o docs/assets/images/package-icon.png
for size in 16 32 48; do rsvg-convert -w $size -h $size design/mark-light.svg -o favicon-$size.png; done
magick favicon-16.png favicon-32.png favicon-48.png docs/assets/favicon/favicon.ico && rm favicon-*.png
```

## Using the Logo on the Repository Host

The rule that catches everyone: **a repository host strips SVG filter effects when an SVG is rendered through an `<img>` element.** The placeholder is flat, without gradients, blurs, or any other filter, which is why its copies can stay SVG. A logo that relies on a filter has to be baked to PNG before it can appear in a read me, and its copies in `docs/assets/images/` become PNG files.

Light and dark variants are selected with the host's own URL-suffix convention, `#gh-dark-mode-only` and `#gh-light-mode-only`, on two Markdown images, which the host renders as `<img>` elements, so the filter rule above applies to them. The documentation website honors the same suffixes through a stylesheet, so one Markdown image pair works in both places (see [documentation website](tooling/documentation-website.md)).

## Replacing the Placeholder

1. Put the new vector masters into [`design/`](../../design/), keeping the file names, or update [`design/README.md`](../../design/README.md) along with them.
2. Replace the copies in [`docs/assets/`](../assets/README.md), baking them to PNG if the logo uses filter effects, and re-bake the package icon and the favicon with the commands above.
3. Change the colors in `docs/assets/styles/brand-colors.css` to the new palette.
4. Rewrite the sections of this article above, so that the concept, the palette, and the geometry of the new logo are on record.

## Dos and Don'ts

- **Do** keep the clear space around the mark that the master files already build in.
- **Do** use the variant built for the background it sits on, rather than recoloring one by hand.
- **Don't** stretch, rotate, recolor, or add effects to the mark.
- **Don't** put the product name into an image. It is text wherever the mark appears.

## Related

- [Documentation assets](../assets/README.md) — the copies and where each one is used.
- [Documentation website](tooling/documentation-website.md) — how the light and dark pairs, the favicon, and the brand colors are wired up.
- [Architecture](architecture.md) — where `design/` sits in the repository.
