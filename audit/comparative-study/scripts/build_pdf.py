"""Render the complete Markdown report as a shareable, linked PDF."""
from pathlib import Path
import re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/comparative-study'
def rich(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<link href="{m[2]}" color="#236c78">{m[1]}</link>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Courier" size="8">\1</font>',s)
    return s

def main():
    pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
    pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
    styles=getSampleStyleSheet()
    for name in ['Normal','BodyText','Title','Heading1','Heading2','Heading3']:
        styles[name].fontName='Arial'
    styles['BodyText'].fontSize=9.5;styles['BodyText'].leading=13.2;styles['BodyText'].spaceAfter=7
    styles['Title'].fontSize=24;styles['Title'].leading=29;styles['Title'].textColor=colors.HexColor('#225765')
    styles['Heading1'].fontName='ArialBold';styles['Heading1'].fontSize=15;styles['Heading1'].leading=19;styles['Heading1'].spaceBefore=15
    styles['Heading2'].fontName='ArialBold';styles['Heading2'].fontSize=11;styles['Heading2'].leading=15
    small=ParagraphStyle('cell',parent=styles['BodyText'],fontSize=7.4,leading=10,spaceAfter=0)
    story=[];lines=(OUT/'report.md').read_text(encoding='utf-8').splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]);i+=1
            story.append(Paragraph('<font name="Courier" size="7">'+'<br/>'.join(html.escape(x) for x in code)+'</font>',styles['BodyText']));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',x) for x in row):rows.append(row)
                i+=1
            n=len(rows[0]);widths={3:[105,183,183],4:[151,105,110,105],5:[140,66,90,100,75]}[n]
            data=[[Paragraph(rich(x),small) for x in row] for row in rows]
            table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9eb')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#39737e')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d2d7da')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([table,Spacer(1,9)]);continue
        if line.startswith('!['):
            rel=re.search(r'\]\(([^)]+)\)',line)[1];p=OUT/rel
            with PILImage.open(p) as im:w,h=im.size
            factor=min(471/w,570/h)
            story.extend([Spacer(1,6),Image(str(p),width=w*factor,height=h*factor),Spacer(1,6)]);i+=1;continue
        if line.startswith('# '):story.extend([Paragraph(rich(line[2:]),styles['Title']),Spacer(1,13)]);i+=1;continue
        if line.startswith('## '):story.append(Paragraph(rich(line[3:]),styles['Heading1']));i+=1;continue
        if line.startswith('### '):story.append(Paragraph(rich(line[4:]),styles['Heading2']));i+=1;continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','|','![','```')):
            para.append(lines[i].strip());i+=1
        story.append(Paragraph(rich(' '.join(para)),styles['BodyText']))
    def footer(canvas,doc):
        canvas.setFont('Arial',8);canvas.setFillColor(colors.HexColor('#667076'))
        canvas.drawString(47,27,'Curiosity geological comparison | 13 November 2026')
        canvas.drawRightString(565,27,str(doc.page))
    doc=SimpleDocTemplate(str(OUT/'curiosity-geological-comparison.pdf'),pagesize=(612,792),rightMargin=47,leftMargin=47,topMargin=40,bottomMargin=44,title='Curiosity geological comparison study',author='Repository analysis')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

if __name__=='__main__':main()
