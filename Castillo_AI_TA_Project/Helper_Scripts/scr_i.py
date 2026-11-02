import json, numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def layers(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    dark=a.max(2)<235
    grid  = dark & (B-R>=45) & (G-R>=60)              # cyan ruling
    bluep = dark & (B-R>=45) & (G-R<60)               # violet blue pen
    redp  = dark & (R-B>=45) & (R-G>=45)
    black = dark & (B-R<45) & (R-B<45)
    return grid,bluep,redp,black,a
print("=== LAYER SEPARATION (dark = max channel < 235) ===")
print(f"{'pg':>3}{'grid px':>10}{'BLUE PEN':>10}{'RED':>8}{'BLACK':>10}")
L={}
for pg in [1,2,3,4]:
    g,b,r,k,a=layers(pg); L[pg]=(g,b,r,k)
    print(f"{pg:>3}{int(g.sum()):>10}{int(b.sum()):>10}{int(r.sum()):>8}{int(k.sum()):>10}")

print("\n=== A (CORRECTED). COVERAGE with handwriting = black pen OR blue pen (grid excluded) ===")
def runs(idx):
    out=[]; 
    if len(idx)==0: return out
    s=p=idx[0]
    for i in idx[1:]:
        if i==p+1: p=i
        else: out.append((int(s),int(p))); s=p=i
    out.append((int(s),int(p))); return out
for pg in [1,2,3,4]:
    g,b,r,k=L[pg]; hw=b|k|r
    rows=hw.sum(1); H=len(rows)
    inkr=np.where(rows>=3)[0]
    segs=sorted([s for s in man if s["page"]==pg],key=lambda s:s["y0"])
    cov=np.zeros(H,bool)
    for s in segs: cov[s["y0"]:s["y1"]]=True
    unc=np.where((rows>=3)&~cov)[0]
    print(f"PAGE {pg}: ink extent y {inkr.min()}..{inkr.max()} ({len(inkr)} ink rows, {int(hw.sum())} ink px)")
    print(f"    covered union {segs[0]['y0']}..{segs[-1]['y1']}   gap above={segs[0]['y0']-0}  below={H-segs[-1]['y1']}")
    print(f"    UNCOVERED ink rows: n={len(unc)}  runs={runs(list(unc))}")
    if len(unc): print(f"       peak ink px in uncovered row = {int(rows[unc].max())}, total ink px uncovered = {int(hw[unc].sum())}")
    # column coverage
    cols=hw.sum(0); ic=np.where(cols>=3)[0]
    print(f"    ink column extent x {ic.min()}..{ic.max()} (segments span x 0..2550: full-width OK)")

print("\n=== B (CORRECTED). CONNECTED-COMPONENT SEAM TEST on black|blue handwriting ===")
st=np.ones((3,3),bool)
bad=[]
print(f"{'pg':>3}{'seam':>7}{'ink/row +/-25':>15}{'#comps split(>=20px)':>22}{'#not recovered':>16}")
for pg in [1,2,3,4]:
    g,b,r,k=L[pg]; hw=b|k|r
    rows=hw.sum(1)
    lab,n=ndimage.label(hw,st); objs=ndimage.find_objects(lab); sz=ndimage.sum(hw,lab,range(1,n+1))
    segs=sorted([s for s in man if s["page"]==pg],key=lambda s:s["y0"])
    for i,s in enumerate(segs[:-1]):
        y=s["y1"]; nx=segs[i+1]
        w=rows[max(0,y-25):y+26]
        sp=[(kk,objs[kk][0].start,objs[kk][0].stop,objs[kk][1].start,objs[kk][1].stop,int(sz[kk])) for kk in range(n) if objs[kk] and objs[kk][0].start<y<objs[kk][0].stop and sz[kk]>=20]
        nr=[t for t in sp if not (t[1]>=nx['y0'] and t[2]<=nx['y1'])]
        print(f"{pg:>3}{y:>7}{w.mean():>15.1f}{len(sp):>22}{len(nr):>16}")
        for t in nr: bad.append((pg,y,t))
print("\nSPLIT AND NOT RECOVERED:")
for pg,y,t in sorted(bad,key=lambda z:-z[2][5]):
    print(f"  page{pg} seam y={y}: comp area={t[5]}px  y[{t[1]},{t[2]}] x[{t[3]},{t[4]}] h={t[2]-t[1]}")
