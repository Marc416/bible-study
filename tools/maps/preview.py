"""지도를 한 장씩 라이트·다크로 캡처한다(헤드리스 Chrome).
실행: python3 tools/maps/preview.py 2일차/index.html <출력 폴더>
"""
import re, subprocess, sys
G = sys.argv[2]
h = open(sys.argv[1], encoding='utf-8').read()
style = re.search(r'<style>.*?</style>', h, re.S).group(0)
figs = re.findall(r'<figure>\s*<svg viewBox="0 0 900 560".*?</figure>', h, re.S)
# 공유 defs(m0, m2)가 있어야 다른 지도가 그려지므로 전부 넣고 앞의 것은 숨기지 않고 위치만 옮긴다
for i, theme in [(i, t) for i in range(len(figs)) for t in ('light', 'dark')]:
    body = ''.join(f'<div style="{"" if j == i else "position:absolute;left:-5000px"}">{f}</div>' for j, f in enumerate(figs))
    open(f'{G}/p.html', 'w').write(f'<!doctype html><html data-theme="{theme}"><meta charset=utf-8>{style}<body style="width:900px;margin:0;padding:0">{body}</body></html>')
    subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--window-size=900,640', f'--screenshot={G}/shot{i}_{theme}.png', f'file://{G}/p.html'], capture_output=True)
print(len(figs))
