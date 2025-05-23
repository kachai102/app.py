import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="ระบบบัญชีโรงเรียน", layout="wide", page_icon="🏫")

# CSS Styling
st.markdown("""
    <style>
    .title { font-size: 36px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; }
    .subtitle { font-size: 20px; color: #7f8c8d; margin-bottom: 30px; }
    .stButton > button {
        background-color: #3498db; color: white; font-weight: bold; border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ภาพโลโก้
st.image("school.jpg", use_container_width=True)
st.markdown('<div class="title">ระบบบัญชีโรงเรียน</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">จัดการรายรับ รายจ่าย และดูสรุปบัญชี</div>', unsafe_allow_html=True)

# Session state
if 'income_data' not in st.session_state:
    st.session_state.income_data = pd.DataFrame(columns=["วันที่", "หมวดหมู่", "จำนวนเงิน"])
if 'expense_data' not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(columns=["วันที่", "รายละเอียด", "จำนวนเงิน"])

income_categories = [
    "ค่าจัดการเรียนการสอน", "ค่าหนังสือเรียน", "ค่าอุปกรณ์การเรียน",
    "ค่าเครื่องแบบนักเรียน", "ค่ากิจกรรมพัฒนาคุณภาพผู้เรียน"
]

# ===== INPUT =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 เพิ่มรายรับ")
    with st.form("income_form"):
        date_income = st.date_input("วันที่รับเงิน")
        category = st.selectbox("หมวดหมู่รายรับ", income_categories)
        amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f")
        if st.form_submit_button("เพิ่มรายรับ"):
            if amount > 0:
                new_row = {"วันที่": date_income, "หมวดหมู่": category, "จำนวนเงิน": amount}
                st.session_state.income_data = pd.concat([st.session_state.income_data, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"เพิ่มรายรับ '{category}' จำนวน {amount:.2f} บาทเรียบร้อยแล้ว")

with col2:
    st.subheader("💸 เพิ่มรายจ่าย")
    with st.form("expense_form"):
        date_expense = st.date_input("วันที่จ่ายเงิน")
        desc = st.text_input("รายละเอียดรายจ่าย")
        expense_amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f", key="expense_amount")
        if st.form_submit_button("เพิ่มรายจ่าย"):
            if desc and expense_amount > 0:
                new_row = {"วันที่": date_expense, "รายละเอียด": desc, "จำนวนเงิน": expense_amount}
                st.session_state.expense_data = pd.concat([st.session_state.expense_data, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"เพิ่มรายจ่าย '{desc}' จำนวน {expense_amount:.2f} บาทเรียบร้อยแล้ว")

# ===== SUMMARY =====
st.markdown("---")
st.subheader("📊 สรุปบัญชี")

total_income = st.session_state.income_data["จำนวนเงิน"].sum()
total_expense = st.session_state.expense_data["จำนวนเงิน"].sum()
balance = total_income - total_expense

st.metric("รวมรายรับ", f"{total_income:,.2f} บาท")
st.metric("รวมรายจ่าย", f"{total_expense:,.2f} บาท")
st.metric("ยอดคงเหลือ", f"{balance:,.2f} บาท")

with st.expander("📄 ข้อมูลรายรับ"):
    st.dataframe(st.session_state.income_data)

with st.expander("📄 ข้อมูลรายจ่าย"):
    st.dataframe(st.session_state.expense_data)

# ===== FILTER BY DATE =====
st.markdown("---")
st.subheader("📅 ดูข้อมูลตามช่วงวันที่")

income_df = st.session_state.income_data.copy()
income_df["ประเภท"] = "รายรับ"
income_df.rename(columns={"หมวดหมู่": "รายละเอียด"}, inplace=True)

expense_df = st.session_state.expense_data.copy()
expense_df["ประเภท"] = "รายจ่าย"

combined_df = pd.concat([income_df, expense_df], ignore_index=True)

if not combined_df.empty:
    min_date = combined_df["วันที่"].min()
    max_date = combined_df["วันที่"].max()
    start_date, end_date = st.date_input("เลือกช่วงวันที่", [min_date, max_date])

    mask = (combined_df["วันที่"] >= pd.to_datetime(start_date)) & (combined_df["วันที่"] <= pd.to_datetime(end_date))
    filtered_df = combined_df.loc[mask].sort_values("วันที่")

    st.write(f"🔍 พบทั้งหมด {len(filtered_df)} รายการ")
    st.dataframe(filtered_df[["วันที่", "ประเภท", "รายละเอียด", "จำนวนเงิน"]], use_container_width=True)

    st.markdown("### 🗓️ Timeline รายรับ–รายจ่าย")
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x='วันที่:T',
        y='จำนวนเงิน:Q',
        color='ประเภท:N',
        tooltip=['วันที่:T', 'ประเภท:N', 'รายละเอียด:N', 'จำนวนเงิน:Q']
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("ยังไม่มีข้อมูลสำหรับแสดง")
