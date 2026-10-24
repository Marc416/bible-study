"""5일차 지도. 실행: python3 tools/maps/day5.py 5일차/index.html"""
import sys
from mapkit import *


# ───────────── f7 : 아라랏에서 애굽까지 ─────────────
def f7():
    P = NORTH
    s = [base_defs(P, 'g5'), base_use('g5', under=crescent(P, clip='g5-clip'))]
    s.append(SEA_TXT)
    for p, t, a in [((34.3, 31.0), '지중해', None), ((29.95, 49.0), '페르시아만', 'middle')]:
        x, y = P(*p); s.append(text(x, y, t, 14.5 if t == '지중해' else 12.5, 400, 'var(--ink-soft)', a))
    s.append('  </g>')
    s.append(LAND_TXT)
    for p, t in [((29.95, 31.45), '나일강'), ((34.95, 40.05), '유프라테스강'), ((35.15, 43.65), '티그리스강'),
                 ((38.65, 42.0), '반 호수')]:
        x, y = P(*p); s.append(text(x, y, t, 12.5, 400, 'var(--ink-soft)'))
    x, y = P(35.95, 41.5); s.append(text(x, y, '비옥한 초승달', 12.5, 700, 'var(--accent)'))
    s.append('  </g>')
    s.append('''  <defs>
    <marker id="a7w" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--warn)"/></marker>
    <marker id="a7a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)"/></marker>
    <marker id="a7b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--blue)"/></marker>
  </defs>''')
    # 아라랏산 기호
    ax, ay = P(*PL['ararat'])
    s.append(f'  <path d="M{ax - 13:.1f},{ay + 9:.1f} L{ax:.1f},{ay - 12:.1f} L{ax + 13:.1f},{ay + 9:.1f} Z" fill="var(--ink-soft)" opacity=".75"/>')
    r1 = [(39.45, 44.1), (38.2, 42.9), (37.0, 42.75), (35.6, 43.5), (34.0, 44.0), (32.8, 44.35)]
    r2 = [(31.1, 45.95), (31.3, 45.3), (32.4, 44.35), (33.4, 43.3), (34.45, 40.9), (35.33, 40.14), (35.95, 39.05), (36.6, 39.03)]
    r3 = [(36.75, 38.85), (36.2, 37.15), (35.13, 36.75), (33.51, 36.29), (32.4, 35.45)]
    r4 = [(31.15, 34.7), (31.0, 33.9), (30.75, 32.3)]
    s.append('  <g fill="none" stroke-width="3.5" stroke-linecap="round">')
    s.append(f'    <path d="{smooth(P, r1)}" stroke="var(--warn)" stroke-dasharray="9 6" marker-end="url(#a7w)"/>')
    s.append(f'    <path d="{smooth(P, r2)}" stroke="var(--accent)" marker-end="url(#a7a)"/>')
    s.append(f'    <path d="{smooth(P, r3)}" stroke="var(--accent)" marker-end="url(#a7a)"/>')
    s.append(f'    <path d="{smooth(P, r4)}" stroke="var(--blue)" marker-end="url(#a7b)"/>')
    s.append('  </g>')
    c = ''.join(f'<circle cx="{xy(P, n)[0]:.1f}" cy="{xy(P, n)[1]:.1f}" r="4.5"/>' for n in ['nineveh', 'damascus'])
    s.append(f'  <g fill="var(--ink-soft)" stroke="var(--surface)" stroke-width="1.5">{c}</g>')
    s.append(dots(P, ['ur', 'haran', 'shechem', 'jerusalem', 'beersheba']))
    bx, by = P(*PL['babylon']); gx, gy = P(*PL['goshen'])
    s.append(f'  <circle cx="{bx:.1f}" cy="{by:.1f}" r="7.5" fill="var(--warn)" stroke="var(--surface)" stroke-width="2"/>')
    s.append(f'  <circle cx="{gx:.1f}" cy="{gy:.1f}" r="6.5" fill="var(--blue)" stroke="var(--surface)" stroke-width="2"/>')
    s.append(HALO)
    s.append(text(ax + 16, ay - 2, '아라랏산', 14))
    s.append(text(ax + 16, ay + 15, '방주가 머문 곳 (창 8:4)', 11.5, 400, 'var(--ink-soft)'))
    s += label(P, 'nineveh', ['니느웨'], dx=9)
    s[-1] = s[-1].replace('font-size="14.5" font-weight="700" fill="var(--ink)"', 'font-size="13" font-weight="400" fill="var(--ink-soft)"')
    s += label(P, 'damascus', ['다메섹'], dx=9)
    s[-1] = s[-1].replace('font-size="14.5" font-weight="700" fill="var(--ink)"', 'font-size="13" font-weight="400" fill="var(--ink-soft)"')
    s.append(text(bx + 13, by + 5, '바벨 (시날 평지)', 14, 800, 'var(--warn)'))
    s.append(text(bx + 13, by + 22, '니므롯의 나라 · 바벨탑', 11.5, 400, 'var(--ink-soft)'))
    s += label(P, 'ur', ['갈대아 우르', '아브라함의 고향'])
    s += label(P, 'haran', ['하란', '데라가 죽은 곳 · 밧단아람'])
    s += label(P, 'shechem', ['세겜'], dx=-11, dy=0, anchor='end')
    s += label(P, 'jerusalem', ['예루살렘(모리아)'], dx=-11, dy=12, anchor='end')
    s += label(P, 'beersheba', ['브엘세바'], dx=10, dy=12)
    s.append(text(gx - 11, gy - 8, '애굽 고센', 14, 700, 'var(--blue)', 'end'))
    s.append(text(gx - 11, gy + 10, '야곱 가족 70명', 11.5, 400, 'var(--ink-soft)', 'end'))
    s.append('  </g>')
    # 경로 번호
    s.append('  <g font-size="13" font-weight="800" paint-order="stroke" stroke="var(--surface)" stroke-width="4" stroke-linejoin="round">')
    for p, n, col in [((37.6, 43.15), '①', 'warn'), ((33.9, 42.1), '②', 'accent'), ((34.6, 36.0), '③', 'accent'),
                      ((31.25, 33.6), '④', 'blue')]:
        x, y = P(*p); s.append(f'    <text x="{x:.0f}" y="{y:.0f}" fill="var(--{col})">{n}</text>')
    s.append('  </g>')
    s.append('''  <g transform="translate(14,14)" font-size="12">
    <rect x="0" y="0" width="240" height="122" rx="8" fill="var(--surface)" stroke="var(--line)" opacity=".95"/>
    <path d="M14,22 L44,22" stroke="var(--warn)" stroke-width="3" stroke-dasharray="8 5"/><text x="54" y="26" fill="var(--ink)">① 홍수 뒤 사람들 (11:2)</text>
    <path d="M14,48 L44,48" stroke="var(--accent)" stroke-width="3"/><text x="54" y="52" fill="var(--ink)">②③ 아브라함 (11:31, 12:5)</text>
    <path d="M14,74 L44,74" stroke="var(--blue)" stroke-width="3"/><text x="54" y="78" fill="var(--ink)">④ 야곱 가족 (46장)</text>
    <circle cx="29" cy="100" r="6" fill="var(--warn)"/><text x="54" y="104" fill="var(--ink)">세상 나라의 시작</text>
  </g>''')
    s.append(scalebar(P, 200, 560, 528))
    s.append(compass())
    return wrap(s)


MAPS = dict(f7=f7)


if __name__ == '__main__':
    path = sys.argv[1]
    html = open(path, encoding='utf-8').read()
    for mid, fn in MAPS.items():
        html = splice(html, mid, fn())
    open(path, 'w', encoding='utf-8').write(html)
