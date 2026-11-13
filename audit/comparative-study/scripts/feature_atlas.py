"""Human-selected morphological challenge crops, with disclosed source coordinates."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/comparative-study'
FEATURES=[
 dict(id='candidate',scene='sol3556_585',bbox=[1025,935,1098,1013],label='Sol 3556 candidate',note='Reference; apparent rim + straight upper body + partial rear arc'),
 dict(id='winnipesaukee_shell',scene='winnipesaukee',bbox=[817,583,1035,779],label='Winnipesaukee hollow shell',note='Published geological shell analogue; not a verified straight cylinder'),
 dict(id='point_lake_shell',scene='point_lake',bbox=[265,1010,395,1165],label='Point Lake detached shell',note='Hollow/rim-like natural feature near the outcrop; irregular wall'),
 dict(id='haroldswick_stick',scene='haroldswick',bbox=[726,156,834,270],label='Haroldswick rice-size stick',note='Elongate resistant feature; NASA considers vein-remnant origin possible'),
 dict(id='haroldswick_cluster',scene='haroldswick',bbox=[735,70,975,385],label='Haroldswick stick cluster',note='Context reveals connected/angular forms, not isolated machined rods'),
 dict(id='rounded_block',scene='sol3415_182',bbox=[335,10,690,345],label='Sol 3415 rounded block',note='Rounded corners, flat face, granular/pitted surface; lithology not inferred here'),
 dict(id='naukluft_nodule',scene='naukluft',bbox=[435,315,695,545],label='Naukluft sandstone nodule',note='NASA identifies an approximately 2 cm sandstone nodule with visible grains/lamination'),
 dict(id='shaler_pipe_remnant',scene='shaler_pipe',bbox=[725,590,1245,1040],label='Shaler possible pipe remnant',note='Published alternative: hollow spheroid or sedimentary-pipe remnant; vuggy walls'),
 dict(id='blackthorn_branch',scene='blackthorn',bbox=[440,440,1000,905],label='Blackthorn Salt',note='Complex erosion-resistant form; mechanism analogue, not cylinder match'),
 dict(id='garden_veins',scene='garden_city',bbox=[300,70,980,610],label='Garden City resistant veins',note='Thin linear mineral structures survive loss of softer host rock'),
]
def main():
    manifest=json.loads((OUT/'image-manifest.json').read_text())['images'];lookup={r['id']:r for r in manifest}
    canvas=Image.new('RGB',(1600,330*((len(FEATURES)+3)//4)),'#f6f3ec');draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    for i,f in enumerate(FEATURES):
        im=Image.open(ROOT/lookup[f['scene']]['path']).convert('RGB').crop(f['bbox'])
        # Preview binning is identical for every crop; match only display box, not physical scale.
        im=im.resize((max(1,im.width//2),max(1,im.height//2)),Image.Resampling.BOX)
        im.thumbnail((380,270));scale=min(380/im.width,270/im.height)
        im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
        x=(i%4)*400;y=(i//4)*330
        canvas.paste(im,(x+(400-im.width)//2,y+35))
        draw.text((x+8,y+7),f['label'],font=font,fill='black')
        draw.text((x+8,y+309),f"{f['scene']} | {f['bbox']}",fill='black')
    canvas.save(OUT/'figures/geological-challenge-atlas.png')
    (OUT/'selected-features.json').write_text(json.dumps({'selection':'Deliberate morphological challenge set; not random controls','display':'2x2 bin, independently resized into equal display boxes; not equal physical scale','features':FEATURES},indent=2))
if __name__=='__main__':main()
