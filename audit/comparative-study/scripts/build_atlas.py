from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/comparative-study'
def main():
    rows=[r for r in json.loads((OUT/'image-manifest.json').read_text())['images'] if 'path' in r]
    for chunk in range(0,len(rows),9):
        canvas=Image.new('RGB',(1500,1200),'#f7f5ef'); d=ImageDraw.Draw(canvas)
        for j,row in enumerate(rows[chunk:chunk+9]):
            im=Image.open(ROOT/row['path']).convert('RGB');im.thumbnail((490,350))
            x=j%3*500;y=j//3*400
            canvas.paste(im,(x+(500-im.width)//2,y+35))
            d.text((x+8,y+8),f"{row['id']} | {row['width']} x {row['height']}",fill='black')
        canvas.save(OUT/'figures'/f'scenes-{chunk//9+1:02d}.jpg',quality=94)
if __name__=='__main__':main()
