import json, numpy as np
from PIL import Image
from scipy import ndimage
BASE="/home/plewis/Research/_Completed/AI_TA_Castillo_Project/Multi_Agent_approach/MyNotes/"
man=json.load(open(BASE+"segments/scattering_hamiltonian/segment_manifest.json"))
def inkmask(pg):
    a=np.asarray(Image.open(BASE+f"staging/scattering_hamiltonian/pages/page-{pg}.png").convert("RGB")).astype(int)
    R,B=a[:,:,0],a[:,:,2]
    return (R<150)&((B-R)<45)
st=np.ones((3,3),bool)
print("=== B5. CONNECTED-COMPONENT SEAM TEST ===")
print("A component = one connected stroke/glyph. A seam is unsafe only if a component it")
print("splits is ALSO not wholly contained in the overlapping neighbour segment.\n")
print(f"{'pg':>3}{'seam':>7}{'#comps split':>13}{'largest split comp bbox (y0,y1,h,px)':>42}{'  #NOT recovered by next seg'}")
bad=[]
for pg in [1,2,3,4]:
    m=inkmask(pg)
    lab,n=ndimage.label(m,structure=st)
    objs=ndimage.find_objects(lab)
    sizes=ndimage.sum(m,lab,range(1,n+1))
    segs=sorted([s for s in man if s["page"]==pg], key=lambda s:s["y0"])
    for i,s in enumerate(segs[:-1]):
        y=s["y1"]; nxt=segs[i+1]
        split=[]
        for k,sl in enumerate(objs):
            if sl is None: continue
            a0,a1=sl[0].start,sl[0].stop
            if a0< y < a1 and sizes[k]>=20:   # ignore <20px specks
                split.append((k,a0,a1,int(sizes[k])))
        notrec=[t for t in split if not (t[1]>=nxt['y0'] and t[2]<=nxt['y1'])]
        big = max(split,key=lambda t:t[3]) if split else None
        bs = f"({big[1]},{big[2]},h={big[2]-big[1]},{big[3]}px)" if big else "-"
        print(f"{pg:>3}{y:>7}{len(split):>13}{bs:>42}   {len(notrec)}")
        for t in notrec:
            sl=objs[t[0]]
            bad.append((pg,y,t[1],t[2],sl[1].start,sl[1].stop,t[3]))
print("\nCOMPONENTS SPLIT BY A SEAM AND NOT WHOLLY RECOVERED IN THE NEXT SEGMENT:")
if not bad: print("  NONE")
for b in bad: print(f"  page {b[0]} seam y={b[1]}: comp bbox y[{b[2]},{b[3]}] x[{b[4]},{b[5]}] h={b[3]-b[2]} area={b[6]}px")
