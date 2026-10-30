from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

root=Path(__file__).parent
assets=root/'dist'/'assets'
ink=HexColor('#262c27'); accent=HexColor('#b34c30'); gray=HexColor('#62675d')
styles={
 'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=29,leading=34,textColor=ink,spaceAfter=5),
 'role':ParagraphStyle('role',fontName='Helvetica',fontSize=12,leading=17,textColor=accent,spaceAfter=8),
 'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=8.3,leading=13,textColor=gray,spaceAfter=13),
 'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=accent,spaceBefore=14,spaceAfter=7,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=8.6,leading=13,textColor=ink,spaceAfter=6),
 'job':ParagraphStyle('job',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=ink,spaceBefore=7,spaceAfter=4,keepWithNext=True),
 'meta':ParagraphStyle('meta',fontName='Helvetica-Oblique',fontSize=8,leading=12,textColor=gray,spaceAfter=5,keepWithNext=True),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=8.4,leading=12.7,textColor=ink,spaceAfter=3,leftIndent=10,firstLineIndent=-8),
}
def clean(t):
 t=re.sub(r'\\textbf\{([^{}]*)\}',r'<b>\1</b>',t)
 t=re.sub(r'\\textit\{([^{}]*)\}',r'<i>\1</i>',t)
 for a,b in [(r'\%', '%'),(r'\&','&amp;'),(r'\textbullet{}',' | '),(r'\quad',' '),(r'\textbf',''),(r'\normalsize','')]: t=t.replace(a,b)
 t=re.sub(r'<(?=[ =0-9])','&lt;',t.replace('--','-'))
 return re.sub(r'\s+',' ',t).strip()
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(HexColor('#d9dbd0'));canvas.line(42,35,A4[0]-42,35);canvas.setFont('Helvetica',7);canvas.setFillColor(gray);canvas.drawString(42,23,'ANAS GARA / DEVOPS ENGINEER');canvas.drawRightString(A4[0]-42,23,str(doc.page));canvas.restoreState()
for lang in ['EN','FR']:
 text=(assets/f'Anas-Gara-CV-{lang}.tex').read_text(encoding='utf-8')
 body=text.split(r'\section{',1)[1]
 email='anasgara7@gmail.com'
 story=[Paragraph('Anas Gara',styles['name']),Paragraph('DevOps Engineer | Cloud, CI/CD & Infrastructure as Code' if lang=='EN' else 'Ingénieur DevOps | Cloud, CI/CD & Infrastructure as Code',styles['role']),Paragraph(f'<a href="mailto:{email}" color="#62675d">{email}</a> · Ariana, Tunis<br/><a href="https://github.com/AnasGara" color="#62675d">github.com/AnasGara</a> · <a href="https://linkedin.com/in/anasgara" color="#62675d">linkedin.com/in/anasgara</a>',styles['contact'])]
 for section in re.split(r'\\section\{',body):
  title,content=section.split('}',1)
  if (lang=='EN' and title=='Technical Skills') or (lang=='FR' and title=='Projets Techniques Majeurs'):
   story.extend([PageBreak(),Paragraph('Anas Gara',styles['name']),Paragraph('Technical background & qualifications' if lang=='EN' else 'Projets, compétences & qualifications',styles['role'])])
  story.append(Paragraph(clean(title).upper(),styles['section']))
  pattern=r'\\begin\{twocolentry\}(.*?)\\end\{twocolentry\}|\\begin\{onecolentry\}(.*?)\\end\{onecolentry\}'
  blocks=list(re.finditer(pattern,content,re.S))
  for m in blocks:
   if m.group(1):
    chunk=m.group(1)
    bold=re.findall(r'\\textbf\{([^{}]*)\}',chunk)
    italics=re.findall(r'\\textit\{([^{}]*)\}',chunk)
    # Preserve title, organization, location and dates without layout macros.
    if bold: story.append(Paragraph(clean(' - '.join(bold)),styles['job']))
    remaining=re.sub(r'\\textbf\{[^{}]*\}','',chunk)
    remaining=re.sub(r'\\textit\{([^{}]*)\}',r'\1',remaining)
    remaining=re.sub(r'\\(?:vspace|kern)\{[^{}]*\}','',remaining)
    remaining=remaining.replace('{','').replace('}','').strip()
    meta=clean(remaining)
    if meta: story.append(Paragraph(meta,styles['meta']))
   else:
    chunk=m.group(2)
    if r'\item' in chunk:
     for item in chunk.split(r'\item')[1:]:
      item=re.sub(r'\\(?:end|begin)\{[^}]*\}','',item)
      story.append(Paragraph('• '+clean(item),styles['bullet']))
    else:
     story.append(Paragraph(clean(chunk),styles['body']))
  if not blocks:
   # Education blocks use a compact inline date argument; covered above.
   pass
 output=assets/f'Anas-Gara-CV-{lang}.pdf'
 doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=48,title=f'Anas Gara - CV ({lang})',author='Anas Gara')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 pdf=PdfReader(str(output));print(f'{output.name}: {len(pdf.pages)} pages')
 for page in pdf.pages:
  extracted=page.extract_text()
  assert 'Anas' in extracted or len(extracted)>100
  assert '\\textbf' not in extracted and '\\begin' not in extracted, extracted
