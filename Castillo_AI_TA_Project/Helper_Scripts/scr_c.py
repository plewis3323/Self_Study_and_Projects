import json, numpy as np
from PIL import Image
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def inkmask(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,B=a[:,:,0],a[:,:,2]
    return (R<150)&((B-R)<45)
def bands(rows,thr=3,gap=12):
    on=rows>=thr; out=[]; s=None; last=None
    for i,v in enumerate(on):
        if v:
            if s is None: s=i
            last=i
        else:
            if s is not None and i-last>gap:
                out.append((s,last)); s=None
    if s is not None: out.append((s,last))
    return out
print("=== B2. ORPHANED-BAND ANALYSIS (a band split by a seam and NOT wholly inside either neighbour) ===")
tot_orphan=0
for pg in [1,2,3,4]:
    m=inkmask(pg); rows=m.sum(1); bs=bands(rows)
    segs=sorted([s for s in man if s["page"]==pg], key=lambda s:s["y0"])
    print(f"\nPAGE {pg}: {len(bs)} ink bands; heights min/med/max = {min(b[1]-b[0] for b in bs)}/{int(np.median([b[1]-b[0] for b in bs]))}/{max(b[1]-b[0] for b in bs)}")
    for b0,b1 in bs:
        hosts=[s['name'][-12:] for s in segs if s['y0']<=b0 and b1<s['y1']]
        touched=[s['name'][-12:] for s in segs if not(b1<s['y0'] or b0>=s['y1'])]
        if not hosts:
            tot_orphan+=1
            print(f"   ORPHAN band y=[{b0},{b1}] h={b1-b0} ink={int(rows[b0:b1+1].sum())} touched_by={touched} -> NO single segment contains it")
    print(f"   orphan count page {pg}: {sum(1 for b0,b1 in bs if not any(s['y0']<=b0 and b1<s['y1'] for s in segs))}")
print(f"\nTOTAL ORPHANED BANDS = {tot_orphan}")

print("\n=== B3. per-seam: does the seam land inside an ink band? ===")
for pg in [1,2,3,4]:
    m=inkmask(pg); rows=m.sum(1); bs=bands(rows)
    segs=sorted([s for s in man if s["page"]==pg], key=lambda s:s["y0"])
    for s in segs[:-1]:
        y=s["y1"]
        inside=[(b0,b1) for b0,b1 in bs if b0<=y<=b1]
        if inside:
            b0,b1=inside[0]
            nxt=[t for t in segs if t['y0']==y-150]
            safe = bool(nxt) and b0>=nxt[0]['y0'] and b1<nxt[0]['y1']
            print(f"  p{pg} seam y={y}: INSIDE band [{b0},{b1}] h={b1-b0}; recovered whole by next seg (y0={y-150})? {safe}")
        else:
            d=min(min(abs(y-b0),abs(y-b1)) for b0,b1 in bs)
            print(f"  p{pg} seam y={y}: in gutter, {d}px from nearest band edge")
