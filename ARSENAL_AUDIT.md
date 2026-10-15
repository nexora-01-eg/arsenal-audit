# ARSENAL AUDIT — F:\Arsenal (read-only intelligence audit)

- Audit date: 2026-09-19 · Audit dir: `F:\Arsenal_audit\audit_20260919_01` (versioned; previous reports untouched — none existed)
- Method: read-only walk + header/metadata probes + deterministic sampling + vision review of contact sheets. Nothing in the arsenal was created, renamed, moved, modified, converted, or downloaded.
- Machine tools used (already installed): Python 3.11 + PyAV 18.1 + Pillow 12.3 + OpenCV 5.0 + faster-whisper tiny (cached). NOT installed and NOT fetched: fontTools, mutagen, onnxruntime, whisper.cpp, SVG rasterizer, any VLM.

## 1. Executive Summary

F:\Arsenal is a **124,630-file / 26,668-dir / ~59 GB** media + code warehouse. The user estimates are wrong in both directions: fonts are ~6.6× overestimated (3,573 real TTF/OTF, not 23,501), AI models are ~1000× overestimated (5 files, not 5,000), while icons (~29k SVG), docs (16k MDN files), and code clones (~66k files) were unaccounted for. **~22% of all files (27,481) are exact name+size duplicates**, including an 18.9 GB quarantine folder (المتكرر 00) of byte-confirmed copies. ~21.7 GB of professional SFX sits **locked inside zip archives**. The single most valuable discovery: **`_projects/arsenal-x` already contains a 26-endpoint Arabic asset search API + gallery UI** (token search, X-Code ids, gaps analysis) — broken only by a hardcoded `D:\Arsenal` root. Do not rebuild search; fix and extend it. Real, immediately reusable production assets: 376 stock videos (+27 NASA), 1,441-track CC-BY music library, 189 Arabic-covering font files, 329+ film/camera LUTs, 3 offline STT models + 2 background-removal models, ~29k OSS icons.

## 2. Actual Arsenal Statistics

| Measure | Value |
|---|---|
| Total files | 124,630 (0 unreadable) |
| Total dirs | 26,668 |
| Total bytes | ~59.1 GB |
| Extensions seen | 206 |
| Largest single dir (files) | 06_Templates 36,503 (mostly code clones) |
| Largest single dir (bytes) | المتكرر 00 — 18.92 GB (duplicate quarantine) |
| Media bytes (video+audio+images+fonts) | ~45 GB (76%) |
| Code-clone bytes | ~5.4 GB (9%) |

Machine-readable: `inventory.jsonl` (124,630 rows), `summary.json`, `categories.json`.

## 3. User Estimate vs Actual Inventory

| Category | Estimated | Actual (verified) | Verdict |
|---|---|---|---|
| Fonts | ~23,501 | **3,573** TTF/OTF (+784 webfont files, heavily duplicated; 351 families) | OVER ×6.6 (estimate === stale catalog total) |
| Icons | ~1,184 | **~29,000 SVG** (lucide/phosphor/tabler) + 501 PNG | UNDER ×24 |
| SFX | ~5,000 | **~150 loose + ~700 locked in GDC zips** (<1k addressable) | OVER ×5+ |
| Music | ~9 | **1,490 tracks, ~87 h** (Incompetech CC-BY) | UNDER ×165 |
| Video assets | ~1,442 | **440 files** (+1 locked in BBB zip) | OVER ×3.3 |
| Templates | ~36 | **~240 real web templates** (+36k clone files) | roughly right, buried |
| AI models | ~5,000 | **5 files** (1.56 GB) | OVER ×1000 |
| 3D assets | ~825 | **~640 model files** + textures/HDRI (many Khronos dev samples) | roughly right |
| Docs | ~5,000 | **16,147** (almost all MDN Web Docs clone — dev docs, not video docs) | UNDER ×3, wrong kind |
| Motion design | ~5,000 | **~14k files but ~13.5k are three.js/lottie dev clones**; ~70 real motion assets | category is mislabeled |

Root cause of bad estimates: `catalog.json` (2026-09-01, stale) capped each category at 5,000 rows and sampled misleading first files; folder names do not describe contents (§5).

## 4. Directory Structure

Numbered dirs `01_…10_` are the intended taxonomy but contents drifted. Real layout: `MH - محتوى بصري` (visual stash: `01-صور` 1,843 imgs / `02-فيديو` 376 vids), `04_Music/Incompetech`, `03_SFX` (3 zips), `05_VideoAssets/{NASA,Stock-Footage,Blender}`, `08_3D_Assets` (LUTs-Film/Camera, ambientCG, PolyHaven-HDRI…), `المتكرر 00` (quarantine: FNT/BG/FX/ICN/IMG/LUT/TPL/VID/ZIP/3D/CROSS/review), `06_Templates` (GitClones + HTML5UP + meraki-ui + tailwind-elements), `09_Docs` (mdn-content), `10_MotionDesign` (threejs, lottie-mega, gltf-assets, codrops, textures…), `07_AI_Models` (whisper-ggml, rembg), `_projects` (arsenal-x, gallery backup, lottie-hub, packs), `arsenal-dashboard`, `_scripts` (queue), `_logs` (manifest.tsv), `_tmp`, `lottie/`, `svg/`, `NK4 - png`, `Fonts-Organized`, `Google Fonts` (per-family source folders), `1/2/3` Arabic staging stubs (txt placeholders only), `03-خطوط` (276 TTF), `04-صوتيات` (6 mp3), `05-أخرى` (5 Arabic-named .lottie), `مؤثرات صوتية` (47 mp3), `موسيقى` (43 mp3), `catalog.json` (stale), `README.md` (0 bytes).

## 5. Asset Categories

Inferred (extension + signature + structure + content), counts are addressable files:

- **VIDEO** 440 files / 14.3 GB (433 mp4, 5 mkv, 1 mov + locked BBB mp4 in zip)
- **AUDIO_MUSIC** 1,490 / 11.3 GB · **AUDIO_SFX_LOOSE** 101 / 0.02 GB · **locked SFX** ~800 WAVs / ~21.7 GB in zips
- **IMAGE** ~11.2k / 3.1 GB (MH 1,842 + docs/press + texture jpgs)
- **ICON** ~29k / 0.06 GB (SVG systems)
- **FONT** 4,357 files / 0.62 GB (3,573 parsed + webfonts)
- **3D_MODEL** ~640 / 1.35 GB · **LUT** 720 files (329 .cube + thumbs)
- **MOTION** ~84 real (.lottie/.aep/logo-intros/packs) vs ~13.5k dev-clone files in the same folders
- **TEMPLATE_WEB** 275 real files (meraki-ui 228, HTML5UP 12, ar-template 93, shadcn zips)
- **CODE_CLONE** 66,289 / 5.4 GB (three.js, chakra, MDN, lottie-mega, next.js examples — dev reference, not assets)
- **APP_PROJECT** 16,464 / 1.0 GB (arsenal-x incl. committed node_modules, gallery, lottie-hub)
- **ARCHIVE** 1,560 / 22.8 GB (1,448 npm-cache junk zips + 10 media zips + shadcn)
- **AI_MODEL** 5 / 1.56 GB · **QUARANTINE_DUP** 4,228 / 18.9 GB · **DOC** ~20k (MDN + misc)
- **UNKNOWN/negligible**: `.sample`, extensionless repo files, `.cow` (cowsay junk), `.vercel` build output — all inside clones.

Suspicious classifications: `06_Templates` and `10_MotionDesign` are >95% code clones; `09_Docs` is a web-docs clone; `02_Icons` contains .ts/.vue source of the icon packages (fine); `01_Fonts` contains Google-Fonts git metadata + METADATA.pb (useful license sidecars, §13).

## 6. Video Asset Analysis

Full technical probe: 438/440 open (`video_meta.jsonl`). 2 failures recorded (1 non-video bytes misnamed `.mp4` in a demo folder, 1 corrupt remotion render — both named in report data).

- Codecs/containers: h264 434, vp8 4; mov/mp4 433, matroska 5. No HEVC/AV1/ProRes — uniformly H.264 stock.
- Resolution: 720p 168 · 1440p 88 · 1080p 47 · 4K 31 · vertical 9:16 ≈ 52 (2160×3840:16, 1080×1920:18, 1440×2560:10) · square-ish/misc rest. Vertical + 4K present = Shorts + premium B-roll ready.
- FPS: 30 (141), 25 (112), 29.97 (75), 60 (30), 24 (27), 23.976 (20), 59.94/50 (27). Mixed standards — normalize at ingest.
- Audio present in 153/438 (35%).
- Duration: min 3.4 s, median 15.3 s, p90 46.8 s, max 70 min (NASA EZIE 2.08 GB), total ≈ 389 min.
- Locations: MH 376 · NASA 27 · GitClones demos 10 · threejs/codrops 8 · Stock-Footage 4 · gallery/logo/remotion ≤4 each · quarantine VID 1.

Semantic sampling (deterministic every-10th MH video, 38/376 = 10.1%, 3 frames each at 25/50/75% → 5 contact sheets, `frames/sheet_*.jpg`, index in `frame_index.json`). Observed subjects: European/American city aerials (day/night), business (handshake, meeting, office, laptop macro), technology (server rooms, neon data cube, HUD globe, code screens, binary networks), finance (gold bars/coins, trading screens, equalizer), space (black hole render, NASA reals), traffic (subway B&W, highways, Times Square timelapse), people (desk work, portraits), nature (mountains, ocean), abstract (smoke/ink, bokeh particles, gradients), templates (thank-you outros, countdown, SEO whiteboard, STARTUP mockup), vector explainer animation. Bias: business/tech/finance/city; weak: food, sport, animals, Arabic-context footage. Quality: clean licensed-stock look, stable shots, good light. Vertical clips exist for Shorts. NOT visually verified: remaining 338 MH videos + NASA long-form content (filenames trusted only for NASA, which are descriptive: ISS, solar flares, Webb, aurora, Mars rover).

## 7. Audio / Music / SFX Analysis

Full probe 1,591/1,591 (`audio_meta.jsonl`): mp3 1,572 · wav 14 · ogg 5; stereo 1,553 · mono 38; 44.1 kHz 1,378 · 48 kHz 208; total ≈ 86.9 h; median track 175 s.

- **Music** (`04_Music/Incompetech`, 1,441 + 49 Arabic-folder tracks): real Kevin MacLeod titles, CC-BY (LICENSE.txt present → attribution required, registry missing). Genre: UNKNOWN by policy (no listening, no tags) — titles hint cinematic/ambient/corporate/8-bit variety. Whisper-tiny vocal probe on 8 random tracks: 5 instrumental, **3 contain baked YouTube outro speech ("thank you for watching… subscribe")** — provenance-contaminated, quarantine before broadcast use.
- **SFX loose** (150 files, 86 under 3 s): freesound-style descriptive names — whoosh 18, swoosh 14, boom 10, riser 10, click/UI 7+, transition 6, glitch/chime/sweep/drop/flash 2–4 each; `sfx-transitions-pack` has mp3+wav pairs (boom-deep, chime-logo, reverse-sweep, riser-cinematic, subdrop, whoosh-airy). Acoustic features (`audio_char.jsonl`, 210 files): SFX median centroid 1,115 Hz vs music 926 Hz, higher dynamics — consistent with transient design sounds. Verdict: small but directly usable transition/UI kit.
- **SFX locked** (~21.7 GB zips, central directories listed read-only): GDC2024 Parts 1,2,3,4,6,8,9 + GDC2019 Part1 + 03_SFX Parts 5,9 — UCS-compliant pro names (cinematic hits/impacts, creaks/risers, vehicles, foley, rivers, breath/character). **GDC2019 `Part1of8.zip` (1.35 GB) is NOT a zip (corrupt or renamed)** — re-acquire. One-time local extraction unlocks ~800 files; names are already semantic.

## 8. Image / Icon / Motion Analysis

- **MH images** 1,842/1,842 readable (`image_stats.json`): JPEG 1,808 · PNG 32; 83% vertical (phone-wallpaper collection, median 736×1104, max 7330×7759); alpha only 3. Filenames often descriptive (`736x1308 black-vertical-photo-103.jpg`, `data-center-dark.jpg`, `orange-vertical-photo-12.jpg`) but ~half are numeric IDs. 13-image vision sample: anime posters, cars (GTR/BMW), data-center corridor, product (ring), motorcycle engine, Islamic pattern, marble/gold abstract, portraits, quote graphics, ONE Arabic official certificate (personal-data visible — privacy flag §26).
- **Icons**: lucide (5,303 files) + phosphor (18,189) + tabler + svg/ Material Symbols + meteocons package. Filenames ARE semantic (curated sets, e.g. `arrow-right.svg`, `1k_24dp…`) — filename indexing valid here. No SVG rasterizer installed → no rendered previews (limitation; lucide/phosphor docs are the visual reference).
- **Motion**: real assets ≈ 70 — `lottie/` 17, `05-أخرى` 5 Arabic-named (.lottie), lottie-library 154, logo-intros 5, sfx/social/fashion packs; lottie-mega is 4,077 SDK samples (700 real + scaffolding, per existing code comments). `.aep` 36 = lottie-android samples (dev, not templates).

## 9. Font Analysis

Parsed 3,573/3,573 name tables with a hand-rolled reader (no fontTools): 3,243 TrueType + 330 OpenType, 0 corrupt, **351 distinct families**. Duplication is extreme (Inter optical-size × weight grid, DM Sans/Jakarta dozens each — cross-location copies confirmed §14). **189 files cover Arabic** (cmap U+0627 probe): Amiri 41, Aref Ruqaa 19+14 Ink, Scheherazade New 17+16, Tajawal 6, Blaka Ink 6, Harmattan 5+, IBM Plex Sans Arabic 5+, Cairo 4, Almarai 3+7, Rakkas 3, Changa/El Messiri/Kufam 2–4 — a broadcast-ready Arabic caption shortlist. +784 webfont files (woff/woff2/eot, mostly family dupes). Google `METADATA.pb` sidecars exist for OFL families (license evidence). Variable/static not fingerprinted (limitation — `fvar` check recommended). Nothing installed (rule).

## 10. AI Model Inventory

`models.jsonl` — 5 files, all standard public releases (name+size matched, never executed): whisper `ggml-base/small/large-v3-turbo-q5_0` (148/488/547 MB, STT offline **with whisper.cpp only — faster-whisper cannot read ggml**), rembg `u2net/isnet-general-use` .onnx (176/179 MB, bg-removal, needs onnxruntime — not installed). No configs/docs alongside. No vision/VLM/embedding/upscaling/detection models present.

## 11. Templates

Real: meraki-ui 228 files, HTML5UP 12, `_projects/ar-template-restaurant` 93, shadcn template zips, tailwind-elements. Rest of `06_Templates` is GitClones dev (chakra, react-three-fiber, nextjs-examples — demos/scaffolding, some with demo videos). No video-editing templates (no Premiere/Resolve/DaVinci project templates found).

## 12. 3D Assets

~640 model files: glTF 237 + GLB 220 (mostly Khronos `gltf-assets` dev samples — NOT production), 30 .blend (ambientCG material scenes), 22 .usdc (material sidecars), marble 4K set, PolyHaven-HDRI (17), Cardboard/Metal/Paper PBR sets, .mtlx/.tres. Production-usable: PBR texture sets + HDRI + marble; the 400+ Khronos samples are reference only.

## 13. Documentation

16,147 files ≈ MDN Web Docs clone (dev reference) + 36k more docs inside code clones (tsx/js READMEs). **Almost zero video-production documentation.** Valuable exception: Google-Fonts METADATA.pb + Incompetech LICENSE.txt + GDC pdf/txt/xlsx manifests inside zips (license/provenance sidecars — ingest these first).

## 14. Duplicate Analysis

7,915 exact (name+size) groups / 27,481 files (22%); 1,643 cross-directory groups (`duplicates.json`). 60/60 sampled cross-location pairs confirmed byte-identical (head+tail sha256) → EXACT_DUPLICATE verdict for the quarantine pattern. `المتكرر 00/ZIP/review/` is a human staging tree (`dup/`, `review/`) — the user already quarantines dupes there. Internal clone dupes (MDN locales, node_modules) dominate counts; real reclaimable media dupes ≈ FNT 785 + BG/FX/IMG/LUT ≈ 1,000+ files / ~19 GB. Recommendation: сложи hash registry (below) before ANY move; never auto-delete (locale variants and intentional packs look like dupes).

## 15. Unknown / Unclassified Assets

Truly unknown ≈ small: 1,891 extensionless files (all inside code clones — repo dotfiles), `.sample` (717, dev fixtures), corrupt GDC2019 zip (1.35 GB, format unknown), 2 unreadable videos, `.rev/.idx/.pack` (git object stores). Everything else classified ≥ by signature. No encrypted/obscure blobs of consequence.

## 16. Existing Tools and Infrastructure

- **arsenal-x** (`_projects/arsenal-x`, Next.js 15 + Tailwind + lottie-web + gsap, node_modules committed): 26 API routes (search, discover, gaps, resolve, reindex, fonts/icons/images/video/music/sfx/models/luts/templates/fx/backgrounds/archives/collections/vault/kit/tools/system…), `lib/indexer.ts` (curated per-category roots, X-Code stable ids, junk filters, Arabic BG tags), `lib/arsenalSearch.ts` (scored AND/OR token search), `lib/{indexCache,quality,workspace}.ts`. Verdict: the asset backend to extend — BUT `ROOT='D:\Arsenal'` (wrong drive) and search is filename-only.
- **arsenal-dashboard**: 5-file static server + Arabic UI over `catalog.json` (500-row cap, no previews). Reuse pattern only.
- **catalog.json** (10.8 MB, 2026-09-01): 23,501 rows capped at 5,000/category; stale (predates 09-17 additions), categories misaligned with reality. Regenerate, don't patch.
- **Acquisition**: `_scripts/download_queue.ps1` (curl worker, single-instance lock, manifest.tsv provenance log — 5+ logged OK downloads incl. SFX/models) + `queue.txt` (empty). Reusable pattern with fixed paths + license/validation steps.
- **Previews**: `_projects/arsenal-gallery-BEFORE-XUPGRADE`, `lottie-hub`, `logo-intros`, `social-pack-restaurants`, `nexora-remotion` (has `out/dramatic-reveal.mp4` — prior render attempts), `sfx-transitions-pack`, `fashion-icons-pack`.

## 17. Existing Databases / Indexes

None durable: `indexCache.ts` is in-memory; no SQLite/JSONL store/vector DB found (searched extensions: no .db/.sqlite/.faiss/.index outside clones). `manifest.tsv` (download log) is the only provenance store. The audit's own `inventory.jsonl` + `video/audio_meta.jsonl` + `fonts.jsonl` are the first durable indexes — adopt as seeds.

## 18. Existing Semantic Search Capabilities

Filename/tag token search only (arsenal-x AND/OR scorer; dashboard substring). No embeddings, no visual features, no speech content index, no mood/genre tags. Gap is total — this is the build target, not a reuse item (reuse the API shell).

## 19. Existing Vision Capabilities

None in-arsenal (no VLM, no tagger, no frame index). This audit substituted methodically: 114 video thumbs (38 videos × 3) + 13 stills reviewed as contact sheets (§6/§8). Available local vision primitives for the build: OpenCV 5 (dhash/hist/pHash-able), PIL (color stats), PyAV (frame decode) — enough for near-dup, color/mood, and brightness/quality signals; NOT enough for object/scene semantics without a VLM.

## 20. Existing AI Models That Could Help Asset Analysis

whisper-ggml (transcribe SFX-voice/music-vocal detection, vocal-vs-instrumental, silence profiling — needs whisper.cpp), faster-whisper tiny already on machine (same, different format), rembg onnx (subject masks/thumbnails — needs onnxruntime), nothing for embeddings/objects/faces/OCR/mood. First acquisition targets/attempts: CLIP-style embedding model, PaddleOCR/locale-OCR, audio embedding (CLAP-ish) — via the future acquisition flow, not now.

## 21. Reusable Components

`reuse_candidates.json` (11 entries). Headline order: (1) arsenal-x API+UI shell, (2) whisper models for audio intelligence, (3) this audit's JSONL indexes as registry seeds, (4) LUT packs, (5) Arabic font shortlist + METADATA.pb licenses, (6) Incompetech + GDC SFX (post-extraction), (7) MH/NASA video + full tech metadata, (8) icon systems, (9) rembg models, (10) download-queue pattern, (11) dashboard server pattern.

## 22. Missing Capabilities

Semantic video tags (90% untagged), audio genre/mood tags, embedding + vector store, perceptual-hash registry, license/attribution registry, preview/thumbnail pipeline, SVG rasterizer, fontTools-class inspection (worked around), onnxruntime/whisper.cpp runtimes, VLM tagger, acquisition validator, quarantine/delete workflow, ROOT path fixes (D:→F: across 3+ scripts), catalog regeneration, vertical-video and 4K-aware search facets.

## 23. Recommended Future Asset Intelligence Architecture

`ingest` (walk → file row: path/size/mtime/mime) → `identify` (signature+ext → category; quarantine review for UNKNOWN) → `fingerprint` (sha256 head+tail → full on demand; pHash for images/video-frames; duration/dims for media) → `probe` (PyAV technical; fontTools-class tables; zip central dirs) → `understand` (VLM frames ×3/video; whisper vocal/silence; font cmap; icon-name taxonomy; UCS SFX names) → `registry` (JSONL-first, SQLite on growth; asset_id = stable code à la X-Code) → `serve` (extend arsenal-x routes: semantic search, previews, license, gaps) → `verify` (match cards with evidence lists, §11 flow). Deterministic, offline, incremental reindex by mtime.

## 24. Recommended Future Asset Acquisition Architecture

Requirement → local search (arsenal-x extended) → hit? serve : acquisition request (need, specs, budget, approved sources: Sonniss/GDC, Incompetech, NASA, Pexels-license-checked, Google Fonts) → download worker (existing queue pattern + manifest.tsv) → validate (format/probe/corruption — cf. GDC2019 zip) → analyze (same pipeline as §23) → license/provenance record (METADATA.pb/LICENSE sidecars mandatory) → registry → notify. Never bulk-download; every fetch traces to a stated video need.

## 25. Recommended Integration Points With The Future Video Engine

Asset Engine exposes: `search/requirement → candidates+evidence`, `resolve/X-Code → file + technical + license`, `keyframes/preview` endpoints. Video Engine consumes: B-roll casting (Phase 13 executor), caption fonts (Arabic shortlist → Phase 14 styles), LUT intents (color phase), SFX spotting (whoosh/riser/impact taxonomy maps to transition points), music beds (attribution-aware). Shared contracts: stable X-Codes, content hashes, timeline-technical metadata (this audit's `video/audio_meta.jsonl` shape). Orchestrator (MASTER) routes local-first; n8n/automation engine handles watch-folders + reindex triggers; model engine hosts whisper/rembg/embedding runtimes.

## 26. Important Risks / Limitations

1. Licenses unverified per-file (CC-BY needs attribution registry; GDC/Sonniss terms; font OFL vs unknowns; NASA mostly public domain but not per-file confirmed; YouTube-outro contamination in 3+ mp3s).
2. Personal data: Arabic certificate scan in MH images — exclude from any shared index/preview.
3. Stale/broken paths: D: hardcodes, stale catalog, corrupt zip + 2 bad videos.
4. Coverage: vision 10% video / <1% images; genres/moods UNKNOWN by design (no hallucination).
5. No VLM/embeddings on machine — semantic depth capped until acquisition.
6. 22% duplication + 18.9 GB quarantine — reclaim only via hash registry + human review.
7. node_modules/.next committed (~1 GB reinstallable weight).

## 27. Exact Next-Step Recommendation

1. Fix arsenal-x `ROOT` → F:\Arsenal and regenerate its index (1 day). 2. One-time local extraction of the 9 readable GDC zips + BBB zip into a staged (not arsenal-mutating… actually new sibling dir) area and index the ~800 WAVs (names already semantic). 3. Adopt this audit's JSONL as registry seeds + add sha256/pHash columns. 4. Acquire (via future flow) one CLIP-style embedding model + onnxruntime + whisper.cpp → backfill semantic tags starting with the 376 MH videos. 5. Build attribution/license registry before any publish use. Then STOP — no engine work until the registry exists.

## WHAT THE FUTURE AL-MONTIER SYSTEM WILL BE ABLE TO ASK

- "Find me a 5-second 16:9 futuristic server-room shot." → facet filter (16:9, ≤8 s) over `video_meta` → semantic tags (server/tech/blue) → top: MH data-center clips verified by the `data-center-dark.jpg` frame pattern + teal/blue histogram + 16:9 + 5–8 s; match card lists evidence; rejected example: laptop-desk clip (office, warm light, no racks).
- "Find a clean technology background for a title." → backgrounds index (gradient/grain/gold tags exist today) + dark, low-detail frames (variance filter) → e.g. blue-HUD clip [13] verified dark + center-safe.
- "Find a dark cinematic city-at-night clip." → night-city frames (Times Square timelapse [17], highway aerial [18]) via brightness + city tags.
- "Find a UI animation suitable for explaining software." → lottie category (Business Analysis/Data Analytics files exist) + rendered preview check once rasterizer acquired.
- "Find an SFX for a fast text transition." → SFX taxonomy (whoosh-airy 18, swoosh 14, riser 10, <1 s, high-centroid) → exact files + peak/RMS evidence.
- "Find Arabic-compatible fonts suitable for modern captions." → fonts.jsonl arabic=true ∩ modern families (IBM Plex Sans Arabic, Tajawal, Cairo, Almarai) + OFL license evidence from METADATA.pb.

Each answer carries a match card (score + evidence bullets + rejection reasons), exactly per the §11 flow — served by the extended arsenal-x API, grounded in this audit's indexes.
