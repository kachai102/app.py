import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ระบบบัญชีโรงเรียน", layout="centered",
                   page_icon="🏫")

# --- ใช้ URL โดยตรงกับ st.image() ---
school_img_url = "https://images.unsplash.com/photo-1596495577886-d920f1d9a8cc?auto=format&fit=crop&w=800&q=60"
st.image(school_img_url, caption="WATBANKACHAI SCHOOL", use_column_width=True)

# --- CSS ปรับแต่ง UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
        padding: 25px 40px 40px 40px;
        border-radius: 15px;
    }
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #004466;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ฟังก์ชันเก็บข้อมูล ---
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

st.markdown('<div class="section-title">ระบบบัญชีโรงเรียน</div>', unsafe_allow_html=True)

# --- ฟอร์มเพิ่มรายรับ ---
with st.form("income_form"):
    st.markdown("💰 เพิ่มรายรับ")
    category = st.selectbox("หมวดหมู่รายรับ", income_categories)
    amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f")
    submitted_income = st.form_submit_button("เพิ่มรายรับ")
    if submitted_income:
        if amount > 0:
            new_row = {"หมวดหมู่": category, "จำนวนเงิน": amount}
            st.session_state.income_data = pd.concat([st.session_state.income_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"เพิ่มรายรับ '{category}' จำนวน {amount:.2f} บาทเรียบร้อยแล้ว")
        else:
            st.error("กรุณาใส่จำนวนเงินมากกว่า 0")

st.markdown("---")

# --- ฟอร์มเพิ่มรายจ่าย ---
with st.form("expense_form"):
    st.markdown("💸 เพิ่มรายจ่าย")
    desc = st.text_area("รายละเอียดรายจ่าย")
    expense_amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f", key="expense_amount")
    submitted_expense = st.form_submit_button("เพิ่มรายจ่าย")
    if submitted_expense:
        if desc.strip() and expense_amount > 0:
            new_row = {"รายละเอียด": desc, "จำนวนเงิน": expense_amount}
            st.session_state.expense_data = pd.concat([st.session_state.expense_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"เพิ่มรายจ่าย '{desc}' จำนวน {expense_amount:.2f} บาทเรียบร้อยแล้ว")
        else:
            st.error("กรุณากรอกรายละเอียดและจำนวนเงินให้ถูกต้อง")

st.markdown("---")

# --- สรุปบัญชี ---
total_income = st.session_state.income_data["จำนวนเงิน"].sum()
total_expense = st.session_state.expense_data["จำนวนเงิน"].sum()
balance = total_income - total_expense

st.markdown("📊 สรุปบัญชี")
st.write(f"- รวมรายรับ: **{total_income:,.2f} บาท**")
st.write(f"- รวมรายจ่าย: **{total_expense:,.2f} บาท**")
st.write(f"- ยอดคงเหลือ: **{balance:,.2f} บาท**")

with st.expander("ดูข้อมูลรายรับทั้งหมด"):
    st.dataframe(st.session_state.income_data)

with st.expander("ดูข้อมูลรายจ่ายทั้งหมด"):
    st.dataframe(st.session_state.expense_data)
