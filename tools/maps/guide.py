"""제작지침서 6절의 표준 베이스맵. 실행: python3 tools/maps/guide.py 스터디자료-제작지침서.html"""
import sys
from mapkit import *

NAMES = dict(ur='우르', haran='하란', nineveh='니느웨', babylon='바벨론', damascus='다메섹', shechem='세겜',
             jerusalem='예루살렘', moab='모압 평지', beersheba='브엘세바', kadesh='가데스바네아',
             sinai='시내산', ezion='에시온게벨', goshen='애굽(고센)')
LEFT = dict(shechem=(-11, 0), jerusalem=(-11, 10), beersheba=(-11, 14), kadesh=(-11, 20), goshen=(-11, 5))


def basemap():
    P = FULL
    # 2일차와 같은 문서에 들어가지 않지만, id는 'gd'로 따로 둔다
    s = [base_defs(P, 'gd'), base_use('gd', under=crescent(P, clip='gd-clip'))]
    s += full_water_labels()
    s.append(dots(P, NAMES, r=5.5))
    s.append(HALO)
    for n, ko in NAMES.items():
        if n in LEFT:
            s += label(P, n, [ko], dx=LEFT[n][0], dy=LEFT[n][1], anchor='end')
        elif n == 'moab':
            s += label(P, n, [ko], dx=9, dy=-2)
        elif n == 'ezion':
            s += label(P, n, [ko], dx=9, dy=12)
        else:
            s += label(P, n, [ko])
    s.append('  </g>')
    s.append(scalebar(P, 200, 730, 528))
    s.append(compass())
    return wrap(s)


if __name__ == '__main__':
    path = sys.argv[1]
    html = open(path, encoding='utf-8').read()
    html = splice(html, 'baseMap', basemap(), title_id='baseMapTitle')
    open(path, 'w', encoding='utf-8').write(html)
