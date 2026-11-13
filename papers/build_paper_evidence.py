"""Build paper evidence from retained files; no image acquisition or resampling."""
from pathlib import Path
import csv, gzip, hashlib, importlib.util, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from geometry_figure import build_geometry_figure

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PRED = ROOT/'audit/predictive-validation'
COMP = ROOT/'audit/comparative-study'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))

def verify(p):
    for name, digest in p['input_hashes'].items():
        assert sha(ROOT/'independent-reconstruction'/name) == digest, name
    for name,n in [('front',35),('rear',24),('dorsal',26)]:
        scored=[]; residuals=[]
        for fold in p['blocked_m1_prediction']['folds']:
            f=fold['features'][name]
            scored.extend(f['test_indices']);residuals.extend(f['test_residuals_px'])
            assert fold['successful_starts']==3 and not fold['bound_hits']
        assert sorted(scored)==list(range(n)), name
        assert abs(np.sqrt(np.mean(np.square(residuals)))-p['blocked_m1_prediction']['pooled_rms_px'][name])<1e-12
    sparse=p['sparse_rear_registration']
    assert set(sparse['anchor_indices']).isdisjoint(sparse['test_indices'])
    assert sorted(sparse['anchor_indices']+sparse['test_indices'])==list(range(24))
    assert sorted(i for f in p['blocked_rear_registration']['folds'] for i in f['test_indices'])==list(range(24))
    images=[r for r in read(COMP/'image-manifest.json')['images'] if 'path' in r]
    assert len(images)==28
    for r in images: assert sha(ROOT/r['path'])==r['sha256'],r['id']
    summary=read(COMP/'comparison-summary.json')['sigma0.7_span36.4']
    n=below=0
    with gzip.open(COMP/'edge-windows-sigma0.7_span36.4.csv.gz','rt',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            n+=1;below+=float(r['rms_px'])<=summary['target_selected']['rms_px']
    assert (n,below)==(226426,835)
    assert (n,below)==(summary['n_control_windows'],summary['n_at_or_below_target'])

def figures(p):
    build_geometry_figure()
    spec=importlib.util.spec_from_file_location('paper_validation',PRED/'run_validation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data,_,im=module.load_data()
    out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':13,'pdf.fonttype':42})
    low,high=np.percentile(im[932:1007,1014:1104],[2,98])
    def image(ax):
        ax.imshow(im,cmap='gray',interpolation='nearest',vmin=low,vmax=high)
        ax.set(xlim=(1014,1104),ylim=(1007,932),xlabel='Native x (px)',ylabel='Native y (px)')
    fig,axes=plt.subplots(1,2,figsize=(12,5.4))
    for ax in axes:image(ax)
    axes[0].set_title('(a) Native radiometric crop')
    axes[1].set_title('(b) Recorded boundaries and exclusions')
    ax=axes[1]
    for name,color in [('front','#54f087'),('rear','#ffd451'),('dorsal','#38d8ff')]:
        ax.scatter(*data[name]['xy'].T,s=13,c=color,zorder=4)
    s3=read(ROOT/'independent-reconstruction/step3_features.json')
    pebble=next(q for q in s3['arch_radial_points'] if abs(q['theta_deg']+45)<.001)
    ax.scatter(pebble['x_erf'],pebble['y_erf'],marker='x',c='#ff77d9',s=48,zorder=5)
    for label,xy,text,color in [
        ('Rear terminus',(1032,947),(1016,936),'#ffd451'),
        ('Dorsal boundary',(1054,954),(1043,940),'#38d8ff'),
        ('Excluded pebble',(pebble['x_erf'],pebble['y_erf']),(1070,953),'#ff77d9'),
        ('Front rim',(1051.75,985),(1083,988),'#54f087'),
        ('Soil contact',(1039.71,971.30),(1016,985),'white'),
        ('Shadow on soil',(1084,995),(1060,1004),'white')]:
        ax.annotate(label,xy=xy,xytext=text,color=color,fontsize=12,
                    arrowprops=dict(arrowstyle='->',color=color,lw=.8),
                    bbox=dict(facecolor='black',alpha=.6,edgecolor='none',pad=1.5))
    fig.tight_layout();fig.savefig(out/'target-boundaries.pdf',bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.4),gridspec_kw={'width_ratios':[1,1.35]})
    ax=axes[0];image(ax);ax.set(xlim=(1025,1042),ylim=(953,942),xticks=[1026,1030,1034,1038])
    frozen=p['frozen_front_shape'];sparse=p['sparse_rear_registration']
    th=np.radians(frozen['angle_deg']);psi=np.linspace(0,2*np.pi,2000)
    u,v=frozen['b']*np.cos(psi),frozen['a']*np.sin(psi);cx,cy=sparse['center_xy']
    ax.plot(cx+u*np.cos(th)-v*np.sin(th),cy+u*np.sin(th)+v*np.cos(th),c='#38d8ff',lw=1.2,label='Frozen transferred curve')
    rear=data['rear']['xy'];anchors=sparse['anchor_indices'];test=sparse['test_indices']
    ax.scatter(*rear[anchors].T,c='#ffd451',marker='s',s=30,label='Six fitted anchors',zorder=4)
    ax.scatter(*rear[test].T,c='#54f087',s=16,label='18 withheld stations',zorder=4)
    ax.set_title('(a) Rear arc after sparse registration',fontsize=13);ax.legend(fontsize=11,loc='lower center')
    ax=axes[1];blocked=np.full(24,np.nan)
    for fold in p['blocked_rear_registration']['folds']:blocked[fold['test_indices']]=fold['test_residuals_px']
    ax.axhline(0,c='gray',lw=.7)
    ax.plot(np.arange(24),blocked,'o-',color='#287d84',ms=4,label='Guarded blocks: each station withheld')
    ax.scatter(test,sparse['test_residuals_px'],c='#a05a20',marker='x',label='Six-anchor fit: other 18 stations')
    ax.set(xlabel='Rear station index',ylabel='Signed orthogonal residual (px)',title='(b) Predictions beyond registration points')
    ax.legend(fontsize=11,loc='upper center',bbox_to_anchor=(.5,-.20));ax.grid(alpha=.15)
    fig.tight_layout();fig.savefig(out/'rear-prediction.pdf',bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def main():
    p=read(PRED/'results.json');verify(p)
    values={'RegisteredRearRMS':p['rear_registration_reproduction']['test_rms_px'],
            'SparseRearRMS':p['sparse_rear_registration']['test_rms_px'],
            'BlockedRearRMS':p['blocked_rear_registration']['pooled_test_rms_px'],
            'FullJointRMS':p['full_m1_fit']['total_rms_px'],
            'BlockedJointRMS':p['blocked_m1_prediction']['total_rms_px'],
            'DorsalWithheldRMS':p['dorsal_entirely_withheld']['withheld_dorsal_rms_px']}
    (HERE/'paper-analysis-values.tex').write_text('% Generated from predictive results JSON.\n'+''.join(
        f'\\newcommand{{\\{k}}}{{{v:.4f}}}\n' for k,v in values.items()),encoding='utf-8')
    figures(p)
    paths=[HERE/'martian-cylinder-technical-paper.tex',Path(__file__).resolve(),
           HERE/'geometry_figure.py',HERE/'figures/geometry-constraints.pdf',
           ROOT/'audit/shading-sampling-review/check_sampling.py',
           ROOT/'audit/shading-sampling-review/results.json',
           PRED/'run_validation.py',PRED/'protocol.md',PRED/'results.json',PRED/'report.md',
           COMP/'protocol.md',COMP/'comparison-summary.json',COMP/'image-manifest.json',
           COMP/'report.md',COMP/'requirements.txt',COMP/'artifact-checksums.json',
           ROOT/'audit/priority-review/report.md',HERE/'paper-analysis-values.tex',
           HERE/'figures/target-boundaries.pdf',HERE/'figures/rear-prediction.pdf']
    paths+=sorted((COMP/'scripts').glob('*.py'))
    paths+=sorted((ROOT/'independent-reconstruction').glob('*.py'))
    paths+=[ROOT/'independent-reconstruction'/n for n in ['step1_provenance.json','step2_camera_geometry.json',
            'step3_features.json','step4_endface_models.json','step5_3d_interpretations.json',
            'step8_pebble_and_rear_terminus.json','step9_joint_model.json','measurements.json']]
    manifest=dict(revision_date='2026-11-13',reconstruction_base_commit='90fbf8f89ac2634a9dbd2b27f81fc80d68b9943c',
        scope='Working revision; no new commit or NASA acquisition implied.',
        validation=dict(images_checked=28,control_windows=226426,qualifying_windows=835),
        sha256={x.relative_to(ROOT).as_posix():sha(x) for x in paths})
    (HERE/'paper-evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    principal=[PRED/'protocol.md',PRED/'run_validation.py',PRED/'results.json',
               COMP/'comparison-summary.json',COMP/'image-manifest.json',HERE/'martian-cylinder-technical-paper.tex']
    tex=[r'\noindent Paths are relative to the repository root. The accompanying JSON manifest lists all synthesis inputs, scripts, and figure digests.',
         r'\begin{longtable}{@{}p{0.97\linewidth}@{}}\toprule']
    for x in principal:
        digest=sha(x)
        tex.extend([r'\sourcepath{'+x.relative_to(ROOT).as_posix()+r'}\\',
                    r'{\scriptsize\ttfamily '+digest[:32]+r'\allowbreak{}'+digest[32:]+r'}\\[5pt]'])
    tex.append(r'\bottomrule\end{longtable}')
    (HERE/'paper-evidence-hashes.tex').write_text('\n'.join(tex)+'\n',encoding='utf-8')
    print('Checked 28 unchanged images and 226426 exported windows (835 qualifying); built 2 figures and evidence manifest.')

if __name__=='__main__':main()
