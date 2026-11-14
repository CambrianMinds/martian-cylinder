"""Compare historical M4 with camera-projected taper, enforcing finite extent."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import physical_model as model
import target_benchmark as benchmark

BASE=Path(__file__).resolve().parents[1]


def extent(parameters,data):
    _,line=model.projected_boundaries(parameters)
    direction=line[1]-line[0]
    fractions=(data['dorsal']['xy']-line[0])@direction/(direction@direction)
    finite=model.residuals(parameters,data,finite_generator=True)
    return dict(generator_endpoints_xy=line.tolist(),dorsal_fraction_range=[float(fractions.min()),float(fractions.max())],
                stations_outside_finite_generator=np.flatnonzero((fractions<0)|(fractions>1)).tolist(),
                finite_dorsal_rms_px=benchmark.rms(finite['dorsal']),
                finite_total_rms_px=benchmark.rms(np.concatenate(list(finite.values()))))


def main():
    data,_,image=benchmark.load_data()
    old=json.loads((model.ROOT/'independent-reconstruction/step9_joint_model.json').read_text())['joint_models']['M4_Tapered_Conical_Frustum_Coupled_8DOF']
    p=old['params'];slope=(1-p['scale_ratio_s'])*p['r_dorsal']/p['L_proj']
    result={'old_m4':old,'old_m4_required_intercept_px':float(np.sqrt(p['a']**2+slope**2*p['b']**2)),
            'original_fits':{},'finite_generator_refits':{}}
    fig,axes=plt.subplots(1,2,figsize=(13,6))
    for ax,(name,file) in zip(axes,[('cylinder','physical-model.json'),('frustum','physical-frustum.json')]):
        source=json.loads((BASE/'results'/file).read_text());parameters=np.array(source['parameters'])
        result['original_fits'][name]=dict(parameters=parameters.tolist(),axis_bearing_deg=float(np.degrees(parameters[4])),
            rms_by_feature_px={k:benchmark.rms(v) for k,v in model.residuals(parameters,data).items()},**extent(parameters,data))
        predicted={k:np.empty(len(v['xy'])) for k,v in data.items()};folds=[]
        all_masks={k:np.ones(len(v['xy']),dtype=bool) for k,v in data.items()}
        fitted,diagnostic=model.fit(data,all_masks,fit_taper=name=='frustum',finite_generator=True)
        raw=model.residuals(fitted,data,finite_generator=True)
        record=dict(parameters=fitted.tolist(),diagnostics=diagnostic,
                    full_rms_px=benchmark.rms(np.concatenate(list(raw.values()))),
                    full_rms_by_feature_px={k:benchmark.rms(v) for k,v in raw.items()},**extent(fitted,data))
        for fold in range(5):
            tests={k:np.array_split(np.arange(len(v['xy'])),5)[fold] for k,v in data.items()}
            masks={k:benchmark.split_masks(len(v['xy']),tests[k]) for k,v in data.items()}
            trial,diagnostic=model.fit(data,masks,fit_taper=name=='frustum',finite_generator=True)
            values=model.residuals(trial,data,finite_generator=True)
            groups={}
            for k,indices in tests.items():
                predicted[k][indices]=values[k][indices]
                groups[k]=dict(training_indices=np.flatnonzero(masks[k]).tolist(),test_indices=indices.tolist(),test_residuals_px=values[k][indices].tolist())
            folds.append(dict(fold=fold,parameters=trial.tolist(),diagnostics=diagnostic,features=groups))
        record.update(guarded_rms_px=benchmark.rms(np.concatenate(list(predicted.values()))),
                      guarded_rms_by_feature_px={k:benchmark.rms(v) for k,v in predicted.items()},folds=folds)
        result['finite_generator_refits'][name]=record
        ax.imshow(image,cmap='gray',vmin=np.percentile(image[937:1005,1018:1095],2),vmax=np.percentile(image[937:1005,1018:1095],98))
        curves,line=model.projected_boundaries(parameters)
        for curve in curves.values():ax.plot(*np.vstack([curve,curve[0]]).T,lw=1)
        ax.plot(*line.T,c='cyan',lw=2,label='Finite generator of original fit')
        xy=data['dorsal']['xy'];ax.scatter(*xy.T,c='orange',s=14,label='Retained dorsal points')
        outside=result['original_fits'][name]['stations_outside_finite_generator']
        ax.scatter(*xy[outside].T,facecolors='none',edgecolors='red',s=55,label='Beyond generator endpoint')
        ax.set(xlim=(1018,1095),ylim=(1005,937),title=name+' / original line-scored fit');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(BASE/'figures/finite-generator-review.png',dpi=160);plt.close(fig)
    (BASE/'results/m4-reevaluation.json').write_text(json.dumps(result,indent=2)+'\n')
    for name,row in result['finite_generator_refits'].items():
        print(name,'original outside',result['original_fits'][name]['stations_outside_finite_generator'],
              'finite full',row['full_rms_px'],'finite guarded',row['guarded_rms_px'],'parameters',row['parameters'])


if __name__=='__main__':
    main()
