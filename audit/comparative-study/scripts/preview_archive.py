from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
files=list((ROOT/'archive/legacy_data/survey_images').glob('*.jpg'))
out=Image.new('RGB',(1200,350*((len(files)+2)//3)), 'white')
draw=ImageDraw.Draw(out)
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB'); im.thumbnail((390,310))
    x=(i%3)*400;y=(i//3)*350
    out.paste(im,(x,y+25));draw.text((x+5,y+5),p.name,fill='black')
out.save(ROOT/'audit/comparative-study/figures/archive-scenes.jpg')
