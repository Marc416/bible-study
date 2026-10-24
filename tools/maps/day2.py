"""2일차 지도. 실행: python3 tools/maps/day2.py 2일차/index.html"""
import sys
from mapkit import *


# ───────────── m0 : 전체 지도 ─────────────
def m0():
    P = FULL
    s = [base_defs(P, 'ne'), base_use('ne'), crescent(P, accent=True)]
    s += full_water_labels()
    s.append(dots(P, ['ur', 'haran', 'nineveh', 'babylon', 'shechem', 'jerusalem', 'kadesh', 'sinai', 'goshen']))
    s.append(HALO)
    s += label(P, 'ur', ['우르'])
    s += label(P, 'haran', ['하란'])
    s += label(P, 'nineveh', ['니느웨 · 앗수르'])
    s += label(P, 'babylon', ['바벨론'])
    s += label(P, 'shechem', ['가나안(약속의 땅)'], dx=-11, dy=0, anchor='end')
    s += label(P, 'jerusalem', ['예루살렘'], dx=-11, dy=12, anchor='end')
    s += label(P, 'kadesh', ['가데스바네아'], dx=-11, dy=6, anchor='end')
    s += label(P, 'sinai', ['시내산'])
    s += label(P, 'goshen', ['애굽(고센)'], dx=-11, anchor='end')
    s.append('  </g>')
    s.append('''  <g transform="translate(300,516)">
    <rect x="0" y="0" width="372" height="30" rx="6" fill="var(--surface)" opacity=".9"/>
    <rect x="10" y="8" width="15" height="15" rx="3" fill="var(--accent)" opacity=".25"/>
    <text x="33" y="20" font-size="12.5" fill="var(--ink-soft)">비옥한 초승달 — 물이 있어 사람이 모여 살던 띠 모양의 땅</text>
  </g>''')
    s.append(scalebar(P, 200, 730, 528))
    s.append(compass())
    return wrap(s)


# ───────────── m1 : 아브라함 ─────────────
def m1():
    P = FULL
    s = [base_use('ne'), crescent(P)]
    s += full_water_labels((33.45, 40.9))
    s.append('  <defs><marker id="ar1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--warn)"/></marker></defs>')
    routes = [
        [(31.05, 45.95), (31.3, 45.3), (32.4, 44.35), (33.4, 43.3), (34.45, 40.9), (35.33, 40.14), (35.95, 39.05), (36.6, 39.03)],
        [(36.75, 38.85), (36.2, 37.15), (35.13, 36.75), (33.51, 36.29), (32.4, 35.45)],
        [(32.05, 35.2), (31.53, 35.1), (31.25, 34.75), (31.05, 33.9), (30.8, 32.35)],
    ]
    s.append('  <g fill="none" stroke="var(--warn)" stroke-width="4" stroke-dasharray="10 6" stroke-linecap="round">')
    s += [f'    <path d="{smooth(P, r)}" marker-end="url(#ar1)"/>' for r in routes]
    s.append('  </g>')
    s.append(dots(P, ['ur', 'haran', 'shechem', 'goshen']))
    s.append(HALO)
    s += label(P, 'ur', ['① 우르', '고향. 우상 만들어 팔던 곳'])
    s += label(P, 'haran', ['② 하란', '아버지 데라가 죽은 곳'])
    s += label(P, 'shechem', ['③ 가나안 (세겜)', '약속의 땅 · 아브라함·이삭·야곱'], dx=-12, dy=-6, anchor='end')
    s += label(P, 'goshen', ['④ 애굽 고센', '70명 가족 이주 → 창세기 끝'], dx=-100, dy=28)
    dx_, dy_ = P(33.51, 36.29)
    s.append(f'    <circle cx="{dx_:.1f}" cy="{dy_:.1f}" r="3.5" fill="var(--ink-soft)" stroke="var(--surface)" stroke-width="1.5"/>')
    s.append(text(dx_ + 8, dy_ + 4, '다메섹', 12, 400, 'var(--ink-soft)'))
    s.append('  </g>')
    s.append(scalebar(P, 200, 560, 528))
    s.append(compass())
    return wrap(s)


# ───────────── m2 : 출애굽 ─────────────
def m2():
    P = ZOOM
    s = [base_defs(P, 'sn'), base_use('sn', river_w=2.6)]
    s += zoom_water_labels()
    s.append('''  <defs>
    <marker id="ar2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--warn)"/></marker>
    <marker id="ar3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--blue)"/></marker>
  </defs>''')
    r1 = [(30.62, 32.0), (30.35, 32.6), (29.95, 33.55), (29.6, 34.6), (29.1, 35.0), (28.5, 35.1)]
    r2 = [(28.62, 33.9), (29.05, 33.75), (29.7, 33.35), (30.3, 32.6), (30.58, 32.05)]
    r3 = [(30.6, 31.95), (30.55, 32.15), (30.05, 32.5), (29.55, 32.78), (29.05, 33.1), (28.75, 33.5), (28.58, 33.9)]
    s.append('  <g fill="none" stroke="var(--blue)" stroke-width="3.5" stroke-linecap="round">')
    s.append(f'    <path d="{smooth(P, r1)}" marker-end="url(#ar3)"/>')
    s.append(f'    <path d="{smooth(P, r2)}" stroke-dasharray="9 6" marker-end="url(#ar3)"/>')
    s.append('  </g>')
    s.append(f'  <path d="{smooth(P, r3)}" fill="none" stroke="var(--warn)" stroke-width="6" stroke-linecap="round" marker-end="url(#ar2)"/>')
    s.append(dots(P, ['goshen', 'sinai', 'midian']))
    s.append(HALO)
    s += label(P, 'goshen', ['애굽 (고센)'], dx=-11, anchor='end')
    s += label(P, 'sinai', ['시내산 (호렙산)'], dx=-11, dy=18, anchor='end')
    s += label(P, 'midian', ['미디안 광야'], dx=11, dy=5)
    s.append(text(*P(30.0, 32.35), '홍해를 건넘', 12, 400, 'var(--ink-soft)', 'end'))
    s.append('  </g>')
    s.append('''  <g transform="translate(572,92)">
    <rect x="0" y="0" width="316" height="206" rx="10" fill="var(--surface)" opacity=".92"/>
    <text x="16" y="30" font-size="13.5" fill="var(--ink)">① 40세 모세가 애굽을 떠나 광야로</text>
    <text x="16" y="58" font-size="13.5" fill="var(--ink)">② 80세에 하나님을 만나 애굽으로 돌아감</text>
    <text x="32" y="82" font-size="13" fill="var(--ink-soft)">→ 열 가지 재앙, 유월절</text>
    <text x="16" y="110" font-size="13.5" fill="var(--ink)">③ 250만 명을 이끌고 시내산 아래 도착</text>
    <text x="16" y="140" font-size="14" font-weight="700" fill="var(--warn)">여기까지가 출애굽기 18장</text>
    <line x1="16" y1="176" x2="42" y2="176" stroke="var(--blue)" stroke-width="3.5"/>
    <text x="50" y="181" font-size="13" fill="var(--ink-soft)">모세 혼자</text>
    <line x1="140" y1="176" x2="166" y2="176" stroke="var(--warn)" stroke-width="6"/>
    <text x="174" y="181" font-size="13" fill="var(--ink-soft)">250만 명과 함께</text>
  </g>''')
    s.append(scalebar(P, 100, 40, 528))
    s.append(compass())
    return wrap(s)


# ───────────── m3 : 민수기 ─────────────
def m3():
    P = ZOOM
    s = [base_use('sn', river_w=2.6)]
    s += zoom_water_labels()
    s.append(LAND_TXT)
    for p, t in [((30.45, 35.45), '에돔'), ((31.3, 35.72), '모압'), ((32.05, 36.05), '암몬'), ((31.62, 36.25), '아모리(시혼)')]:
        x, y = P(*p); s.append(text(x, y, t, 13, 700, 'var(--ink-soft)'))
    s.append('  </g>')
    s.append('  <defs><marker id="ar4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--warn)"/></marker></defs>')
    r1 = [(28.6, 34.02), (28.92, 34.42), (29.6, 34.55), (30.5, 34.43)]
    r2 = [(30.58, 34.52), (30.1, 34.85), (29.6, 34.98), (29.85, 35.45), (30.4, 35.95), (31.0, 36.15), (31.45, 36.0), (31.78, 35.72)]
    s.append(f'  <path d="{smooth(P, r1)}" fill="none" stroke="var(--warn)" stroke-width="4.5" stroke-linecap="round" marker-end="url(#ar4)"/>')
    kx, ky = P(*PL['kadesh'])
    s.append(f'  <path d="M{kx - 8:.0f},{ky + 14:.0f} q-34,-6 -30,-30 q6,-26 34,-14 q24,16 4,34 q-26,16 -40,-8 q-10,-26 22,-34 q30,-4 34,22" fill="none" stroke="var(--warn)" stroke-width="2.2" opacity=".75"/>')
    s.append(f'  <path d="{smooth(P, r2)}" fill="none" stroke="var(--warn)" stroke-width="4.5" stroke-dasharray="10 6" stroke-linecap="round" marker-end="url(#ar4)"/>')
    s.append(dots(P, ['sinai', 'kadesh', 'moab']))
    s.append(dots(P, ['ezion'], r=5))
    s.append(HALO)
    s += label(P, 'sinai', ['① 시내산'])
    s += label(P, 'kadesh', ['② 가데스바네아', '= 바란 광야. 물샘이 있던 곳', '여기서 38년을 맴돌았습니다'], dx=-44, dy=-4, anchor='end')
    s += label(P, 'moab', ['③ 모압 평지', '요단강 동편. 모세오경이 끝나는 자리'], dx=-12, dy=-8, anchor='end')
    s += label(P, 'ezion', ['에시온게벨'], dx=-9, dy=18, anchor='end')
    s.append('  </g>')
    s.append('''  <g transform="translate(600,414)">
    <rect x="0" y="0" width="288" height="62" rx="10" fill="var(--surface)" opacity=".92"/>
    <text x="16" y="26" font-size="13.5" fill="var(--ink)">에돔 · 모압 · 암몬 · 아모리를</text>
    <text x="16" y="48" font-size="13.5" fill="var(--ink)">빙 돌아서 올라갑니다</text>
  </g>''')
    s.append(scalebar(P, 100, 40, 528))
    s.append(compass())
    return wrap(s)


# ───────────── m5 : 남북 왕국 멸망 ─────────────
def m5():
    P = FULL
    s = [base_use('ne'), crescent(P)]
    s += full_water_labels((33.45, 40.9))
    s.append('''  <defs>
    <marker id="arR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--warn)"/></marker>
    <marker id="arB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--blue)"/></marker>
  </defs>''')
    nx, ny = P(32.65, 35.4); jx, jy = P(31.6, 35.0)
    s.append(f'  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="28" fill="var(--warn)" opacity=".2"/>')
    s.append(f'  <circle cx="{jx:.1f}" cy="{jy:.1f}" r="24" fill="var(--accent)" opacity=".2"/>')
    ra = [(36.45, 42.95), (36.75, 41.4), (36.9, 39.6), (36.45, 37.6), (35.0, 36.4), (33.6, 35.85), (33.05, 35.55)]
    rb = [(32.7, 44.25), (33.4, 43.2), (34.45, 40.9), (35.5, 39.6), (35.9, 38.4), (34.6, 36.85), (33.0, 36.15), (31.95, 35.6)]
    s.append(f'  <path d="{smooth(P, ra)}" fill="none" stroke="var(--warn)" stroke-width="4" stroke-linecap="round" marker-end="url(#arR)"/>')
    s.append(f'  <path d="{smooth(P, rb)}" fill="none" stroke="var(--blue)" stroke-width="4" stroke-linecap="round" marker-end="url(#arB)"/>')
    s.append(dots(P, ['nineveh', 'babylon', 'samaria', 'jerusalem'], r=5.5))
    s.append(HALO)
    s += label(P, 'nineveh', ['앗수르 (니느웨)'])
    s += label(P, 'babylon', ['바벨론'])
    s.append(text(nx - 36, ny - 12, '북이스라엘', 14.5, 700, 'var(--warn)', 'end'))
    s.append(text(nx - 36, ny + 7, '수도 사마리아', 12.5, 400, 'var(--ink-soft)', 'end'))
    s.append(text(nx - 36, ny + 26, '주전 722년 · 앗수르에게', 12.5, 700, 'var(--ink)', 'end'))
    s.append(text(jx - 32, jy + 14, '남유다', 14.5, 700, 'var(--accent)', 'end'))
    s.append(text(jx - 32, jy + 33, '수도 예루살렘', 12.5, 400, 'var(--ink-soft)', 'end'))
    s.append(text(jx - 32, jy + 52, '주전 586년 · 바벨론에게', 12.5, 700, 'var(--ink)', 'end'))
    s.append(text(jx - 32, jy + 70, '세 차례에 걸쳐 무너집니다', 12.5, 400, 'var(--ink-soft)', 'end'))
    s.append('  </g>')
    s.append('''  <g transform="translate(330,430)">
    <rect x="0" y="0" width="396" height="80" rx="10" fill="var(--surface)" opacity=".92"/>
    <text x="16" y="25" font-size="13.5" fill="var(--ink)">두 멸망 사이에 약 130년의 간격이 있고,</text>
    <text x="16" y="47" font-size="13.5" fill="var(--ink)">그 사이 제국이 앗수르 → 바벨론으로 바뀝니다</text>
    <text x="16" y="69" font-size="12.5" fill="var(--ink-soft)">두 군대 모두 사막을 피해 초승달 길로 돌아 내려왔습니다</text>
  </g>''')
    s.append(scalebar(P, 200, 760, 528))
    s.append(compass())
    return wrap(s)


# ───────────── m10 : 백지도 ─────────────
def m10():
    P = FULL
    s = [base_use('ne', faded=True)]
    c = ''.join(f'<circle cx="{xy(P, n)[0]:.1f}" cy="{xy(P, n)[1]:.1f}" r="9"/>' for n in
                ['ur', 'haran', 'nineveh', 'babylon', 'shechem', 'moab', 'kadesh', 'sinai', 'goshen'])
    s.append(f'  <g fill="var(--surface)" fill-opacity=".6" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 3">{c}</g>')
    s.append(compass())
    s.append('  <g paint-order="stroke" stroke="var(--surface)" stroke-width="4" stroke-linejoin="round">')
    s.append(text(450, 540, '점선 동그라미 아홉 곳의 이름을 직접 써 보세요', 13.5, 400, 'var(--ink-soft)', 'middle'))
    s.append('  </g>')
    return wrap(s)


MAPS = dict(m0=m0, m1=m1, m2=m2, m3=m3, m5=m5, m10=m10)


if __name__ == '__main__':
    path = sys.argv[1]
    html = open(path, encoding='utf-8').read()
    for mid, fn in MAPS.items():
        html = splice(html, mid, fn())
    open(path, 'w', encoding='utf-8').write(html)
