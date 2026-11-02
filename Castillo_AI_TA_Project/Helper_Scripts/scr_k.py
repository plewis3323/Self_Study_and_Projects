import json, numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def lay(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; dark=a.max(2)<235
    grid=dark&(B-R>=45)&(G-R>=60); blue=dark&(B-R>=45)&(G-R<60)
    red=dark&(R-B>=45)&(R-G>=45); black=dark&~grid&~blue&~red
    return grid,blue,red,black
LA={p:lay(p) for p in (1,2,3,4)}

print("=== MANIFEST ink_rows FIELD VERIFICATION (rows with >=1 handwriting px, grid excluded) ===")
print(f"{'segment':>18}{'h':>6}{'manifest ink_rows':>19}{'measured(>=1px)':>17}{'measured(>=3px)':>17}  delta")
for s in man:
    g,b,r,k=LA[s['page']]; hw=(b|r|k)[s['y0']:s['y1']]
    rr=hw.sum(1)
    m1=int((rr>=1).sum()); m3=int((rr>=3).sum())
    print(f"{s['name']:>18}{s['h']:>6}{s['ink_rows']:>19}{m1:>17}{m3:>17}  {s['ink_rows']-m1:+d}")

print("\n=== TEXT LINE HEIGHT (for judging whether 150px overlap is enough context) ===")
hs=[]
for pg in (1,2,3,4):
    g,b,r,k=LA[pg]; hw=b|r|k; rows=hw.sum(1)
    on=rows>=3; runs=[];s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None: runs.append((s,i)); s=None
    if s is not None: runs.append((s,len(on)))
    hh=[e-b_ for b_,e in runs if 40<=e-b_<=260]
    hs+=hh
hs=np.array(hs)
print(f"  n={len(hs)} plausible text-line bands; median={np.median(hs):.0f}px mean={hs.mean():.0f}px p25={np.percentile(hs,25):.0f} p75={np.percentile(hs,75):.0f} max={hs.max()}")
print(f"  overlap 150px = {150/np.median(hs):.2f} median line-heights = {150/300:.2f} inch")

print("\n=== G. COLOUR LAYER MAP ===")
for pg in (1,2,3,4):
    g,b,r,k=LA[pg]
    print(f"\nPAGE {pg}: grid={int(g.sum()):>7}  BLUE PEN={int(b.sum()):>6}  RED={int(r.sum()):>5}  BLACK={int(k.sum()):>7}   blue as % of pen ink = {b.sum()/(b.sum()+k.sum()+r.sum())*100:.2f}%")
    for nm,m in (("BLUE",b),("RED",r)):
        if m.sum()<40: 
            print(f"   {nm}: {int(m.sum())}px - negligible"); continue
        d=ndimage.binary_dilation(m,np.ones((9,9),bool))
        lab,n=ndimage.label(d,np.ones((3,3),bool)); objs=ndimage.find_objects(lab)
        sz=ndimage.sum(m,lab,range(1,n+1))
        big=sorted([(int(sz[i]),objs[i]) for i in range(n) if sz[i]>=150],key=lambda t:-t[0])
        print(f"   {nm}: {int(m.sum())}px total, {len(big)} clusters >=150px:")
        for s_,sl in big[:10]:
            print(f"       {s_:>6}px  bbox y[{sl[0].start},{sl[0].stop}] x[{sl[1].start},{sl[1].stop}]  (w={sl[1].stop-sl[1].start}, h={sl[0].stop-sl[0].start})")
