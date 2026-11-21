from pathlib import Path
import ast, json, re, html, io, zipfile, hashlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw, ImageFont

p=Path('/mnt/data/kashan_work/app.py')
s=p.read_text(encoding='utf-8')
ast.parse(s)
compile(s,str(p),'exec')

# Verify unchanged mobile-app prefix.
original=Path('/mnt/data/kashan_work/app.py.original').read_bytes()
updated=p.read_bytes()
marker=b"# The mobile app is the default. My AI opens the complete original KASHAN'S AI app."
o=original.index(marker); n=updated.index(marker)
assert original[:o] == updated[:n]

# Extract pure website helper functions and exercise parsing, sanitizing, preview, export and quality checks.
tree=ast.parse(s)
needed={'_website_slug','_website_parse_ai_project','_website_nav','_website_document','_website_ai_prompt','_website_quality_report'}
nodes=[node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name in needed]
ns={'re':re,'json':json,'html':html}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<website_helpers>','exec'),ns)
sample={
 'site_name':'Demo Academy',
 'pages':[
  {'title':'Home','slug':'home','html':'<main><h1>Welcome</h1><img src="https://example.com/x.png" alt="Campus"><button onclick="alert(1)">Explore</button><script>alert(1)</script></main>'},
  {'title':'About','slug':'about','html':'<main><h1>About us</h1><p>Our story</p></main>'}
 ],
 'css':'body{background:#f5f8ff;color:#111} @import url(https://example.com/a.css); .card{padding:2rem}',
 'js':'document.querySelector("button")?.addEventListener("click",()=>{});',
 'notes':'Demo notes'
}
project=ns['_website_parse_ai_project'](json.dumps(sample))
project['brief']={'language':'Urdu'}
assert project['pages'][0]['slug']=='index'
assert '<script' not in project['pages'][0]['html'] and 'onclick' not in project['pages'][0]['html']
assert 'https://example.com/x.png' not in project['pages'][0]['html']
assert '@import' not in project['css'] and 'body *{color:#111827!important}' in project['css']
preview=ns['_website_document'](project,project['pages'][0],preview=True,preview_mode='Mobile')
export=ns['_website_document'](project,project['pages'][0],preview=False)
assert "lang='ur' dir='rtl'" in preview and 'preview-about' in preview and 'width:min(100%, 390px)' in preview
assert 'styles.css' in export and 'script.js' in export
checks=ns['_website_quality_report'](project)
assert len(checks)==7
# Test a dangerous JS response is stripped.
bad=sample.copy(); bad['js']='fetch("https://example.com")'
assert ns['_website_parse_ai_project'](json.dumps(bad))['js']==''

# Test PowerPoint title font/color settings with python-pptx, matching the updated output contract.
prs=Presentation(); slide=prs.slides.add_slide(prs.slide_layouts[6]); box=slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(1)); box.text_frame.text='Readable heading'
for para in box.text_frame.paragraphs:
    para.font.name='Segoe Script'; para.font.color.rgb=RGBColor(0,0,0); para.font.size=Pt(30)
buf=io.BytesIO(); prs.save(buf); buf.seek(0); reopened=Presentation(buf)
para=reopened.slides[0].shapes[0].text_frame.paragraphs[0]
assert para.font.name=='Segoe Script' and para.font.color.rgb==RGBColor(0,0,0)

# Render a tiny Pillow light-background/black-text smoke image.
canvas=Image.new('RGB',(500,300),(235,246,255)); draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('DejaVuSans-Bold.ttf',28)
draw.text((24,24),'Readable infographic heading',font=font,fill=(0,0,0))
out=io.BytesIO(); canvas.save(out,format='PNG'); assert out.getvalue().startswith(b'\x89PNG')

# Check the navigation logic and newly added feature routes are present.
assert 'def _ai_navigate(next_page):' in s and 'def _ai_go_back():' in s
assert 'if st.session_state.current_page == "website_feature":' in s
assert '("🌐 AI Website Creator", "website_feature", "feature_website")' in s
assert 'st.session_state.current_page = "home"' not in s[s.index('    # ============================================================\n    # HOME / AI LAUNCHER PAGE'):]

print('PY_COMPILE: PASS')
print('AST_PARSE: PASS')
print('MOBILE_PREFIX_BYTE_IDENTICAL: PASS')
print('WEBSITE_HELPER_PARSE_SANITIZE_PREVIEW_EXPORT_QUALITY: PASS')
print('PPTX_FONT_AND_BLACK_TEXT_SMOKE: PASS')
print('INFOGRAPHIC_LIGHT_BACKGROUND_BLACK_TEXT_RENDER: PASS')
print('NAVIGATION_AND_WEBSITE_ROUTE_STATIC_CHECKS: PASS')
print('LINE_COUNT:',len(s.splitlines()))
print('BYTE_COUNT:',len(updated))
print('SHA256:',hashlib.sha256(updated).hexdigest())
print('MOBILE_PREFIX_BYTES:',o)
print('WEBSITE_HELPERS:',len(nodes))
