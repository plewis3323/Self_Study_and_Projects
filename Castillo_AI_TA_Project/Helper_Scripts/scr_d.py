import json, numpy as np
from PIL import Image
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def inkmask(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,B=a[:,:,0],a[:,:,2]
    return (R<150)&((B-R)<45)
def bands(rows,thr=3,gap=0):
    on=rows>=thr; out=[]; s=None; last=None
    for i,v in enumerate(on):
        if v:
            if s is None: s=i
            last=i
        elif s is not None and i-last>gap:
            out.append((s,last)); s=None
    if s is not None: out.append((s,last))
    return out
for GAP in (0,4):
  print(f"\n########## GAP={GAP} ##########")
  tot=0
  for pg in [1,2,3,4]:
    rows=inkmask(pg).sum(1); bs=bands(rows,gap=GAP)
    segs=sorted([s for s in man if s["page"]==pg], key=lambda s:s["y0"])
    orph=[(b0,b1) for b0,b1 in bs if not any(s['y0']<=b0 and b1<s['y1'] for s in segs)]
    hs=[b[1]-b[0] for b in bs]
    print(f"PAGE {pg}: {len(bs)} bands, h med={int(np.median(hs))} max={max(hs)}; ORPHANS={len(orph)}")
    for b0,b1 in orph:
        print(f"    orphan [{b0},{b1}] h={b1-b0} ink={int(rows[b0:b1+1].sum())}")
    tot+=len(orph)
  print(f"TOTAL ORPHANS gap={GAP}: {tot}")

print("\n=== B4. seam local density, corrected: ink in +/-25 window, and whether ANY band crosses seam (gap=4) ===")
print(f"{'pg':>3}{'seam':>7}{'ink/row mean':>14}{'max':>6}{'band crossing seam':>24}{'  contained in next seg?'}")
for pg in [1,2,3,4]:
    rows=inkmask(pg).sum(1); bs=bands(rows,gap=4)
    segs=sorted([s for s in man if s["page"]==pg], key=lambda s:s["y0"])
    for i,s in enumerate(segs[:-1]):
        y=s["y1"]; nxt=segs[i+1]
        w=rows[max(0,y-25):y+26]
        cross=[(b0,b1) for b0,b1 in bs if b0<=y<=b1]
        if cross:
            b0,b1=cross[0]
            ok = b0>=nxt['y0'] and b1<nxt['y1']
            print(f"{pg:>3}{y:>7}{w.mean():>14.1f}{w.max():>6}{f'[{b0},{b1}] h={b1-b0}':>24}   {ok}")
        else:
            print(f"{pg:>3}{y:>7}{w.mean():>14.1f}{w.max():>6}{'none (gutter)':>24}   n/a")
