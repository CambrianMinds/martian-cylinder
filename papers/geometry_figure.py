"""Reproducible vector explanation of the paper's geometric constraints."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
FRONT, REAR, DORSAL = '#19804b', '#af7f00', '#0085a6'
INK, SOIL = '#202934', '#e5ddd0'


def build_geometry_figure():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                         'pdf.fonttype': 42})
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.7))
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

    body(axes[0])
    axes[0].set_title('(a) Shared section and tangent', loc='left', weight='bold', pad=10)
    body(axes[1], buried=True)
    axes[1].set_title('(b) Burial can mimic narrowing', loc='left', weight='bold', pad=10)
    fig.legend(handles=[Line2D([0], [0], color=INK, lw=2, label='Visible model boundary'),
                        Line2D([0], [0], color=INK, ls='--', lw=1.2,
                               label='Concealed / continued geometry')],
               loc='lower center', ncol=2, frameon=False, fontsize=12)
    fig.subplots_adjust(left=.025, right=.985, top=.86, bottom=.18, wspace=.14)
    out = HERE/'figures/geometry-constraints.pdf'
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(out.with_suffix('.png'), dpi=150)
    plt.close(fig)
    return out


if __name__ == '__main__':
    print(build_geometry_figure())
