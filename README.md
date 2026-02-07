# Scotty vs. Squirrels

## Project Description

Scotty vs. Squirrels is a fast-paced and retro-style mobile browser game where you play as CMU's mascot Scotty the Terrier, chasing squirrels across an infinitely generating world. Using a virtual joystick, you chase down squirrels before time runs out. Catching a squirrel triggers a tap-battle cutscene where rapid clicking earns bonus points and extra seconds on the clock. Catching squirrels in quick succession activates a double-kill multiplier, rewarding aggressive play. New squirrels continuously spawn from off-screen to keep the pressure on, while the soundtrack, generated entirely through the Web Audio API, drives the intensity of the countdown.

The entire game ships as a single HTML file with just over 13KB compressed, with zero external dependencies. The infinite world is built on a chunk-based system with grass, dirt paths, and water, determined by a custom smooth value noise function that creates organic water bodies and meandering paths, with dithered pixel blending at terrain borders for natural transitions. All visual assets are defined as coordinate arrays and rendered pixel-by-pixel onto an HTML5 canvas. The game's physics use an acceleration-based model with forward/lateral split for satisfying movement feel, and the squirrel AI dynamically flees, wanders, or approaches based on proximity. Every sound in the game is synthesized procedurally at runtime using oscillators and noise buffers, requiring no audio files whatsoever.

## How to Run

**Option 1 — Open directly:** Open `index.html` in a modern browser (Chrome, Firefox, Safari, or Edge).

**Option 2 — Local server (recommended for mobile testing):** From the project root, run a simple HTTP server, then open the URL on your device:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000` (or your machine's IP and port from another device on the same network).

**Option 3 — From compressed archive:** If you have the Brotli-compressed tarball (`app.tar.br`), extract and serve in one step:

```bash
./extract_and_serve.sh app.tar.br
```

Then open `http://localhost:8000` in your browser.
