"""Draws the Volsplat preview image: an original illustration of a Gaussian splat.

A trefoil-knot tube and a floor are built from ~40,000 soft, translucent, flattened ellipses ("Gaussians"),
sorted back to front and blended, the way a splat renderer does. A circular lens shows the outlines of
individual Gaussians. Output: site/assets/img/volsplat-preview.webp.   python3 tools/make_preview.py
"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1600, 900
rng = np.random.default_rng(7)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "assets", "img")

# ---- scene -------------------------------------------------------------------------------------------
def knot(t):
    return np.stack([np.sin(t) + 2*np.sin(2*t), np.cos(t) - 2*np.cos(2*t), -np.sin(3*t)], -1)

N, M, R = 230, 16, 0.42
t = np.linspace(0, 2*np.pi, N, endpoint=False)
c = knot(t); d = 1e-3
T = (knot(t + d) - knot(t - d)); T /= np.linalg.norm(T, axis=1, keepdims=True)
up = np.array([0, 0, 1.0]); Nn = np.cross(T, up); Nn /= np.linalg.norm(Nn, axis=1, keepdims=True); Bn = np.cross(T, Nn)
phi = np.linspace(0, 2*np.pi, M, endpoint=False)
P, NRM, TAN, PAR, COL = [], [], [], [], []
pal = np.array([[1.0, .10, .30], [.10, 1.0, .55], [.25, .45, 1.0]])
for i in range(N):
    off = (rng.random() - .5) * 2*np.pi / M
    for j in range(M):
        a = phi[j] + off + i * 0.11
        n = np.cos(a) * Nn[i] + np.sin(a) * Bn[i]
        P.append(c[i] + R * n * (1 + rng.normal(0, .015))); NRM.append(n); TAN.append(T[i])
        PAR.append(np.cross(n, T[i]))
        u = (t[i] / (2*np.pi) * 3) % 3; k = int(u); f = u - k
        base = pal[k] * (1 - f) + pal[(k + 1) % 3] * f
        COL.append(base)
P, NRM, TAN, PAR, COL = map(np.array, (P, NRM, TAN, PAR, COL))
SZ = np.full(len(P), 1.0) * (2*np.pi * R / M) * 0.5
OP = np.full(len(P), 0.9)

# floor: a disc of small flat splats with a faint grid in its colour
G = 2600
r = 5.6 * np.sqrt(rng.random(G)); th = rng.random(G) * 2*np.pi
fp = np.stack([r*np.cos(th), r*np.sin(th), np.full(G, -1.55)], -1)
gx = (np.abs(((fp[:, 0] * 1.2) % 1) - .5) < .06) | (np.abs(((fp[:, 1] * 1.2) % 1) - .5) < .06)
fc = np.where(gx[:, None], np.array([.30, .38, .70]), np.array([.08, .10, .20])) * (1 - r[:, None] / 6.4)
fn = np.tile([0, 0, 1.0], (G, 1)); ft = np.tile([1.0, 0, 0], (G, 1)); fpar = np.tile([0, 1.0, 0], (G, 1))
fsz = np.full(G, .20); fop = np.full(G, .8)

# a few floaters, as every real capture has
F = 160
flp = np.stack([rng.normal(0, 3.2, F), rng.normal(0, 3.2, F), rng.normal(0, 1.2, F)], -1)
flc = pal[rng.integers(0, 3, F)] * .5
fln = np.tile([0, 0, 1.0], (F, 1)); flt = np.tile([1.0, 0, 0], (F, 1)); flpar = np.tile([0, 1.0, 0], (F, 1))
flsz = rng.uniform(.08, .22, F); flop = np.full(F, .3)

P = np.concatenate([fp, P, flp]); NRM = np.concatenate([fn, NRM, fln]); TAN = np.concatenate([ft, TAN, flt])
PAR = np.concatenate([fpar, PAR, flpar]); COL = np.concatenate([fc, COL, flc]); SZ = np.concatenate([fsz, SZ, flsz])
OP = np.concatenate([fop, OP, flop]); ISSURF = np.concatenate([np.zeros(G), np.ones(N*M), np.zeros(F)])

# ---- camera ------------------------------------------------------------------------------------------
cam = np.array([7.4, -8.6, 4.6]); tgt = np.array([0, 0, -.2])
fwd = tgt - cam; fwd /= np.linalg.norm(fwd)
right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
upv = np.cross(right, fwd)
foc = 1180.0

def project(X):
    rel = X - cam
    z = rel @ fwd
    return np.stack([W/2 + foc * (rel @ right) / z, H/2 - foc * (rel @ upv) / z], -1), z

ctr, z = project(P)
ax1 = (project(P + TAN * SZ[:, None] * 1.0)[0] - ctr)
ax2 = (project(P + PAR * SZ[:, None] * 1.0)[0] - ctr)

# shading: soft key light + rim + a glint, tinted by the splat's own colour
L = np.array([-.4, -.6, .7]); L /= np.linalg.norm(L)
V = -(P - cam); V /= np.linalg.norm(V, axis=1, keepdims=True)
lam = np.clip(NRM @ L, 0, 1)
rim = np.clip(1 - np.abs((NRM * V).sum(1)), 0, 1) ** 2
Hh = L + V; Hh /= np.linalg.norm(Hh, axis=1, keepdims=True)
spec = np.clip((NRM * Hh).sum(1), 0, 1) ** 40
shade = np.where(ISSURF > 0, .35 + .75 * lam + .5 * rim, 1.0)
col = np.clip(COL * shade[:, None] + (spec * .8 * ISSURF)[:, None], 0, 1)

# ---- background and blending ---------------------------------------------------------------------
yy, xx = np.mgrid[0:H, 0:W]
bg = np.zeros((H, W, 3), np.float32)
vig = np.clip(1 - (((xx - W*.55)/ (W*.75))**2 + ((yy - H*.5)/(H*.85))**2), 0, 1)
bg += (np.array([.030, .040, .085]) * vig[..., None] + np.array([.012, .013, .028]))
img = bg.copy()

order = np.argsort(-z)                       # far to near
OUTL = []
LC, LR = (640, 500), 130
for idx in order:
    cx, cy = ctr[idx]
    a1, a2 = ax1[idx], ax2[idx]
    cov = np.outer(a1, a1) * 1.5 + np.outer(a2, a2) * 0.55 + np.eye(2) * 0.25
    ev = np.linalg.eigvalsh(cov); rad = int(np.ceil(3 * np.sqrt(ev[-1])))
    if rad < 1 or cx < -rad or cx > W + rad or cy < -rad or cy > H + rad: continue
    if rad > 45: continue
    x0, x1 = max(int(cx) - rad, 0), min(int(cx) + rad + 1, W); y0, y1 = max(int(cy) - rad, 0), min(int(cy) + rad + 1, H)
    if x1 <= x0 or y1 <= y0: continue
    gx_, gy_ = np.meshgrid(np.arange(x0, x1) - cx, np.arange(y0, y1) - cy)
    inv = np.linalg.inv(cov)
    e = inv[0, 0]*gx_*gx_ + 2*inv[0, 1]*gx_*gy_ + inv[1, 1]*gy_*gy_
    al = np.exp(-.5 * e) * OP[idx]
    al = al[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al) + col[idx] * al
    if ISSURF[idx] and (cx-LC[0])**2+(cy-LC[1])**2 < LR*LR and rng.random() < .09:
        OUTL.append((cx, cy, cov, col[idx]))

out = Image.fromarray((np.clip(img, 0, 1) ** (1/1.08) * 255).astype(np.uint8))

# strip on the left: outlines of single Gaussians (2-sigma ellipses)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
for cx, cy, cov, cl in OUTL:
    w, v = np.linalg.eigh(cov); s = 2 * np.sqrt(np.maximum(w, 1e-6))
    ang = np.linspace(0, 2*np.pi, 40)
    pts = (v @ (np.stack([np.cos(ang) * s[0], np.sin(ang) * s[1]]))).T + [cx, cy]
    a = 200
    dr.line([tuple(p) for p in pts], fill=(235, 240, 255, a), width=1)
dr.ellipse([LC[0]-LR, LC[1]-LR, LC[0]+LR, LC[1]+LR], outline=(235, 240, 255, 150), width=2)
out = Image.alpha_composite(out.convert("RGBA"), ov).convert("RGB")

os.makedirs(ROOT, exist_ok=True)
out.save(os.path.join(ROOT, "volsplat-preview.webp"), quality=84, method=6)
out.save("/tmp/volsplat-preview.png")
print("saved", os.path.getsize(os.path.join(ROOT, "volsplat-preview.webp")) // 1024, "KB;", len(P), "gaussians")
