# Start here (Claude Code)

1. Unzip this folder, `cd` into it, and run `claude`. `CLAUDE.md` loads automatically and holds the full context.
2. Build the site with `pip install pillow && python3 build.py`, then open `dist/hanzi-designs-mockup.html` in a real browser (Chrome or Safari) with internet, so the fonts and Unsplash photos load.
3. Suggested first prompt:

> Read CLAUDE.md. Open dist/hanzi-designs-mockup.html in a browser and check whether the Unsplash photo plates load. Then back up the current build and make v19 from the "Known issues / next steps" list, items 1–8, without changing any of the settled design preferences.

Optional: `git init && git add . && git commit -m "Hanzi portfolio v18 handoff"` before you start, so every version is tracked instead of saved as backup files.
