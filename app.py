import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="تحليل الأمثال الشعبية الفلسطينية",
    page_icon="🇵🇸",
    layout="centered"
)

st.title("🇵🇸 تطبيق تحليل الأمثال الشعبية الفلسطينية (Agentic RAG)")

# ---------------------------------------------------------
# الشريط الجانبي (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ إعدادات النظام")
    
    api_key = st.text_input(
        "Gemini API Key:", 
        value="", 
        type="password", 
        help="أدخل مفتاح Google AI Studio API الخاص بك"
    )
    
    st.divider()
    
    csv_filename = "proverbs.csv"
    df_proverbs = None
    
    if os.path.exists(csv_filename):
        try:
            df_proverbs = pd.read_csv(csv_filename)
            st.success(f"📂 قاعدة البيانات محملة: **{len(df_proverbs):,}** مثل")
        except Exception as e:
            st.error(f"خطأ في قراءة ملف CSV: {e}")
    else:
        st.warning("⚠️ لم يتم العثور على `proverbs.csv` في المجلد. يرجى رفع الملف:")
        uploaded_file = st.file_uploader("اختر ملف CSV:", type=["csv"])
        if uploaded_file is not None:
            df_proverbs = pd.read_csv(uploaded_file)
            st.success(f"تم تحميل **{len(df_proverbs):,}** مثل بنجاح!")

    st.divider()
    analysis_mode = st.radio(
        "نمط المعالجة (Execution Mode):",
        ["Auto-RAG (الهجين التلقائي)", "Grounded RAG Only (من الملف فقط)", "Out-of-Scope Deductive (استدلال خارجي)"]
    )

# ---------------------------------------------------------
# الواجهة الرئيسية لتحليل الأمثال
# ---------------------------------------------------------
st.markdown("### أهلاً بك! أدخل المثل الشعبي الفلسطيني للتحليل الأكاديمي الخماسي:")

user_proverb = st.text_input("أدخل المثل هنا (مثال: بنت الأصل بتخلي كوخها قصر):", "")

if st.button("🚀 تحليل وترجمة المثل"):
    if not api_key:
        st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
    elif not user_proverb:
        st.warning("⚠️ يرجى كتابة مثل شعبي للتحليل.")
    else:
        try:
            # تهيئة مفتاح الـ API بالطريقة المستقرة
            genai.configure(api_key=api_key)
            
            system_instruction = (
                "You are an expert Palestinian folklorist, dialectologist, and Nida-trained functional translation theorist. "
                "Provide a rigorous 5-Tier Analysis for the given Palestinian proverb: "
                "Tier 1: Proverb Text & Dialectal Classification, "
                "Tier 2: Socio-Cultural Context & Pragmatic Explanation, "
                "Tier 3: Literal Translation (Morphosyntactic Alignment), "
                "Tier 4: Functional & Communicative Meaning, "
                "Tier 5: Idiomatic English Equivalent & 3-Step Decision Hierarchy."
            )
            
            # استخدام النموذج المستقر عبر المكتبة الكلاسيكية
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=system_instruction
            )
            
            with st.spinner("⏳ جاري تحليل المثل عبر نموذج الذكاء الاصطناعي..."):
                response = model.generate_content(
                    user_proverb,
                    generation_config=genai.types.GenerationConfig(temperature=0.2)
                )
                
                st.success("✨ تم التحليل بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالـ API: {e}")
