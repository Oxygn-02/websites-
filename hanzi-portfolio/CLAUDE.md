# Hanzi portfolio: concept mockup (handoff)

A single-file portfolio site concept for **Hanzi** (`hanzi_designs`), a young UK graphic designer whose work is UK rap and street culture: cover art, event flyers, logos and marketing posters (10 pieces). It is a **pitch mockup**. The owner of this repo designs sites for young creators and plans to show it to her. She has not seen or approved it.

## Quick start

```bash
pip install pillow
python3 build.py      # src/template.html + assets/art/*.png -> dist/hanzi-designs-mockup.html
open dist/hanzi-designs-mockup.html
```

- **Edit `src/template.html` only.** `dist/` is generated.
- The build embeds each artwork as base64 JPEG (max 900px) in place of the `__IMG__` placeholder.
- It also extracts a 5-colour palette per piece in place of `__PAL__`. The palette uses histogram bins plus a hue-cluster pass, so a small vivid accent (for example the blue face in Rush Hour) always survives.
- The page needs **internet** for Google Fonts and the Unsplash photo plates. Offline it falls back to system fonts and fully drawn canvas scenes.

## Repo map

| Path | What it is |
|---|---|
| `src/template.html` | The whole site: CSS, markup and JS, about 1,100 lines |
| `build.py` | Embeds the art and palettes |
| `assets/art/*.png` | The 10 original artworks, named by key |
| `dist/hanzi-designs-mockup.html` | Latest build (v22) |
| `archive/v21-cover-reel.html` | v21: drawn scenes, intro cover reel, client list |
| `archive/v20-embedded-plates.html` | v20: all ten photo plates embedded (replaced in v21 by drawn scenes, Power keeps its photo) |
| `archive/v18-photo-plates.html` | v18: photo plates, before the v19 changes |
| `archive/v16-drawn-scenes.html` | Last version before photo plates and the lens pass |
| `archive/v17-lens-pass.html` | Adds soft focus, bloom and grain; no photos |
| `docs/screenshots/` | Reference renders. These are sandbox renders with fallback fonts and no photos. |

## Page structure: three sections

1. **Intro (`.hero`).**
   - "HANZI" fades in one face, then each letter cycles through typefaces taken from her work.
   - The letters keep the same cap height and baseline, sit in fixed tight slots, and cross-fade. No two neighbours share a font.
   - It's a left-to-right wave, one letter every 90ms, and pauses off-screen.
   - Below the name: the tagline and an "Enter the gallery" glass pill.
2. **Gallery (`#gallery`).** A 3D CSS wheel (`.ring` and `.card`, `R` = 900 desktop or 420 mobile, STEP = 36°) on a full-height glass panel.
   - **Arrival:** when first reached, or when Gallery/Enter is pressed, it spins fast and brakes onto the first piece.
   - **Cards:** all the same size, with the art matted in a 4:5 frame. The mat is tinted with the piece's accent. Near-4:5 art fills the frame (`.box.fill`).
   - **Labels:** a floating category pill above the front card, with the title and subtitle below.
   - **Navigation:** drag/swipe, wheel, arrow keys, or tap a side card. Tapping the front card opens the piece page.
3. **About + contact (`#contact`).** Bio, "Let's make it real" with Start a project, the pitch line, the footer disclaimer and Unsplash credits.

**Piece page (`#piece`).** A full-screen overlay that FLIP-grows the art from the wheel.
- **Content:**
  - Category pill.
  - Title in the piece's own typeface.
  - "The vision" paragraph.
  - Three design choices.
  - Palette dots.
  - Credits: Made for / Year / Tools. Empty or TBC fields are hidden; fill them via `YEAR` and `TOOLS`.
- **Navigation:** a pinned "Next" button. Swipe, arrow keys or Next close the page, return to the wheel and turn it one step. Esc or × closes.
- **Focus:** the content behind is made `inert` while the page is open.

## Data you will edit

All of this lives in the script near the top of `src/template.html`.

- **`SITE`:** name, tagline and pitch fields.
- **`P[key]`:** per piece.

  | Field | Meaning |
  |---|---|
  | `c` | Category |
  | `t` | Title |
  | `s` | Subtitle |
  | `viz` | Scene name |
  | `v` | Vision text |
  | `dc` | Design choices |
  | `th` | Theme: `ink`, `ac`, `fd` (display font) |
  | `br` | Background brightness |

- **`ORDER`:** wheel order. It's shuffled so neighbouring pieces never share a category, wrap-around included.
- **`CREDIT`, `YEAR`, `TOOLS`:** credits line. Currently mostly TBC.
- **`PLATE[key]`:** the Unsplash photo behind each piece.

  | Field | Meaning |
  |---|---|
  | `u` | Photo id |
  | `g` | CSS filter grade |
  | `tint` | Colour-blend tint |
  | `to` | Tint opacity |
  | `o` | Plate opacity |
  | `by`, `at` | Photographer name and handle, used for credits |

  The photos are hotlinked from `images.unsplash.com`, as Unsplash's API terms expect, and credited in the footer.

> The **vision and design-choice copy is placeholder**, written by AI from looking at the art. Hanzi must rewrite it in her own words before anything is shared.

## Background "worlds" (the visualiser system)

Each piece has a world behind it in the gallery and on its piece page. Layers, bottom to top:

1. **`.gb`:** the piece itself, heavily blurred.
2. **`.pl`:** the Unsplash photo plate, graded, blurred and slowly zooming (Ken Burns).
   - **Smoke:** this plate uses two mirrored layers and an animated SVG `feTurbulence`/`feDisplacementMap` filter (`#flow`) so the smoke billows.
3. **`canvas.viz`:** drawn by `class Viz`.
   - **Offscreen render:** the scene is drawn to an offscreen canvas first.
   - **Lens pass** (`LENS`): a soft-focus blur, then a blurred copy added on top for bloom.
   - **Phones:** capped at 30fps and lower resolution on touch devices.
   - **Cross-fade:** switching pieces fades between scenes.
4. **`.vig`:** vignette, animated film grain (an SVG noise data URI) and light leaks.

Which scenes draw:
- **Plate loaded** (`PLATE_OK[k]`): the light accent in `LITE[viz]`.
- **Plate fails to load:** the full drawn scene in `SCENES[viz]`.

| Piece (key → viz) | Idea | `LITE` accent over photo | Full drawn fallback |
|---|---|---|---|
| Alpha House (`alpha` → `sun`) | Knucks's "Alpha House": growing up on the Kilburn estate, sirens, Venna's sax outro | Siren wash and sax line | Estate block at golden hour, windows lighting over a 60s dusk, ball cage with bouncing ball |
| Bad Route (`badroute` → `dial`) | Watch and London map; "the wrong road to the nice things" | Full scene kept | A dive-watch dial laid flat as a floor, with diamond hour markers that glint, a warped street grid with parks, a gold route that tours the dial taking wrong turns and dead ends (dims behind its head, 40s cycle), and a lume sweep |
| Crosshair (`target` → `radar`) | Being watched | Full scene kept | CCTV scanlines; a red laser that searches, then locks with TARGET ACQUIRED brackets; heartbeat speeds up |
| Smoke and Paint (`smoke` → `smoke`) | Hazy creative night | Full scene kept (photo smoke animated) | Smoke blowing in from off-screen left, brush strokes painting themselves |
| Don't Be A Menace (`menace` → `road`) | Night street | Lamp flicker, fog, cobwebs | Perspective road, zebra crossing, red line, lamp pool, fog, car lights |
| Lacoste × LV (`lacoste` → `monogram`) | Boutique | Spotlight and gold dust | Croc-scale wall, monogram-tile floor runway |
| Power (`power` → `stage`) | Theatre | Beams and dust | Floorboards, velvet curtains, valance, comedy and tragedy masks |
| Gabos London (`gabos` → `street`) | Flash-lit doorway shoot, London night | Lit rain and camera flash | Terrace silhouettes, windows, lamps, wet road, bus, bokeh, flash |
| The City Is Your Track (`nike` → `bridge`) | Commute as race | Red speed lines | Running-track floor, lane numbers, Tower Bridge on the horizon |
| Rush Hour (`tfl` → `tube`) | Shared rush | Train light rushing past | Platform floor, MIND THE GAP, rails, tube-map wall, passing train |

The perspective-floor scenes use the helper `floor(w,h,hy)`.

## Owner's design preferences (settled; don't reverse without asking)

- **Look:** frosted glass, rounded corners, gradients and opacity. Centred layout. No two-tone buttons.
- **Sections:** exactly three (Intro / Gallery / Contact+About). Nav reads Welcome · Gallery · Contact.
- **Gallery wheel:** a curved rotating wheel. Same-size cards. No counter, arrows or "drag/click" instruction text in the gallery. The category label floats above the work.
- **Name animation:** fast, consistent size and height, tight spacing, no two neighbours in the same font.
- **Hover/focus:** shrink and calm the text and draw attention to the art. Don't change fonts on hover.
- **Backgrounds:** premium and subtle, never pulling attention from the art, never overcrowded. "Should feel like a senior designer made it, not a computer." The owner liked the Bad Route floor dial and gold route, the Gabos street and the smoke drifting from off-screen.
- **Process:** always back up the current build before making a new version.

## Known issues / next steps (council recommendations for v19)

1. **Photos didn't show for the owner.** The likely cause is that the file was viewed in a preview that blocks external requests. Verify in a real browser, or self-host the graded plates (download them via the Unsplash API, keep the credits) so they don't depend on hotlinking.
2. **Bigger art.**
   - Piece page: `.pp` padding to `7vh 5vw 9vh`, gap `3.5vw`, `.pp-art img` max-height `84vh`.
   - Wheel: a larger front card.
3. **Thinner mat:** `.fr .box` padding 7% → about 4.5%. Widen the `.fill` range to `ar>.7 && ar<.95`.
4. **"Next" overlap:** the Next pill overlaps the last palette dot on desktop. Add `padding-bottom` to `.pp-text`.
5. **Embedded title font:** embed one condensed display font (subset to A–Z, base64 `@font-face`) so titles never fall back.
6. **Stricter photo plates:**
   - more blur and darker;
   - no photos with readable text;
   - must contrast with the art (avoid orange-on-orange for Alpha House and a white glare behind Power);
   - fade in when loaded instead of popping.
7. **Siren speed:** slow the Alpha House red/blue alternation, which is close to the flashing-content limit.
8. **Performance:**
   - only the front world runs;
   - preload only the next plate;
   - reduced-motion must also stop the plates' Ken Burns zoom and the `#flow` filter (the animation is removed already).
9. **Wheel discoverability without text:** a one-time nudge on arrival, where the wheel turns about 30° and springs back.
10. **Intro:**
    - add a small "Graphic designer · London" line;
    - let the gallery's top edge peek in at the bottom;
    - optionally hold the settled wordmark for about 1.2s before the letters cycle.
11. **Before showing her:**
    - remove the owner's pitch line and "[Your name]" from her page;
    - label the brand-pastiche pieces (Rolex, LV/Lacoste, Nike, TfL) as concept work;
    - replace the AI copy with prompts for her own words;
    - keep the link private until she agrees.
12. **Hosting:** Vercel or Netlify with `noindex`. Extract the base64 images to WebP files with `srcset` to cut the roughly 1.2MB file.

## Testing tips

- Playwright with Chrome works for screenshots: desktop 1280×800, mobile 390×780 with `isMobile`/`hasTouch` and a device scale factor of 2.
- To preview the photo-plate path offline, route `images.unsplash.com/**` to a local JPEG.
- Useful globals in the console: `goTo(i)`, `openPiece(key, imgEl|null)`, `closePiece()`, `galViz.t0 -= 28000` (fast-forward a scene), `ORDER`, `P`, `PLATE_OK`.
