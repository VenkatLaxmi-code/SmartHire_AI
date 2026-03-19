import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from resume_parser import extract_text
from skill_extractor import extract_skills, extract_name, extract_email
from ranking import rank_resumes

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '')
        files = request.files.getlist('resumes')
        
        if not job_description or not files or files[0].filename == '':
            return render_template('index.html', error="Please provide both job description and resumes.")
            
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_files.append((filename, filepath))
                
        if not saved_files:
            return render_template('index.html', error="No valid files uploaded. Only PDF and DOCX are allowed.")
            
        # Process resumes
        candidates = []
        resumes_text = []
        
        jd_skills = extract_skills(job_description)
        
        for filename, filepath in saved_files:
            text = extract_text(filepath)
            resumes_text.append(text)
            
            name = extract_name(text)

# fallback if name not extracted
            if name == "Unknown Candidate":
                name = os.path.splitext(filename)[0].replace("_", " ").title()
            email = extract_email(text)
            skills = extract_skills(text)
            
            # Missing skills
            missing_skills = [skill for skill in jd_skills if skill not in skills]
            
            # Suggestions
            suggestions = []
            if missing_skills:
                suggestions.append(f"Add missing technical skills: {', '.join(missing_skills[:3])}")
            if len(skills) < 5:
                suggestions.append("Improve skills section by listing more relevant technologies.")
            if "project" not in text.lower():
                suggestions.append("Add relevant projects to demonstrate experience.")
            if "achieve" not in text.lower() and "improved" not in text.lower():
                suggestions.append("Include measurable achievements (e.g., 'Increased efficiency by 20%').")
                
            if not suggestions:
                suggestions.append("Resume looks solid! Tailor further to specific JD keywords.")
                
            candidates.append({
                'filename': filename,
                'name': name,
                'email': email,
                'skills': skills,
                'missing_skills': missing_skills,
                'suggestions': suggestions
            })
            
        # Rank resumes
        scores = rank_resumes(job_description, resumes_text)
        
        for i, candidate in enumerate(candidates):
            candidate['score'] = round(scores[i] * 100, 2)
            
        # Sort candidates by score descending
        candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        # Clean up uploaded files
        for _, filepath in saved_files:
            try:
                os.remove(filepath)
            except:
                pass
                
        session['candidates'] = candidates
        session['jd_skills'] = jd_skills
        return render_template('results.html', candidates=candidates, jd_skills=jd_skills)
        
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    candidates = session.get('candidates', [])
    if not candidates:
        flash("No candidates found to send emails.")
        return redirect(url_for('index'))
        
    # Configure your SMTP settings here
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "vyshnavi2603@gmail.com"
    SENDER_PASSWORD = "gfwm nyrk yhro lukl"
    
    if SENDER_EMAIL == "your_email@gmail.com" or SENDER_PASSWORD == "your_app_password":
        flash("Email configuration missing! Please open app.py and update SENDER_EMAIL and SENDER_PASSWORD with your real Gmail address and a Google App Password.")
        return render_template('results.html', candidates=candidates, jd_skills=session.get('jd_skills', []))
    
    emails_sent = 0
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        for candidate in candidates:
            email = candidate.get('email')
            if email and email != "No email found":
                score = candidate.get('score')
                suggestions = "\n".join([f"- {s}" for s in candidate.get('suggestions', [])])
                
                msg = EmailMessage()
                msg['Subject'] = "Resume Improvement Suggestions"
                msg['From'] = SENDER_EMAIL
                msg['To'] = email
                
                body = f"""Hello {candidate.get('name', '')},

Thank you for submitting your resume.

Based on our automated resume screening system, here are suggestions to improve your resume for the applied job role.

Match Score: {score}%

Suggested Improvements:
{suggestions}

Best regards,
AI Resume Screening System"""
                msg.set_content(body)
                server.send_message(msg)
                print(f"Sent email to {email}")
                emails_sent += 1
                
        server.quit()
        flash(f"Successfully sent improvement emails to {emails_sent} candidates!")
    except smtplib.SMTPAuthenticationError:
        flash("Authentication failed! Please ensure you are using a valid Gmail address and a generated 16-character 'App Password' (not your regular Gmail password). Go to Google Account -> Security -> 2-Step Verification -> App Passwords to generate one.")
    except Exception as e:
        flash(f"Error sending emails: {str(e)}")
        
    return render_template('results.html', candidates=candidates, jd_skills=session.get('jd_skills', []))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
