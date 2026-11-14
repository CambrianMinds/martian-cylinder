"""Reproducible vector explanation of the paper's geometric constraints."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
FRONT, REAR, DORSAL = '#19804b', '#af7f00', '#0085a6'
INK, SOIL, RED = '#202934', '#e5ddd0', '#b24839'


def build_geometry_figure():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                         'pdf.fonttype': 42})
    fig = plt.figure(figsize=(12, 9.2), facecolor='white')
    grid = fig.add_gridspec(3, 2, width_ratios=[1.65, 1],
                           height_ratios=[1, 1, 1.13], hspace=.56, wspace=.15)
    angle = np.linspace(0, 2*np.pi, 1000)
    centers, a, b = [1.1, 4.5], .78, .48

    def body(ax, buried=False):
        ax.set(xlim=(.15, 5.4), ylim=(-1.14, 1.38))
        ax.set_aspect('equal'); ax.axis('off')
        ground = lambda x: .35 - .26*(x-1.1)
        if buried:
            x = np.linspace(.15, 5.4, 300)
            ax.fill_between(x, -1.14, ground(x), color=SOIL, zorder=0)
            ax.plot(x, ground(x), color='#8b7660', lw=1.3)
        for cx, color in zip(centers, [REAR, FRONT]):
            x, y = cx+b*np.cos(angle), a*np.sin(angle)
            visible = y >= (ground(x) if buried else 0)
            ax.plot(x, y, color=color, ls=(0, (4, 3)), lw=1.1, alpha=.75)
            ax.plot(np.where(visible, x, np.nan),
                    np.where(visible, y, np.nan), color=color, lw=2.4)
        ax.plot(centers, [a, a], color=DORSAL, lw=2.7)
        ax.plot(centers, [-a, -a], color='#7b8791', ls=(0, (4, 3)), lw=1)
        ax.plot([.5, 5.05], [0, 0], color='#7b8791', ls='-.', lw=.9)
        ax.scatter(centers, [0, 0], s=14, color=INK, zorder=5)
        if not buried:
            ax.text(1.1, 1.05, 'Rear section', color=REAR, ha='center')
            ax.text(4.5, 1.05, 'Front section', color=FRONT, ha='center')
            ax.text(2.8, -.31, 'Common axis', color='#53616c', ha='center')
        else:
            ax.annotate('Soil contact', xy=(2.65, ground(2.65)),
                        xytext=(3.2, -.98), ha='center', color='#705c48',
                        arrowprops={'arrowstyle': '->', 'color': '#705c48'})

    def note(ax, title, text):
        ax.axis('off')
        ax.text(0, .91, title, color=INK, weight='bold', fontsize=14,
                transform=ax.transAxes, va='top')
        ax.text(0, .66, text, color=INK, fontsize=14,
                transform=ax.transAxes, va='top', linespacing=1.35)

    ax = fig.add_subplot(grid[0, 0]); body(ax)
    ax.set_title('(a) One common-section model', loc='left', weight='bold', pad=9)
    note(fig.add_subplot(grid[0, 1]), 'Shared constraints',
         'Same end size and shape\nCollinear centers\nOne upper tangent; no free offset')
    ax = fig.add_subplot(grid[1, 0]); body(ax, buried=True)
    ax.set_title('(b) Burial can mimic narrowing', loc='left', weight='bold', pad=9)
    note(fig.add_subplot(grid[1, 1]), 'Changing exposure',
         'More of the rear is concealed.\nThe section stays the same size;\nthe soil contact is not a second\nsilhouette generator.')

    models = json.loads((HERE.parent/'independent-reconstruction/step9_joint_model.json').read_text())
    p = models['joint_models']['M4_Tapered_Conical_Frustum_Coupled_8DOF']['params']
    a, b, r = p['a'], p['b'], p['r_dorsal']
    m = (1-p['scale_ratio_s'])*r/p['L_proj']
    tangent_r = np.sqrt(a*a+m*m*b*b)
    tangent_u = -m*b*b/tangent_r
    u = np.linspace(-6.5, 2.1, 1000)
    ellipse = a*np.sqrt(1-(u/b)**2)
    ax = fig.add_subplot(grid[2, 0])
    ax.plot(u, ellipse, color=FRONT, lw=2.4, label='M4 front ellipse')
    ax.plot(u, r+m*u, color=RED, lw=2, ls='--', label='M4 proposed boundary')
    ax.plot(u, tangent_r+m*u, color=DORSAL, lw=1.7, label='Required parallel tangent')
    ax.scatter([tangent_u], [tangent_r+m*tangent_u], color=DORSAL, s=25, zorder=5)
    ax.annotate('', xy=(tangent_u, tangent_r+m*tangent_u),
                xytext=(tangent_u, r+m*tangent_u),
                arrowprops={'arrowstyle': '<->', 'color': INK, 'lw': 1})
    ax.set(xlim=(-6.5, 2.1), ylim=(17.8, 19.95),
           xlabel='Axial coordinate u (px)', ylabel='Outward coordinate -v (px)')
    ax.set_title('(c) M4 line cuts its own end ellipse', loc='left', weight='bold', pad=12)
    ax.grid(alpha=.15); ax.spines[['top', 'right']].set_visible(False)
    ax.legend(loc='lower right', fontsize=11, framealpha=.95)
    note(fig.add_subplot(grid[2, 1]), 'Actual fitted M4 geometry',
         '$r_{\\mathrm{tangent}}^2=a^2+m^2b^2$\n'
         f'Proposed r: {r:.6f} px\n'
         f'Required r: {tangent_r:.6f} px\n'
         f'Difference: {tangent_r-r:.6f} px\n'
         'Close-up uses unequal axis scales.')
    fig.legend(handles=[Line2D([0], [0], color=INK, lw=2, label='Visible model boundary (a, b)'),
                        Line2D([0], [0], color=INK, ls='--', lw=1.2,
                               label='Concealed / continued geometry (a, b)')],
               loc='lower center', ncol=2, frameon=False, fontsize=12)
    fig.subplots_adjust(left=.075, right=.98, top=.95, bottom=.12)
    out = HERE/'figures/geometry-constraints.pdf'
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(out.with_suffix('.png'), dpi=150)
    plt.close(fig)
    return out


if __name__ == '__main__':
    print(build_geometry_figure())
