"""4일차 지도. 실행: python3 tools/maps/day4.py 4일차/index.html"""
import sys
from mapkit import *

MESOPOTAMIA = [(37.1, 40.6), (36.9, 42.6), (35.6, 43.6), (34.2, 44.4), (33.0, 45.2), (31.6, 46.6),
               (30.8, 46.9), (30.7, 46.1), (31.6, 44.9), (32.6, 43.9), (33.6, 42.6), (34.3, 40.9),
               (35.3, 39.8), (36.4, 39.3)]


# ───────────── f8 : 비옥한 초승달과 메소포타미아 ─────────────
def f8():
    P = FULL
    ex, ey = P(30.95, 46.9)
    cx, cy = P(31.95, 35.1)
    # 영역 표시는 강·해안선 아래에 깐다
    under = '\n'.join([
        crescent(P, clip='g4-clip'),
        f'  <path d="{smooth(P, MESOPOTAMIA + MESOPOTAMIA[:1])}Z" fill="var(--warn)" opacity=".13" stroke="var(--warn)" stroke-width="2"/>',
        f'  <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="20" ry="52" fill="var(--accent)" opacity=".16" stroke="var(--accent)" stroke-width="2"/>',
    ])
    s = [base_defs(P, 'g4'), base_use('g4', under=under)]
    s.append(f'  <path d="{smooth(P, CRESCENT)}" fill="none" stroke="var(--accent)" stroke-width="3" stroke-dasharray="10 7" opacity=".75"/>')
    s.append(f'  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="36" fill="none" stroke="var(--blue)" stroke-width="2.5" stroke-dasharray="6 5"/>')
    s += full_water_labels((33.45, 40.9))
    c = ''.join(f'<circle cx="{xy(P, n)[0]:.1f}" cy="{xy(P, n)[1]:.1f}" r="4.5"/>' for n in ['haran', 'nineveh', 'goshen'])
    s.append(f'  <g fill="var(--ink-soft)" stroke="var(--surface)" stroke-width="1.5">{c}</g>')
    s.append(dots(P, ['ur', 'babylon', 'jerusalem']))
    s.append(HALO)
    for n, t, dx, a in [('haran', '하란', 9, None), ('nineveh', '니느웨', 9, None), ('goshen', '애굽', -9, 'end')]:
        x, y = xy(P, n); s.append(text(x + dx, y + 5, t, 13, 400, 'var(--ink-soft)', a))
    s += label(P, 'ur', ['우르'], dx=-11, dy=5, anchor='end')
    s += label(P, 'babylon', ['바벨론'])
    s += label(P, 'jerusalem', ['예루살렘'], dx=-11, dy=5, anchor='end')
    x, y = P(35.75, 41.0); s.append(text(x, y, '메소포타미아', 15, 800, 'var(--warn)'))
    s.append(text(x, y + 18, '"두 강 사이의 땅"', 12, 400, 'var(--ink-soft)'))
    s.append(text(ex + 40, ey - 10, '에덴?', 13, 700, 'var(--blue)'))
    s.append(text(ex + 40, ey + 6, '추정만 가능', 11.5, 400, 'var(--ink-soft)'))
    x, y = P(32.15, 35.75)
    s.append(text(x, y, '가나안', 14, 800, 'var(--accent)'))
    s.append(text(x, y + 17, '약속의 땅', 11.5, 400, 'var(--ink-soft)'))
    s.append(text(x, y + 32, '기근이 먼저 오는 땅', 11.5, 400, 'var(--ink-soft)'))
    x, y = P(37.55, 37.3); s.append(text(x, y, '비옥한 초승달', 13, 700, 'var(--accent)'))
    s.append('  </g>')
    s.append('''  <g transform="translate(14,440)" font-size="12">
    <rect x="0" y="0" width="200" height="98" rx="8" fill="var(--surface)" stroke="var(--line)" opacity=".95"/>
    <path d="M14,20 L44,20" stroke="var(--accent)" stroke-width="3" stroke-dasharray="8 5"/><text x="54" y="24" fill="var(--ink)">비옥한 초승달</text>
    <ellipse cx="29" cy="44" rx="15" ry="8" fill="var(--warn)" opacity=".2" stroke="var(--warn)" stroke-width="1.5"/><text x="54" y="48" fill="var(--ink)">문명이 시작된 곳</text>
    <circle cx="29" cy="68" r="9" fill="none" stroke="var(--blue)" stroke-width="2" stroke-dasharray="4 3"/><text x="54" y="72" fill="var(--ink)">에덴 추정 지역</text>
    <ellipse cx="29" cy="88" rx="15" ry="7" fill="var(--accent)" opacity=".2" stroke="var(--accent)" stroke-width="1.5"/><text x="54" y="92" fill="var(--ink)">아브라함이 간 땅</text>
  </g>''')
    s.append(scalebar(P, 200, 560, 528))
    s.append(compass())
    return wrap(s)


MAPS = dict(f8=f8)


if __name__ == '__main__':
    path = sys.argv[1]
    html = open(path, encoding='utf-8').read()
    for mid, fn in MAPS.items():
        html = splice(html, mid, fn())
    open(path, 'w', encoding='utf-8').write(html)
