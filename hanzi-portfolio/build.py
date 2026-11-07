"""Build: python3 build.py [src/template.html] [dist/hanzi-designs-mockup.html]
Embeds assets/art/*.png as base64 JPEG (max 900px) into __IMG__ and extracts 5-colour palettes into __PAL__."""
import base64, io, json, sys
from PIL import Image

import os
HERE = os.path.dirname(os.path.abspath(__file__))
U = os.path.join(HERE, 'assets', 'art') + os.sep
ORDER = [
    ('alpha',    'alpha.png'),
    ('badroute', 'badroute.png'),
    ('target',   'target.png'),
    ('smoke',    'smoke.png'),
    ('menace',   'menace.png'),
    ('lacoste',  'lacoste.png'),
    ('power',    'power.png'),
    ('gabos',    'gabos.png'),
    ('nike',     'nike.png'),
    ('tfl',      'tfl.png'),
]

imgs = {}
pals = {}
for key, fn in ORDER:
    im = Image.open(U + fn).convert('RGB')
    if max(im.size) > 900:
        im.thumbnail((900, 900))
    q = im.copy(); q.thumbnail((180,180))
    px = list((q.get_flattened_data() if hasattr(q,'get_flattened_data') else q.getdata())); tot = len(px)
    buckets = {}
    for p in px:  # group into coarse colour bins, keep the average colour of each bin
        key2 = (p[0]>>4, p[1]>>4, p[2]>>4); b2 = buckets.setdefault(key2, [0,0,0,0])
        b2[0]+=1; b2[1]+=p[0]; b2[2]+=p[1]; b2[3]+=p[2]
    cols = [(v[0], (v[1]//v[0], v[2]//v[0], v[3]//v[0])) for v in buckets.values() if v[0] > tot*0.0006]
    def sat(c):
        mx, mn = max(c), min(c); return 0 if mx == 0 else (mx-mn)/mx
    def dist(a, b):
        return ((a[0]-b[0])**2*.35 + (a[1]-b[1])**2*.45 + (a[2]-b[2])**2*.2) ** .5
    # vivid accents spread thinly over many bins (a blue face in a grey crowd): gather them by hue
    import colorsys
    hues = {}
    for p in px:
        hh, ss, vv = colorsys.rgb_to_hsv(*(x/255 for x in p))
        if ss > .4 and vv > .25:
            hb = hues.setdefault(int(hh*12) % 12, [0,0,0,0]); hb[0]+=1; hb[1]+=p[0]; hb[2]+=p[1]; hb[3]+=p[2]
    for v in hues.values():
        if v[0] > tot*0.004: cols.append((v[0], (v[1]//v[0], v[2]//v[0], v[3]//v[0])))
    # merge near bins so area reflects a real colour, then score: area, boosted for vivid accents
    merged = []
    for n, c in sorted(cols, key=lambda x: -x[0]):
        for m in merged:
            if dist(m[1], c) < 28: m[0] += n; break
        else: merged.append([n, c])
    def score(m):
        n, c = m; v = sat(c) * max(c) / 255
        return (n/tot) ** .45 * (1 + 4*v*v)
    picked = []
    viv = [m for m in merged if m[0] > tot*0.004 and sat(m[1])*max(m[1])/255 > .22]
    if viv: picked.append(max(viv, key=lambda m: sat(m[1])*max(m[1])/255 * (m[0]/tot)**.2)[1])  # always keep the signature accent
    for gap in (40, 30, 20, 12):
        for n, c in sorted(merged, key=lambda m: -score(m)):
            if len(picked) == 5: break
            if c not in picked and all(dist(c, p) > gap for p in picked): picked.append(c)
    picked.sort(key=lambda c: .3*c[0]+.59*c[1]+.11*c[2])
    pals[key] = ['#%02x%02x%02x' % c for c in picked]
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=88, optimize=True)
    imgs[key] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "src", "template.html")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "dist", "hanzi-designs-mockup.html")
tpl = open(SRC).read()
out = tpl.replace('__IMG__', json.dumps(imgs)).replace('__PAL__', json.dumps(pals))
open(OUT, "w").write(out)
print('built', len(out) // 1024, 'KB')
