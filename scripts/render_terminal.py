# Convierte cada salida real capturada (capturas/txt/*.txt) en una imagen estilo terminal (capturas/img/*.png).
import glob, html, os, re
from playwright.sync_api import sync_playwright

CSS = """
body{margin:0;background:#fff}
.win{display:inline-block;background:#000;border:1px solid #9a9a9a;border-radius:8px 8px 0 0;overflow:hidden;min-width:760px}
.bar{background:#fff;height:32px;display:flex;align-items:center;font:12px 'Segoe UI';color:#000}
.bar svg{margin:0 8px 0 10px}
.ctl{margin-left:auto;display:flex;height:32px;align-items:center;font-size:14px}
.ctl span{width:46px;display:flex;justify-content:center;align-items:center}
.body{display:flex}
.body pre{flex:1}
.sb{width:17px;background:#f0f0f0;display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:5px 0}
pre{margin:0;padding:6px 4px 10px 4px;color:#bfbfbf;font-family:Consolas,'Lucida Console',monospace;font-size:13px;line-height:1.3;white-space:pre}
.u{color:#00bc00}.m{color:#c836c8}.y{color:#bcbc00}.e{color:#e74856}.ok{color:#00bc00}.w{color:#e5e5a0}.c{color:#bfbfbf}
"""
GIT_ICON = """<svg width="18" height="18" viewBox="0 0 100 100">
<g transform="rotate(45 50 50)">
<rect x="14" y="14" width="34" height="34" rx="5" fill="#F47C7C"/>
<rect x="52" y="14" width="34" height="34" rx="5" fill="#7DCB5F"/>
<rect x="52" y="52" width="34" height="34" rx="5" fill="#FFE07A"/>
<rect x="14" y="52" width="34" height="34" rx="5" fill="#7AB2F7"/>
</g>
<g stroke="#fff" stroke-width="6" stroke-linecap="round" fill="#fff">
<line x1="34" y1="12" x2="50" y2="28"/><line x1="49" y1="28" x2="47" y2="70"/><line x1="50" y1="28" x2="71" y2="50"/>
<circle cx="50" cy="28" r="7" stroke="none"/><circle cx="71" cy="50" r="7" stroke="none"/><circle cx="47" cy="70" r="7" stroke="none"/>
</g></svg>"""
def colorize(line):
    s = html.escape(line)
    if line.startswith('$ '):
        cmd, _, com = line[2:].partition('   #')
        out = '<span class="u">jball@JuanFernandoB</span> <span class="m">MINGW64</span> <span class="y">/e/UIS 2/reto poo</span>\n$ ' + html.escape(cmd)
        return out + (f'<span class="c">   #{html.escape(com)}</span>' if com else '')
    return s

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    pg = b.new_page(viewport={"width": 1700, "height": 400}, device_scale_factor=2)
    for f in sorted(glob.glob('capturas/txt/*.txt')):
        lines = open(f, encoding='utf-8').read().rstrip('\n').split('\n')
        body = '\n'.join(colorize(l) for l in lines)
        bar = f"<div class='bar'>{GIT_ICON}MINGW64:/e/UIS 2/reto poo<div class='ctl'><span><svg width='10' height='10'><line x1='0' y1='5.5' x2='10' y2='5.5' stroke='#000' stroke-width='1'/></svg></span><span><svg width='10' height='10'><rect x='0.5' y='0.5' width='9' height='9' rx='1.5' fill='none' stroke='#000' stroke-width='1'/></svg></span><span><svg width='10' height='10'><path d='M0.5 0.5L9.5 9.5M9.5 0.5L0.5 9.5' stroke='#000' stroke-width='1'/></svg></span></div></div>"
        pg.set_content(f"<style>{CSS}</style><div class='win'>{bar}<div class='body'><pre>{body}</pre><div class='sb'><svg width='9' height='6'><path d='M0 6L4.5 0L9 6Z' fill='#a0a0a0'/></svg><svg width='9' height='6'><path d='M0 0L4.5 6L9 0Z' fill='#a0a0a0'/></svg></div></div></div>")
        out = 'capturas/img/' + os.path.basename(f)[:-4] + '.png'
        pg.locator('.win').screenshot(path=out)
    b.close()
print('ok')
