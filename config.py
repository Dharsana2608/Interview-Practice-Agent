# TechAssess Pro Configuration
# Professional Interview Platform Settings

# Application Settings
APP_CONFIG = {
    "title": "TechAssess Pro",
    "subtitle": "Professional Technical Interview Platform",
    "version": "1.0.0",
    "max_questions": 15,
    "question_timeout": 30,  # seconds
    "recording_timeout": 10,  # seconds after mic activation
}

# Role Templates
ROLE_TEMPLATES = {
    "Senior Backend Engineer": {
        "topics": ["System Design", "Database Design", "API Development", "Performance Optimization"],
        "skills": ["Python/Java", "SQL", "REST APIs", "Microservices"]
    },
    "Frontend Developer": {
        "topics": ["React/Vue", "JavaScript", "CSS", "Performance"],
        "skills": ["HTML/CSS", "JavaScript", "Framework Experience", "Browser APIs"]
    },
    "Full Stack Developer": {
        "topics": ["Frontend & Backend", "Database Design", "System Architecture"],
        "skills": ["Multiple Languages", "Database Design", "API Development", "UI/UX"]
    },
    "DevOps Engineer": {
        "topics": ["CI/CD", "Infrastructure", "Monitoring", "Security"],
        "skills": ["Docker/K8s", "AWS/Azure", "Automation", "Monitoring Tools"]
    }
}

# Experience Level Mappings
EXPERIENCE_LEVELS = {
    "Junior (0-2 years)": {
        "code": "Junior",
        "focus": "Basic concepts and problem-solving",
        "difficulty": "Beginner"
    },
    "Mid-Level (2-5 years)": {
        "code": "Mid-Level",
        "focus": "Practical experience and best practices",
        "difficulty": "Intermediate"
    },
    "Senior (5+ years)": {
        "code": "Senior",
        "focus": "Architecture and leadership",
        "difficulty": "Advanced"
    },
    "Lead/Principal (8+ years)": {
        "code": "Lead",
        "focus": "System design and mentoring",
        "difficulty": "Expert"
    }
}

# UI Theme Colors
THEME_COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2", 
    "success": "#4CAF50",
    "warning": "#FFC107",
    "error": "#f44336",
    "info": "#2196F3"
}

# Assessment Criteria
ASSESSMENT_CRITERIA = {
    "technical_knowledge": 30,
    "problem_solving": 25,
    "communication": 20,
    "experience_relevance": 15,
    "cultural_fit": 10
}