import streamlit as st
import pandas as pd

st.set_page_config(page_title="ระบบบัญชีโรงเรียน", layout="wide", page_icon="🏫")

# ===== CSS สไตล์ Web App =====
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f3f6fa;
    }
    .title {
        font-size: 36px;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea textarea {
        border-radius: 8px;
    }
    .block-container {
        padding: 3rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== แสดงภาพโลโก้และชื่อแอป =====
st.image("school.jpg", use_container_width=True)
st.markdown('<div class="title">ระบบบัญชีโรงเรียน</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">จัดการรายรับ รายจ่าย และดูสรุปอย่างง่าย</div>', unsafe_allow_html=True)

# ===== เตรียมข้อมูล session =====
if 'income_data' not in st.session_state:
    st.session_state['income_data'] = pd.DataFrame(columns=["หมวดหมู่", "จำนวนเงิน"])
if 'expense_data' not in st.session_state:
    st.session_state['expense_data'] = pd.DataFrame(columns=["รายละเอียด", "จำนวนเงิน"])

income_categories = [
    "ค่าจัดการเรียนการสอน",
    "ค่าหนังสือเรียน",
    "ค่าอุปกรณ์การเรียน",
    "ค่าเครื่องแบบนักเรียน",
    "ค่ากิจกรรมพัฒนาคุณภาพผู้เรียน"
]

# ===== แบ่ง 2 คอลัมน์: รายรับ | รายจ่าย =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 เพิ่มรายรับ")
    with st.form("income_form"):
        category = st.selectbox("หมวดหมู่รายรับ", income_categories)
        amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f")
        if st.form_submit_button("เพิ่มรายรับ"):
            if amount > 0:
                new_row = {"หมวดหมู่": category, "จำนวนเงิน": amount}
                st.session_state.income_data = pd.concat([st.session_state.income_data, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"เพิ่มรายรับ '{category}' จำนวน {amount:.2f} บาทเรียบร้อยแล้ว")
            else:
                st.error("กรุณาใส่จำนวนเงินมากกว่า 0")

with col2:
    st.subheader("💸 เพิ่มรายจ่าย")
    with st.form("expense_form"):
        desc = st.text_input("รายละเอียดรายจ่าย")
        expense_amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f", key="expense_amount")
        if st.form_submit_button("เพิ่มรายจ่าย"):
            if desc.strip() and expense_amount > 0:
                new_row = {"รายละเอียด": desc, "จำนวนเงิน": expense_amount}
                st.session_state.expense_data = pd.concat([st.session_state.expense_data, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"เพิ่มรายจ่าย '{desc}' จำนวน {expense_amount:.2f} บาทเรียบร้อยแล้ว")
            else:
                st.error("กรุณากรอกรายละเอียดและจำนวนเงินให้ถูกต้อง")

# ===== สรุปผลบัญชี =====
st.markdown("---")
st.subheader("📊 สรุปบัญชี")

total_income = st.session_state.income_data["จำนวนเงิน"].sum()
total_expense = st.session_state.expense_data["จำนวนเงิน"].sum()
balance = total_income - total_expense

st.metric("รวมรายรับ", f"{total_income:,.2f} บาท")
st.metric("รวมรายจ่าย", f"{total_expense:,.2f} บาท")
st.metric("ยอดคงเหลือ", f"{balance:,.2f} บาท")

with st.expander("📄 ข้อมูลรายรับทั้งหมด"):
    st.dataframe(st.session_state.income_data)

with st.expander("📄 ข้อมูลรายจ่ายทั้งหมด"):
    st.dataframe(st.session_state.expense_data)
