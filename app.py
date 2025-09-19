<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, send_file
import json
import io
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ─── Initialize Flask App ──────────────────────────────────────────────
app = Flask(__name__)

# Ensure upload folder exists
os.makedirs('static/uploads', exist_ok=True)

# ─── Study Plan Generation Logic ───────────────────────────────────────
def generate_study_plan(current_score, target_score, hours_daily, test_type, num_weeks):
    """
    Generate a personalized weekly study plan
    """
    # Calculate intensity
    score_gap = float(target_score) - float(current_score)
    intensity = "High" if score_gap > 1.5 else "Medium" if score_gap > 0.5 else "Low"

    # Base activities by skill
    base_activities = {
        'listening': [
            'Practice with real IELTS listening tests',
            'Focus on identifying key information and details',
            'Listen to English podcasts and audio recordings'
        ],
        'reading': [
            'Practice IELTS reading passages with time limits',
            'Work on skimming and scanning techniques',
            'Build academic vocabulary'
        ],
        'writing': [
            'Practice Task 1 and Task 2 essay writing',
            'Focus on structure and coherence',
            'Build vocabulary for academic writing'
        ],
        'speaking': [
            'Practice speaking on various topics',
            'Record yourself and analyze fluency',
            'Work on pronunciation and intonation'
        ]
    }

    # Weekly focus logic
    def get_week_focus(week, total_weeks, score_gap):
        if week <= total_weeks // 3:
            return "Foundation Building"
        elif week <= 2 * total_weeks // 3:
            return "Skill Development"
        else:
            return "Test Preparation & Practice"

    # Daily schedule generator
    def generate_daily_schedule(hours_daily, test_type, intensity):
        hours = int(hours_daily)
        allocation = {'listening': 0.25, 'reading': 0.25, 'writing': 0.30, 'speaking': 0.20}
        
        daily_schedule = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in days:
            schedule = []
            for skill, ratio in allocation.items():
                time_allocated = int(hours * ratio * 60)  # minutes
                if time_allocated > 0:
                    schedule.append({
                        'skill': skill.title(),
                        'duration': f"{time_allocated} minutes",
                        'activities': get_skill_activities(skill, test_type, time_allocated)
                    })
            daily_schedule[day] = schedule
        
        return daily_schedule

    def get_skill_activities(skill, test_type, duration_minutes):
        activities = {
            'listening': [
                'Listen to IELTS practice tests',
                'Practice with academic lectures' if test_type == 'academic' else 'Practice with everyday conversations',
                'Focus on identifying main ideas and details'
            ],
            'reading': [
                'Complete IELTS reading passages',
                'Practice academic texts' if test_type == 'academic' else 'Practice general interest articles',
                'Work on time management'
            ],
            'writing': [
                'Practice Task 1 (graphs/charts)' if test_type == 'academic' else 'Practice Task 1 (letters)',
                'Practice Task 2 essay writing',
                'Focus on structure and linking words'
            ],
            'speaking': [
                'Practice Part 1 personal questions',
                'Work on Part 2 cue card topics',
                'Practice Part 3 discussion questions'
            ]
        }
        return activities.get(skill, [])

    def get_weekly_goals(week, target_score):
        return [
            f"Maintain consistent daily study routine",
            f"Complete all scheduled practice activities",
            f"Track progress towards {target_score} target",
            f"Review and identify areas for improvement"
        ]

    # Generate full plan
    weekly_plan = {}
    for week in range(1, num_weeks + 1):
        weekly_plan[f'Week {week}'] = {
            'focus': get_week_focus(week, num_weeks, score_gap),
            'daily_schedule': generate_daily_schedule(hours_daily, test_type, intensity),
            'goals': get_weekly_goals(week, target_score),
            'resources': {
                'sparkskytech': [
                    'https://www.sparkskytech.com/ielts',
                    'https://www.sparkskytech.com/ielts/ielts_free_resources'
                ],
                'official': [
                    'https://www.ielts.org/',
                    'https://takeielts.britishcouncil.org/'
                ],
                'practice': [
                    'https://www.ieltsonlinetests.com/',
                    'https://ieltsliz.com/'
                ]
            }
        }

    return {
        'current_score': current_score,
        'target_score': target_score,
        'test_type': test_type,
        'duration': f"{num_weeks} weeks",
        'hours_daily': hours_daily,
        'intensity': intensity,
        'weekly_plan': weekly_plan,
        'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ─── Routes ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    """Generate study plan from form data"""
    try:
        # Get form data (support both slider and dropdown names)
        current_score = request.form.get('current_score') or request.form.get('currentLevel')
        target_score = request.form.get('target_score') or request.form.get('targetBand')
        hours_daily = request.form.get('hours_daily') or request.form.get('hoursDaily')
        test_type = request.form.get('test_type') or request.form.get('testType')
        num_weeks_str = request.form.get('num_weeks') or request.form.get('prepDuration')

        # Validate required fields
        if not all([current_score, target_score, hours_daily, test_type, num_weeks_str]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        num_weeks = int(num_weeks_str)

        # Generate the plan
        study_plan = generate_study_plan(
            current_score, target_score, hours_daily, test_type, num_weeks
        )

        return jsonify({'success': True, 'plan': study_plan})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/export-text', methods=['POST'])
def export_text():
    """Export study plan as plain text"""
    try:
        plan_data = request.get_json()
        if not plan_data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        buffer = io.StringIO()

        # Header
        buffer.write("IELTS STUDY PLAN\n")
        buffer.write("=" * 50 + "\n\n")

        # Overview
        buffer.write(f"Current Score: {plan_data['current_score']}\n")
        buffer.write(f"Target Score: {plan_data['target_score']}\n")
        buffer.write(f"Test Type: {plan_data['test_type'].title()}\n")
        buffer.write(f"Duration: {plan_data['duration']}\n")
        buffer.write(f"Daily Hours: {plan_data['hours_daily']} hours\n")
        buffer.write(f"Generated: {plan_data['generated_date']}\n\n")

        # Weekly plans
        for week, details in plan_data['weekly_plan'].items():
            buffer.write(f"{week.upper()}\n")
            buffer.write(f"Focus: {details['focus']}\n\n")
            for day, schedule in details['daily_schedule'].items():
                buffer.write(f"  {day}:\n")
                for activity in schedule:
                    buffer.write(f"    • {activity['skill']}: {activity['duration']}\n")
                    if 'activities' in activity:
                        for task in activity['activities']:
                            buffer.write(f"      - {task}\n")
                buffer.write("\n")
            buffer.write("-" * 30 + "\n\n")

        content = buffer.getvalue()
        buffer.close()

        return jsonify({'success': True, 'content': content})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    """Export study plan as professional PDF with clickable footer and page numbers"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import HexColor
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        plan_data = request.get_json()
        if not plan_data:
            return jsonify({'error': 'No data provided'}), 400

        buffer = io.BytesIO()
        
        # Custom Canvas for headers/footers
        class ProfessionalCanvas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self._saved_page_states = []
                self.page_count = 0

            def showPage(self):
                self._saved_page_states.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                num_pages = len(self._saved_page_states)
                for (page_num, page_state) in enumerate(self._saved_page_states):
                    self.__dict__.update(page_state)
                    self.draw_page_elements(page_num + 1, num_pages)
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)

            def draw_page_elements(self, page_num, total_pages):
                # Header
                self.setFont("Helvetica-Bold", 16)
                self.setFillColor(HexColor("#667eea"))
                self.drawCentredText(letter[0]/2, letter[1] - 50, "IELTS Smart Study Plan")
                
                # Subheader
                self.setFont("Helvetica", 12)
                self.setFillColor(HexColor("#764ba2"))
                self.drawCentredText(letter[0]/2, letter[1] - 70, "by SparkSkyTech")
                
                # Page number (top right)
                self.setFont("Helvetica", 10)
                self.setFillColor(colors.gray)
                self.drawRightString(letter[0] - 50, letter[1] - 50, f"Page {page_num} of {total_pages}")
                
                # Footer with clickable links
                footer_y = 50
                
                # Company name
                self.setFont("Helvetica-Bold", 11)
                self.setFillColor(HexColor("#667eea"))
                self.drawString(50, footer_y + 20, "SparkSkyTech - IELTS Study Plan Generator")
                
                # Website link (clickable)
                self.setFont("Helvetica", 10)
                self.setFillColor(colors.blue)
                website_text = "Visit: www.sparkskytech.com/ielts"
                self.drawString(50, footer_y, website_text)
                
                # Make website clickable
                self.linkURL("https://www.sparkskytech.com/ielts", 
                           (50, footer_y - 5, 200, footer_y + 10))
                
                # Generation date (right side)
                self.setFont("Helvetica", 9)
                self.setFillColor(colors.gray)
                gen_date = f"Generated: {plan_data['generated_date']}"
                self.drawRightString(letter[0] - 50, footer_y, gen_date)
                
                # Separator line
                self.setStrokeColor(HexColor("#e2e8f0"))
                self.setLineWidth(0.5)
                self.line(50, letter[1] - 90, letter[0] - 50, letter[1] - 90)  # Top line
                self.line(50, footer_y + 35, letter[0] - 50, footer_y + 35)   # Bottom line

        # Create document with custom canvas
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=120,  # More space for header
            bottomMargin=100,  # More space for footer
            leftMargin=60,
            rightMargin=60
        )

        # Enhanced Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor("#667eea"),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor("#764ba2"),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor("#e2e8f0"),
            borderPadding=8,
            backColor=HexColor("#f8fafc")
        )
        
        week_style = ParagraphStyle(
            'WeekHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=HexColor("#667eea"),
            spaceAfter=12,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=16,
            fontName='Helvetica'
        )
        
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leading=14,
            leftIndent=20,
            fontName='Helvetica'
        )

        # Build content
        content = []
        
        # Title Section
        content.append(Paragraph("Your Personalized Study Plan", title_style))
        content.append(Spacer(1, 20))

        # Overview Table
        overview_data = [
            ['<b>Current Score:</b>', plan_data['current_score']],
            ['<b>Target Score:</b>', plan_data['target_score']],
            ['<b>Test Type:</b>', plan_data['test_type'].title()],
            ['<b>Duration:</b>', plan_data['duration']],
            ['<b>Daily Hours:</b>', f"{plan_data['hours_daily']} hours"],
            ['<b>Intensity Level:</b>', plan_data['intensity']]
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 3*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#667eea")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor("#f8fafc")])
        ]))
        
        content.append(overview_table)
        content.append(Spacer(1, 30))

        # Weekly Plans
        content.append(Paragraph("Weekly Study Schedule", section_style))
        
        for week_name, details in plan_data['weekly_plan'].items():
            content.append(Paragraph(f"{week_name}", week_style))
            content.append(Paragraph(f"<b>Focus:</b> {details['focus']}", normal_style))
            content.append(Spacer(1, 10))
            
            # Daily schedule
            for day, activities in details['daily_schedule'].items():
                content.append(Paragraph(f"<b>{day}:</b>", normal_style))
                
                for activity in activities:
                    activity_text = f"• <b>{activity['skill']}:</b> {activity['duration']}"
                    content.append(Paragraph(activity_text, bullet_style))
                    
                    # Add specific activities if available
                    if 'activities' in activity:
                        for task in activity['activities'][:2]:  # Limit to 2 tasks for space
                            task_text = f"  - {task}"
                            content.append(Paragraph(task_text, bullet_style))
                
                content.append(Spacer(1, 8))
            
            # Weekly goals
            if 'goals' in details and details['goals']:
                content.append(Paragraph("<b>Weekly Goals:</b>", normal_style))
                for goal in details['goals']:
                    content.append(Paragraph(f"• {goal}", bullet_style))
                
            content.append(Spacer(1, 20))

        # Resources Section
        content.append(Paragraph("Recommended Resources", section_style))
        
        resources_text = f"""
        <b>SparkSkyTech Resources:</b><br/>
        • Comprehensive IELTS preparation materials<br/>
        • Free practice tests and mock exams<br/>
        • Expert strategies and tips<br/>
        • Visit: <link href="https://www.sparkskytech.com/ielts">www.sparkskytech.com/ielts</link><br/><br/>
        
        <b>Official IELTS Resources:</b><br/>
        • Official practice materials and sample tests<br/>
        • Test format and scoring information<br/>
        • Registration and test center details<br/><br/>
        
        <b>Additional Practice:</b><br/>
        • British Council IELTS preparation courses<br/>
        • Online mock tests and practice exercises<br/>
        • Mobile apps for daily vocabulary building
        """
        
        content.append(Paragraph(resources_text, normal_style))
        
        # Success tips
        content.append(Spacer(1, 20))
        content.append(Paragraph("Success Tips", week_style))
        
        tips_text = """
        • <b>Consistency is key:</b> Study regularly even if for shorter periods<br/>
        • <b>Track your progress:</b> Keep a study journal and note improvements<br/>
        • <b>Practice under timed conditions:</b> Simulate real exam environment<br/>
        • <b>Focus on weak areas:</b> Spend extra time on challenging skills<br/>
        • <b>Use official materials:</b> Supplement with authentic IELTS content<br/>
        • <b>Get feedback:</b> Have your writing and speaking assessed by experts
        """
        
        content.append(Paragraph(tips_text, normal_style))

        # Build PDF with custom canvas
        doc.build(content, canvasmaker=ProfessionalCanvas)
        buffer.seek(0)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"IELTS_StudyPlan_SparkSkyTech_{timestamp}.pdf"

        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        print("PDF Export Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


# ─── Run App ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
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

# ─── Centered Logo in Sidebar ──────────────────────────────────────────────────
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
    "Try it free now — first 30 users only!"
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
        duration_options = {"2 Weeks": 2, "1 Month": 4, "2 Months": 8, "Custom": None}
        dur_label = st.selectbox("Preparation Duration", list(duration_options.keys()))
        if dur_label == "Custom":
            total_weeks = st.number_input("Enter number of weeks", min_value=1, value=8)
        else:
            total_weeks = duration_options[dur_label]
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
st.markdown(f"**Current:** {current_score} ➜ **Target:** {target_score} | **Daily Hours:** {daily_hours}")

for week, days in plan.items():
    st.markdown(f"### {week}")
    for day, sessions in days.items():
        st.markdown(f"**{day}:**")
        for sess in sessions:
            res_list = ", ".join(sess["Resources"][:2])
            st.markdown(f"- **Hour {sess['Hour']}:** {sess['Task']}  \n  _Resources:_ {res_list}")
    st.markdown("")

# ─── PDF Download Function ──────────────────────────────────────────────────────
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
        # Update this path to match where you installed wkhtmltopdf
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        return pdf
    except Exception as e:
        st.error(f"🚨 PDF generation failed: {e}")
        return None


# ─── Trigger PDF Generation and Show Button ─────────────────────────────────────
pdf = make_pdf(plan)

if pdf is not None:
    st.download_button(
        "📥 Download as PDF",
        data=pdf,
        file_name=f"IELTS_Plan_{test_format}.pdf",
        mime="application/pdf"
    )

# ─── Optional: Feedback Form Link (for collecting testimonials) ─────────────────
st.markdown("### 📝 Want to help improve this tool? Share your thoughts!")
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
>>>>>>> 11442c5835ce787d04033632d03c9a68422a5f01
