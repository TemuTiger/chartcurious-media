"""Chart Curious — v2 renderer: punchline-first hook, motion from frame 0, sound bed, ~8s loop.

Why v2 (27 Nov 2026): v1 showed a question over an empty chart for 2.2s and revealed the
takeaway at ~7s; average watch was ~3s (TikTok) and ~4.5s (IG), so most viewers never saw
the point. v2 states the surprise at frame 0 and has the chart moving immediately.

Usage: python3 render_v2.py spec.json out.mp4
spec: v1 fields plus `hook` lines where *text* is drawn in amber; optional `takeaway`.
"""
import json, sys, subprocess, tempfile, os, glob, wave, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (14, 17, 23); BLUE = (90, 140, 255); AMB = (255, 184, 0)
WH = (240, 240, 240); MUT = (160, 170, 185); DIM = (60, 68, 82)
MAXW = 860
T_GROW, T_PING, T_TAKE, T_FOLLOW, T_END = 2.2, 2.3, 2.6, 4.2, 8.0

def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def mix(c, a):
    return tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))

def mark(d, x, y, s):
    w = s * 0.2; g = s * 0.1
    for i, h in enumerate([0.35, 0.6, 0.85]):
        x0 = x + i * (w + g)
        d.rounded_rectangle([x0, y + s * (1 - h), x0 + w, y + s], radius=int(w * 0.18), fill=BLUE if i < 2 else WH)
    cx = x + 2 * (w + g) + w / 2; r = s * 0.09
    d.ellipse([cx - r, y + s * 0.02 - r, cx + r, y + s * 0.02 + r], fill=AMB)

def segs(line):
    return [(p, i % 2 == 1) for i, p in enumerate(re.split(r"\*", line)) if p]

def fit(d, lines, size, bold=True):
    while size > 30:
        f = font(size, bold)
        if all(sum(d.textlength(p, font=f) for p, _ in segs(l)) <= MAXW for l in lines):
            return f
        size -= 2
    return font(size, bold)

def rich(d, lines, f, y, alpha=1.0, gap=14, base=WH):
    for ln in lines:
        x = 80
        for p, hl in segs(ln):
            d.text((x, y), p, font=f, fill=mix(AMB if hl else base, alpha)); x += d.textlength(p, font=f)
        y += f.size + gap
    return y

def sound(path, dur):
    sr = 44100; n = int(sr * dur); t = np.arange(n) / sr; a = np.zeros(n)
    # soft kick pulse, 120 bpm
    for k in np.arange(0, dur, 0.5):
        i = int(k * sr); m = min(n - i, int(0.35 * sr)); tt = np.arange(m) / sr
        f = 50 + 70 * np.exp(-tt * 30)
        a[i:i + m] += 0.55 * np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 9)
    # rising whoosh while bars grow
    m = int(T_GROW * sr); rng = np.random.default_rng(7); nz = rng.standard_normal(m)
    tt = np.arange(m) / sr; env = (tt / T_GROW) ** 2 * np.exp(-(tt - T_GROW) ** 2 * 0) * 0.18
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 660 * (tt / T_GROW) ** 2) / sr)
    a[:m] += env * (0.5 * nz * np.abs(sweep) + 0.6 * sweep)
    # bright ping on the reveal
    i = int(T_PING * sr); m = min(n - i, int(1.2 * sr)); tt = np.arange(m) / sr
    a[i:i + m] += 0.35 * (np.sin(2 * np.pi * 880 * tt) + 0.6 * np.sin(2 * np.pi * 1320 * tt)) * np.exp(-tt * 5)
    # quiet pad for warmth
    a += 0.05 * (np.sin(2 * np.pi * 110 * t) + np.sin(2 * np.pi * 164.8 * t)) * np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.3)
    a = a / max(1e-9, np.abs(a).max()) * 0.5
    s = (np.stack([a, a], 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(s.tobytes())

def render(spec, out):
    bars = spec["bars"]; n = len(bars)
    vmax = max(b["value"] for b in bars) * 1.08
    dec = spec.get("decimals", 1); unit = spec.get("unit", ""); prefix = spec.get("prefix", "")
    total = int(T_END * FPS); tmp = tempfile.mkdtemp()
    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    F_HOOK = fit(probe, spec["hook"], 72); F_SUB = fit(probe, [spec.get("subhook", "")], 34, False)
    F_TAKE = fit(probe, spec.get("takeaway", []), 46) if spec.get("takeaway") else None
    F_LAB, F_VAL, F_SRC = font(34), font(36), font(26, False)
    yh = 250 + len(spec["hook"]) * (F_HOOK.size + 14)
    top = max(520, yh + 70); area = 1250 - top; step = area / n; bh = step * 0.42
    for i in range(total):
        t = i / FPS
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        mark(d, 80, 150, 60); d.text((160, 164), "Chart Curious", font=font(34), fill=MUT)
        y = rich(d, spec["hook"], F_HOOK, 240)
        if spec.get("subhook"):
            d.text((80, y + 4), spec["subhook"], font=F_SUB, fill=MUT)
        for k, b in enumerate(bars):
            yy = top + k * step
            g = ease((t - k * 0.08) / (T_GROW - 0.7))
            w = 600 * b["value"] / vmax * g
            hl = b.get("highlight"); fade = 1.0
            if t > T_PING and not hl:
                fade = 1 - 0.55 * ease((t - T_PING) / 0.5)
            col = AMB if hl else BLUE
            if hl and T_PING < t < T_PING + 0.5:
                pulse = 1 + 0.06 * np.sin((t - T_PING) / 0.5 * np.pi)
            else:
                pulse = 1.0
            d.text((80, yy), b["label"], font=F_LAB, fill=mix(WH, fade))
            if w > 2:
                d.rounded_rectangle([80, yy + 44, 80 + w * pulse, yy + 44 + bh], radius=8, fill=mix(col, fade))
            dd = b.get("decimals", dec)
            # value appears only once its bar is fully grown, so no still frame shows a partial number
            va = max(0.0, min(1.0, (g - 0.97) / 0.03))
            if va > 0:
                d.text((80 + w * pulse + 16, yy + 44 + bh / 2 - 21), f"{prefix}{b['value']:,.{dd}f}{unit}", font=F_VAL, fill=mix(WH, fade * va))
        if F_TAKE and t > T_TAKE:
            rich(d, spec["takeaway"], F_TAKE, 1268, alpha=ease((t - T_TAKE) / 0.4))
        if t > T_FOLLOW:
            d.text((80, 1478), "Follow for a new chart every day", font=font(30), fill=mix(BLUE, ease((t - T_FOLLOW) / 0.4)))
        d.text((80, 1408), spec["source"], font=F_SRC, fill=MUT)
        if spec.get("note"):
            d.text((80, 1440), spec["note"], font=F_SRC, fill=DIM)
        im.save(f"{tmp}/{i:05d}.png")
    sound(f"{tmp}/a.wav", T_END)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.png",
                    "-i", f"{tmp}/a.wav", "-shortest",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], check=True)
    Image.open(f"{tmp}/00000.png").save(out.replace(".mp4", "_f0.png"))
    Image.open(f"{tmp}/{int(5.0 * FPS):05d}.png").save(out.replace(".mp4", "_frame.png"))
    for f in glob.glob(f"{tmp}/*"): os.remove(f)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
