# Chart Curious production playbook (public-safe; no credentials or private data)

## Format
- 1080x1920, 30fps, H.264 + AAC, 10-15s. Render with tools/render_bars.py from a spec JSON in specs/.
- Hook = a question or claim the chart answers. Hook visible from frame 0. Takeaway states the surprise in plain words.
- Safe zones: keep text x 80..940, y 150..1520. Nothing important below y=1520 (captions cover it) or right of x=940 (buttons).
- Source line on screen every time ("Source: X via Y"). Flag early estimates / filters in the note line.

## Data rules
- Use primary or reputable aggregated data that is reachable from GitHub raw (e.g. owid/co2-data, owid/energy-data, datasets/* repos) or a primary source page you have read. Never invent or round in a misleading way. Recompute any ratio shown.
- Comparisons must be like-for-like (same year, same definition). State filters (e.g. "countries generating 20+ TWh").
- No gambling, politics-baiting, health advice, finance advice or tragedy content. No real people's images, logos or copyrighted footage.

## QA before queueing (all must pass)
1. Every number on screen matches the computed data.  2. Text widths <= 860px at render size.  3. View the takeaway frame and frame 0.  4. ffprobe: 1080x1920, h264, 10-15s.  5. Caption has the source, a question to prompt comments, 4-5 hashtags; YouTube caption starts with #shorts in hashtags and has a title <= 100 chars.

## Posting
- One post per day per platform at 10:37 Darwin (US evening). Same video to TikTok, Instagram Reel (shouldShareToFeed true), YouTube Short (categoryId 27, madeForKids false, public).
- Keep 3-7 days queued per channel; Buffer free plan caps 10 scheduled posts per channel.
- Upload video to this repo (posts/sNNN.mp4), wait for raw URL 200, then create_post with customScheduled dueAt (+11:00 Sydney offset in Buffer).
