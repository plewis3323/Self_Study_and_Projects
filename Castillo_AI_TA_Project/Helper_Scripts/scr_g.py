import json, numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
cj=json.load(open(BASE+"Final_Product_Ready/figures/figure_crops.json"))
print("=== COLOUR DEPTH OF CROPS vs SOURCE ===")
for name in cj:
    im=Image.open(BASE+"Final_Product_Ready/figures/"+name)
    a=np.asarray(im.convert("RGB")).reshape(-1,3)
    u=np.unique(a,axis=0)
    print(f"{name:>34} mode={im.mode} unique_colors={len(u)} sample={u[:4].tolist()}")
for pg in [1,2,3,4]:
    im=Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png")
    a=np.asarray(im.convert("RGB")).reshape(-1,3)
    print(f"page-{pg}.png mode={im.mode} unique_colors={len(np.unique(a,axis=0))}")

print("\n=== G. COLOUR ANALYSIS OF SOURCE PAGES ===")
for pg in [1,2,3,4]:
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    mx=a.max(2); mn=a.min(2); sat=mx-mn
    dark = mx<200
    black = dark & (sat<40)
    blue  = dark & (B-R>=45)
    red   = dark & (R-B>=45) & (R-G>=45)
    tot=int((black|blue|red).sum())
    def bbox(m):
        ys,xs=np.where(m)
        return (int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())) if ys.size else None
    print(f"\npage {pg}: dark px={int(dark.sum())}  black={int(black.sum())} blue={int(blue.sum())} red={int(red.sum())}")
    for nm,m in (("blue",blue),("red",red)):
        if m.sum()<50: print(f"   {nm}: negligible ({int(m.sum())} px)"); continue
        lab,n=ndimage.label(m,np.ones((3,3),bool))
        sz=ndimage.sum(m,lab,range(1,n+1)); objs=ndimage.find_objects(lab)
        big=[(int(sz[k]),objs[k]) for k in range(n) if sz[k]>=300]
        big.sort(key=lambda t:-t[0])
        print(f"   {nm}: {int(m.sum())} px, full bbox y[{bbox(m)[0]},{bbox(m)[1]}] x[{bbox(m)[2]},{bbox(m)[3]}], {len(big)} comps>=300px")
        for s,sl in big[:8]:
            print(f"       comp {s}px  y[{sl[0].start},{sl[0].stop}] x[{sl[1].start},{sl[1].stop}]")
