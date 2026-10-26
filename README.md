# Atelier / Motion Lab

A browser-native character animation experiment: original layered illustration, real Potrace tracing, hierarchical SVG rigs, authored motion curves, and two-bone leg IK. No frontend framework, CDN, external fonts, or browser runtime dependencies.

## Run locally

From this directory:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000` in your browser. Or run `npm start`. Use an HTTP server, since ES modules and artwork JSON cannot load reliably from `file://`.

The shipped traced assets are ready to use. **Potrace is needed only when rebuilding artwork.**

## Playground

- **Ren**, an original school-uniform character: idle, walk, run, wave, jump.
- **Mochi**, an original dog: idle with tail wag, walk, sit, head tilt.
- Play/pause, playback speed, loop, and reset to a paused neutral pose.
- Developer mode draws the inherited bone chains and joint pivots. Select any joint and drag its rotation slider to pause and pose it. The readout gives parent, local pivot, angle, and translation. Highlight part boundaries to inspect overlapping segments.
- Export a self-contained SVG of the current pose, or save and load a JSON rig. Load the matching character first. JSON contains joint pivots, parent relationships, and current local transforms; loading pauses the pose. Play blends smoothly back to the selected animation.
- Expand the process panel to compare the full raster source with the full monochrome Potrace trace.

## Rebuild the actual tracing pipeline

Install genuine Potrace 1.16 and Cairo using your OS package manager. On Debian/Ubuntu:

```sh
sudo apt-get install potrace libcairo2
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-art.txt
python scripts/build_assets.py
```

Set `POTRACE=/path/to/potrace` for a nonstandard executable location. The setup machine used Potrace 1.16, CairoSVG 2.9.1, and Pillow 13.0.0. It already has generated output; rebuilding is optional.

`scripts/build_assets.py` is the original source-art definition, made from custom Bézier paths. It writes each bone's `.source.svg`, renders individual illustration fills and outlines to 3× PNG masks on a common coordinate system, composites transparency onto white, thresholds to 1-bit PBM, and invokes the **real Potrace CLI** for each mask. The resulting Bézier outlines are recolored with the original palette and assembled as SVG path groups. Outline and fill masks are traced separately to retain line weight. Paths are mapped from the raster dimensions back to local drawing coordinates. Joint offsets are never inferred from trace bounds.

`assets/characters.json` ships these real traced paths and authored bone metadata. Each part's assembled `.svg`, each intermediate PNG/PBM/trace, the full source PNG, and a separate full silhouette Potrace SVG are included for inspection. No PNG is embedded in the animated SVG. The source art is intentionally authored in separate layers; **automatic anatomy detection is not implemented**. Full-image tracing is only a comparison artifact.

## Architecture

```text
index.html                    Playground and comparison panel
styles/main.css               Responsive interface
src/main.js                   Playback, transition, UI, blink, import/export
src/engine/Skeleton.js        Parented SVG groups, pivots, pose application
src/engine/Animation.js       Keyframes, smoothstep, blending, two-bone IK
scripts/build_assets.py       Original art and reproducible raster/trace build
assets/boy, assets/dog        Source layers, raster masks, genuine traced paths
tests                         Motion mathematics and browser integration checks
```

Local joint coordinates use SVG's positive-down Y axis; angles are degrees. Each nested group first translates to its parent's pivot, rotates, then scales. A shoulder carries its elbow and wrist; a hip carries its knee and ankle. Garment caps extend behind adjacent segments, concealing seams over the authored range. Fringes, ears, and the segmented tail have inherited motion. The boy's head has a fixed base scale for approximately five-head proportions.

Animation time advances via `requestAnimationFrame` delta time, capped on resuming a hidden tab. Smoothstep interpolates authored keyframes. State changes blend from the current pose for 350 ms. Walk/run have explicit stance and swing phases; two-bone IK targets flat planted feet and raised swing feet, with ankle compensation. Root bounce is canceled in the planted target. Sine curves are used for breathing and secondary motion. Jump has crouch, takeoff, float, landing compression, recovery. Blinking follows the head through local eyelid overlays.

## Validation

```sh
npm test
# Optional browser integration checks, with the server running:
npm install --no-save --package-lock=false playwright@1.62.1
node tests/browser.cjs
```

Browser tests use `/usr/bin/chromium` by default. Set `CHROMIUM_PATH` and/or `BASE_URL` if needed. They exercise both characters, all nine clips, manual joint editing, JSON roundtrip, real SVG downloads, mobile overflow, and browser errors. Unit tests check IK forward reconstruction, finite motion over complete cycles, loop seam continuity, interpolation, and traced hierarchy integrity.

## Current limits / next experiments

This is a cutout animation prototype, not a deformable mesh or frame-by-frame animation system. The boy faces forward; walking and running are stylized treadmill studies with depth foreshortening omitted. IK uses a fixed flat ground and a single bend direction, without collision, terrain adaptation, or contact constraints across animation transitions. Extreme manually entered joint rotations can expose hidden overlap edges; the rig is tuned to the included clips. Sitting is an authored dog pose, not a physics solution. Blinks use vector eyelid overlays. JSON saves the current rig/pose, not custom timeline clips. SVG export is a static pose. WebM export is deliberately deferred.

For future development: side-view and three-quarter artwork, deformable garment patches, editable contact markers, per-joint limits, spring dynamics, and a timeline editor can build on the existing rig and animation evaluator.
