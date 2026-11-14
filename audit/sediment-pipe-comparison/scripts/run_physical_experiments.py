"""Observed-target 3D fits, burial checks, and labeled synthetic stress tests."""
from pathlib import Path
import json
import sys
import numpy as np
from scipy.optimize import least_squares, brentq
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import physical_model as model
import target_benchmark as benchmark

BASE = Path(__file__).resolve().parents[1]


def score(parameters, data, depth_sign=-1, intrinsic_ratio=1):
    residuals = model.residuals(parameters, data, depth_sign, intrinsic_ratio)
    diameter = 2*parameters[2]
    return dict(rms_px={name:benchmark.rms(values) for name,values in residuals.items()},
                total_rms_px=benchmark.rms(np.concatenate(list(residuals.values()))),
                normalized_rms=benchmark.rms(np.concatenate(list(residuals.values())))/diameter,
                residuals_px={name:values.tolist() for name,values in residuals.items()})


def validation(data):
    masks = {name:np.ones(len(group['xy']),dtype=bool) for name,group in data.items()}
    parameters, diagnostics = model.fit(data, masks)
    result = {'parameters':parameters.tolist(), 'independent_parameters':6,
              'fixed_range_m':model.RANGE, 'diagnostics':diagnostics,
              'full_fit':score(parameters,data), 'folds':[]}
    predicted = {name:np.empty(len(group['xy'])) for name,group in data.items()}
    for fold in range(5):
        tests = {name:np.array_split(np.arange(len(group['xy'])),5)[fold]
                 for name,group in data.items()}
        masks = {name:benchmark.split_masks(len(group['xy']),tests[name])
                 for name,group in data.items()}
        fitted, diagnostic = model.fit(data,masks)
        residuals = model.residuals(fitted,data)
        record = {'fold':fold,'parameters':fitted.tolist(),'diagnostics':diagnostic,'features':{}}
        for name, indices in tests.items():
            predicted[name][indices] = residuals[name][indices]
            record['features'][name] = {'test_indices':indices.tolist(),
                                       'training_indices':np.flatnonzero(masks[name]).tolist(),
                                       'test_residuals_px':residuals[name][indices].tolist()}
        result['folds'].append(record)
    result['guarded_prediction'] = {'rms_px':{name:benchmark.rms(values) for name,values in predicted.items()},
                                     'total_rms_px':benchmark.rms(np.concatenate(list(predicted.values())))}
    all_masks = {name:np.ones(len(group['xy']),dtype=bool) for name,group in data.items()}
    alternatives = []
    for depth_sign, ratio in [(1,1),(-1,.9),(-1,1.1)]:
        fitted, diagnostic = model.fit(data,all_masks,depth_sign=depth_sign,intrinsic_ratio=ratio)
        alternatives.append(dict(depth_sign=depth_sign,intrinsic_cross_section_ratio=ratio,
                                 parameters=fitted.tolist(),diagnostics=diagnostic,
                                 **score(fitted,data,depth_sign,ratio)))
    result['alternative_geometries'] = alternatives
    # The physically collinear rear registration has one length parameter.
    front_masks = {name:np.ones(len(group['xy']),dtype=bool) if name!='rear'
                   else np.zeros(len(group['xy']),dtype=bool) for name,group in data.items()}
    free = [0,1,2,4,5]
    initial = np.array([1068.3,985.95,20,40.86,np.radians(31.2),np.radians(38)])
    def front_objective(values):
        trial = initial.copy();trial[free] = values
        residuals = model.residuals(trial,data)
        return np.concatenate([residuals[name]/data[name]['sigma'] for name in ['front','dorsal']])
    front_fit = least_squares(front_objective,initial[free],bounds=(model.LOW[free],model.HIGH[free]))
    frozen = initial.copy();frozen[free] = front_fit.x
    anchors = np.arange(0,24,4); test = np.setdiff1d(np.arange(24),anchors)
    def registration(values):
        trial=frozen.copy();trial[3]=values[0]
        return model.residuals(trial,data)['rear'][anchors]
    length_fit=least_squares(registration,[40.86],bounds=([15],[75]))
    frozen[3]=length_fit.x[0];rear=model.residuals(frozen,data)['rear']
    result['one_parameter_rear_registration'] = dict(parameters=frozen.tolist(),
        anchor_indices=anchors.tolist(), test_indices=test.tolist(),
        test_rms_px=benchmark.rms(rear[test]),
        scope='Distinct stronger test. Front/dorsal determine five parameters. Six rear anchors fit length only.')
    return parameters,result


def synthetic_coordinates(parameters, data, taper=0, bend=0, modulation=0, terminal_tilt_deg=0):
    """Project actual parametric surfaces with analytic/numerical tangency."""
    g = model.geometry(parameters)
    phase_grid = np.linspace(0,2*np.pi,2048,endpoint=False)
    def radial(phase):
        return np.cos(phase)[...,None]*g['first']+np.sin(phase)[...,None]*g['second']
    tilt = np.tan(np.radians(terminal_tilt_deg))
    output = {}
    for name, fraction in [('front',0),('rear',1)]:
        radius = g['radius']*(1-taper*fraction)
        along = -fraction*g['length']-radius*tilt*np.cos(phase_grid)*(name=='front')
        points = g['front']+along[:,None]*g['axis']+radius*radial(phase_grid)
        projected = model.project(points)
        _,indices=cKDTree(projected).query(data[name]['xy'])
        output[name] = {'xy':projected[indices],'sigma':np.ones(len(indices))}
    # Each side-boundary point satisfies the tangent-plane viewing condition.
    source_axis=np.array([np.cos(parameters[4]),np.sin(parameters[4])])
    front_pixel=model.project(g['front']);rear_pixel=model.project(g['rear'])
    fractions=np.clip((data['dorsal']['xy']-front_pixel)@source_axis /
                      ((rear_pixel-front_pixel)@source_axis),0,1)
    dorsal=[]
    for fraction in fractions:
        along=-fraction*g['length']
        center=g['front']+along*g['axis']+bend*g['radius']*np.sin(np.pi*fraction)*g['first']
        center_derivative=g['axis']-bend*g['radius']*np.pi/g['length']*np.cos(np.pi*fraction)*g['first']
        radius=g['radius']*(1-taper*fraction+modulation*np.sin(2*np.pi*fraction))
        radius_derivative=g['radius']/g['length']*(taper-2*np.pi*modulation*np.cos(2*np.pi*fraction))
        def condition(phase):
            normal_radial=radial(np.asarray(phase))
            surface=center+radius*normal_radial
            transverse=-np.sin(phase)*g['first']+np.cos(phase)*g['second']
            normal=np.cross(transverse,center_derivative+radius_derivative*normal_radial)
            return np.dot(surface-model.CAMERA['C'],normal)
        phases=np.linspace(0,2*np.pi,181)
        values=[condition(phase) for phase in phases]
        roots=[brentq(condition,phases[i],phases[i+1]) for i in range(len(phases)-1)
               if values[i]*values[i+1]<0]
        candidates=model.project(np.array([center+radius*radial(np.asarray(phase)) for phase in roots]))
        image_normal=np.array([-np.sin(parameters[4]),np.cos(parameters[4])])
        dorsal.append(candidates[np.argmin(candidates@image_normal)])
    output['dorsal']={'xy':np.array(dorsal),'sigma':np.ones(len(dorsal))}
    return output


def render(parameters, plane, supersampling=3, blur=.7, depth_sign=-1, foreground_bank=None):
    """Ray trace a finite solid segment plus the fitted planar soil surface."""
    g=model.geometry(parameters, depth_sign)
    xs=np.arange(1018,1095,1/supersampling)
    ys=np.arange(937,1005,1/supersampling)
    xx,yy=np.meshgrid(xs,ys);xy=np.column_stack([xx.ravel(),yy.ravel()])
    rays=model.unit(np.cross(model.CAMERA['V']-xy[:,1,None]*model.CAMERA['A'],
                              model.CAMERA['H']-xy[:,0,None]*model.CAMERA['A']))
    rays[rays@model.CAMERA['A']<0]*=-1
    for _ in range(4):
        error=model.project(model.CAMERA['C']+rays)-xy
        rays=model.unit(rays-error[:,0,None]*model.INTRINSICS['h_unit']/model.INTRINSICS['hs_px']
                             -error[:,1,None]*model.INTRINSICS['v_unit']/model.INTRINSICS['vs_px'])
    origin=model.CAMERA['C']-g['front']
    perpendicular=rays-(rays@g['axis'])[:,None]*g['axis']
    off=origin-origin@g['axis']*g['axis']
    aa=np.sum(perpendicular**2,axis=1);bb=2*perpendicular@off
    cc=off@off-g['radius']**2;disc=bb*bb-4*aa*cc
    depth=np.full(len(rays),np.inf)
    normals=np.zeros_like(rays)
    for sign in [-1,1]:
        candidate=(-bb+sign*np.sqrt(np.maximum(disc,0)))/(2*aa)
        points=model.CAMERA['C']+candidate[:,None]*rays
        axial=(points-g['front'])@g['axis']
        valid=(disc>=0)&(axial<=0)&(axial>=-g['length'])&(candidate>0)&(candidate<depth)
        depth[valid]=candidate[valid]
        normal=points-g['front']-axial[:,None]*g['axis']
        normals[valid]=model.unit(normal[valid])
    for center,normal in [(g['front'],g['axis']),(g['rear'],-g['axis'])]:
        distance=(center-model.CAMERA['C'])@normal/(rays@normal)
        points=model.CAMERA['C']+distance[:,None]*rays
        valid=(np.linalg.norm(points-center,axis=1)<=g['radius'])&(distance>0)&(distance<depth)
        depth[valid]=distance[valid];normals[valid]=normal
    soil_normal=np.array(plane['normal']);soil_distance=(plane['offset_m']-model.CAMERA['C']@soil_normal)/(rays@soil_normal)
    object_visible=np.isfinite(depth)&((soil_distance<0)|(depth<soil_distance))
    if foreground_bank is not None:
        # A finite 3D foreground patch with a straight top edge, specified by two
        # camera rays. Its depth is an explicit exploratory scene assumption.
        edge_rays=model.rays(np.array(foreground_bank['edge_endpoints_xy']))
        edge_plane=model.unit(np.cross(edge_rays[0],edge_rays[1]))
        test_ray=model.cahvor_pixel_to_ray(1035,990,model.CAMERA)
        edge_plane*=np.sign(edge_plane@test_ray)
        bank_depth=foreground_bank['depth_m']/(rays@g['ray'])
        covered=(rays@edge_plane>0)&(bank_depth>0)&(bank_depth<depth)
        object_visible=np.isfinite(depth)&~covered
    camera_metadata=json.loads((model.ROOT/'independent-reconstruction/step2_camera_geometry.json').read_text())
    light=np.array(camera_metadata['solar_illumination_geometry']['sun_direction_rover_nav'])
    image=np.full(len(rays),.22)
    image[object_visible]=.03+.8*np.maximum(normals[object_visible]@light,0)
    image=image.reshape(len(ys),len(xs))
    image=gaussian_filter(image,blur*supersampling)
    image=image.reshape(68,supersampling,77,supersampling).mean(axis=(1,3))
    return image,object_visible.reshape(len(ys),len(xs))[::supersampling,::supersampling]


def burial_visibility(parameters, result, soil_xy, data):
    records=[]
    fig,axes=plt.subplots(2,3,figsize=(14,9))
    for index,(depth_sign,root_sign) in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)]):
        fitted=np.array(parameters if depth_sign==-1 else result['alternative_geometries'][0]['parameters'])
        plane=model.fit_burial_plane(fitted,soil_xy,depth_sign,root_sign)
        image,mask=render(fitted,plane,depth_sign=depth_sign)
        support={}
        for name,group in data.items():
            pixel=np.rint(group['xy']-[1018,937]).astype(int)
            support[name]=int(sum(mask[max(0,y-1):y+2,max(0,x-1):x+2].any() for x,y in pixel))
        records.append(dict(depth_sign=depth_sign,intersection_root=root_sign,
                            soil_contact_rms_px=plane['rms_px'],
                            approximate_pixel_support_within_1px=support,
                            scope='Pixel support alone does not establish terminal-edge visibility.',plane=plane))
        ax=axes.flat[index];ax.imshow(image,cmap='gray',extent=(1018,1095,1005,937),vmin=.1,vmax=.85)
        ax.set_title(f'SYNTHETIC plane / depth {depth_sign}, root {root_sign}',fontsize=11)
    center=soil_xy.mean(axis=0);_,_,vh=np.linalg.svd(soil_xy-center)
    direction=vh[0];along=(soil_xy-center)@direction
    endpoints=np.array([center+along.min()*direction,center+along.max()*direction])
    normal=vh[-1];distance=(soil_xy-center)@normal
    bank={'edge_endpoints_xy':endpoints.tolist(),'depth_m':3.90,
          'edge_rms_px':benchmark.rms(distance),'fitted_edge_parameters':2,
          'assumed_depth_parameters':1,
          'scope':'Exploratory finite foreground bank patch. Its distance and slope are not measured terrain properties.'}
    image,mask=render(parameters,result['burial_plane'],foreground_bank=bank)
    axes.flat[4].imshow(image,cmap='gray',extent=(1018,1095,1005,937),vmin=.1,vmax=.85)
    axes.flat[4].set_title('SYNTHETIC / finite foreground soil bank',fontsize=11)
    axes.flat[5].axis('off');axes.flat[5].text(0,.9,
        'Plane intersection and a finite foreground bank\nare different scene assumptions.\n\nThe bank edge uses 2 fitted image-line parameters.\nIts 3.90 m depth is assumed.\n\nPixel support is an initial visibility diagnostic.\nPhotometry and cast shadows are not fitted.',va='top',fontsize=11)
    fig.tight_layout();fig.savefig(BASE/'figures/burial-visibility-cases.png',dpi=150);plt.close(fig)
    return {'plane_cases':records,'foreground_bank':bank}


def main():
    data,_,observed=benchmark.load_data()
    for name,group in data.items():
        (BASE/'boundary-inventory'/('target-'+name+'.json')).write_text(json.dumps(
            {'source':'existing target extraction, unchanged', 'feature':name,
             'xy':group['xy'].tolist(),'sigma':group['sigma'].tolist()},indent=2)+'\n')
    parameters,result=validation(data)
    s3=json.loads((model.ROOT/'independent-reconstruction/step3_features.json').read_text())
    soil_xy=np.array([[point['x_erf'],point['y_erf']] for point in s3['ventral_stations']])
    plane=model.fit_burial_plane(parameters,soil_xy)
    result['burial_plane']=plane
    result['burial_visibility']=burial_visibility(parameters,result,soil_xy,data)
    g=model.geometry(parameters)
    result['physical_dimensions_at_fixed_range']={'diameter_mm':2*g['radius']*1000,
        'length_mm':g['length']*1000,'axis_tilt_to_view_deg':float(np.degrees(parameters[5]))}
    # Check the conic approximation against dense, genuinely projected curves.
    curves,dorsal=model.projected_boundaries(parameters)
    result['conic_approximation_rms_px']={}
    for name,curve in curves.items():
        center,a,b,angle=model.ellipse_from_curve(curve)
        residual=model.point_to_ellipse_orth_dist(curve[:,0],curve[:,1],*center,a,b,angle)
        result['conic_approximation_rms_px'][name]=benchmark.rms(residual)
    synthetic=[]
    cases=[('ideal',{}),('taper_5pct',{'taper':.05}),('taper_20pct',{'taper':.2}),
           ('centerline_bend_5pct_radius',{'bend':.05}),('centerline_bend_20pct_radius',{'bend':.2}),
           ('radius_modulation_2pct',{'modulation':.02}),('radius_modulation_10pct',{'modulation':.1}),
           ('front_terminal_tilt_10deg',{'terminal_tilt_deg':10})]
    for name,changes in cases:
        generated=synthetic_coordinates(parameters,data,**changes)
        masks={key:np.ones(len(group['xy']),dtype=bool) for key,group in generated.items()}
        fit,diagnostic=model.fit(generated,masks,weighted=False)
        synthetic.append({'id':name,'domain':'synthetic projected geometry','parameters':changes,
                          'fit_parameters':fit.tolist(),'diagnostics':diagnostic,**score(fit,generated)})
        (BASE/'boundary-inventory'/('synthetic-'+name+'.json')).write_text(json.dumps(
            {key:{'xy':group['xy'].tolist(),'sigma':group['sigma'].tolist()}
             for key,group in generated.items()},indent=2)+'\n')
    result['scope']='Observed target coordinates fitted to a specified 3D surface. Geological production of that surface is a conditional scenario.'
    (BASE/'results/physical-model.json').write_text(json.dumps(result,indent=2)+'\n')
    (BASE/'results/synthetic-controls.json').write_text(json.dumps(synthetic,indent=2)+'\n')
    rendered,mask=render(parameters,plane,foreground_bank=result['burial_visibility']['foreground_bank'])
    fig,axes=plt.subplots(1,3,figsize=(15,5))
    low,high=np.percentile(observed[937:1005,1018:1095],[2,98])
    for ax in axes[:2]:
        ax.imshow(observed,cmap='gray',vmin=low,vmax=high)
        ax.set(xlim=(1018,1095),ylim=(1005,937))
    for name,color in [('front','#48e296'),('rear','#ffd453'),('dorsal','#38c9ef')]:
        xy=data[name]['xy'];axes[0].scatter(*xy.T,s=10,c=color,label=name)
    for name,curve in curves.items():axes[1].plot(*curve.T,lw=1.3,label=name)
    axes[1].plot(*dorsal.T,c='cyan',lw=1.3)
    curve=np.array(plane['curve_xy']);axes[1].scatter(*curve.T,s=.2,c='#e590ff')
    axes[0].set_title('Observed target / retained stations');axes[0].legend(fontsize=8)
    axes[1].set_title('Observed image / projected 3D surface')
    axes[2].imshow(rendered,cmap='gray',extent=(1018,1095,1005,937),vmin=.1,vmax=.85)
    axes[2].set_title('SYNTHETIC / segment and foreground bank')
    fig.tight_layout();fig.savefig(BASE/'figures/physical-model-comparison.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    names=list(data);axes[0].bar(names,[result['full_fit']['rms_px'][n] for n in names],label='Observed target fit')
    axes[0].plot(names,[result['guarded_prediction']['rms_px'][n] for n in names],'o-',c='orange',label='Guarded prediction')
    axes[0].set(ylabel='Native-pixel RMS',title='Observed target / 3D model');axes[0].legend()
    axes[1].barh([x['id'] for x in synthetic],[x['total_rms_px'] for x in synthetic])
    axes[1].set(xlabel='Constant-cylinder fit RMS (px)',title='SYNTHETIC geometry stress tests')
    fig.tight_layout();fig.savefig(BASE/'figures/prediction-and-synthetic-sensitivity.png',dpi=160);plt.close(fig)
    print('3D full fit:',result['full_fit']['total_rms_px'])
    print('3D guarded:',result['guarded_prediction']['total_rms_px'])
    print('Planar soil-contact RMS:',plane['rms_px'],'failed rays',plane['nonintersecting_soil_rays'])
    print('Physical length-only registration:',result['one_parameter_rear_registration']['test_rms_px'])


if __name__ == '__main__':
    main()
