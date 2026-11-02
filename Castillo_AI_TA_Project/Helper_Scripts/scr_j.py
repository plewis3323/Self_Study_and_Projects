import numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
OUT="/tmp/claude-1000/-home-plewis-Sum-26-AI-TA-task-Summer-26-Dr--Castillo-AI-TA-Task-Multi-Agent-approach-MyNotes/9fa0a01a-49bf-4b50-9471-fcf4fbb65f69/scratchpad/"
def hw(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    dark=a.max(2)<235
    return (dark&~((B-R>=45)&(G-R>=60))), a
m,a=hw(1)
lab,n=ndimage.label(m,np.ones((3,3),bool))
objs=ndimage.find_objects(lab)
# find the component containing y 94..938 x119..1585
target=None
for k,sl in enumerate(objs):
    if sl and sl[0].start==94 and sl[0].stop==938: target=k
comp=(lab==target+1)
print("fig1 main drawing component: area",int(comp.sum()))
above=int(comp[:917].sum()); below=int(comp[917:].sum())
print(f"  ink px at y<917 (in seg01): {above}   ink px at y>=917 (NOT in seg01): {below}  ({below/comp.sum()*100:.2f}%)")
ys,xs=np.where(comp[917:]); 
print(f"  the part missing from seg01 occupies y[{917+ys.min()},{917+ys.max()}] x[{xs.min()},{xs.max()}]")
print(f"  in seg02 (767..1479) this comp has rows 767..938 only -> {int(comp[767:1479].sum())} px of {int(comp.sum())} ({comp[767:1479].sum()/comp.sum()*100:.1f}%)")
# save a zoom of the seam region
Image.fromarray(np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB"))[820:1000,100:1700]).save(OUT+"p1_seam917.png")
# fig1 clipped region: show crop box + generous pad
box=[20,150,1438,848]
pad=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB"))[max(0,box[1]-120):box[3]+140, max(0,box[0]-40):box[2]+320]
Image.fromarray(pad).resize((pad.shape[1]//2,pad.shape[0]//2)).save(OUT+"fig1_padded.png")
b3=[1420,1515,2320,2030]
p3=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB"))[b3[1]-60:b3[3]+60, b3[0]-130:min(2550,b3[2]+180)]
Image.fromarray(p3).save(OUT+"fig3_padded.png")
b4=[60,2050,1010,2370]
m3,a3=hw(3)
p4=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-3.png").convert("RGB"))[b4[1]-70:b4[3]+40, b4[0]-40:b4[2]+120]
Image.fromarray(p4).save(OUT+"fig4_padded.png")
b2=[30,1515,985,1965]
p2=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB"))[b2[1]-40:b2[3]+40, max(0,b2[0]-40):b2[2]+400]
Image.fromarray(p2).save(OUT+"fig2_padded.png")
print("saved padded views")

print("\n=== E2. CONTRAST, corrected: separate BLACK ink, BLUE pen, and GRID vs background ===")
def lumf(c):
    c=c/255.0
    c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
    return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
import json
cj=json.load(open(BASE+"Final_Product_Ready/figures/figure_crops.json"))
print(f"{'file':>32}{'L_bg':>8}{'L_black':>9}{'CR_blk':>8}{'L_blue':>8}{'CR_blue':>9}{'L_grid':>8}{'CR_grid':>9}")
lo=[]
for name,meta in cj.items():
    A=np.asarray(Image.open(BASE+"Final_Product_Ready/figures/"+name).convert("RGB")).astype(int)
    R,G,B=A[...,0],A[...,1],A[...,2]
    dark=A.max(2)<235
    grid=dark&(B-R>=45)&(G-R>=60); blue=dark&(B-R>=45)&(G-R<60); blk=dark&(B-R<45)
    L=lumf(A.astype(float))
    Lb=np.percentile(L,90)
    def cr(mask):
        if mask.sum()<30: return None,None
        Li=np.percentile(L[mask],2); return Li,(Lb+0.05)/(Li+0.05)
    lk,ck=cr(blk); lu,cu=cr(blue); lg,cg=cr(grid)
    f=lambda v,fm: ("%"+fm)%v if v is not None else "  n/a"
    print(f"{name:>32}{Lb:>8.3f}{f(lk,'9.4f')}{f(ck,'8.2f')}{f(lu,'8.4f')}{f(cu,'9.2f')}{f(lg,'8.4f')}{f(cg,'9.2f')}")
    for c in (ck,cu):
        if c: lo.append((c,name))
    if cg: lo.append((cg,name+" [grid]"))
print("LOWEST overall:",sorted(lo)[0])
print("LOWEST ink-only (excl grid):",sorted([x for x in lo if '[grid]' not in x[1]])[0])
