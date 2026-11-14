"""Summarize completed measurements, preserving threshold and selection sensitivity."""
from pathlib import Path
import json,csv,gzip,io,collections
import numpy as np
from scipy import ndimage as ndi
from skimage.measure import find_contours
from PIL import Image
from analyze import ROOT,OUT,gray,sample_window,overview_panel
import matplotlib.pyplot as plt

def main():
    results=json.loads((OUT/'results.json').read_text());summary={}
    for key in ['sigma0.7_span36.4','sigma1.2_span36.4','sigma0.7_span24.0']:
        d=results[key];selected=min(d['target_records'],key=lambda r:r['reference_distance_px'])
        t=selected['rms_px']; rows=list(csv.DictReader((OUT/f'edge-windows-{key}.csv').open()))
        matched=[r for r in rows if .5*selected['median_gradient_dn_px']<=float(r['median_gradient_dn_px'])<=2*selected['median_gradient_dn_px']]
        grouped=collections.defaultdict(list)
        for r in rows:grouped[r['scene']].append(float(r['rms_px']))
        cells={}
        for r in rows:
            cell=(r['scene'],int(float(r['x'])//64),int(float(r['y'])//64))
            if cell not in cells or float(r['rms_px'])<float(cells[cell]['rms_px']):cells[cell]=r
        scene_rows=[]
        for scene,vals in grouped.items():
            scene_rows.append(dict(scene=scene,n_windows=len(vals),count_at_or_below_target=int(np.sum(np.array(vals)<=t)),fraction_at_or_below_target=float(np.mean(np.array(vals)<=t))))
        summary[key]=dict(target_selection='Minimum mean distance to pre-existing erf stations, not minimum RMS',
            target_selected=selected,n_control_windows=len(rows),n_at_or_below_target=sum(float(r['rms_px'])<=t for r in rows),
            fraction_at_or_below_target=float(np.mean([float(r['rms_px'])<=t for r in rows])),
            contrast_matched_n=len(matched),contrast_matched_at_or_below=sum(float(r['rms_px'])<=t for r in matched),
            n_spatial_cells=len(cells),n_cells_with_at_least_one_matching_edge=sum(float(r['rms_px'])<=t for r in cells.values()),
            per_scene=scene_rows)
    rows=list(csv.DictReader((OUT/'ellipse-arcs.csv').open()))
    summary['arcs']=dict(n_candidate_arcs=len(rows),minimum_control_rms_px=min(float(r['ellipse_rms_px']) for r in rows),
        target_selection_status='Not used to rank rarity: selected isophote differs from prior rim stations by 2.88 px on average; full-resolution erf method is different.',
        target_isophote_rms_px=results['arcs']['target_median_rms_px'])
    (OUT/'comparison-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    baseline=summary['sigma0.7_span36.4'];print(json.dumps({k:v for k,v in baseline.items() if k!='per_scene'},indent=2))
    # Regenerate visual examples from their exact contour indices, displaying the binned input.
    manifest=json.loads((OUT/'image-manifest.json').read_text())['images'];lookup={r['id']:r for r in manifest}
    cache={}
    def recover(r):
        key=(r['scene'],r['level_dn'],r['sigma_px'])
        if key not in cache:
            a=ndi.gaussian_filter(gray(ROOT/lookup[r['scene']]['path']),r['sigma_px']/2)
            cache[key]=find_contours(a,float(r['level_dn']),fully_connected='high')
        contour=cache[key][r['contour']]
        arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(contour,axis=0),axis=1))]
        return sample_window(contour,arc,r['start_arc_px']/2,r['span_px']/2,26 if 'rms_px'in r else 35)*2+.5
    for name,key,filename in [('straight_examples','rms_px','straight-edge-examples.png'),('arc_examples','ellipse_rms_px','round-arc-examples.png')]:
        rr=results[name];pp=[recover(r) for r in rr];overview_panel(rr,pp,manifest,filename,key)
    # Replot target paths without implicit false color.
    rr=results['sigma0.7_span36.4']['target_records'];fig,ax=plt.subplots(figsize=(8,6))
    im=Image.open(OUT/'images/sol3556_585.jpg').convert('RGB');im=im.resize((im.width//2,im.height//2),Image.Resampling.BOX).resize(im.size,Image.Resampling.NEAREST)
    ax.imshow(im)
    for r in rr:
        pts=recover(r);ax.plot(pts[:,0],pts[:,1],label=f"{r['level_dn']} DN: {r['rms_px']:.3f}px")
    ax.set_xlim(1025,1085);ax.set_ylim(980,930);ax.legend();fig.tight_layout();fig.savefig(OUT/'figures/target-isophotes.png',dpi=170);plt.close(fig)
    # Actual per-scene fraction using the closest-boundary target choice.
    pr=baseline['per_scene'];fig,ax=plt.subplots(figsize=(10,7));ax.barh([r['scene'] for r in pr],[100*r['fraction_at_or_below_target'] for r in pr],color='#367b83')
    ax.set_xlabel('Percent of sampled photometric windows with RMS <= target (0.303 native px)')
    ax.set_title('Conditional window frequency; not independent clasts or origin probability')
    fig.tight_layout();fig.savefig(OUT/'figures/straight-edge-frequency.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()
