import spacy
import re

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# A basic list of common tech/business skills for matching
COMMON_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "react", "angular", "vue",
    "node.js", "express", "django", "flask", "spring", "sql", "mysql", "postgresql", "mongodb", "nosql",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "machine learning", "deep learning", "nlp",
    "artificial intelligence", "data science", "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "keras", "excel", "tableau", "power bi", "agile", "scrum", "project management",
    "communication", "leadership", "problem solving", "teamwork", "linux", "bash", "shell scripting"
]

def extract_email(text):
    import re

    # Normalize text
    text = text.replace("\n", " ").replace("\t", " ")

    # Fix broken emails from PDFs
    text = re.sub(r"\s*@\s*", "@", text)
    text = re.sub(r"\s*\.\s*", ".", text)

    # Standard email pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    matches = re.findall(email_pattern, text)

    if matches:
        return matches[0].strip()

    # Backup method for weird formatted emails
    words = text.split()
    for word in words:
        if "@" in word and "." in word:
            word = word.replace(",", "").replace(";", "").replace(")", "").replace("(", "")
            if re.match(email_pattern, word):
                return word

    return "No email found"

def extract_skills(text, custom_skills=None):
    text = text.lower()
    skills_found = set()
    
    skills_to_check = COMMON_SKILLS.copy()
    if custom_skills:
        skills_to_check.extend([s.lower() for s in custom_skills])
        
    for skill in skills_to_check:
        # Use regex for exact word match
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            skills_found.add(skill.title())
            
    return list(skills_found)

def is_valid_name(name):
    name_lower = name.lower().strip()
    
    # 1. Check length and word count
    if not re.match(r'^[A-Za-z\s]+$', name):
        return False
        
    word_count = len(name.split())
    if not (2 <= word_count <= 4):
        return False
        
    # 2. Check against forbidden exact matches (sections, common words)
    forbidden_words = {
        "education", "skills", "languages", "experience", "projects", 
        "summary", "cloud computing", "machine learning", "artificial intelligence",
        "profile", "contact", "resume", "curriculum vitae", 
        "objective", "certifications", "interests", "hobbies", "about",
        "personal", "details", "work", "history", "employment", "professional",
        "technical", "core", "competencies", "qualifications", "achievements",
        "awards", "honors", "publications", "references", "declaration"
    }
    if name_lower in forbidden_words:
        return False
        
    # 3. Check if the name contains ANY known skill
    # We check if any word in the name is a known skill
    name_words = set(name_lower.split())
    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        # Exact match of the whole skill
        if name_lower == skill_lower:
            return False
        # If a single-word skill is part of the name (e.g., "Java Developer")
        if len(skill_lower.split()) == 1 and skill_lower in name_words:
            return False
        # If a multi-word skill is in the name (e.g., "Machine Learning")
        if len(skill_lower.split()) > 1 and skill_lower in name_lower:
            return False
            
    # 4. Check against common job title words and academic words
    forbidden_parts = {
        "engineer", "developer", "manager", "learning", "science", 
        "data", "analyst", "student", "university", "college", 
        "bachelor", "master", "phd", "degree", "technology", "software",
        "intern", "assistant", "associate", "senior", "junior", "lead",
        "specialist", "consultant", "administrator", "architect", "designer"
    }
    if any(part in name_lower.split() for part in forbidden_parts):
        return False
        
    return True

def extract_name(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Check first 10 lines (name usually at top)
    for line in lines[:10]:
        clean = re.sub(r'[^A-Za-z\s]', '', line).strip()
        words = clean.split()

        # valid name conditions
        if 2 <= len(words) <= 3:
            if all(word[0].isupper() for word in words):
                return clean

    return "Unknown Candidate"