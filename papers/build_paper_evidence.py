"""Build paper evidence from retained files; no image acquisition or resampling."""
from pathlib import Path
import csv, gzip, hashlib, importlib.util, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from native_image_figures import build_native_figures

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PRED = ROOT/'audit/predictive-validation'
COMP = ROOT/'audit/comparative-study'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))

def canonical_text_sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()

def matches_recorded_text_hash(path, expected):
    raw = path.read_bytes()
    lf = raw.replace(b'\r\n', b'\n')
    return expected in {hashlib.sha256(raw).hexdigest(), hashlib.sha256(lf).hexdigest(),
                        hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest()}

def verify(p):
    for name, digest in p['input_hashes'].items():
        assert matches_recorded_text_hash(ROOT/'independent-reconstruction'/name,digest), name
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
    sys.path.insert(0,str(ROOT/'independent-reconstruction/scripts'))
    sys.path.insert(0,str(ROOT/'independent-reconstruction'))
    import step3_feature_extraction
    step3_feature_extraction.DATA_DIR=str(ROOT/'data')
    spec=importlib.util.spec_from_file_location('paper_validation',PRED/'run_validation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data,_,im=module.load_data()
    strict=read(ROOT/'independent-reconstruction/step9_joint_model.json')['joint_models']['M1_Strict_Right_Circular_Cylinder_6DOF']
    build_native_figures(data,im,strict,module.point_to_ellipse_orth_dist)
    out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':13,'pdf.fonttype':42})
    low,high=np.percentile(im[932:1007,1014:1104],[2,98])
    def image(ax):
        ax.imshow(im,cmap='gray',interpolation='nearest',vmin=low,vmax=high)
        ax.set(xlim=(1014,1104),ylim=(1007,932),xlabel='Native x (px)',ylabel='Native y (px)')
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
    finite=read(ROOT/'audit/sediment-pipe-comparison/results/m4-reevaluation.json')['finite_generator_refits']
    for name,prefix in [('cylinder','FiniteCylinder'),('frustum','FiniteFrustum')]:
        values[prefix+'FitRMS']=finite[name]['full_rms_px']
        values[prefix+'GuardedRMS']=finite[name]['guarded_rms_px']
    values['FiniteFrustumScale']=finite['frustum']['parameters'][6]
    (HERE/'paper-analysis-values.tex').write_text('% Generated from predictive results JSON.\n'+''.join(
        f'\\newcommand{{\\{k}}}{{{v:.4f}}}\n' for k,v in values.items()),encoding='utf-8')
    figures(p)
    paths=[HERE/'martian-cylinder-technical-paper.tex',Path(__file__).resolve(),
           HERE/'native_image_figures.py',HERE/'verify_journal_revision.py',
           HERE/'requirements.txt',HERE/'run_comparison_checks.py',HERE/'comparison-checks.txt',
           HERE/'figure-provenance.json',HERE/'figure-determinism.json',HERE/'journal-revision-baseline.json',
           HERE/'journal-predictive-replay.json',
           HERE/'figures/joint-m1-overlay.pdf',HERE/'figures/joint-m1-overlay.png',
           ROOT/'data/3556MR1025170721700585C00_DRXX.IMG',ROOT/'data/3556MR1025170721700585C00_DRXX.LBL',
           ROOT/'audit/shading-sampling-review/check_sampling.py',
           ROOT/'audit/shading-sampling-review/results.json',
           PRED/'run_validation.py',PRED/'protocol.md',PRED/'results.json',PRED/'report.md',
           COMP/'protocol.md',COMP/'comparison-summary.json',COMP/'image-manifest.json',
           COMP/'report.md',COMP/'requirements.txt',COMP/'artifact-checksums.json',
           ROOT/'audit/priority-review/report.md',HERE/'paper-analysis-values.tex',
           HERE/'figures/target-boundaries.pdf',HERE/'figures/rear-prediction.pdf']
    paths+=sorted((COMP/'scripts').glob('*.py'))
    paths+=sorted((ROOT/'independent-reconstruction/scripts').glob('*.py'))
    paths+=sorted((ROOT/'independent-reconstruction').glob('*.py'))
    pipe=ROOT/'audit/sediment-pipe-comparison'
    paths+=[pipe/x for x in ['m4-reevaluation.md','protocol.md','image-manifest.csv',
        'results/m4-reevaluation.json','results/physical-model.json','results/physical-frustum.json',
        'results/observed-controls.json','scripts/physical_model.py','scripts/reevaluate_m4.py',
        'scripts/target_benchmark.py','boundary-inventory/screening.json']]
    paths+=sorted((pipe/'boundary-inventory').glob('target-*.json'))
    paths+=sorted((pipe/'sources/images').glob('*'))
    paths+=[ROOT/'independent-reconstruction'/n for n in ['step1_provenance.json','step2_camera_geometry.json',
            'step3_features.json','step4_endface_models.json','step5_3d_interpretations.json',
            'step8_pebble_and_rear_terminus.json','step9_joint_model.json','measurements.json']]
    manifest=dict(revision_date='2026-11-13',reconstruction_base_commit='90fbf8f89ac2634a9dbd2b27f81fc80d68b9943c',
        revision_parent_commit=read(HERE/'journal-revision-baseline.json')['starting_commit'],
        branch='paper/nov13-journal-revision',
        scope='November 13 journal revision from verified local source. Figure-only transformations recorded separately.',
        validation=dict(images_checked=28,control_windows=226426,qualifying_windows=835),
        sha256={x.relative_to(ROOT).as_posix():sha(x) for x in paths},
        canonical_lf_sha256={x.relative_to(ROOT).as_posix():canonical_text_sha(x) for x in paths
                            if x.suffix in {'.py','.json','.tex','.md','.txt'}},
        hash_policy='Raw SHA-256 records the observed bytes. Canonical LF digests permit only text newline conversion on checkout. PDS image and label bytes remain exact.')
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
    print('Checked 28 unchanged images and 226426 exported windows (835 qualifying); built locator, M1 overlay and rear prediction.')

if __name__=='__main__':main()
