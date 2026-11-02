import numpy as np
from PIL import Image
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
a=np.asarray(Image.open(BASE+"staging/scattering_hamiltonian/pages/page-1.png").convert("RGB")).astype(int)
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
mx=a.max(2); mn=a.min(2)
print("global: mean RGB",a.reshape(-1,3).mean(0).round(1),"  bg mode:",np.bincount((a.reshape(-1,3)@np.array([1,0,0])).astype(int)).argmax())
# sample the blue trajectory: in fig1 crop coords the beam line is near y=470 abs (150+320), x 400-900 abs (20+380)
print("\n-- sample rows across the blue beam line, page1 abs y 455..480, x 500..900 --")
sub=a[455:485,500:900]
d=sub[(sub.max(2)<245)]
print("n dark-ish px:",len(d)," mean:",d.mean(0).round(1) if len(d) else None)
# histogram of (B-R) for pixels with max<250
sel=(mx<250)
br=(B-R)[sel]
print("\n(B-R) histogram for px with max<250 (n=%d):"%sel.sum())
h,e=np.histogram(br,bins=[-50,-20,0,10,20,30,45,60,80,100,130,160,200,256])
for i in range(len(h)): print(f"   B-R [{e[i]:>4},{e[i+1]:>4}): {h[i]:>9}")
print("\nmax-channel histogram for px with (B-R)>=45:")
sel2=(B-R)>=45
h,e=np.histogram(mx[sel2],bins=[0,60,100,140,170,190,210,225,240,256])
for i in range(len(h)): print(f"   max [{e[i]:>4},{e[i+1]:>4}): {h[i]:>9}")
print("\n-- candidate rules, page 1 --")
grid = (B-R>=45)&(mx>=200)          # pale blue ruling
bluepen=(B-R>=45)&(mx<200)
blackpen=(mx<200)&(B-R<45)
print("pale-blue ruling px:",int(grid.sum()),"  blue PEN px:",int(bluepen.sum()),"  black pen px:",int(blackpen.sum()))
for nm,m in (("ruling",grid),("bluepen",bluepen)):
    d=a[m]; print(f"   {nm} mean RGB {d.mean(0).round(1)}")
