import json, numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
cj=json.load(open(BASE+"Final_Product_Ready/figures/figure_crops.json"))
def ink(a):
    R,B=a[:,:,0].astype(int),a[:,:,2].astype(int)
    return (R<150)&((B-R)<45)
def lum(a):
    c=a[:,:,:3].astype(float)/255.0
    c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
    return 0.2126*c[:,:,0]+0.7152*c[:,:,1]+0.0722*c[:,:,2]
print("=== D. CROP DIMENSIONS / DPI / BORDER-INK ===")
print(f"{'file':>34}{'px WxH':>12}{'in WxH':>13}{'eff DPI':>9}   border ink (T,B,L,R) of 3px frame")
rows=[]
for name,meta in cj.items():
    p=BASE+"Final_Product_Ready/figures/"+name
    im=Image.open(p); a=np.asarray(im.convert("RGB")); W,H=im.size
    m=ink(a)
    dpi=meta["render_dpi"]
    bx=meta["box"]
    match = (W==bx[2]-bx[0] and H==bx[3]-bx[1] and [W,H]==meta["size"])
    T=int(m[:3,:].sum()); Bo=int(m[-3:,:].sum()); L=int(m[:,:3].sum()); R=int(m[:,-3:].sum())
    print(f"{name:>34}{f'{W}x{H}':>12}{f'{W/dpi:.2f}x{H/dpi:.2f}':>13}{dpi:>9}   T={T} B={Bo} L={L} R={R}   box_ok={match}")
    rows.append((name,W,H,T,Bo,L,R))

print("\n=== D2. IS THE DRAWING CLIPPED? compare crop box to the ink component(s) it captures on the source page ===")
for name,meta in cj.items():
    pg=meta["source_page"]; x0,y0,x1,y1=meta["box"]
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB"))
    m=ink(a)
    lab,n=ndimage.label(m,np.ones((3,3),bool))
    objs=ndimage.find_objects(lab); sizes=ndimage.sum(m,lab,range(1,n+1))
    # components that intersect the crop box
    over=[]
    for k,sl in enumerate(objs):
        if sl is None or sizes[k]<60: continue
        cy0,cy1,cx0,cx1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
        if not(cy1<=y0 or cy0>=y1 or cx1<=x0 or cx0>=x1):
            # fraction of the comp inside box
            inside=((cy0>=y0)and(cy1<=y1)and(cx0>=x0)and(cx1<=x1))
            over.append((k,cy0,cy1,cx0,cx1,int(sizes[k]),inside))
    clipped=[o for o in over if not o[6]]
    print(f"\n{name}  page{pg} box=[{x0},{y0},{x1},{y1}]  comps>=60px touching box: {len(over)}, CLIPPED: {len(clipped)}")
    for o in sorted(clipped,key=lambda t:-t[5])[:6]:
        sides=[]
        if o[1]<y0: sides.append(f"TOP by {y0-o[1]}")
        if o[2]>y1: sides.append(f"BOTTOM by {o[2]-y1}")
        if o[3]<x0: sides.append(f"LEFT by {x0-o[3]}")
        if o[4]>x1: sides.append(f"RIGHT by {o[4]-x1}")
        print(f"    comp area={o[5]}px bbox y[{o[1]},{o[2]}] x[{o[3]},{o[4]}]  overflows: {', '.join(sides)}")

print("\n=== E. WCAG CONTRAST (ink vs background) ===")
print(f"{'file':>34}{'L_ink':>9}{'L_bg':>9}{'ratio':>8}  pass>=3:1")
worst=(None,99)
for name in cj:
    a=np.asarray(Image.open(BASE+"Final_Product_Ready/figures/"+name).convert("RGB"))
    L=lum(a); m=ink(a)
    Li=np.percentile(L[m],2); Lb=np.percentile(L,90)
    r=(Lb+0.05)/(Li+0.05)
    if r<worst[1]: worst=(name,r)
    print(f"{name:>34}{Li:>9.4f}{Lb:>9.4f}{r:>8.2f}  {'PASS' if r>=3 else 'FAIL'}")
print(f"LOWEST: {worst[0]} = {worst[1]:.2f}:1")
