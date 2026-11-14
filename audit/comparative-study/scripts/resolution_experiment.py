"""Show how apparent surface texture changes at equal projected image size.

This is a sampling experiment, not a physical-size/radiometric calibration.
"""
from pathlib import Path
from io import BytesIO
import csv,json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/comparative-study'
CASES=[
 ('Candidate (PDS DRCX color)','target-drcx.png',(1034,942,1090,997)),
 ('Naukluft sandstone nodule','naukluft.jpg',(450,326,665,520)),
 ('Rounded Sol 3415 block','sol3415_182.jpg',(360,20,650,300)),
 ('Winnipesaukee shell','winnipesaukee.jpg',(829,595,1015,752)),
 ('Haroldswick stick','haroldswick.jpg',(737,167,815,257)),
]

def normalized_high_frequency(a):
    a=np.asarray(a.convert('L'),float)
    # Central image patch; intentionally disclosed, not an identified material ROI.
    h,w=a.shape;y0,y1=int(h*.3),int(h*.7);x0,x1=int(w*.3),int(w*.7)
    p=a[y0:y1,x0:x1]
    lp=ndi.laplace(ndi.gaussian_filter(a,.6))[y0:y1,x0:x1]
    return float(np.var(lp)/(np.mean(p)**2+1e-9))

def main():
    fig,axes=plt.subplots(len(CASES),3,figsize=(10,3*len(CASES)))
    rows=[]
    for i,(name,file,box) in enumerate(CASES):
        im=Image.open(OUT/'images'/file).convert('RGB').crop(box)
        for j,width in enumerate([im.width,40,20]):
            down=im.resize((width,max(1,round(im.height*width/im.width))),Image.Resampling.BOX)
            axes[i,j].imshow(down,interpolation='nearest');axes[i,j].set_xticks([]);axes[i,j].set_yticks([])
            axes[i,j].set_title(f'{name}\n{width} sample columns',fontsize=9)
            rows.append(dict(case=name,source_file=file,bbox=str(box),sample_columns=width,
                high_frequency_proxy=normalized_high_frequency(down),
                interpretation='Central patch image-frequency proxy; includes albedo/shading, unequal camera PSFs; not physical roughness'))
    fig.suptitle('Equal displayed size hides different sampling: no panel establishes metal or geological origin')
    fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/'figures/resolution-comparison.png',dpi=170);plt.close(fig)
    with (OUT/'resolution-experiment.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    # JPEG sensitivity of the target at the same sampling, not artificial precision claims.
    target=Image.open(OUT/'images/target-drcx.png').convert('RGB')
    from analyze import gray,windows,choose_target,target_reference
    refs,_=target_reference();tests=[]
    for quality in [100,95,85,70]:
        buf=BytesIO();target.save(buf,format='JPEG',quality=quality);buf.seek(0)
        p=OUT/'images'/f'target-drcx-jpeg-q{quality}.jpg';p.write_bytes(buf.getvalue())
        # Work only in a fixed crop, offset references accordingly; same crop in every variant.
        a=gray(p);x0,y0=500,460;a=a[y0:515,x0:560]
        c=list(windows(a,36.4,.7,'line','compression_experiment'))
        selected=choose_target(c,refs-[2*x0,2*y0],'line')
        vals=[r['rms_px'] for r,p in selected]
        closest=min(selected,key=lambda item:item[0]['reference_distance_px'])[0] if selected else None
        tests.append(dict(jpeg_quality=quality,n_levels=len(vals),median_rms_px=float(np.median(vals)) if vals else None,
                          closest_reference_rms_px=closest['rms_px'] if closest else None,
                          closest_reference_distance_px=closest['reference_distance_px'] if closest else None))
    (OUT/'jpeg-sensitivity.json').write_text(json.dumps(tests,indent=2))
if __name__=='__main__':main()
