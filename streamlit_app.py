import streamlit as st
from datetime import datetime

st.set_page_config(page_title="지니 | 학교협동조합 중고책 서점", page_icon="📚", layout="wide")

SEED_BOOKS = [
    {"id": 1, "title": "불편한 편의점", "author": "김호연", "publisher": "나무옆의자", "category": "소설", "price": 9000, "grade": "상", "condition": "표지와 본문 상태가 양호하고 필기 흔적이 거의 없습니다.", "stock": 2, "emoji": "📘"},
    {"id": 2, "title": "아몬드", "author": "손원평", "publisher": "창비", "category": "소설", "price": 7500, "grade": "중", "condition": "읽는 데 문제 없으며 가장자리에 사용감이 있습니다.", "stock": 1, "emoji": "📗"},
    {"id": 3, "title": "세상을 바꾼 과학 이야기", "author": "청소년 과학 편집부", "publisher": "꿈터", "category": "과학", "price": 6000, "grade": "상", "condition": "깨끗하게 보관된 도서입니다.", "stock": 3, "emoji": "📙"},
    {"id": 4, "title": "공부머리 독서법", "author": "최승필", "publisher": "책구루", "category": "학습", "price": 8000, "grade": "중", "condition": "일부 밑줄이 있으며 본문은 양호합니다.", "stock": 2, "emoji": "📕"},
    {"id": 5, "title": "지구를 지키는 작은 습관", "author": "이은재", "publisher": "푸른숲주니어", "category": "환경", "price": 5500, "grade": "상", "condition": "눈에 띄는 손상 없이 상태가 좋습니다.", "stock": 1, "emoji": "🌿"},
]

if "books" not in st.session_state: st.session_state.books = [b.copy() for b in SEED_BOOKS]
if "cart" not in st.session_state: st.session_state.cart = {}
if "orders" not in st.session_state: st.session_state.orders = []
if "next_id" not in st.session_state: st.session_state.next_id = 100

st.markdown("""<style>
.main {background:#fbfaf7;} .block-container{padding-top:1.5rem;max-width:1200px}
.hero{padding:28px 30px;border-radius:20px;background:linear-gradient(120deg,#f1eadc,#e4eddf);margin-bottom:20px}
.hero h1{font-size:2.2rem;color:#243c2c;margin:0}.hero p{color:#536457;margin:8px 0 0}
.book{border:1px solid #e8e4dc;border-radius:16px;padding:16px;background:#ffffff;color:#242820;min-height:180px}
.book b,.book h3,.book p,.book div{color:#242820}
.book .small{color:#626a61;font-size:.88rem}
.book h3{margin:.65rem 0;color:#245c3b;font-weight:800}
.stApp, .stMarkdown, .stText, label, p {color:#242820}
[data-testid="stSidebar"] {color:#242820}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>📚 지니</h1><p>알라딘처럼 편리하게 찾는 학교협동조합 중고책 서점</p><p>학교 구성원 전용 · 교내 지정 장소 수령 · 택배 배송 없음</p></div>', unsafe_allow_html=True)

page = st.sidebar.radio("메뉴", ["도서 둘러보기", "장바구니 / 주문", "주문 내역", "조합 도서 관리"])
st.sidebar.caption("지니 · Streamlit 데모")
st.sidebar.info("현재 데이터는 이 앱 세션에 임시 저장됩니다. 실제 운영 전에는 데이터베이스와 로그인/권한 및 결제 연동이 필요합니다.")

def money(v): return f"{v:,}원"

if page == "도서 둘러보기":
    st.subheader("마음에 드는 책을 찾아보세요")
    c1,c2,c3 = st.columns([2,1,1])
    query = c1.text_input("도서 검색", placeholder="책 제목, 저자, 출판사 검색")
    cats = ["전체"] + sorted({b["category"] for b in st.session_state.books})
    category = c2.selectbox("분야", cats)
    sort = c3.selectbox("정렬", ["추천순", "가격 낮은순", "가격 높은순", "제목순"])
    books = [b for b in st.session_state.books if b["stock"] > 0 and (category == "전체" or b["category"] == category) and query.lower() in (b["title"]+b["author"]+b["publisher"]).lower()]
    if sort == "가격 낮은순": books.sort(key=lambda b:b["price"])
    elif sort == "가격 높은순": books.sort(key=lambda b:b["price"], reverse=True)
    elif sort == "제목순": books.sort(key=lambda b:b["title"])
    st.caption(f"검색 결과 {len(books)}권")
    cols = st.columns(3)
    for i,b in enumerate(books):
        with cols[i%3]:
            st.markdown(f'''<div class="book"><div style="font-size:2.2rem">{b['emoji']}</div><b>{b['title']}</b><div class="small">{b['author']} · {b['publisher']}</div><p>상태 {b['grade']} · 재고 {b['stock']}권</p><h3>{money(b['price'])}</h3><div class="small">{b['condition']}</div></div>''', unsafe_allow_html=True)
            qty = st.number_input("수량", min_value=1, max_value=max(1,b["stock"]), value=1, key=f"qty_{b['id']}")
            if st.button("장바구니 담기", key=f"add_{b['id']}", use_container_width=True):
                st.session_state.cart[b["id"]] = min(b["stock"], st.session_state.cart.get(b["id"],0)+qty)
                st.success("장바구니에 담았어요.")
    if not books: st.info("검색 결과가 없습니다. 다른 검색어를 입력해 주세요.")

elif page == "장바구니 / 주문":
    st.subheader("장바구니")
    items = [(next((b for b in st.session_state.books if b["id"]==bid), None), qty) for bid,qty in st.session_state.cart.items()]
    items = [(b,q) for b,q in items if b]
    if not items: st.info("장바구니가 비어 있어요. 도서를 먼저 담아 주세요.")
    else:
        total = 0
        for b,q in items:
            row = st.columns([3,1,1,1])
            row[0].write(f"**{b['title']}**\n\n{b['author']}")
            row[1].write(f"수량: {q}")
            row[2].write(money(b['price']*q)); total += b['price']*q
            if row[3].button("삭제", key=f"remove_{b['id']}"): del st.session_state.cart[b['id']]; st.rerun()
        st.divider(); st.subheader(f"합계: {money(total)}")
        st.markdown("#### 주문자 정보")
        with st.form("checkout"):
            name = st.text_input("이름")
            school_id = st.text_input("학교 이메일 또는 학번", help="데모에서는 인증하지 않습니다.")
            pickup = st.selectbox("수령 장소", ["학교 도서관 앞 안내 데스크", "학생회실 앞 수령대", "협동조합 사무실"])
            payment = st.radio("결제 방식", ["현장 결제", "온라인 결제(데모)"], horizontal=True)
            submitted = st.form_submit_button("주문 접수하기", use_container_width=True)
        if submitted:
            if not name.strip() or not school_id.strip(): st.error("이름과 학교 이메일 또는 학번을 입력해 주세요.")
            else:
                order = {"number": f"CR-{datetime.now().strftime('%y%m%d%H%M%S')}", "name":name, "school_id":school_id, "pickup":pickup, "payment":payment, "items":[{"title":b['title'],"qty":q,"subtotal":b['price']*q} for b,q in items], "total":total, "status":"주문 접수", "date":datetime.now().strftime("%Y-%m-%d %H:%M")}
                for b,q in items: b["stock"] = max(0,b["stock"]-q)
                st.session_state.orders.insert(0,order); st.session_state.cart = {}
                st.success(f"주문이 접수되었습니다. 주문번호: {order['number']}")
                if payment == "온라인 결제(데모)": st.warning("온라인 결제는 시연용 선택 기능이며 실제 결제가 진행되지 않았습니다.")

elif page == "주문 내역":
    st.subheader("주문 내역")
    if not st.session_state.orders: st.info("아직 접수된 주문이 없습니다.")
    for o in st.session_state.orders:
        with st.expander(f"{o['number']} · {o['date']} · {money(o['total'])}"):
            st.write(f"주문자: {o['name']} · 결제: {o['payment']}")
            st.write(f"수령 장소: {o['pickup']} · 상태: {o['status']}")
            for it in o['items']: st.write(f"- {it['title']} × {it['qty']} — {money(it['subtotal'])}")

else:
    st.subheader("조합 도서 관리")
    st.warning("데모 화면입니다. 실제 서비스에서는 관리자 로그인과 권한 확인을 반드시 추가해야 합니다.")
    with st.expander("새 중고 도서 등록", expanded=True):
        with st.form("new_book"):
            title = st.text_input("책 제목")
            author = st.text_input("저자")
            publisher = st.text_input("출판사")
            category = st.selectbox("분야", ["소설","학습","과학","인문","환경","기타"])
            price = st.number_input("판매 가격(원)", min_value=0, step=500, value=5000)
            grade = st.selectbox("품질 등급", ["상","중","하"])
            condition = st.text_area("상태 설명")
            stock = st.number_input("재고 수량", min_value=1, step=1, value=1)
            add = st.form_submit_button("도서 등록")
        if add:
            if not title.strip() or not author.strip(): st.error("책 제목과 저자를 입력해 주세요.")
            else:
                st.session_state.books.append({"id":st.session_state.next_id,"title":title,"author":author,"publisher":publisher or "미입력","category":category,"price":int(price),"grade":grade,"condition":condition or "상태 설명 없음","stock":int(stock),"emoji":"📚"})
                st.session_state.next_id += 1
                st.success("도서를 등록했습니다."); st.rerun()
    st.markdown("#### 등록된 도서")
    for b in st.session_state.books:
        a,c,d = st.columns([4,1,1])
        a.write(f"**{b['title']}** — {b['author']} · 재고 {b['stock']} · {money(b['price'])}")
        if c.button("재고 +1", key=f"stock_{b['id']}"): b['stock'] += 1; st.rerun()
        if d.button("판매 중지", key=f"off_{b['id']}"): b['stock'] = 0; st.rerun()
