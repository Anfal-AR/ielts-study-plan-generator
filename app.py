import streamlit as st
from study_plan_logic import generate_study_plan
import pdfkit
from jinja2 import Template
import os
import base64
from PIL import Image

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IELTS Study Plan Generator",
    layout="centered",
    page_icon="📚"
)

# ─── Centered Logo ─────────────────────────────────────────────────────────────
logo_path = os.path.join(os.getcwd(), "assets", "logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""<div style='text-align:center; margin:30px 0;'>
              <img src="data:image/png;base64,{encoded}" width="180"/>
            </div>""",
        unsafe_allow_html=True
    )
else:
    st.warning("Logo not found — put `logo.png` in `assets/`.")

# ─── Sidebar About ─────────────────────────────────────────────────────────────
st.sidebar.title("📘 About")
st.sidebar.info(
    "Generate a personalized weekly IELTS study plan based on your current score, target, daily time, and test type.\n\n"
    "🎯 For students preparing for Academic/General Training exams."
)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; color:#2E86AB;'>🎯 IELTS Study Plan Generator</h1>"
    "<p style='text-align:center;'>Create your personalized weekly plan for Academic or General Training.</p>",
    unsafe_allow_html=True
)

# ─── Step 1: Collect Study Factors ──────────────────────────────────────────────
with st.form("study_factors_form"):
    col1, col2 = st.columns(2)
    with col1:
        current_score = st.slider("Current IELTS Score", 0.0, 9.0, 5.5, step=0.5)
        daily_hours = st.slider("Hours Available Daily", 1, 8, 3)
        duration_map = {"2 Weeks": 2, "1 Month": 4, "2 Months": 8, "Custom": None}
        dur_label = st.selectbox("Preparation Duration", list(duration_map.keys()))
        if dur_label == "Custom":
            total_weeks = st.number_input("Enter number of weeks", min_value=1, value=8)
        else:
            total_weeks = duration_map[dur_label]
    with col2:
        target_score = st.slider("Target IELTS Score", 0.0, 9.0, 7.0, step=0.5)
        test_format = st.selectbox("Test Type", ["Academic", "General Training"])

    submitted_factors = st.form_submit_button("🚀 Generate My Study Plan")

if not submitted_factors:
    st.stop()

# ─── Step 2: Generate & Display Study Plan ─────────────────────────────────────
plan = generate_study_plan(test_format, current_score, target_score, daily_hours, total_weeks)

st.markdown("---")
st.subheader(f"📅 Your {test_format} Study Plan ({total_weeks} Week{'s' if total_weeks != 1 else ''})")
st.markdown(f"**Current:** {current_score} ➜ **Target:** {target_score} | **Daily:** {daily_hours}h")

for week, days in plan.items():
    st.markdown(f"### {week}")
    for day, sessions in days.items():
        st.markdown(f"**{day}:**")
        for sess in sessions:
            res_list = ", ".join(sess["Resources"][:2])
            st.markdown(f"- **Hour {sess['Hour']}:** {sess['Task']}  \n  _Resources:_ {res_list}")
    st.markdown("")

# ─── PDF Download ──────────────────────────────────────────────────────────────
def make_pdf(plan_data):
    html = """
    <h1>IELTS Study Plan</h1>
    {% for wk, days in plan.items() %}
      <h2>{{ wk }}</h2>
      {% for d, sess_list in days.items() %}
        <h3>{{ d }}</h3><ul>
        {% for s in sess_list %}
          <li><strong>Hour {{ s.Hour }}:</strong> {{ s.Task }}
            <ul>{% for r in s.Resources %}<li>{{ r }}</li>{% endfor %}</ul>
          </li>
        {% endfor %}
        </ul>
      {% endfor %}
    {% endfor %}
    """
    tpl = Template(html)
    rendered = tpl.render(plan=plan_data)

    try:
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        return pdfkit.from_string(rendered, False, configuration=config)
    except Exception as e:
        st.error(f"🚨 PDF generation failed: {e}")
        return None

pdf_bytes = make_pdf(plan)
if pdf_bytes is not None:
    st.download_button(
        "📥 Download as PDF",
        data=pdf_bytes,
        file_name=f"IELTS_Plan_{test_format}.pdf",
        mime="application/pdf"
    )

# ─── Optional: Feedback Form Link (for collecting testimonials) ─────────────────
st.markdown("### 📝 Want to help improve this tool? Share your thoughts!")
st.markdown("We'd love to hear how we can make this app more helpful to future users.")
FEEDBACK_URL = "https://forms.gle/XBLTgBpPTHAaUDCi6 "
st.markdown(f"[📝 Open Feedback Form]({FEEDBACK_URL})", unsafe_allow_html=True)

# ─── Footer Links ──────────────────────────────────────────────────────────────
st.markdown(
    """---  
<div style="text-align:center; font-size:0.9em;">
📘 <a href="https://www.sparkskytech.com/ielts ">Free IELTS Materials</a> |
🛒 <a href="https://www.sparkskytech.com/shop ">Shop IELTS Tools</a> |
🎥 <a href="https://www.youtube.com/ @SparkSkyTech">YouTube Channel</a> |
👥 <a href="https://web.facebook.com/groups/1424280558598301 ">Facebook Group</a>  
<br>© 2025 Spark Sky Tech — Made with ❤️ for Learners  
</div>""",
    unsafe_allow_html=True
)