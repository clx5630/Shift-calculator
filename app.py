import streamlit as st
import pandas as pd
import math

st.title("目標逆算型シフト計算機")

# セッションステートの初期化（リスト保持用）
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

# --- サイドバー：現在の見込み収入入力 ---
st.sidebar.header("現在の収入見込み")
teaching_hours = st.sidebar.number_input("確定済みの授業時間 (時給1800円)", min_value=0.0, value=10.0, step=1.0)
admin_hours = st.sidebar.number_input("確定済みの事務時間 (時給1500円)", min_value=0.0, value=5.0, step=1.0)

current_income = (teaching_hours * 1800) + (admin_hours * 1500)
st.sidebar.write(f"**現在の見込み収入:** {int(current_income):,}円")

# --- メイン画面：欲しいものリスト ---
st.header("欲しいもの・やりたいことリスト")
col1, col2 = st.columns([3, 1])
with col1:
    item_name = st.text_input("項目名", placeholder="例: iPad Air (M4) + Pencil Pro")
with col2:
    item_price = st.number_input("金額 (円)", min_value=0, step=1000)

if st.button("リストに追加") and item_name:
    st.session_state.wishlist.append({"項目名": item_name, "金額": item_price})

# --- 結果の計算と表示 ---
if st.session_state.wishlist:
    df = pd.DataFrame(st.session_state.wishlist)
    st.dataframe(df, use_container_width=True)
    
    total_target = df["金額"].sum()
    shortfall = max(0, total_target - current_income)
    
    st.header("逆算結果")
    st.write(f"**目標総額:** {int(total_target):,}円")
    
    if shortfall > 0:
        st.error(f"**不足額:** {int(shortfall):,}円")
        
        st.subheader("必要な追加労働の目安")
        req_teaching = math.ceil(shortfall / 1800)
        req_admin = math.ceil(shortfall / 1500)
        
        st.write(f"- **授業のみで稼ぐ場合:** あと **{req_teaching}** 時間 (約{math.ceil(req_teaching/1.5)}コマ)")
        st.write(f"- **事務のみで稼ぐ場合:** あと **{req_admin}** 時間")
    else:
        st.success("現在のシフト見込みで目標金額を達成しています！")
