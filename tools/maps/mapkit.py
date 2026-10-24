"""지도 공통 부품: 투영, 지명 위경도, 바탕(땅·호수·강), 경로·라벨·축척."""
import re
import geo

FULL = geo.Proj(29.3, 50.3, 38.0, 32.5)     # 고대 근동 전체
ZOOM = geo.Proj(29.9, 38.1, 32.25, 30.0)    # 시내 반도 확대
NORTH = geo.Proj(29.3, 50.3, 40.4, 35.0)    # 아라랏산까지 위로 넓힌 전체

# (위도, 경도). 위치가 논쟁 중인 곳은 전통적 위치를 쓴다.
PL = dict(
    ur=(30.963, 46.103), haran=(36.865, 39.031), nineveh=(36.359, 43.153),
    babylon=(32.536, 44.421), jerusalem=(31.778, 35.235), shechem=(32.213, 35.282),
    samaria=(32.276, 35.197), kadesh=(30.65, 34.42), sinai=(28.539, 33.975),
    goshen=(30.6, 31.9), moab=(31.83, 35.62), ezion=(29.53, 34.97), midian=(28.4, 35.15),
    damascus=(33.513, 36.292), beersheba=(31.245, 34.84), hebron=(31.532, 35.095),
    bethel=(31.93, 35.22), ararat=(39.70, 44.30),
)
# 새 지명은 여기에 위경도로 추가한다. FULL·ZOOM·NORTH 범위를 모두 벗어나는 곳은
# 그 지도만 geo.Proj로 범위를 넓혀 그린다.

HALO = '<g paint-order="stroke" stroke="var(--surface)" stroke-width="4.5" stroke-linejoin="round">'
SEA_TXT = '<g font-size="13" font-style="italic" fill="var(--ink-soft)" paint-order="stroke" stroke="var(--map-sea)" stroke-width="3" stroke-linejoin="round">'
LAND_TXT = '<g font-size="12.5" font-style="italic" fill="var(--ink-soft)" paint-order="stroke" stroke="var(--map-desert)" stroke-width="3" stroke-linejoin="round">'


def xy(P, p):
    return P(*PL[p]) if isinstance(p, str) else P(*p)


def smooth(P, pts):
    """위경도 점 목록을 Catmull-Rom 곡선(3차 베지어)으로 잇는다."""
    q = [xy(P, p) for p in pts]
    d = f'M{q[0][0]:.1f},{q[0][1]:.1f}'
    for i in range(len(q) - 1):
        p0 = q[i - 1] if i else q[i]
        p1, p2 = q[i], q[i + 1]
        p3 = q[i + 2] if i + 2 < len(q) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d


def text(x, y, s, size=14.5, weight=700, fill='var(--ink)', anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'    <text x="{x:.0f}" y="{y:.0f}"{a} font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>'


def label(P, p, lines, dx=11, dy=5, anchor=None):
    """점 옆에 제목 한 줄 + 설명 여러 줄을 단다."""
    x, y = xy(P, p)
    out = [text(x + dx, y + dy, lines[0], anchor=anchor)]
    for i, s in enumerate(lines[1:]):
        out.append(text(x + dx, y + dy + 19 * (i + 1), s, 12.5, 400, 'var(--ink-soft)', anchor))
    return out


def dots(P, names, r=6.5):
    c = ''.join(f'<circle cx="{xy(P, n)[0]:.1f}" cy="{xy(P, n)[1]:.1f}" r="{r}"/>' for n in names)
    return f'  <g fill="var(--accent)" stroke="var(--surface)" stroke-width="2">{c}</g>'


def compass():
    return '''  <g transform="translate(862,46)" stroke="var(--ink-soft)" fill="var(--ink-soft)">
    <line x1="0" y1="22" x2="0" y2="-12" stroke-width="2"/><path d="M0,-18 L6,-6 L-6,-6 Z" stroke="none"/>
    <text x="0" y="38" font-size="13" font-weight="700" text-anchor="middle" stroke="none" paint-order="stroke">N</text>
  </g>'''


def scalebar(P, km, x, y):
    w = P.km(km)
    return f'''  <g transform="translate({x},{y})" fill="var(--ink-soft)" font-size="12">
    <rect x="0" y="0" width="{w:.1f}" height="5" fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="1"/>
    <rect x="0" y="0" width="{w / 2:.1f}" height="5" fill="var(--ink-soft)"/>
    <text x="0" y="19">0</text><text x="{w:.1f}" y="19" text-anchor="middle">{km} km</text>
  </g>'''


def base_defs(P, pid):
    b = geo.base(P)
    return f'''  <defs>
    <path id="{pid}-land" d="{b['land']}"/>
    <path id="{pid}-lakes" d="{b['lakes']}"/>
    <path id="{pid}-rivers" d="{b['rivers']}"/>
    <clipPath id="{pid}-clip"><use href="#{pid}-land"/></clipPath>
  </defs>'''


def base_use(pid, w=900, h=560, faded=False, river_w=1.8, under=''):
    """바다 → 땅 → under(초승달 같은 영역 표시) → 해안선 → 호수 → 강 순서로 그린다.
    영역 표시를 강·해안선 아래에 두어 지형이 가려지지 않게 한다."""
    o = ' opacity=".55"' if faded else ''
    return f'''  <rect x="0" y="0" width="{w}" height="{h}" fill="var(--map-sea)"{o}/>
  <use href="#{pid}-land" fill="var(--map-desert)"{o}/>
{under + chr(10) if under else ''}  <use href="#{pid}-land" fill="none" stroke="var(--map-stroke)" stroke-width="0.9"{o}/>
  <use href="#{pid}-lakes" fill="var(--map-sea)" stroke="var(--map-stroke)" stroke-width="0.6"{o}/>
  <use href="#{pid}-rivers" fill="none" stroke="var(--map-river)" stroke-width="{river_w}" stroke-linejoin="round" stroke-linecap="round"{o}/>'''


CRESCENT = [(30.4, 47.4), (31.3, 45.9), (32.5, 44.5), (33.8, 43.6), (35.5, 43.4), (36.6, 42.0),
            (36.95, 39.8), (36.6, 37.6), (35.3, 36.5), (33.6, 35.8), (32.3, 35.2), (31.3, 34.8)]


def crescent(P, accent=False, clip='ne-clip'):
    """비옥한 초승달 띠. 반투명 색이라 아래 지형이 비친다. base_use(under=...)로 넣는다."""
    op = '.2' if accent else '.13'
    return (f'  <path d="{smooth(P, CRESCENT)}" fill="none" stroke="var(--accent)" stroke-width="62" opacity="{op}" '
            f'stroke-linecap="round" stroke-linejoin="round" clip-path="url(#{clip})"/>')


def full_water_labels(euphrates=(34.9, 40.0)):
    P = FULL
    s = [SEA_TXT]
    for p, t, a in [((34.3, 31.0), '지중해', None), ((28.4, 49.6), '페르시아만', 'middle'),
                    ((27.3, 34.7), '홍해', 'middle')]:
        x, y = P(*p); s.append(text(x, y, t, 14.5 if t == '지중해' else 12.5, 400, 'var(--ink-soft)', a))
    s.append('  </g>')
    s.append(LAND_TXT)
    for p, t in [((28.3, 29.6), '나일강'), (euphrates, '유프라테스강'), ((35.15, 43.65), '티그리스강')]:
        x, y = P(*p); s.append(text(x, y, t, 12.5, 400, 'var(--ink-soft)'))
    s.append('  </g>')
    return s


def zoom_water_labels():
    P = ZOOM
    s = [SEA_TXT]
    for p, t, size in [((31.95, 31.3), '지중해', 14.5), ((28.75, 32.75), '수에즈만', 12),
                       ((28.15, 34.62), '아카바만', 12)]:
        x, y = P(*p); s.append(text(x, y, t, size, 400, 'var(--ink-soft)', 'end' if t in ('수에즈만', '아카바만') else None))
    s.append('  </g>')
    s.append(LAND_TXT)
    for p, t in [((29.4, 31.05), '나일강'), ((32.1, 35.6), '요단강'), ((29.65, 33.55), '시나이 반도')]:
        x, y = P(*p); s.append(text(x, y, t, 12.5, 400, 'var(--ink-soft)'))
    x, y = P(31.3, 35.36); s.append(text(x, y, '사해', 12, 400, 'var(--ink-soft)', 'end'))
    s.append('  </g>')
    return s


def wrap(parts):
    return '\n'.join(p for p in parts if p)


def splice(html, mid, body, title_id=None):
    """<title id="{mid}t"> 다음부터 </svg> 앞까지를 body로 바꾼다."""
    pat = re.compile(r'(<title id="%s">[^<]*</title>\n)(.*?)(\n    </svg>)' % (title_id or mid + 't'), re.S)
    new, n = pat.subn(lambda m: m.group(1) + body + m.group(3), html)
    assert n == 1, mid
    return new
