import json, numpy as np
from PIL import Image
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def inkmask(p):
    a=np.asarray(Image.open(p).convert("RGB")).astype(int)
    R,B=a[:,:,0],a[:,:,2]
    return (R<150)&((B-R)<45)
print("=== SANITY: dark border check page1 ===")
m1=inkmask(BASE+"staging/scattering_hamiltonian/pages/page-1.png")
print(" row0 ink px:",int(m1[0].sum())," row1:",int(m1[1].sum())," row3300:",int(m1[3300].sum()))
print(" col0 ink px:",int(m1[:,0].sum())," col2549:",int(m1[:,2549].sum()))
cols=m1.sum(0); print(" ink col extent:",int(np.where(cols>=3)[0].min()),"..",int(np.where(cols>=3)[0].max()))

print("\n=== B. SEAM SAFETY (ink px/row within +/-25 of each seam) ===")
print(f"{'page':>4} {'seam_y':>7} {'seg':>16} {'mean/row':>9} {'max/row':>8} {'min/row':>8} {'@seam':>6} {'verdict'}")
seamdata=[]
for pg in [1,2,3,4]:
    m=inkmask(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png")
    rows=m.sum(1)
    segs=[s for s in man if s["page"]==pg]
    glob_mean = rows[rows>=3].mean()
    for s in segs[:-1]:
        y=s["y1"]; lo=max(0,y-25); hi=min(len(rows),y+26)
        w=rows[lo:hi]
        v = "CUT-THROUGH-CONTENT" if w.mean()>40 else ("marginal" if w.mean()>15 else "clean")
        print(f"{pg:>4} {y:>7} {s['name'][-12:]:>16} {w.mean():>9.1f} {w.max():>8} {w.min():>8} {rows[y]:>6}  {v}")
        seamdata.append((pg,y,w.mean(),int(w.max()),int(rows[y])))
    print(f"     page mean ink/row over ink rows = {glob_mean:.1f}")

print("\n=== C. OVERLAP ===")
print(f"{'page':>4} {'boundary':>28} {'overlap_px':>11}  flag")
for pg in [1,2,3,4]:
    segs=[s for s in man if s["page"]==pg]
    for i in range(len(segs)-1):
        ov=segs[i]["y1"]-segs[i+1]["y0"]
        f="" if 100<=ov<=350 else ("LOW" if ov<100 else "HIGH")
        print(f"{pg:>4} {segs[i]['name'][-12:]+'/'+segs[i+1]['name'][-12:]:>28} {ov:>11}  {f}")

print("\n=== SEGMENT FILE vs MANIFEST DIMENSION CHECK ===")
import os
for s in man:
    p=BASE+"segments/scattering_hamiltonian/"+s["name"]
    im=Image.open(p); w,h=im.size
    ok = (w==s["w"] and h==s["h"])
    # pixel-identity check vs source page crop
    src=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{s['page']}.png").convert("RGB"))[s["y0"]:s["y1"], s["x0"]:s["x1"]]
    seg=np.asarray(im.convert("RGB"))
    ident = (src.shape==seg.shape) and bool((src==seg).all())
    print(f"{s['name']}: file {w}x{h} manifest {s['w']}x{s['h']} dims_ok={ok} pixel_identical_to_source_crop={ident}")
