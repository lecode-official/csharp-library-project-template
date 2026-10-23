# Documentation Assets

This article covers the static files the documentation, the read me, and the package use.

Anything under this directory that is not excluded is copied into the built [documentation website](../developer-manual/tooling/documentation-website.md) as-is, at the same relative path, so `docs/assets/images/logo-light.svg` is served at `assets/images/logo-light.svg`.

## What Goes Where

- `images/` — the logo copies. `header-logo-light.svg` and `header-logo-dark.svg` are the mark for the read me header, `logo-light.svg` and `logo-dark.svg` are the badge for the header of the documentation website, and `package-icon.png` is the badge baked to the PNG file the library's NuGet package carries as its icon.
- `favicon/` — `favicon.ico` as the universal fallback, plus `favicon-light.svg` and `favicon-dark.svg` for the browsers that honor a `media` query on a favicon link.
- `styles/` — the stylesheets wired in through `extra_css`: `gh-mode-only-images.css` teaches the documentation theme the repository host's own `#gh-dark-mode-only` and `#gh-light-mode-only` image suffixes, `site-logo.css` swaps the header logo for its dark variant, and `brand-colors.css` sets the logo's colors as the theme's primary color.
- `templates/` — the theme template override that adds the light and dark favicon links. It is read by the theme through `custom_dir` rather than published, so `exclude_docs` keeps it out of the built site.

## A Placeholder to Replace

Every project starts with a placeholder logo, an open book with the name of its language on the pages, so that the read me, the documentation website, the favicon, and the package icon are complete from the first commit. Replace the files here, together with their vector masters in [`design/`](../../design/), with the project's own logo — see [logo design](../developer-manual/logo-design.md), which also has the commands that bake the PNG and ICO files.

## Related

- [Documentation website](../developer-manual/tooling/documentation-website.md) — how these assets are wired in, and the light/dark mechanics.
- [Logo design](../developer-manual/logo-design.md) — the logo itself and how to replace it.
- [Documentation index](../README.md) — the articles these assets support.
