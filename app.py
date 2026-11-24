import datetime
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="🌴palm tree",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "step" not in st.session_state:
  st.session_state.step = 1
if "customer_name" not in st.session_state:
  st.session_state.customer_name = ""
if "customer_phone" not in st.session_state:
  st.session_state.customer_phone = ""
if "customer_notes" not in st.session_state:
  st.session_state.customer_notes = ""
if "last_order_summary" not in st.session_state:
  st.session_state.last_order_summary = None

FILE_PATH = "orders.csv"
STC_BANK_INFO = "STC Bank - رقم الجوال: 0559085927"

ARABIC_DAYS = {
    "Monday": "الاثنين",
    "Tuesday": "الثلاثاء",
    "Wednesday": "الأربعاء",
    "Thursday": "الخميس",
    "Friday": "الجمعة",
    "Saturday": "السبت",
    "Sunday": "الأحد",
}

with st.sidebar:
  st.header("🔐 لوحة تحكم الإدارة")
  admin_pass = st.text_input("أدخل الرقم السري:", type="password")

  if admin_pass == "1234":
    st.success("تم تسجيل الدخول بنجاح!")
    if os.path.exists(FILE_PATH):
      df = pd.read_csv(FILE_PATH)
      st.subheader("📋 الطلبات الواردة:")
      st.dataframe(df)

      if not df.empty:
        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 تحميل الطلبات (Excel / CSV)",
            data=csv_data,
            file_name=f"orders_backup_{datetime.date.today()}.csv",
            mime="text/csv",
        )

        st.write("---")
        if st.button("🗑️ حذف جميع الطلبات"):
          os.remove(FILE_PATH)
          st.rerun()
    else:
      st.info("لا توجد طلبات مسجلة حتى الآن.")
  elif admin_pass:
    st.error("الرقم السري خاطئ.")

st.markdown(
    "<h1 style='text-align: center;'>palm tree 🌴</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>شيء نظيف ومضبوط بالبيت،"
    " يغنيك عن برا ✨</p>",
    unsafe_allow_html=True,
)
st.write("---")

if st.session_state.step == 1:
  st.subheader("الخطوة 1 من 2: بيانات العميل ✌🏼")
  name = st.text_input(
      "اسمك الله يرضيك 💕:", value=st.session_state.customer_name
  )
  phone_label = (
      "رقم الجوال (للي بيستلم من الشارع/برّا فقط، أما الاستلام من داخل مو"
      " لازم) 📱:"
  )
  phone = st.text_input(
      phone_label,
      value=st.session_state.customer_phone,
      placeholder="05xxxxxxxx (اختياري للاستلام من داخل)",
  )

  if st.button("التالي: اختيار المنتجات ⬅️"):
    if name.strip() == "":
      st.warning("الرجاء إدخال الاسم قبل المتابعة.")
    else:
      st.session_state.customer_name = name.strip()
      st.session_state.customer_phone = (
          phone.strip() if phone.strip() else "استلام من داخل"
      )
      st.session_state.step = 2
      st.rerun()

elif st.session_state.step == 2:
  st.subheader(
      f"الخطوة 2 من 2: اختيار الطلبات والملاحظات لـ"
      f" {st.session_state.customer_name}"
  )

  st.write("حدد الكميات المطلوبة:")
  sea_salt_matcha_qty = st.number_input(
      "🍵 Sea Salt Matcha (السعر: ٢٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )
  classic_matcha
