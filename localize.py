"""Generate static English, French and German pages from one English source.

Run after editing dist/index.html, content/translations.json, or shared UI files.
Official credential titles and technology/product names retain their issued names.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import json,re

root=Path(__file__).parent
dist=root/'dist'
translations=json.loads((root/'content/translations.json').read_text(encoding='utf-8'))

def translate(text,lang):
    if lang=='en':return text
    stripped=text.strip()
    pair=translations.get(stripped)
    if pair:return text.replace(stripped,pair[0 if lang=='fr' else 1],1)
    if stripped.startswith('Verify ') and stripped.endswith(' on Credly'):
        title=stripped[len('Verify '):-len(' on Credly')]
        result=f'Vérifier {title} sur Credly' if lang=='fr' else f'{title} auf Credly prüfen'
        return text.replace(stripped,result,1)
    return text

class LocalizedHTML(HTMLParser):
    def __init__(self,lang):super().__init__(convert_charrefs=True);self.lang=lang;self.output=[]
    def handle_decl(self,decl):self.output.append('<!'+decl+'>')
    def handle_starttag(self,tag,attrs):
        updated=[]
        for key,value in attrs:
            if tag=='html' and key=='lang':value=self.lang
            if value is not None and key in ['aria-label','title','content']:value=translate(value,self.lang)
            if key in ['src','href'] and value:
                if value.startswith('assets/') or value in ['interface.css','theme.css','app.js','theme.js','locale-data.js','i18n.js']:value='/'+value
            if key=='href' and value=='__CANONICAL__':value='https://anas-gara-devops.bladedgeode.chatgpt.site'+({'en':'/','fr':'/fr/','de':'/de/'}[self.lang])
            updated.append(' '+key if value is None else ' '+key+'="'+escape(value,quote=True)+'"')
        self.output.append('<'+tag+''.join(updated)+'>')
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        self.output[-1]=self.output[-1][:-1]+'/>'
    def handle_endtag(self,tag):self.output.append('</'+tag+'>')
    def handle_data(self,data):self.output.append(escape(translate(data,self.lang),quote=False))
    def handle_comment(self,data):self.output.append('<!--'+data+'-->')

html=(dist/'index.html').read_text(encoding='utf-8-sig')
if 'id="site-language"' not in html:
    menu='<button class="menu-toggle" aria-label="Open navigation" aria-expanded="false"><span></span><span></span></button>'
    controls='''<div class="header-controls"><label class="sr-only" for="site-language">Language</label><select id="site-language" aria-label="Language"><option value="en" lang="en">EN</option><option value="fr" lang="fr">FR</option><option value="de" lang="de">DE</option></select><button id="theme-toggle" aria-label="Switch to light mode" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☼</span><span class="theme-label">Light</span></button>'''+menu+'</div>'
    assert menu in html
    html=html.replace(menu,controls,1)
if 'src="/theme.js"' not in html and 'src="theme.js"' not in html:
    html=html.replace('<link rel="icon"','<script src="/theme.js"></script><link rel="icon"',1)
if 'theme.css' not in html:
    html=html.replace('<script src="app.js" defer>','<link rel="stylesheet" href="/theme.css"><script src="/locale-data.js" defer></script><script src="/i18n.js" defer></script><script src="/app.js" defer>',1)
    if 'theme.css' not in html:
        html=html.replace('<script src="/app.js" defer>','<link rel="stylesheet" href="/theme.css"><script src="/locale-data.js" defer></script><script src="/i18n.js" defer></script><script src="/app.js" defer>',1)
if 'hreflang=' not in html:
    links=''.join(f'<link rel="alternate" hreflang="{lang}" href="https://anas-gara-devops.bladedgeode.chatgpt.site{path}">' for lang,path in [('en','/'),('fr','/fr/'),('de','/de/'),('x-default','/')])
    html=html.replace('</head>','<link rel="canonical" href="__CANONICAL__">'+links+'</head>')
# Canonical URLs get rebuilt on every run, including when English is the template.
html=re.sub(r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="__CANONICAL__">',html)
for lang,path in [('en',dist/'index.html'),('fr',dist/'fr/index.html'),('de',dist/'de/index.html')]:
    parser=LocalizedHTML(lang);parser.feed(html)
    path.parent.mkdir(exist_ok=True)
    path.write_text(''.join(parser.output),encoding='utf-8')
(dist/'locale-data.js').write_text('window.PortfolioTranslations='+json.dumps(translations,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('Built /, /fr/, /de/ with translated metadata, accessible labels, shared assets, and language/theme controls.')
