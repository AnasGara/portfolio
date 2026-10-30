"""Render the bilingual LaTeX CV sources as selectable, two-page PDFs."""
from pathlib import Path
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader

ROOT = Path(__file__).parent
ASSETS = ROOT / 'dist' / 'assets'
INK, BLUE, GRAY = map(HexColor, ('#17232e', '#004f90', '#52606c'))
WIDTH = letter[0] - 84
STYLES = {
    'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=INK, spaceAfter=3),
    'role': ParagraphStyle('role', fontName='Helvetica', fontSize=11, leading=15, textColor=BLUE, spaceAfter=6),
    'contact': ParagraphStyle('contact', fontName='Helvetica', fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=5),
    'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLUE, spaceBefore=11, spaceAfter=3, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.4, leading=13, textColor=INK, spaceAfter=5),
    'entry': ParagraphStyle('entry', fontName='Helvetica', fontSize=9.4, leading=12.5, textColor=INK),
    'meta': ParagraphStyle('meta', fontName='Helvetica-Oblique', fontSize=8.3, leading=11.5, textColor=GRAY, alignment=TA_RIGHT),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.3, leading=12.6, textColor=INK, spaceAfter=3, leftIndent=11, firstLineIndent=-9),
    'continuation': ParagraphStyle('continuation', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=INK, spaceAfter=1),
}


def clean(text):
    """Convert the source vocabulary to escaped ReportLab markup."""
    text = text.replace(r'\textbullet{}', ' | ').replace(r'\quad', ' ')
    text = text.replace(r'\%', '%').replace(r'\&', '&').replace('--', '-')
    text = re.sub(r'\\(?:end|begin)\{[^}]*\}', '', text)
    text = escape(text)
    text = re.sub(r'\\textbf\{([^{}]*)\}', r'<b>\1</b>', text)
    text = re.sub(r'\\textit\{([^{}]*)\}', r'<i>\1</i>', text)
    return re.sub(r'\s+', ' ', text).strip()


def braced(text):
    """Split a balanced leading LaTeX argument from the remaining text."""
    text = text.lstrip()
    if not text.startswith('{'):
        raise ValueError('Expected a braced entry argument')
    depth = 0
    for index, char in enumerate(text):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[1:index], text[index + 1:].strip()
    raise ValueError('Unbalanced entry argument')


def entry(chunk):
    right, left = braced(chunk)
    left = '<br/>'.join(clean(line) for line in left.splitlines() if line.strip())
    right_parts = re.findall(r'\\textit\{([^{}]*)\}', right)
    right = '<br/>'.join(clean(part) for part in right_parts) or clean(right)
    table = Table([[Paragraph(left, STYLES['entry']), Paragraph(right, STYLES['meta'])]], colWidths=[WIDTH - 140, 140], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 10),
        ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return table


def content_blocks(content):
    pattern = r'\\begin\{twocolentry\}(.*?)\\end\{twocolentry\}|\\begin\{onecolentry\}(.*?)\\end\{onecolentry\}'
    blocks = []
    for match in re.finditer(pattern, content, re.S):
        if match.group(1):
            blocks.append(entry(match.group(1)))
        else:
            chunk = match.group(2)
            if r'\item' in chunk:
                bullets = [Paragraph('• ' + clean(item), STYLES['bullet']) for item in chunk.split(r'\item')[1:]]
                if blocks and isinstance(blocks[-1], Table):
                    blocks[-1] = KeepTogether([blocks[-1], bullets.pop(0)])
                blocks.extend(bullets)
                blocks.append(Spacer(1, 3))
            else:
                blocks.append(Paragraph(clean(chunk), STYLES['body']))
    return blocks


def footer(lang):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(HexColor('#ccd5dd'))
        canvas.line(42, 30, letter[0] - 42, 30)
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(GRAY)
        canvas.drawString(42, 18, 'Anas GARA | DevOps Engineer')
        label = f'Page {doc.page} of 2' if lang == 'EN' else f'Page {doc.page} sur 2'
        canvas.drawRightString(letter[0] - 42, 18, label)
        canvas.restoreState()
    return draw


def generate(lang):
    source = (ASSETS / f'Anas-Gara-CV-{lang}.tex').read_text(encoding='utf-8')
    role = 'DevOps Engineer | AWS Certified Solutions Architect' if lang == 'EN' else 'Ingénieur DevOps | Certifié AWS Solutions Architect'
    contact = '<a href="mailto:anasgara7@gmail.com" color="#004f90">anasgara7@gmail.com</a> | Tunis, ' + ('Tunisia' if lang == 'EN' else 'Tunisie') + '<br/><a href="https://linkedin.com/in/anasgara" color="#004f90">linkedin.com/in/anasgara</a> | <a href="https://github.com/AnasGara" color="#004f90">github.com/AnasGara</a>'
    story = [Paragraph('Anas GARA', STYLES['name']), Paragraph(role, STYLES['role']), Paragraph(contact, STYLES['contact'])]
    for section in re.split(r'\\section\{', source)[1:]:
        title, content = section.split('}', 1)
        if title in ('Technical Projects', 'Projets Techniques'):
            story.extend([PageBreak(), Paragraph('Anas GARA', STYLES['continuation'])])
        story.append(Paragraph(clean(title), STYLES['section']))
        rule = HRFlowable(width='100%', thickness=0.6, color=BLUE, spaceAfter=6)
        rule.keepWithNext = True
        story.append(rule)
        story.extend(content_blocks(content))
    output = ASSETS / f'Anas-Gara-CV-{lang}.pdf'
    doc = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=42, leftMargin=42, topMargin=30, bottomMargin=42, title=f'Anas Gara - CV ({lang})', author='Anas Gara')
    doc.build(story, onFirstPage=footer(lang), onLaterPages=footer(lang))
    pdf = PdfReader(output)
    assert len(pdf.pages) == 2, f'{lang}: expected 2 pages, got {len(pdf.pages)}'
    text = '\n'.join(page.extract_text() for page in pdf.pages)
    for required in ('anasgara7@gmail.com', 'A1.2', 'DBaaS', 'Terraform', 'Zipkin'):
        assert required in text, f'{lang}: missing {required}'
    assert '\\textbf' not in text and '\\begin' not in text
    print(f'{output.name}: {len(pdf.pages)} pages')


if __name__ == '__main__':
    for language in ('EN', 'FR'):
        generate(language)
