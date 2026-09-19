# 성경이 읽어지네 — 스터디 자료

"성경이 읽어지네" 강의를 정리한 성경 통독 스터디 자료입니다. GitHub Pages(Jekyll)로 배포됩니다.

- 사이트: https://marc416.github.io/bible-study/

## 구조

- `index.html` — 홈. 회차별 자료 목록
- `스터디자료-제작지침서.html` — 자료 제작 지침서
- `N일차/index.html` — 각 회차 정리 자료 (자기완결형 정적 HTML)
- `N일차/transcript/`, `*.m4a` — 원본 녹음/전사본. **git에는 올리지 않음** (`.gitignore` 처리)

## 새 회차 추가하기

1. `N일차/index.html`을 만든다 (기존 `2일차/index.html`을 템플릿으로 복사해서 내용만 교체).
2. 원본 녹음(`.m4a`)과 전사본(`transcript/`)은 같은 폴더에 두되, 자동으로 git에서 제외된다.
3. 루트 `index.html`의 회차 목록 카드에 새 회차 링크를 추가한다.
4. `main` 브랜치에 push하면 GitHub Actions가 자동으로 빌드·배포한다.
