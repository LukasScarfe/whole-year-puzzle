# CLAUDE.md — The Whole Year Puzzle

`README.md` covers what the project is, the results, and what each file does. This file covers how
to change it.

## Theming: match lukasscarfe.com

The site has to look like part of lukasscarfe.com (Hugo + Blowfish theme). Any new UI must use the
existing tokens, not new colours or fonts.

- **Colours** come only from the `:root` / `:root[data-theme="light"]` tokens at the top of
  `docs/index.html`, which are copied from the website's palette. Dark (green ground, purple
  primary) is the default; light is the site's dusty-pink ground with teal primary. If you need a
  colour that isn't a token, take it from the website's Blowfish palette and add it as a token in
  **both** themes.
- **Text colours** follow the website's computed styles: body text `--ink-2` (light green / dark
  red), page title `--ink` (white / black), bold `--bold` (weight 600; white / dark red, as the
  site's `<strong>`), section headings `--heading`, captions and
  footer `--muted` (the site's date/meta colour). No grey text; the only opacity-faded text is the
  footer AI note, kept quiet on purpose.
- **Fonts** are the site's system stacks (`--font-display`, `--font-body`, `--font-mono`). No web
  fonts. Headings are extrabold (800) like the website.
- **Logos** match the theme: `logo-dark.png` (purple/green) in dark, `logo-light.png` (red/cyan)
  in light. Favicon is `favicon-32x32.png`, the website's.
- **Pieces** are alphabetical (L before l, as in `solve.py`) and coloured by name via `PIECE_COLOR`,
  so a piece shared by both shapes looks the same everywhere, in both themes.
- Check every UI change in **both** themes and at phone width.
- Charts scale down to the column width (`.fit`); nothing scrolls sideways on a phone.

## Who it's for

Both audiences: puzzle owners (Solutions view: find today's solution, see how hard a date is) and
the curious/math crowd (Statistics view). Design **phone and desktop equally** — a change isn't
done until it looks good on both.

## Content conventions

- **Naming:** always "Shape 1" / "Shape 2" / "Heart" on the site — never "Puzzle 1", "Puzzle Shape 1"
  or "Pointed Heart". The names come from `name` in `solve.py` (and so `data.js`). The Heart has one
  piece set (F N P Y Z l o s t, from calendar-puzzle-designs' Pointed Heart); the old two-set keys
  `heart1` / `heart2` survive only as aliases so published links still open the Heart.
- **Dates:** short month + day, e.g. "Jan 25".
- **Numbers:** whole numbers (floor/round) everywhere, except where a fraction is the point, like
  a ratio. Thousands separators via `fmt()`.
- **Copy:** brief captions — one sentence under each chart saying what it shows and how to read it.
  No intro paragraphs.

## Statistics page

- It is about **the selected shape**. The title is "Statistics of Shape 1" / "Statistics of
  Shape 2". Summary boxes show only the selected shape — no "other shape" subtext, no
  shape-vs-shape boxes.
- **Easier before harder**, everywhere stats are listed: easiest tile before hardest, the
  "Most solutions" table before "Fewest", easiest finds before hardest. (Numeric axes and colour
  ramps still run low to high.)
- "Interesting finds" is also selected-shape only: easiest/hardest month, date number and
  combination (any two open cells, ignoring unsolvable pairs). No subheading.
- Every chart shows the selected shape only (board cells, months, days, etc.); captions don't name
  the shape, since it's obvious from the selector. The two exceptions show every puzzle: "Dates
  that don't exist" (a small table) and the comparison (last on the page): a 2D scatter of any two
  puzzles picked by Horizontal / Vertical dropdowns, or, behind a button, a 3D scatter with one
  puzzle per axis (hand-drawn SVG, no library: drag turns, wheel / pinch / +− zoom, Reset). Both use
  one shared log scale on every axis.

## Shared links and previews

The Play win popup's Share text links to `docs/shape1/`, `docs/shape2/` or `docs/heart/` (`#play/9-30` to try it,
`#solutions/9-30/20` for the spoiler), always on the public site. Those pages exist only for their
link-preview tags, which show that shape's empty board, and forward to the main page. The preview
images `docs/og-shape1.png` / `og-shape2.png` / `og-heart.png` come from the page's `?og=shape1` mode. If the board's
look changes, regenerate them with the preview running:

```sh
~/scripts/screenshot.sh "http://192.168.1.241:8799/?og=shape1" docs/og-shape1.png 1200 630 2500 viewport
```

## Dependencies

No build step: the site is hand-written `docs/index.html` + generated `docs/data.js`, and the
Python is stdlib only. Small libraries loaded from a CDN are fine when they clearly help.

## After every change: restart the preview

The LAN preview runs on raccoon at **http://192.168.1.241:8799/** (`#stats` for the statistics
page). After any change, restart it. The user reloads it and looks for themselves, so don't
screenshot or send images unless asked.

```sh
pkill -f "[h]ttp.server 8799"          # bracket so pkill doesn't match its own shell
cd docs && python3 -m http.server 8799 # separate call, in the background
```

Run the two in separate commands: if they share one command line, pkill matches that shell too.

Port 8798 is FreshRSS — don't use it.

## Finishing a change

Without asking: edit → restart preview → **commit to `main` locally**. Keep
`README.md` (feature list, results table) in sync in the same commit.

Only when asked: push. No claude.ai artifacts — the user doesn't want them.

## Publishing

Push `main` to `origin` (`git@github.com:LukasScarfe/whole-year-puzzle.git`); GitHub Pages
serves `docs/` at **https://yearpuzzle.michelleyap.ca/** (`docs/CNAME`; DNS is a Cloudflare
CNAME to `lukasscarfe.github.io`). Share links and preview-image URLs use that domain too, so
change them together if it ever moves.

If `solve.py` changes, regenerate with `python3 solve.py` and check with `python3 verify.py` before
publishing.
