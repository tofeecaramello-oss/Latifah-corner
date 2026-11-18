import datetime
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="لمسة لطيفة", page_icon="🍵", layout="centered")

# تهيئة حالة الخطوات والبيانات
if "step" not in st.session_state:
    st.session_state.step = 1
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""
if "custom_notes" not in st.session_state:
    st.session_state.custom_notes = ""
if "last_order_summary" not in st.session_state:
    st.session_state.last_order_summary = None

FILE_PATH = "orders.csv"

# العنوان والوصف الهادئ
st.markdown(
    "<h1 style='text-align: center; color: #385e42;'>لمسة لطيفة</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #666666;'>شيء نظيف ومضبوط"
    " بالبيت، يغنيك عن برا.</p>",
    unsafe_allow_html=True,
)
st.write("---")

# تبويبات للتنقل بين صفحة الطلب وصفحة متابعة الطلبات لكِ
tab1, tab2 = st.tabs(["تسجيل طلب جديد", "جدول الطلبات (لكِ)"])

# ==================== التبويب الأول: تسجيل الطلب ====================
with tab1:
    # --- الخطوة 1: الاسم فقط ---
    if st.session_state.step == 1:
        st.subheader("الخطوة 1 من 2: بيانات العميل")

        name_input = st.text_input(
            "اسمك الكريم:",
            value=st.session_state.customer_name,
            placeholder="اكتب اسمك هنا",
        )

        if st.button("التالي: اختيار التاريخ والطلب ←"):
            if name_input.strip() == "":
                st.warning("فضلاً، اكتب اسمك أولاً.")
            else:
                st.session_state.customer_name = name_input.strip()
                st.session_state.step = 2
                st.rerun()

    # --- الخطوة 2: اختيار التاريخ، الأصناف، الكميات، والملاحظات ---
    elif st.session_state.step == 2:
        st.subheader(f"الخطوة 2 من 2: تفاصيل طلب {st.session_state.customer_name}")

        if st.button("→ رجوع لتعديل الاسم"):
            st.session_state.step = 1
            st.rerun()

        order_date = st.date_input(
            "يوم الاستلام المطلوب:",
            min_value=datetime.date.today(),
        )

        available_items = [
            "ماتشا اليوم (نوع مختلف ومميز)",
            "كوب آساي منزلي (مع إضافاتك الخاصة)",
            "صنف خاص متنوع (مثل آيسكريم المانجا)",
        ]

        selected_items = st.multiselect(
            "اختر صنف أو أكثر:",
            options=available_items,
            default=[available_items[0]],
        )

        quantities = {}
        if selected_items:
            st.markdown("**حدد عدد كل صنف:**")
            for item in selected_items:
                quantities[item] = st.number_input(
                    f"العدد — {item}",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"qty_{item}",
                )

        # الملاحظات صارت هنا بعد اختيار الأعداد والطلبات
        notes_input = st.text_input(
            "إضافاتك أو ملاحظاتك (اختياري):",
            value=st.session_state.custom_notes,
            placeholder="مثال: فواكه معينة للآساي، تقليل التحلية...",
        )

        if st.button("تأكيد الطلب المسبق"):
            if not selected_items:
                st.warning("اختر صنف واحد على الأقل.")
            else:
                st.session_state.custom_notes = notes_input.strip()
                items_formatted = " | ".join(
                    [
                        f"{item} (العدد: {quantities[item]})"
                        for item in selected_items
                    ]
                )
                total_count = sum(quantities.values())

                order_record = {
                    "تاريخ_الطلب": datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "الاسم": st.session_state.customer_name,
                    "يوم_الاستلام": str(order_date),
                    "الأصناف_والأعداد": items_formatted,
                    "إجمالي_العدد": total_count,
                    "الملاحظات": (
                        st.session_state.custom_notes
                        if st.session_state.custom_notes
                        else "لا يوجد"
                    ),
                }

                # حفظ الطلب في الملف المركزي
                df_new = pd.DataFrame([order_record])
                if os.path.exists(FILE_PATH):
                    df_existing = pd.read_csv(FILE_PATH)
                    df_all = pd.concat([df_existing, df_new], ignore_index=True)
                else:
                    df_all = df_new
                df_all.to_csv(FILE_PATH, index=False, encoding="utf-8-sig")

                st.session_state.last_order_summary = order_record
                st.session_state.step = 3
                st.rerun()

    # --- الخطوة 3: صفحة تأكيد الطلب للعميل ---
    elif st.session_state.step == 3:
        summary = st.session_state.last_order_summary
        st.success(f"تم تسجيل طلبك يا {summary['الاسم']} بنجاح 🤍")

        st.markdown(f"**يوم الاستلام:** {summary['يوم_الاستلام']}")
        st.markdown(f"**الطلبات:** {summary['الأصناف_والأعداد']}")
        st.markdown(f"**إجمالي العدد:** {summary['إجمالي_العدد']}")
        st.markdown(f"**الملاحظات:** {summary['الملاحظات']}")

        if st.button("تسجيل طلب جديد"):
            st.session_state.step = 1
            st.session_state.custom_notes = ""
            st.session_state.last_order_summary = None
            st.rerun()

# ==================== التبويب الثاني: جدول الطلبات لكِ ====================
with tab2:
    st.subheader("الطلبات المسجلة")

    if st.button("تحديث الجدول"):
        st.rerun()

    if os.path.exists(FILE_PATH):
        df_orders = pd.read_csv(FILE_PATH)
        if not df_orders.empty:
            st.dataframe(df_orders, use_container_width=True)

            csv_data = df_orders.to_csv(index=False, encoding="utf-8-sig").encode(
                "utf-8-sig"
            )
            st.download_button(
                label="تحميل جدول الطلبات (CSV)",
                data=csv_data,
                file_name="orders.csv",
                mime="text/csv",
            )
        else:
            st.info("لا توجد طلبات مسجلة حتى الآن.")
    else:
        st.info("لا توجد طلبات مسجلة حتى الآن.")

st.write("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray;'>مصنوع بكل"
    " عناية بالبيت</p>",
    unsafe_allow_html=True,
)
