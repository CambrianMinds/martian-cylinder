"""Uniform fixed-span photometric edge and ellipse-arc comparison.

Image windows are NOT independent clasts or classified material silhouettes.
Target selection uses proximity to previously recorded features, never residual.
"""
from pathlib import Path
import sys,json,csv,math,hashlib,platform
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from skimage.measure import find_contours,EllipseModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'audit/comparative-study'
sys.path.insert(0,str(ROOT/'independent-reconstruction'))
from step4_endface_and_conic_models import point_to_ellipse_orth_dist

def gray(path):
    a=np.asarray(Image.open(path).convert('RGB'),float)
    a=a@np.array([.299,.587,.114])
    # Uniform 2x2 area bin suppresses pixel-periodic raw-preview sampling.
    # Coordinates and all residuals below are converted back to native pixels.
    h,w=a.shape; a=a[:h//2*2,:w//2*2]
    return a.reshape(h//2,2,w//2,2).mean(axis=(1,3))

def line_fit(points):
    q=points-points.mean(0);_,_,vh=np.linalg.svd(q,full_matrices=False)
    residual=q@vh[-1]
    return float(np.sqrt(np.mean(residual**2))),float(np.degrees(np.arctan2(vh[0,1],vh[0,0]))%180)

def ellipse_fit(points):
    model=EllipseModel()
    if not model.estimate(points):return None
    xc,yc,a,b,th=model.params
    if b>a:a,b,th=b,a,th+np.pi/2
    if not (14<=a<=28 and .65<=b/a<=1):return None
    q=points-[xc,yc];c,s=np.cos(th),np.sin(th)
    ang=np.sort(np.mod(np.arctan2((-q[:,0]*s+q[:,1]*c)/b,(q[:,0]*c+q[:,1]*s)/a),2*np.pi))
    coverage=float(np.degrees(2*np.pi-np.max(np.diff(np.r_[ang,ang[0]+2*np.pi]))))
    if not 120<=coverage<=220:return None
    residual=point_to_ellipse_orth_dist(points[:,0],points[:,1],xc,yc,a,b,th-np.pi/2)
    return dict(ellipse_rms_px=float(np.sqrt(np.mean(residual**2))),a_px=float(a),
                b_over_a=float(b/a),coverage_deg=coverage,ellipse_xc=float(xc),ellipse_yc=float(yc))

def sample_window(contour,arc,start,span,n):
    u=np.linspace(start,start+span,n)
    return np.column_stack([np.interp(u,arc,contour[:,1]),np.interp(u,arc,contour[:,0])])

def windows(image,span=36.4,sigma=.7,kind='line',scene=''):
    native_span=span
    span=span/2
    sm=ndi.gaussian_filter(image,sigma/2)
    gx=ndi.sobel(sm,axis=1)/8;gy=ndi.sobel(sm,axis=0)/8
    mag=np.hypot(gx,gy)/2
    h,w=image.shape
    for level in range(24,233,16):
        contours=find_contours(sm,float(level),fully_connected='high')
        for ci,contour in enumerate(contours):
            if len(contour)<25:continue
            arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(contour,axis=0),axis=1))]
            if arc[-1]<span:continue
            for start in np.arange(0,arc[-1]-span+1e-6,span/2):
                pts=sample_window(contour,arc,start,span,26 if kind=='line' else 35)
                x,y=pts[:,0],pts[:,1]
                if x.min()<5 or y.min()<5 or x.max()>w-6 or y.max()>h-6:continue
                # Exclude sky/horizon from distant Twin Cairns landscape views.
                if scene.startswith('twin_cairns') and y.min()<300:continue
                strength=ndi.map_coordinates(mag,[y,x],order=1)
                if np.median(strength)<2.0:continue
                pts=pts*2+.5
                mean=pts.mean(0)
                record=dict(scene=scene,level_dn=level,contour=ci,start_arc_px=float(start*2),
                    span_px=native_span,sigma_px=sigma,x=float(mean[0]),y=float(mean[1]),
                    median_gradient_dn_px=float(np.median(strength)))
                if kind=='line':
                    rms,angle=line_fit(pts);record.update(rms_px=rms,angle_deg=angle)
                    # Flag potential JPEG grid-aligned edges; report a filtered sensitivity.
                    axis_angle=min(angle,abs(angle-90),abs(angle-180))
                    gridx=np.mean(np.minimum(np.mod(pts[:,0],8),8-np.mod(pts[:,0],8))<.8)
                    gridy=np.mean(np.minimum(np.mod(pts[:,1],8),8-np.mod(pts[:,1],8))<.8)
                    record['jpeg_grid_flag']=bool(axis_angle<2 and max(gridx,gridy)>.8)
                else:
                    fit=ellipse_fit(pts)
                    if fit is None:continue
                    record.update(fit)
                yield record,pts

def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def target_reference():
    s3=json.loads((ROOT/'independent-reconstruction/step3_features.json').read_text())
    dorsal=np.array([[p['x_erf'],p['y_erf']] for p in s3['dorsal_stations']])
    rim=[p for p in s3['arch_radial_points'] if (p['theta_deg']>=150 or p['theta_deg']<=-35) and abs(p['theta_deg']+45)>.001]
    return dorsal,np.array([[p['x_erf'],p['y_erf']] for p in rim])

def choose_target(candidates,ref,kind):
    center=ref.mean(0);tree=cKDTree(ref);by_level={}
    for r,p in candidates:
        if np.linalg.norm(p.mean(0)-center)>12:continue
        dist=float(np.mean(tree.query(p)[0]))
        if dist>4:continue
        if kind=='line' and abs(r['angle_deg']-28.895)>12:continue
        if r['level_dn'] not in by_level or dist<by_level[r['level_dn']][0]:
            by_level[r['level_dn']]=(dist,r,p)
    return [(dict(r,reference_distance_px=d),p) for d,r,p in by_level.values()]

def overview_panel(records,points,manifest,filename,key,n=18):
    selected=sorted(range(len(records)),key=lambda i:records[i][key])
    # Spread examples spatially, avoid same patch repeated at different thresholds.
    keep=[]
    for i in selected:
        r=records[i]
        if any(r['scene']==records[j]['scene'] and np.hypot(r['x']-records[j]['x'],r['y']-records[j]['y'])<50 for j in keep):continue
        keep.append(i)
        if len(keep)>=n:break
    fig,axes=plt.subplots(math.ceil(n/3),3,figsize=(12,3*math.ceil(n/3)))
    lookup={r['id']:r for r in manifest};cache={}
    for ax,i in zip(axes.flat,keep):
        r=records[i];scene=r['scene']
        if scene not in cache:
            im=Image.open(ROOT/lookup[scene]['path']).convert('RGB')
            cache[scene]=im.resize((im.width//2,im.height//2),Image.Resampling.BOX).resize(im.size,Image.Resampling.NEAREST)
        pts=points[i];cx,cy=r['x'],r['y'];pad=48
        ax.imshow(cache[scene]);ax.plot(pts[:,0],pts[:,1],color='#00ffff',lw=1)
        ax.set_xlim(cx-pad,cx+pad);ax.set_ylim(cy+pad,cy-pad)
        ax.set_title(f"{scene} ({cx:.0f},{cy:.0f})\n{key}={r[key]:.3f} px; level={r['level_dn']}",fontsize=9)
        ax.set_xticks([]);ax.set_yticks([])
    for ax in list(axes.flat)[len(keep):]:ax.axis('off')
    fig.suptitle('Photometric contour examples; cyan tracks are not automatically classified object boundaries')
    fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/'figures'/filename,dpi=150);plt.close(fig)
    return [records[i] for i in keep]

def main():
    manifest=json.loads((OUT/'image-manifest.json').read_text())['images']
    scenes=[r for r in manifest if r.get('role')=='whole_frame' and 'path' in r]
    dorsal,rim=target_reference();all_summary={};baseline_records=[];baseline_points=[];arc_records=[];arc_points=[]
    for sigma,span in [(.7,36.4),(1.2,36.4),(.7,24.0)]:
        records=[];points=[];target=[]
        for scene in scenes:
            a=gray(ROOT/scene['path'])
            candidates=list(windows(a,span,sigma,'line',scene['id']))
            if scene['id']=='sol3556_585':target=choose_target(candidates,dorsal,'line')
            for r,p in candidates:
                if scene['id']=='sol3556_585' and 1015<r['x']<1110 and 925<r['y']<1020:continue
                records.append(r);points.append(p)
            print(f"line sigma={sigma} span={span}: {scene['id']} {len(candidates)} windows",flush=True)
        target_values=[r['rms_px'] for r,p in target]
        threshold=float(np.median(target_values)) if target_values else None
        per_scene=[]
        for scene in scenes:
            rr=[r for r in records if r['scene']==scene['id']];vals=np.array([r['rms_px'] for r in rr])
            per_scene.append(dict(scene=scene['id'],n_windows=len(vals),median_rms_px=float(np.median(vals)) if len(vals) else None,
                count_at_or_below_target=int(np.sum(vals<=threshold)) if threshold is not None else None,
                fraction_at_or_below_target=float(np.mean(vals<=threshold)) if len(vals) and threshold is not None else None))
        eligible=[r for r in records if not r['jpeg_grid_flag']]
        key=f'sigma{sigma}_span{span}'
        all_summary[key]=dict(n_scenes=len(scenes),n_control_windows=len(records),target_levels=len(target),
            target_median_rms_px=threshold,target_min_rms_px=min(target_values) if target_values else None,
            target_max_rms_px=max(target_values) if target_values else None,
            fraction_control_windows_at_or_below_target=float(np.mean([r['rms_px']<=threshold for r in records])) if threshold is not None else None,
            fraction_without_jpeg_grid_flags=float(np.mean([r['rms_px']<=threshold for r in eligible])) if threshold is not None else None,
            per_scene=per_scene,target_records=[r for r,p in target])
        write_csv(OUT/f'edge-windows-{key}.csv',records)
        if sigma==.7 and span==36.4:
            baseline_records,baseline_points=records,points
            # Target overlay preserves exact paths selected by geometric proximity.
            fig,ax=plt.subplots(figsize=(8,6));ax.imshow(Image.open(OUT/'images/sol3556_585.jpg').convert('RGB'))
            for r,p in target:ax.plot(p[:,0],p[:,1],label=f"{r['level_dn']} DN: {r['rms_px']:.3f}px")
            ax.scatter(dorsal[:,0],dorsal[:,1],s=8,c='white',label='prior erf reference')
            ax.set_xlim(1025,1085);ax.set_ylim(980,930);ax.legend(fontsize=8);fig.tight_layout()
            fig.savefig(OUT/'figures/target-isophotes.png',dpi=180);plt.close(fig)
    # Partial arcs at the same apparent radius: geometric evidence only, not terminal-face classification.
    target_arcs=[]
    for scene in scenes:
        candidates=list(windows(gray(ROOT/scene['path']),54,.7,'arc',scene['id']))
        if scene['id']=='sol3556_585':target_arcs=choose_target(candidates,rim,'arc')
        for r,p in candidates:
            if scene['id']=='sol3556_585' and 1015<r['x']<1110 and 925<r['y']<1020:continue
            arc_records.append(r);arc_points.append(p)
        print(f"arcs {scene['id']}: {len(candidates)}",flush=True)
    arc_target=[r['ellipse_rms_px'] for r,p in target_arcs]
    all_summary['arcs']=dict(n_control_arcs=len(arc_records),target_records=[r for r,p in target_arcs],
        target_median_rms_px=float(np.median(arc_target)) if arc_target else None,
        interpretation='Selected isophote arc fits; not automatically verified geological end faces')
    write_csv(OUT/'ellipse-arcs.csv',arc_records)
    all_summary['straight_examples']=overview_panel(baseline_records,baseline_points,manifest,'straight-edge-examples.png','rms_px')
    all_summary['arc_examples']=overview_panel(arc_records,arc_points,manifest,'round-arc-examples.png','ellipse_rms_px')
    # Per-frame comparison avoids presenting the many overlapping windows as independent rocks.
    fig,ax=plt.subplots(figsize=(10,7));names=[];data=[]
    for sc in scenes:
        vals=[r['rms_px'] for r in baseline_records if r['scene']==sc['id']]
        if vals:data.append(vals);names.append(sc['id'])
    ax.boxplot(data,orientation='horizontal',tick_labels=names,showfliers=False)
    t=all_summary['sigma0.7_span36.4']['target_median_rms_px']
    if t is not None:ax.axvline(t,color='#b33c28',label=f'Target isophote median {t:.3f}px')
    ax.set_xlim(0,4);ax.set_xlabel('36.4 px contour span: orthogonal line RMS (px)');ax.legend();fig.tight_layout()
    fig.savefig(OUT/'figures/straightness-by-scene.png',dpi=170);plt.close(fig)
    all_summary['environment']={'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform()}
    all_summary['scope']='Uniform 2x2 binning, coordinates/residuals in equivalent native pixels. Exploratory fixed-span photometric windows, correlated within/between thresholds; no clast-level rarity or origin probability.'
    (OUT/'results.json').write_text(json.dumps(all_summary,indent=2)+'\n')
    print('Completed uniform image-window study.',flush=True)

if __name__=='__main__':main()
