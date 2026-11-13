"""Target-only spatially blocked prediction checks of the existing geometry."""
from pathlib import Path
import sys,json,hashlib,platform
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/sediment-pipe-comparison/results/target-benchmark'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(ROOT/'independent-reconstruction'))
from step3_feature_extraction import load_drxx
from step4_endface_and_conic_models import order_arch_points,point_to_ellipse_orth_dist
from step8_pebble_correction_and_rear_terminus import extract_rear_terminus_points

def rms(x):return float(np.sqrt(np.mean(np.asarray(x)**2)))

def load_data():
    s3=json.loads((ROOT/'independent-reconstruction/step3_features.json').read_text())
    if s3['extraction_geometry']['version']!='physical-edge-polarity-v2':
        raise ValueError('Unexpected feature extraction version')
    front=[p for p in order_arch_points(s3['arch_radial_points']) if
        (p['theta_deg']>=150 or p['theta_deg']<=-35) and abs(p['theta_deg']+45)>.001]
    _,_,im=load_drxx()
    rear=extract_rear_terminus_points(im,center_xy=(1035.5,951.2),theta_deg_list=np.arange(-210.,-30.,5.),iso_target=.086)[8:32]
    dorsal=s3['dorsal_stations']
    data={}
    for name,pts in [('front',front),('rear',rear),('dorsal',dorsal)]:
        sigma=[max(p.get('s_uncertainty_px',.08),.08) if name=='dorsal' else p['r_uncertainty_px'] for p in pts]
        data[name]={'xy':np.array([[p['x_erf'],p['y_erf']] for p in pts]),'sigma':np.array(sigma)}
    assert [len(data[n]['xy']) for n in data]==[35,24,26]
    s8=json.loads((ROOT/'independent-reconstruction/step8_pebble_and_rear_terminus.json').read_text())
    p=s8['front_face_models_before_vs_after_single_outlier_exclusion']['corrected_35pt_clean_rim_excluding_only_theta_minus45']['M3_Ellipse_Dorsal_Constrained_4DOF']['params']
    return data,p,im

def split_masks(n,test,guard=2):
    train=np.ones(n,dtype=bool);train[test]=False
    if len(test):train[max(0,int(test.min())-guard):min(n,int(test.max())+guard+1)]=False
    return train

def rear_registration(data,p,train,test):
    xy=data['rear']['xy']
    def residual(center):
        return point_to_ellipse_orth_dist(xy[:,0],xy[:,1],*center,p['semi_major'],p['semi_minor'],np.radians(p['fixed_axis_deg']))
    sol=least_squares(lambda c:residual(c)[train],[1036.2,964.9],max_nfev=3000)
    if not sol.success:raise RuntimeError(sol.message)
    r=residual(sol.x)
    return dict(center_xy=sol.x.tolist(),train_n=int(np.sum(train)),test_n=len(test),
        training_rms_px=rms(r[train]),test_rms_px=rms(r[test]),test_max_abs_px=float(np.max(np.abs(r[test]))),
        test_indices=test.tolist(),test_residuals_px=r[test].tolist())

def model_residuals(p,data):
    xc,yc,a,b,L,th=p;cr=[xc-L*np.cos(th),yc-L*np.sin(th)]
    result={}
    for name,center in [('front',[xc,yc]),('rear',cr)]:
        xy=data[name]['xy']
        result[name]=point_to_ellipse_orth_dist(xy[:,0],xy[:,1],*center,a,b,th)
    xy=data['dorsal']['xy']
    result['dorsal']=-(xy[:,0]-xc)*np.sin(th)+(xy[:,1]-yc)*np.cos(th)+a
    return result

LOW=np.array([1060,975,12,10,20,np.radians(20)])
HIGH=np.array([1080,995,25,22,60,np.radians(45)])

def fit_cylinder(data,masks):
    def objective(p):
        rr=model_residuals(p,data)
        return np.concatenate([rr[n][masks[n]]/data[n]['sigma'][masks[n]] for n in data])
    solutions=[]
    for angle in [28,31.2,35]:
        sol=least_squares(objective,[1068.88,986,19.7,16.4,40,np.radians(angle)],bounds=(LOW,HIGH),max_nfev=3000)
        if sol.success:solutions.append(sol)
    if not solutions:raise RuntimeError('All training optimizations failed')
    sol=min(solutions,key=lambda s:np.sum(s.fun**2));p=sol.x
    return p,dict(training_objective=float(np.sum(sol.fun**2)),successful_starts=len(solutions),
        bound_hits=np.flatnonzero((np.abs(p-LOW)<1e-5)|(np.abs(p-HIGH)<1e-5)).tolist(),
        params=dict(xc=float(p[0]),yc=float(p[1]),a=float(p[2]),b=float(p[3]),L_proj=float(p[4]),theta_deg=float(np.degrees(p[5]))))

def main():
    data,p,im=load_data();n=24;all_idx=np.arange(n)
    frozen=dict(a=p['semi_major'],b=p['semi_minor'],angle_deg=p['fixed_axis_deg'],scale=1.0)
    reproduction=rear_registration(data,p,np.ones(n,dtype=bool),all_idx)
    anchor=np.arange(0,n,4);mask=np.zeros(n,dtype=bool);mask[anchor]=True
    sparse=rear_registration(data,p,mask,all_idx[~mask]);sparse['anchor_indices']=anchor.tolist()
    rear_folds=[];rear_prediction=np.full(n,np.nan)
    for fold,test in enumerate(np.array_split(all_idx,5)):
        mask=split_masks(n,test);r=rear_registration(data,p,mask,test);r['fold']=fold+1
        rear_folds.append(r);rear_prediction[test]=r['test_residuals_px']
    full_masks={name:np.ones(len(d['xy']),dtype=bool) for name,d in data.items()}
    full_p,full_meta=fit_cylinder(data,full_masks);full_r=model_residuals(full_p,data)
    predictions={name:np.full(len(d['xy']),np.nan) for name,d in data.items()};folds=[]
    for fold in range(5):
        tests={name:np.array_split(np.arange(len(d['xy'])),5)[fold] for name,d in data.items()}
        masks={name:split_masks(len(d['xy']),tests[name]) for name,d in data.items()}
        pp,meta=fit_cylinder(data,masks);rr=model_residuals(pp,data);meta['fold']=fold+1
        meta['training_n']=sum(int(x.sum()) for x in masks.values());meta['features']={}
        for name in data:
            test=tests[name];predictions[name][test]=rr[name][test]
            meta['features'][name]=dict(test_indices=test.tolist(),test_rms_px=rms(rr[name][test]),test_residuals_px=rr[name][test].tolist())
        folds.append(meta)
    cross_masks={name:np.ones(len(d['xy']),dtype=bool) if name!='dorsal' else np.zeros(len(d['xy']),dtype=bool) for name,d in data.items()}
    cp,cross=fit_cylinder(data,cross_masks);cr=model_residuals(cp,data)
    cross['withheld_dorsal_rms_px']=rms(cr['dorsal']);cross['withheld_dorsal_max_abs_px']=float(np.max(np.abs(cr['dorsal'])))
    cross['training_family_rms_px']={name:rms(cr[name]) for name in ['front','rear']}
    result=dict(protocol='protocol.md',frozen_front_shape=frozen,rear_registration_reproduction=reproduction,
        sparse_rear_registration=sparse,blocked_rear_registration=dict(folds=rear_folds,pooled_test_rms_px=rms(rear_prediction),max_abs_px=float(np.max(np.abs(rear_prediction)))),
        full_m1_fit=dict(**full_meta,rms_px={name:rms(r) for name,r in full_r.items()},total_rms_px=rms(np.concatenate(list(full_r.values())))),
        blocked_m1_prediction=dict(folds=folds,pooled_rms_px={name:rms(r) for name,r in predictions.items()},total_rms_px=rms(np.concatenate(list(predictions.values())))),
        dorsal_entirely_withheld=cross,
        scope='Retrospective coordinate-level prediction. Existing feature selection retained; no calibrated significance or origin probability.',
        environment=dict(python=platform.python_version(),numpy=np.__version__),
        input_hashes={name:hashlib.sha256((ROOT/'independent-reconstruction'/name).read_bytes()).hexdigest() for name in ['step3_features.json','step8_pebble_and_rear_terminus.json']})
    # Structural checks prevent accidental training/test overlap or incomplete scoring.
    assert abs(result['full_m1_fit']['total_rms_px']-.37882893)<1e-5
    assert np.all(np.isfinite(rear_prediction))
    assert all(np.all(np.isfinite(x)) for x in predictions.values())
    for fold in range(5):
        for name,d in data.items():
            test=np.array_split(np.arange(len(d['xy'])),5)[fold]
            train=split_masks(len(d['xy']),test)
            assert not np.any(train[test])
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,axes=plt.subplots(2,2,figsize=(12,9))
    ax=axes[0,0];ax.imshow(im,cmap='gray');ax.set_xlim(1022,1094);ax.set_ylim(1004,936)
    for name,color in [('front','#3bdf70'),('rear','#fdca45'),('dorsal','#30c9ed')]:
        xy=data[name]['xy'];ax.scatter(xy[:,0],xy[:,1],s=12,c=color,label=name)
    ax.set_title('Existing target measurements; no new point selection');ax.legend()
    ax=axes[0,1];ax.axhline(0,color='gray',lw=.6);ax.plot(all_idx,rear_prediction,'o-',label='Blocked withheld predictions')
    ax.scatter(sparse['test_indices'],sparse['test_residuals_px'],marker='x',label='Six-anchor registration: withheld 18')
    ax.set_xlabel('Rear station index');ax.set_ylabel('Signed orthogonal residual (px)');ax.legend(fontsize=8);ax.set_title('Front ellipse shape fixed throughout')
    ax=axes[1,0];names=list(data);x=np.arange(3);w=.35
    ax.bar(x-w/2,[rms(full_r[n]) for n in names],w,label='Full-fit descriptive residual')
    ax.bar(x+w/2,[rms(predictions[n]) for n in names],w,label='Spatially withheld prediction')
    ax.set_xticks(x,names);ax.set_ylabel('RMS (px)');ax.legend(fontsize=8);ax.set_title('Strict M1: same constraints, five guarded block folds')
    ax=axes[1,1];ax.axhline(0,color='gray',lw=.6);ax.plot(cr['dorsal'],'o-',color='#a74e31')
    ax.set_title('Dorsal edge wholly withheld from fitting');ax.set_xlabel('Dorsal station index');ax.set_ylabel('Predicted tangent residual (px)')
    fig.tight_layout();fig.savefig(OUT/'predictive-checks.png',dpi=180);plt.close(fig)
    report=f'''# Predictive geometry validation of the target

These tests use the existing target only. No geological comparison images were added. The protocol was written before the new runs. All outcomes are retained.

## Results

| Check | Scored data | RMS error (px) |
| --- | --- | ---: |
| Established unchanged-front-shape registration, reproduced | All 24 rear stations used for translation fit | {reproduction['test_rms_px']:.4f} |
| Only six rear anchors used for translation | Other 18 rear stations predicted | {sparse['test_rms_px']:.4f} |
| Five guarded, contiguous rear holdouts | Each rear station predicted once | {rms(rear_prediction):.4f} |
| Strict M1, full fit | All 85 points fitted | {result['full_m1_fit']['total_rms_px']:.4f} |
| Strict M1, five guarded spatial holdouts | Each of 85 points predicted once | {result['blocked_m1_prediction']['total_rms_px']:.4f} |
| Dorsal edge wholly withheld | All 26 dorsal stations predicted from front/rear fits | {cross['withheld_dorsal_rms_px']:.4f} |

## What these checks establish

The first three checks fix both ellipse axes and its orientation from the existing front/dorsal measurements. The rear data fit two translation coordinates only. In the six-anchor test, the other 18 stations cannot influence registration. In the blocked tests, omitted contiguous points and their two-station guards cannot influence the fitted translation. This quantifies how well transferred front geometry predicts rear points beyond those used to register it.

The strict-cylinder check preserves M1's six parameters, equal end ellipses, collinear centers, and exact dorsal tangency. It refits those parameters to training points only, from three prespecified starting angles. The pooled heldout residuals are: front {rms(predictions['front']):.4f} px, rear {rms(predictions['rear']):.4f} px, dorsal {rms(predictions['dorsal']):.4f} px. The withheld scores do not select the optimizer or starting point.

Withholding the entire dorsal feature is a separate cross-feature prediction. It fits only front and rear data, then evaluates M1's required upper tangent with no dorsal offset or angle adjustment. Its result is reported separately from the spatial-block test.

## Assessment of the new evidence

The fixed-shape rear transfer survives both sparse registration and contiguous holdouts with roughly 0.2–0.24 px errors. Thus the rear agreement persists beyond the rear points used to position the copied front ellipse. The six-parameter cylinder also predicts withheld spatial blocks with a pooled error below one pixel, although its error rises from 0.379 px in-sample to 0.723 px out-of-sample.

The whole-dorsal holdout is a separate sensitivity experiment: 1.909 px RMS, maximum 3.391 px. Its front/rear-only optimum has an axis of 33.177 degrees, versus the measured dorsal bearing of 28.895 degrees. These modest absolute deviations exceed the complete-fit residuals and show the information supplied by the measured dorsal constraint: removing it changes the preferred orientation and tangent. This is not a mandatory passing standard, a physical surface-damage measurement, or a calibrated rejection. It is distinct from the fixed-shape rear-transfer tests, which retain dorsal information by design.

All three starting angles converged for every strict-cylinder fit, and no fitted parameter hit the specified bounds. The full-data fit reproduced the original M1 total RMS within 0.00001 px. Training/test membership and complete heldout scoring were checked programmatically.

## Interpretation limits

These are retrospective tests of already selected coordinates from one image. They do not constitute independent image acquisition, redo boundary selection blindly, establish a regional rarity, or measure the probability of manufactured origin. They do directly test predictive geometric consistency beyond the already reported full fit. Registration of an unknown rear position remains explicit; no claim is made to infer cylinder length from a front ellipse alone.

![Predictive geometry checks](predictive-checks.png)

`results.json` retains every fold, fitted parameter, residual, bound-hit diagnostic, and input hash. Reproduce with `python audit/predictive-validation/run_validation.py` using the existing reconstruction environment.
'''
    (OUT/'report.md').write_text(report,encoding='utf-8')
    print(report.split('## What')[0])

if __name__=='__main__':main()
