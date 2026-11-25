"""Chart Curious — animated bar chart renderer (1080x1920, 30fps, H.264).

Usage: python3 render_bars.py spec.json out.mp4
spec: {hook:[lines], subhook, bars:[{label,value,highlight?}], unit, decimals,
       takeaway:[lines], source, note}
"""
import json, sys, subprocess, tempfile, os, glob
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (14, 17, 23); BLUE = (90, 140, 255); AMB = (255, 184, 0)
WH = (240, 240, 240); MUT = (160, 170, 185); DIM = (60, 68, 82)

def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)

F_HOOK, F_SUB, F_LAB, F_VAL, F_SRC, F_TAKE = font(56), font(34, False), font(34), font(36), font(26, False), font(46)

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def mark(d, x, y, s):
    w = s * 0.2; g = s * 0.1
    for i, h in enumerate([0.35, 0.6, 0.85]):
        x0 = x + i * (w + g)
        d.rounded_rectangle([x0, y + s * (1 - h), x0 + w, y + s], radius=int(w * 0.18), fill=BLUE if i < 2 else WH)
    cx = x + 2 * (w + g) + w / 2; r = s * 0.09
    d.ellipse([cx - r, y + s * 0.02 - r, cx + r, y + s * 0.02 + r], fill=AMB)

def text_block(d, lines, f, y, fill, x=80, gap=12, alpha=1.0):
    col = tuple(int(BG[i] + (fill[i] - BG[i]) * alpha) for i in range(3))
    for ln in lines:
        d.text((x, y), ln, font=f, fill=col); y += f.size + gap
    return y

def render(spec, out):
    bars = spec["bars"]; n = len(bars)
    vmax = max(b["value"] for b in bars) * 1.08
    dec = spec.get("decimals", 1); unit = spec.get("unit", "")
    T_HOOK, T_GROW, T_TAKE, T_END = 2.2, 4.5, 4.0, 2.3
    total = int((T_HOOK + T_GROW + T_TAKE + T_END) * FPS)
    tmp = tempfile.mkdtemp()
    top = 500; area = 1270 - top; step = area / n; bh = step * 0.42
    for i in range(total):
        t = i / FPS
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        if t < T_HOOK + T_GROW + T_TAKE:
            mark(d, 80, 150, 60)
            d.text((160, 164), "Chart Curious", font=font(34), fill=MUT)
            y = text_block(d, spec["hook"], F_HOOK, 250, WH, alpha=1.0)
            if spec.get("subhook"):
                text_block(d, [spec["subhook"]], F_SUB, y + 8, MUT, alpha=ease((t - 0.3) / 0.5))
            g = ease((t - T_HOOK) / T_GROW)
            for k, b in enumerate(bars):
                yy = top + k * step
                stagger = ease((t - T_HOOK - k * 0.12) / (T_GROW * 0.8))
                w = 600 * b["value"] / vmax * stagger
                hl = b.get("highlight")
                fade = 1.0
                if t > T_HOOK + T_GROW and not hl:
                    fade = 1 - 0.55 * ease((t - T_HOOK - T_GROW) / 0.6)
                col = AMB if hl else BLUE
                col = tuple(int(BG[c] + (col[c] - BG[c]) * fade) for c in range(3))
                d.text((80, yy), b["label"], font=F_LAB, fill=tuple(int(BG[c] + (WH[c] - BG[c]) * fade) for c in range(3)))
                if w > 2:
                    d.rounded_rectangle([80, yy + 44, 80 + w, yy + 44 + bh], radius=8, fill=col)
                val = b["value"] * stagger; dd = b.get("decimals", dec)
                d.text((80 + w + 16, yy + 44 + bh / 2 - 21), f"{val:.{dd}f}{unit}", font=F_VAL,
                       fill=tuple(int(BG[c] + (WH[c] - BG[c]) * fade) for c in range(3)))
            if t > T_HOOK + T_GROW:
                a = ease((t - T_HOOK - T_GROW - 0.4) / 0.6)
                text_block(d, spec["takeaway"], F_TAKE, 1300, WH, alpha=a)
            d.text((80, 1440), spec["source"], font=F_SRC, fill=MUT)
            if spec.get("note"):
                d.text((80, 1476), spec["note"], font=F_SRC, fill=DIM)
        else:
            a = ease((t - (T_HOOK + T_GROW + T_TAKE)) / 0.5)
            mark(d, 440, 640, 200)
            ttl = "Chart Curious"; tw = d.textlength(ttl, font=font(80))
            d.text(((W - tw) / 2, 900), ttl, font=font(80), fill=tuple(int(BG[c] + (WH[c] - BG[c]) * a) for c in range(3)))
            sub = "Follow for one surprising chart a day"; sw = d.textlength(sub, font=F_SUB)
            d.text(((W - sw) / 2, 1020), sub, font=F_SUB, fill=tuple(int(BG[c] + (MUT[c] - BG[c]) * a) for c in range(3)))
        im.save(f"{tmp}/{i:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.png",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], check=True)
    # cover frame for checking
    Image.open(f"{tmp}/{int((T_HOOK + T_GROW + T_TAKE - 0.5) * FPS):05d}.png").save(out.replace(".mp4", "_frame.png"))
    for f in glob.glob(f"{tmp}/*.png"): os.remove(f)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
