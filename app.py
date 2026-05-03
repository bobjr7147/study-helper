import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# --- Setup ---
st.set_page_config(page_title="Missed Class Explainer")

st.title("📚 Explain It Like I Missed Class")
st.write("Paste your notes and get a quick, test-focused explanation.")

# --- Input ---
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

user_input = st.text_area("Or paste your notes here:", height=200)

pdf_text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text() or ""

final_input = pdf_text if pdf_text.strip() else user_input
# --- Button ---
if st.button("I have 10 minutes"):
    if final_input.strip() == "":        
        st.warning("Please paste something first.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            prompt = f"""

Explain the following like a student who missed class and has 10 minutes before an exam.
Think like a teacher.
Break it into:
1. What this actually means
2. What to remember
3. What could be on the test

Keep it concise and intuitive.
Do not write a followup question.

When writing math, ALWAYS use LaTeX formatting.

Examples:
- Write fractions like: $\frac{1}{2}$
- Write exponents like: $x^2$
- Wrap all math in $...$

Format EXACTLY like this:

## What this actually means
- ...

## What to remember
- ...

## What could be on the test
- ...
Text:
{final_input}
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            output = response.choices[0].message.content

            # --- Output ---
            st.subheader("🧠 Your Cram Explanation")
            st.markdown(output)

        except Exception as e:
            st.error(f"Error: {e}")