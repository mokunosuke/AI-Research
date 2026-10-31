from pathlib import Path
import re, html
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

ROOT = Path(r'A:\AI\Research')
MD = ROOT / 'Reports' / '2026-10-17_MiniMax_Report.md'
OUT = ROOT / 'Reports' / '2026-10-17_MiniMax_Report.pdf'
font = r'C:\Windows\Fonts\meiryo.ttc'
pdfmetrics.registerFont(TTFont('Meiryo', font, subfontIndex=0))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='JPTitle', parent=styles['Title'], fontName='Meiryo', fontSize=20, leading=27, textColor=colors.HexColor('#183153'), spaceAfter=10))
styles.add(ParagraphStyle(name='JPH1', parent=styles['Heading1'], fontName='Meiryo', fontSize=15, leading=20, textColor=colors.HexColor('#173d68'), spaceBefore=13, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name='JPH2', parent=styles['Heading2'], fontName='Meiryo', fontSize=12, leading=17, textColor=colors.HexColor('#275d83'), spaceBefore=10, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name='JPBody', parent=styles['BodyText'], fontName='Meiryo', fontSize=9.2, leading=14.2, spaceAfter=5, wordWrap='CJK'))
styles.add(ParagraphStyle(name='JPBullet', parent=styles['BodyText'], fontName='Meiryo', fontSize=9.1, leading=13.8, leftIndent=12, firstLineIndent=-8, spaceAfter=3, wordWrap='CJK'))
styles.add(ParagraphStyle(name='JPTable', parent=styles['BodyText'], fontName='Meiryo', fontSize=7.3, leading=10, spaceAfter=0, wordWrap='CJK'))
styles.add(ParagraphStyle(name='JPNote', parent=styles['BodyText'], fontName='Meiryo', fontSize=8.4, leading=12, textColor=colors.HexColor('#45546a'), backColor=colors.HexColor('#f0f4f8'), borderPadding=7, spaceAfter=8, wordWrap='CJK'))

def rich(s):
    s=s.strip()
    s=html.escape(s, quote=False)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#1769aa">\1</link>', s)
    s=re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s=re.sub(r'`([^`]+)`', r'<font name="Meiryo" color="#6b3e75">\1</font>', s)
    s=s.replace('  ', ' ')
    return s

class Diagram(Flowable):
    def __init__(self, kind, width=174*mm, height=None):
        super().__init__(); self.kind=kind; self.width=width; self.height=68*mm if kind==1 else (55*mm if kind==2 else 57*mm)
    def draw(self):
        c=self.canv; sx=self.width/174
        sy=self.height/(68 if self.kind==1 else (55 if self.kind==2 else 57))
        c.saveState(); c.scale(sx,sy)
        c.setFillColor(colors.HexColor('#f5f7fb')); c.roundRect(0,0,174, self.height/mm,4,fill=1,stroke=0)
        def label(x,y,text,size=7.5,color='#172033',bold=False):
            c.setFillColor(colors.HexColor(color)); c.setFont('Meiryo',size/2.83); c.drawString(x,y,text)
        def box(x,y,w,h,title,lines,fill,stroke):
            c.setFillColor(colors.HexColor(fill)); c.setStrokeColor(colors.HexColor(stroke)); c.setLineWidth(1); c.roundRect(x,y,w,h,3,fill=1,stroke=1)
            label(x+4,y+h-8,title,8.3,'#173d68',True)
            for i,t in enumerate(lines): label(x+4,y+h-16-i*8,t,6.1)
        def arrow(x1,y1,x2,y2):
            c.setStrokeColor(colors.HexColor('#596780')); c.setLineWidth(1.3); c.line(x1,y1,x2,y2)
            c.setFillColor(colors.HexColor('#596780')); c.line(x2,y2,x2-3,y2+2); c.line(x2,y2,x2-3,y2-2)
        if self.kind==1:
            label(5, self.height/mm-10,'RTX 3060 12GB: モデル配置とオフロード',10,'#183153',True)
            box(5,14,47,38,'RTX 3060',['利用可能VRAM 約11.6 GiB','重みを一括常駐できない','#低解像度・短尺から'], '#e8f1ff','#6a92d6')
            box(64,14,55,38,'RAM / SSD',['INT8 DiT 約19.5 GiB','テキスト encoder 約25 GiB','RAMへオフロード'], '#fff4df','#d7a449')
            box(131,14,38,38,'ComfyUI',['低解像度で試作','Turbo LoRA','必要区間を本番生成'], '#e7f6ee','#62a27c')
            arrow(54,33,62,33); arrow(121,33,129,33)
        elif self.kind==2:
            label(5,self.height/mm-10,'低VRAM: 試作から本番へ',10,'#183153',True)
            xs=[5,48,91,134]; titles=['① 試作','② 条件固定','③ 選別','④ 本番']; lines=[['608×352程度','短いクリップ'],['seed固定','1項目ずつ変更'],['映像・音声確認','失敗区間だけ再生成'],['解像度・尺を上げる','編集で接続']]
            for x,t,ls,fc,sc in zip(xs,titles,lines,['#e8f1ff','#fff4df','#e7f6ee','#f3eafa'],['#6a92d6','#d7a449','#62a27c','#9b77b5']): box(x,12,35,31,t,ls,fc,sc)
            for x in [41,84,127]: arrow(x,27,x+5,27)
            label(5,5,'注意: Turbo LoRAのsteps/CFG条件を守り、画質を確認してから採用。',6.2,'#45546a')
        else:
            label(5,self.height/mm-10,'長尺化: チャンクをつないで継続',10,'#183153',True)
            box(5,17,47,30,'チャンク A',['人物・動作・音声','末尾latentを保存'],'#e8f1ff','#6a92d6')
            box(64,17,47,30,'チャンク B',['前区間をガイド','映像/音声を継続'],'#fff4df','#d7a449')
            box(123,17,46,30,'編集・確認',['境界を再生確認','問題区間のみ再生成'],'#e7f6ee','#62a27c')
            arrow(54,32,62,32); arrow(113,32,121,32)
            label(5,8,'限界: 境界で人物・背景・動作や音声がずれる場合がある。完全な連続性は保証されない。',6.2,'#45546a')
        c.restoreState()

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#d8e0ea')); canvas.line(18*mm,14*mm,192*mm,14*mm)
    canvas.setFont('Meiryo',7.5); canvas.setFillColor(colors.HexColor('#66758a'))
    canvas.drawString(18*mm,9*mm,'MiniMax Research Report · 2026-10-17')
    canvas.drawRightString(192*mm,9*mm,str(doc.page)); canvas.restoreState()

lines=MD.read_text(encoding='utf-8-sig').splitlines()
story=[]; i=0
while i<len(lines):
    line=lines[i].strip()
    if not line: i+=1; continue
    if line.startswith('# '): story.append(Paragraph(rich(line[2:]),styles['JPTitle'])); i+=1; continue
    if line.startswith('> '): story.append(Paragraph(rich(line[2:]),styles['JPNote'])); i+=1; continue
    if line.startswith('![最初') or line.startswith('!['):
        kind=1 if '3060-memory' in line else (2 if 'low-vram' in line else 3)
        story += [Diagram(kind),Spacer(1,5)]; i+=1; continue
    if line.startswith('## '): story.append(Paragraph(rich(line[3:]),styles['JPH1'])); i+=1; continue
    if line.startswith('### '): story.append(Paragraph(rich(line[4:]),styles['JPH2'])); i+=1; continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            raw=lines[i].strip().strip('|')
            cells=[x.strip() for x in raw.split('|')]
            if not all(re.fullmatch(r':?-{3,}:?',x.replace(' ','')) for x in cells): rows.append([Paragraph(rich(x),styles['JPTable']) for x in cells])
            i+=1
        if rows:
            n=max(len(r) for r in rows); widths=[174*mm/n]*n
            tbl=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce8f4')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#173d68')),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#b9c7d6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f7f9fc')])]))
            story.extend([tbl,Spacer(1,6)])
        continue
    if line.startswith('- '): story.append(Paragraph('• '+rich(line[2:]),styles['JPBullet'])); i+=1; continue
    if re.match(r'^\d+\.\s',line):
        m=re.match(r'^(\d+)\.\s(.*)',line); story.append(Paragraph(m.group(1)+'. '+rich(m.group(2)),styles['JPBullet'])); i+=1; continue
    if line == '---': story.append(Spacer(1,6)); i+=1; continue
    story.append(Paragraph(rich(line),styles['JPBody'])); i+=1

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=17*mm,bottomMargin=21*mm,title='MiniMax Research Report 2026-10-17',author='Research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT, OUT.stat().st_size)
