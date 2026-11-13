"""Exploratory physical taper, residual diagnostics, and reproducible exclusion figure."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import physical_model as model
import target_benchmark as benchmark
from pds_images import read_image

BASE=Path(__file__).resolve().parents[1]


def diagnostics(values):
    values=np.asarray(values)
    return dict(mean_px=float(values.mean()),std_px=float(values.std()),
                p95_absolute_px=float(np.percentile(abs(values),95)),
                adjacent_correlation=float(np.corrcoef(values[:-1],values[1:])[0,1]))


def main():
    data,_,_=benchmark.load_data()
    result=json.loads((BASE/'results/physical-model.json').read_text())
    extension={'scope':'Exploratory seven-parameter physically tangent frustum; protocol e895201.',
               'folds':[]}
    masks={name:np.ones(len(group['xy']),dtype=bool) for name,group in data.items()}
    parameters,record=model.fit(data,masks,fit_taper=True)
    extension.update(parameters=parameters.tolist(),diagnostics=record,
                     full_rms_px=benchmark.rms(np.concatenate(list(model.residuals(parameters,data).values()))))
    predicted={name:np.empty(len(group['xy'])) for name,group in data.items()}
    for fold in range(5):
        tests={name:np.array_split(np.arange(len(group['xy'])),5)[fold] for name,group in data.items()}
        masks={name:benchmark.split_masks(len(group['xy']),tests[name]) for name,group in data.items()}
        parameters,record=model.fit(data,masks,fit_taper=True)
        residuals=model.residuals(parameters,data)
        groups={}
        for name,indices in tests.items():
            predicted[name][indices]=residuals[name][indices]
            groups[name]=dict(test_indices=indices.tolist(),training_indices=np.flatnonzero(masks[name]).tolist(),
                              test_residuals_px=residuals[name][indices].tolist())
        extension['folds'].append(dict(fold=fold,parameters=parameters.tolist(),diagnostics=record,features=groups))
    extension['guarded_rms_px']=benchmark.rms(np.concatenate(list(predicted.values())))
    extension['guarded_residuals_px']={name:values.tolist() for name,values in predicted.items()}
    (BASE/'results/physical-frustum.json').write_text(json.dumps(extension,indent=2)+'\n')
    residual_diagnostics={'full':{},'guarded':{}}
    for name in data:
        residual_diagnostics['full'][name]=diagnostics(result['full_fit']['residuals_px'][name])
        values=[]
        for fold in result['folds']:
            values.extend(zip(fold['features'][name]['test_indices'],fold['features'][name]['test_residuals_px']))
        residual_diagnostics['guarded'][name]=diagnostics([v for _,v in sorted(values)])
    starts=np.array(result['diagnostics']['start_parameters'])
    residual_diagnostics['full_fit_parameter_peak_to_peak']=np.ptp(starts,axis=0).tolist()
    (BASE/'results/residual-diagnostics.json').write_text(json.dumps(residual_diagnostics,indent=2)+'\n')
    image,_=read_image(BASE/'sources/images/NRB_445620806EDR_F0261274NCAM00354M1.IMG')
    fig,ax=plt.subplots(figsize=(9,9))
    lo,hi=np.percentile(image,[1,99]);ax.imshow(image,cmap='gray',vmin=lo,vmax=hi)
    ax.add_patch(Rectangle((0,825),1024,199,fill=False,edgecolor='red',lw=2))
    ax.add_patch(Rectangle((160,660),155,115,fill=False,edgecolor='#16c0ff',lw=2))
    ax.text(330,710,'Geological ring / partial rim',color='#16c0ff',fontsize=12)
    ax.text(20,850,'ROVER HARDWARE — EXCLUDED',color='red',fontsize=12)
    ax.set_title('Observed original Navcam / NCAM00354, right camera')
    fig.tight_layout();fig.savefig(BASE/'figures/navcam-rover-exclusion.png',dpi=150);plt.close(fig)
    print(json.dumps({'physical_frustum_full_rms_px':extension['full_rms_px'],
                      'physical_frustum_guarded_rms_px':extension['guarded_rms_px'],
                      'rear_front_radius_ratio':extension['parameters'][6]}))


if __name__=='__main__':
    main()
