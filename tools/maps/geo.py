"""Natural Earth 10m 데이터를 등장방형 투영으로 SVG path 문자열로 바꾼다."""
import json, math, os, urllib.request

NE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
NE_URL = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_{}.geojson'
W, H = 900, 560

class Proj:
    def __init__(self, lon0, lon1, lat_top, latc, w=W, h=H):
        self.lon0, self.lat_top = lon0, lat_top
        # 가로 폭에 맞추고, 중앙 위도(latc)의 cos 값으로 경도 간격을 줄인다
        k = math.cos(math.radians(latc))
        self.k = k
        self.S = w / ((lon1 - lon0) * k)
        self.w, self.h = w, h
        self.lat_bot = lat_top - h / self.S
    def __call__(self, lat, lon):
        return ((lon - self.lon0) * self.k * self.S, (self.lat_top - lat) * self.S)
    def km(self, km):
        return km / 111.32 * self.S

def load(name):
    """없으면 Natural Earth 저장소에서 내려받는다(git에는 올리지 않음)."""
    path = os.path.join(NE, f'ne_10m_{name}.geojson')
    if not os.path.exists(path):
        os.makedirs(NE, exist_ok=True)
        urllib.request.urlretrieve(NE_URL.format(name), path)
    with open(path) as f:
        return json.load(f)['features']

def rings(geom):
    if not geom: return []
    if geom['type'] == 'Polygon': return geom['coordinates']
    if geom['type'] == 'MultiPolygon': return [r for p in geom['coordinates'] for r in p]
    return []

def lines(geom):
    if not geom: return []
    if geom['type'] == 'LineString': return [geom['coordinates']]
    if geom['type'] == 'MultiLineString': return geom['coordinates']
    return []

def clip_poly(pts, xmin, ymin, xmax, ymax):
    def clip(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia: out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out
    def ix(x):
        return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))
    def iy(y):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)
    for inside, inter in [(lambda p: p[0] >= xmin, ix(xmin)), (lambda p: p[0] <= xmax, ix(xmax)),
                          (lambda p: p[1] >= ymin, iy(ymin)), (lambda p: p[1] <= ymax, iy(ymax))]:
        if not pts: break
        pts = clip(pts, inside, inter)
    return pts

def rdp(pts, eps):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        s, e = stack.pop()
        ax, ay = pts[s]; bx, by = pts[e]
        dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy)
        dmax, idx = 0, -1
        for i in range(s + 1, e):
            d = (abs(dy * (pts[i][0] - ax) - dx * (pts[i][1] - ay)) / L if L > 1e-6
                 else math.hypot(pts[i][0] - ax, pts[i][1] - ay))
            if d > dmax: dmax, idx = d, i
        if dmax > eps:
            keep[idx] = True
            stack += [(s, idx), (idx, e)]
    return [p for p, k in zip(pts, keep) if k]

def fmt(pts, close):
    s = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return s + ('Z' if close else '')

def poly_path(proj, features, eps=0.5, pad=4, keep=None):
    out = []
    for ft in features:
        if keep and ft['properties'].get('name') not in keep: continue
        for r in rings(ft['geometry']):
            pts = [proj(lat, lon) for lon, lat in r[:-1]]
            pts = clip_poly(pts, -pad, -pad, proj.w + pad, proj.h + pad)
            if len(pts) < 3: continue
            pts = rdp(pts, eps)
            if len(pts) < 3: continue
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            if (max(xs) - min(xs)) * (max(ys) - min(ys)) < 2: continue
            out.append(fmt(pts, True))
    return ''.join(out)

def line_path(proj, features, names, eps=0.5):
    out = []
    for ft in features:
        if ft['properties'].get('name') not in names: continue
        for ln in lines(ft['geometry']):
            seg = []
            for lon, lat in ln:
                x, y = proj(lat, lon)
                if -20 <= x <= proj.w + 20 and -20 <= y <= proj.h + 20:
                    seg.append((x, y))
                else:
                    if len(seg) > 1: out.append(fmt(rdp(seg, eps), False))
                    seg = []
            if len(seg) > 1: out.append(fmt(rdp(seg, eps), False))
    return ''.join(out)

RIVERS = {'Nile', 'Rosetta Branch', 'Damietta Branch', 'Euphrates', 'Firat', 'Al Furat',
          'Tigris', 'Dicle', 'Shatt al Arab', 'Jordan', 'Karkheh'}
LAKES = {'Sea of Galilee', 'Dead Sea', 'Lake Urmia', 'Great Bitter Lake', 'Lake Van'}

def base(proj, eps=0.5):
    land, lakes, rivers = load('land'), load('lakes'), load('rivers_lake_centerlines')
    return dict(land=poly_path(proj, land, eps), lakes=poly_path(proj, lakes, 0.3, keep=LAKES),
                rivers=line_path(proj, rivers, RIVERS, 0.8))
