import numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
OUT="/tmp/claude-1000/-home-plewis-Sum-26-AI-TA-task-Summer-26-Dr--Castillo-AI-TA-Task-Multi-Agent-approach-MyNotes/9fa0a01a-49bf-4b50-9471-fcf4fbb65f69/scratchpad/"
a=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-4.png").convert("RGB")).astype(int)
R,G,B=a[...,0],a[...,1],a[...,2]
red=(R-G>=90)&(R-B>=90)&(R>=120)          # bright red, NOT gated on darkness
print("=== PAGE 4 RED, corrected rule (R-G>=90 & R-B>=90 & R>=120) ===")
print(" red px:",int(red.sum()),"  mean RGB:",a[red].mean(0).round(1))
ys,xs=np.where(red); print(f" bbox y[{ys.min()},{ys.max()}] x[{xs.min()},{xs.max()}]  (w={xs.max()-xs.min()}, h={ys.max()-ys.min()})")
d=ndimage.binary_dilation(red,np.ones((15,15),bool)); lab,n=ndimage.label(d)
sz=ndimage.sum(red,lab,range(1,n+1)); objs=ndimage.find_objects(lab)
for i in np.argsort(-sz)[:5]:
    if sz[i]<100: break
    sl=objs[i]; print(f"   cluster {int(sz[i])}px y[{sl[0].start},{sl[0].stop}] x[{sl[1].start},{sl[1].stop}]")
print("\n Does the brief's ink rule (R<150 & B-R<45) see the red?  red px passing it:",
      int((red&(R<150)&((B-R)<45)).sum()), "of", int(red.sum()))
print(" Does 'dark = max<235' see it? ", int((red&(a.max(2)<235)).sum()), "of", int(red.sum()))
def lum(c):
    c=np.asarray(c,float)/255.
    c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
    return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
Lr=np.percentile(lum(a[red]),50)
print(f"\n red median relative luminance L={Lr:.4f}")
print(f"   CR red vs paper(L=1.0) = {(1.05)/(Lr+0.05):.2f}:1")
print(f"   CR red vs black ink(L=0) = {(Lr+0.05)/0.05:.2f}:1")
# which segments contain the red
import json
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
for s in man:
    if s['page']!=4: continue
    c=int(red[s['y0']:s['y1']].sum())
    if c: print(f"   {s['name']}  contains {c} red px  ({c/red.sum()*100:.1f}% of the strike-through)")
Image.fromarray(np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB"))[1690:1810,1740:2050]).resize((930,360)).save(OUT+"z_fig3_psi.png")
