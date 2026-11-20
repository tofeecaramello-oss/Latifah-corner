import datetime
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="🌴لمسة لطيفة",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# تهيئة حالة الخطوات والبيانات
if "step" not in st.session_state:
  st.session_state.step = 1
if "customer_name" not in st.session_state:
  st.session_state.customer_name = ""
if "customer_notes" not in st.session_state:
  st.session_state.customer_notes = ""
if "last_order_summary" not in st.session_state:
  st.session_state.last_order_summary = None

FILE_PATH = "orders.csv"

# ================= القائمة الجانبية السرية (لأصحاب المتجر فقط) =================
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
        if st.button("حذف جميع الطلبات"):
          os.remove(FILE_PATH)
          st.rerun()
    else:
      st.info("لا توجد طلبات مسجلة حتى الآن.")
  elif admin_pass:
    st.error("الرقم السري خاطئ.")

# ================= واجهة العميل الأساسية =================
st.markdown(
    "<h1 style='text-align: center;'>لمسة لطيفة 🌴</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>شيء نظيف ومضبوط بالبيت،"
    " يغنيك عن برا ✨</p>",
    unsafe_allow_html=True,
)
st.write("---")

# الخطوة الأولى: بيانات العميل (الاسم فقط)
if st.session_state.step == 1:
  st.subheader("الخطوة 1 من 2: بيانات العميل ✌🏼")
  name = st.text_input(
      "اسمك الله يرضيك 💕:", value=st.session_state.customer_name
  )

  if st.button("التالي: اختيار المنتجات ⬅️"):
    if name.strip() == "":
      st.warning("الرجاء إدخال الاسم قبل المتابعة.")
    else:
      st.session_state.customer_name = name
      st.session_state.step = 2
      st.rerun()

# الخطوة الثانية: اختيار المنتجات، الملاحظات، وحساب التكلفة تلقائياً
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
  classic_matcha_qty = st.number_input(
      "🍵 Classic Matcha (السعر: ٢٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )
  healthy_matcha_qty = st.number_input(
      "🍵 Healthy Matcha (السعر: ٢٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )
  ice_qty = st.number_input(
      "🍦 آيسكريم مانجو🥭 (السعر: ١٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )
  acai_qty = st.number_input(
      "🫐 أساي قريبا🚂(السعر: ٢٨ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )

  st.write("---")
  # خانة الملاحظات أصبحت هنا بعد اختيار الطلبات
  notes = st.text_area(
      "ملاحظات إضافية على الطلب (اختياري):",
      value=st.session_state.customer_notes,
  )

  # حساب الأسعار التلقائي
  matcha_price = 20
  ice_price = 10
  acai_price = 28

  total_matcha_qty = sea_salt_matcha_qty + classic_matcha_qty + healthy_matcha_qty
  total_cost = (
      (total_matcha_qty * matcha_price)
      + (ice_qty * ice_price)
      + (acai_qty * acai_price)
  )

  st.write("---")
  st.markdown(f"### 🥋 التوتال الإجمالي: **{total_cost} ريال**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("⬅️ رجوع"):
      st.session_state.customer_notes = (
          notes  # حفظ الملاحظة مؤقتاً لو رجع ورا
      )
      st.session_state.step = 1
      st.rerun()

  with col2:
    if st.button("✅ تأكيد وإرسال الطلب"):
      if total_cost == 0:
        st.warning("الرجاء اختيار منتج واحد على الأقل.")
      else:
        st.session_state.customer_notes = notes

        # تجهيز تفاصيل الطلب
        order_details = []
        if sea_salt_matcha_qty > 0:
          order_details.append(f"Sea Salt Matcha ({sea_salt_matcha_qty})")
        if classic_matcha_qty > 0:
          order_details.append(f"Classic Matcha ({classic_matcha_qty})")
        if healthy_matcha_qty > 0:
          order_details.append(f"Healthy Matcha ({healthy_matcha_qty})")
        if ice_qty > 0:
          order_details.append(f"آيسكريم مانجو ({ice_qty})")
        if acai_qty > 0:
          order_details.append(f"أساي ({acai_qty})")

        order_summary = ", ".join(order_details)

        new_data = pd.DataFrame([{
            "الاسم": st.session_state.customer_name,
            "الطلب": order_summary,
            "المجموع (ريال)": total_cost,
            "ملاحظات": st.session_state.customer_notes,
            "الوقت": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }])

        # حفظ في ملف CSV
        if os.path.exists(FILE_PATH):
          df_old = pd.read_csv(FILE_PATH)
          df_final = pd.concat([df_old, new_data], ignore_index=True)
        else:
          df_final = new_data

        df_final.to_csv(FILE_PATH, index=False)
        st.session_state.last_order_summary = {
            "name": st.session_state.customer_name,
            "total": total_cost,
            "details": order_summary,
            "notes": st.session_state.customer_notes,
        }
        st.session_state.step = 3
        st.rerun()

# الخطوة الثالثة: تأكيد النجاح
elif st.session_state.step == 3:
  summary = st.session_state.last_order_summary
  st.success(" 🫶🏼!🥺تم تسجيل طلبك بفضل الله🎉 الله يجعلنا عند حسن ظنكم")
  if summary:
    note_text = (
        f" | ملاحظاتك: {summary['notes']}" if summary["notes"].strip() else ""
    )
    st.info(
        f"شكراً لكِ يا **{summary['name']}**! طلبك عبارة عن: **{summary['details']}**"
        f" | الإجمالي: **{summary['total']} ريال**{note_text}."
    )

  if st.button("تسجيل طلب جديد ⛳️"):
    st.session_state.customer_name = ""
    st.session_state.customer_notes = ""
    st.session_state.step = 1
    st.rerun()
