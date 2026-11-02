import numpy as np, json
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
OUT="/tmp/claude-1000/-home-plewis-Sum-26-AI-TA-task-Summer-26-Dr--Castillo-AI-TA-Task-Multi-Agent-approach-MyNotes/9fa0a01a-49bf-4b50-9471-fcf4fbb65f69/scratchpad/"
def lay(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; dark=a.max(2)<235
    grid=dark&(B-R>=45)&(G-R>=60); blue=dark&(B-R>=45)&(G-R<60)
    red=dark&(R-B>=45)&(R-G>=45); black=dark&~grid&~blue&~red
    return grid,blue,red,black,a
g,b,r,k,a1=lay(1)
box=[20,150,1438,848]
inside=np.zeros_like(b); inside[box[1]:box[3],box[0]:box[2]]=True
print("=== BLUE TRAJECTORY vs fig1 CROP BOX ===")
print(f" total blue pen px page1: {int(b.sum())}")
print(f"   inside crop box : {int((b&inside).sum())} ({(b&inside).sum()/b.sum()*100:.1f}%)")
print(f"   OUTSIDE crop box: {int((b&~inside).sum())} ({(b&~inside).sum()/b.sum()*100:.1f}%)")
out=b&~inside; ys,xs=np.where(out)
print(f"   lost blue bbox: y[{ys.min()},{ys.max()}] x[{xs.min()},{xs.max()}]")
print(f"   lost above top (y<150): {int(b[:150].sum())} px ; lost right of x=1438: {int(b[:,1438:].sum())} px")
# grayscale separability blue vs black
def lum(c):
    c=np.asarray(c,float)/255.
    c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
    return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
Lb=lum(a1[b]); Lk=lum(a1[k]); Lg=lum(a1[g])
mb,mk,mg=np.percentile(Lb,50),np.percentile(Lk,50),np.percentile(Lg,50)
print("\n=== GRAYSCALE SEPARABILITY (median relative luminance) ===")
print(f"  black ink L={mk:.4f}   blue pen L={mb:.4f}   grid L={mg:.4f}   paper L=1.0")
print(f"  CR blue vs black = {(max(mb,mk)+0.05)/(min(mb,mk)+0.05):.2f}:1   (WCAG non-text needs >=3:1 to be told apart)")
print(f"  CR grid vs blue  = {(max(mg,mb)+0.05)/(min(mg,mb)+0.05):.2f}:1")
print(f"  mean RGB blue pen {a1[b].mean(0).round(1)}   black {a1[k].mean(0).round(1)}   grid {a1[g].mean(0).round(1)}")
# page4 red
g4,b4,r4,k4,a4=lay(4)
ys,xs=np.where(r4)
print(f"\n=== PAGE 4 RED ===\n  red px={int(r4.sum())} bbox y[{ys.min()},{ys.max()}] x[{xs.min()},{xs.max()}]  mean RGB {a4[r4].mean(0).round(1)}")
Image.fromarray(np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-4.png").convert("RGB"))[350:760,1650:2350]).save(OUT+"p4_red.png")
# fig0
Image.fromarray(np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-2.png").convert("RGB"))[0:300,1400:1980]).resize((1160,600)).save(OUT+"fig0_pad.png")
print("saved p4_red.png, fig0_pad.png")
