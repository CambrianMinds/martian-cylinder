"""Rotation/scale-normalized appearance retrieval, not a cylinder classifier."""
from analyze import ROOT,OUT,gray
from scipy import ndimage as ndi
from scipy.signal import fftconvolve
import numpy as np
import json,csv
from PIL import Image
import matplotlib.pyplot as plt

def match(image,template,weight):
    total=weight.sum();mu=(template*weight).sum()/total
    t=(template-mu)*weight;var=((template-mu)**2*weight).sum()
    reverse=lambda x:x[::-1,::-1]
    sums=fftconvolve(image,reverse(weight),mode='valid')
    squares=fftconvolve(image*image,reverse(weight),mode='valid')
    numerator=fftconvolve(image,reverse(t),mode='valid')
    den=np.sqrt(np.maximum(squares-sums*sums/total,1e-9)*max(var,1e-9))
    return np.clip(numerator/den,-1,1)

def main():
    scenes=[r for r in json.loads((OUT/'image-manifest.json').read_text())['images'] if r.get('role')=='whole_frame' and 'path'in r]
    original=gray(OUT/'images/sol3556_585.jpg')
    template=ndi.gaussian_filter(original[465:507,508:552],.5)
    y,x=np.mgrid[:template.shape[0],:template.shape[1]]
    weight=np.exp(-(((x-(x.max()/2))/(x.max()*.4))**2+((y-y.max()/2)/(y.max()*.4))**2)/2)
    variants=[]
    for scale in [.75,1,1.25]:
        for angle in range(0,360,45):
            # Weight masks rotated padding out of the comparison.
            t=ndi.rotate(ndi.zoom(template,scale,order=1),angle,reshape=True,order=1,cval=0)
            w=ndi.rotate(ndi.zoom(weight,scale,order=1),angle,reshape=True,order=1,cval=0)
            variants.append((scale,angle,t,w))
    candidates=[];positive=None
    for scene in scenes:
        a=ndi.gaussian_filter(gray(ROOT/scene['path']),.5)
        for scale,angle,t,w in variants:
            score=match(a,t,w)
            if scene['id']=='sol3556_585' and scale==1 and angle==0:
                positive=float(score[465,508])
            # Keep three spatially separated hits per transform.
            for _ in range(3):
                iy,ix=np.unravel_index(np.argmax(score),score.shape)
                val=float(score[iy,ix]);cx=2*(ix+t.shape[1]/2)+.5;cy=2*(iy+t.shape[0]/2)+.5
                score[max(0,iy-35):iy+36,max(0,ix-35):ix+36]=-1
                if scene['id']=='sol3556_585' and 970<cx<1140 and 890<cy<1050:continue
                if scene['id'].startswith('twin_cairns') and cy<650:continue
                candidates.append(dict(scene=scene['id'],score=val,rotation_deg=angle,scale=scale,x=cx,y=cy,
                    width_native_px=t.shape[1]*2,height_native_px=t.shape[0]*2))
        print('appearance search',scene['id'],flush=True)
    candidates.sort(key=lambda r:r['score'],reverse=True)
    unique=[]
    for r in candidates:
        if any(r['scene']==q['scene'] and np.hypot(r['x']-q['x'],r['y']-q['y'])<70 for q in unique):continue
        unique.append(r)
    with (OUT/'appearance-matches.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(unique[0]));writer.writeheader();writer.writerows(unique)
    (OUT/'appearance-summary.json').write_text(json.dumps(dict(positive_self_match=positive,n_scenes=len(scenes),n_transformations_per_scene=len(variants),top_matches=unique[:18],interpretation='Weighted luminance correlation includes surrounding ground and shadow; not a cylinder likelihood or geological identity.'),indent=2))
    lookup={r['id']:r for r in scenes};fig,axes=plt.subplots(6,3,figsize=(12,18))
    for ax,r in zip(axes.flat,unique[:18]):
        im=Image.open(ROOT/lookup[r['scene']]['path']).convert('RGB');cx,cy=r['x'],r['y'];pad=58
        crop=im.crop((round(cx-pad),round(cy-pad),round(cx+pad),round(cy+pad)))
        crop=crop.resize((58,58),Image.Resampling.BOX)
        ax.imshow(crop,interpolation='nearest');ax.set_xticks([]);ax.set_yticks([])
        ax.set_title(f"{r['scene']} ({cx:.0f},{cy:.0f})\nNCC={r['score']:.3f}, angle={r['rotation_deg']}, scale={r['scale']}",fontsize=9)
    fig.suptitle('Closest appearance matches after rotation/scale search; no object-class labels inferred')
    fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/'figures/appearance-matches.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
