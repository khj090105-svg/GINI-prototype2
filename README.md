# 지니 — Streamlit 배포용 프로젝트

학교협동조합 중고책 서점 MVP입니다. Streamlit Community Cloud에서 실행할 수 있도록 Python 앱으로 변환한 버전입니다.

## Streamlit에서 배포
- Repository: `khj090105-svg/GINI`
- Branch: `main`
- Main file path: `streamlit_app.py`

`requirements.txt`는 실행에 필요한 라이브러리를 설치합니다.

## 로컬 실행
```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 데모 한계
- 데이터는 Streamlit 세션 메모리에 임시 저장됩니다. 앱 재시작/세션 변경 시 영구 보존되지 않습니다.
- 로그인/학교 구성원 인증/관리자 권한이 구현되어 있지 않습니다.
- 온라인 결제는 실제 결제가 아닌 데모 선택 기능입니다.
- 실제 운영 전 데이터베이스, 인증/권한, 결제대행사(PG), 개인정보 보호 및 운영 정책을 연동해야 합니다.
- 기존 React 파일은 참고용으로 ZIP에 유지되어 있습니다. Streamlit 배포의 시작 파일은 `streamlit_app.py`입니다.
