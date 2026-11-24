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

# تهيئة حالة الخطوات والبيانات
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

# ================= واجهة العميل الأساسية =================
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

# الخطوة الأولى: بيانات العميل (الاسم ورقم الجوال لمن يستلم من الشارع)
if st.session_state.step == 1:
  st.subheader("الخطوة 1 من 2: بيانات العميل ✌🏼")
  name = st.text_input(
      "اسمك الله يرضيك 💕:", value=st.session_state.customer_name
  )
  phone = st.text_input(
      "رقم جوالك (للي بيستلم من الشارع/برّا فقط، أما الاستلام من داخل مو"
      " لازم) 📱:",
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

# الخطوة الثانية: اختيار المنتجات، الوقت، الملاحظات، وحساب التكلفة
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
  v60_hot_qty = st.number_input(
      "☕ V60 حار (السعر: ٢٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )
  v60_iced_qty = st.number_input(
      "🧊 V60 بارد (السعر: ٢٠ ريال)",
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
  brownie_qty = st.number_input(
      "🍫 brownie (السعر: ١١٠ ريال)",
      min_value=0,
      max_value=20,
      value=0,
      step=1,
  )

  st.write("---")
  st.write("📅 **متى تبي طلبك يكون جاهز؟**")
  col_date, col_time = st.columns(2)
  with col_date:
    selected_date = st.date_input(
        "اختر اليوم / التاريخ:",
        value=datetime.date.today(),
        min_value=datetime.date.today(),
    )
  with col_time:
    selected_time = st.text_input(
        "الوقت المناسب لك (مثلاً: 5 العصر):",
        placeholder="اكتب الساعة أو الفترة...",
    )

  st.write("---")
  notes = st.text_area(
      "ملاحظات إضافية (مثل: نوع/لون السيارة عند الاستلام، أو تعديل بالطلب):",
      value=st.session_state.customer_notes,
  )

  # حساب الأسعار التلقائي
  matcha_price = 20
  v60_price = 20
  ice_price = 10
  acai_price = 28
  brownie_price = 110

  total_matcha_qty = sea_salt_matcha_qty + classic_matcha_qty + healthy_matcha_qty
  total_v60_qty = v60_hot_qty + v60_iced_qty
  total_cost = (
      (total_matcha_qty * matcha_price)
      + (total_v60_qty * v60_price)
      + (ice_qty * ice_price)
      + (acai_qty * acai_price)
      + (brownie_qty * brownie_price)
  )

  st.write("---")
  st.markdown(f"### 🥋 التوتال الإجمالي: **{total_cost} ريال**")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("⬅️ رجوع"):
      st.session_state.customer_notes = notes
      st.session_state.step = 1
      st.rerun()

  with col2:
    if st.button("✅ تأكيد وإرسال الطلب"):
      if total_cost == 0:
        st.warning("الرجاء اختيار منتج واحد على الأقل.")
      elif selected_time.strip() == "":
        st.warning("الرجاء كتابة الوقت اللي تبي فيه الطلب.")
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
        if v60_hot_qty > 0:
          order_details.append(f"V60 حار ({v60_hot_qty})")
        if v60_iced_qty > 0:
          order_details.append(f"V60 بارد ({v60_iced_qty})")
        if ice_qty > 0:
          order_details.append(f"آيسكريم مانجو ({ice_qty})")
        if acai_qty > 0:
          order_details.append(f"أساي ({acai_qty})")
        if brownie_qty > 0:
          order_details.append(f"brownie ({brownie_qty})")

        order_summary = ", ".join(order_details)

        day_en = selected_date.strftime("%A")
        day_ar = ARABIC_DAYS.get(day_en, day_en)
        delivery_schedule = f"{day_ar} ({selected_date}) - {selected_time.strip()}"

        new_data = pd.DataFrame([{
            "الاسم": st.session_state.customer_name,
            "الجوال": st.session_state.customer_phone,
            "الطلب": order_summary,
            "موعد التسليم": delivery_schedule,
            "المجموع (ريال)": total_cost,
            "ملاحظات": st.session_state.customer_notes,
            "وقت الإرسال": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
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
            "phone": st.session_state.customer_phone,
            "total": total_cost,
            "details": order_summary,
            "notes": st.session_state.customer_notes,
            "schedule": delivery_schedule,
        }
        st.session_state.step = 3
        st.rerun()

# الخطوة الثالثة: تأكيد النجاح والدفع
elif st.session_state.step == 3:
  summary = st.session_state.last_order_summary
  st.success(" 🫶🏼!🥺تم تسجيل طلبك بفضل الله🎉 الله يجعلنا عند حسن ظنكم")
  if summary:
    note_text = (
        f" | ملاحظاتك: {summary['notes']}" if summary["notes"].strip() else ""
    )
    phone_text = (
        f" ({summary['phone']})"
        if summary["phone"] != "استلام من داخل"
        else " | استلام من داخل"
    )
    st.info(
        f"شكراً لكِ يا **{summary['name']}**{phone_text}! طلبك عبارة عن:"
        f" **{summary['details']}** | موعد الاستلام:"
        f" **{summary['schedule']}**{note_text}."
    )
    st.warning(
        f"💳 **الدفع عبر التحويل:**\n"
        f"المبلغ المطلوب: **{summary['total']} ريال**\n"
        f"بيانات التحويل: **{STC_BANK_INFO}**"
    )

  if st.button("تسجيل طلب جديد ⛳️"):
    st.session_state.customer_name = ""
    st.session_state.customer_phone = ""
    st.session_state.customer_notes = ""
    st.session_state.step = 1
    st.rerun()
