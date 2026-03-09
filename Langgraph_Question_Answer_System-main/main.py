import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="Interview Q&A Generator", page_icon="🎯", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#21618C;'>🎯 Interview Q&A Generator</h1>
    <p style='text-align:center; color:gray;'>Generate domain-specific interview questions & answers instantly</p>
    <hr>
""", unsafe_allow_html=True)

# ---- User Inputs ----
col1, col2, col3 = st.columns(3)

with col1:
    domain = st.text_input("📚 Domain", placeholder="e.g. Machine Learning")
with col2:
    no_of_questions = st.slider("🔢 Questions", min_value=3, max_value=15, value=5)
with col3:
    tone = st.selectbox("🎚️ Level", ["beginner", "intermediate", "advanced"])

st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button("🚀 Generate Q&A", use_container_width=True)

# ---- On Button Click ----
if generate_btn:
    if not domain.strip():
        st.warning("⚠️ Please enter a domain!")
    else:
        with st.spinner("⏳ Generating... please wait"):
            # ✅ single POST request — returns PDF directly
            response = requests.post(f"{FASTAPI_URL}/generate", json={
                "domain": domain,
                "no_of_questions": no_of_questions,
                "tone": tone
            })

        if response.status_code == 200:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.success("✅ Q&A Generated Successfully!")

            # ✅ response.content is the PDF bytes directly — no second request needed
            st.download_button(
                label="📥 Download Q&A as PDF",
                data=response.content,
                file_name=f"{domain.replace(' ', '_')}_QA.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error(f"❌ Error: {response.text}")