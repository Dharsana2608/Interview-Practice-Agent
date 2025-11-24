import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import base64
from io import BytesIO
import hashlib
import time
import re

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Interview Practice Partner", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load .env file - try multiple locations
# First, try to get the script directory
script_dir = None
try:
    if '__file__' in globals():
        script_dir = os.path.dirname(os.path.abspath(__file__))
except:
    pass

# Build list of possible .env file locations
env_paths = []
if script_dir:
    env_paths.append(os.path.join(script_dir, '.env'))
    
# Add current working directory and common locations
cwd = os.getcwd()
env_paths.extend([
    os.path.join(cwd, '.env'),
    '.env',
    os.path.join(os.path.dirname(cwd), '.env'),
    os.path.join(os.path.dirname(cwd), 'Interview-practice-partner-main', '.env'),
])

# Try to load from each path
api_key = None
for env_path in env_paths:
    abs_path = os.path.abspath(env_path)
    if os.path.isfile(abs_path):
        load_dotenv(dotenv_path=abs_path, override=True)
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            break

# If still not found, try default load_dotenv()
if not api_key:
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")

# Final check - if still not found, show error
if not api_key:
    error_details = f"""
    **Current working directory:** `{os.getcwd()}`
    **Script directory:** `{script_dir if script_dir else 'Unknown'}`
    
    **Checked paths:**
    """
    for path in env_paths:
        abs_path = os.path.abspath(path)
        exists = "✓ EXISTS" if os.path.isfile(abs_path) else "✗ Not found"
        error_details += f"\n- {exists}: `{abs_path}`"
    
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.markdown(error_details)
    st.info("💡 **Solution:** Ensure `.env` file exists with: `GROQ_API_KEY=your_key_here`")
    st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# --- PROFESSIONAL UI STYLING ---
st.markdown("""
    <style>
        /* Global Theme - Professional Dark */
        .stApp {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            font-size: 1.05rem;
            line-height: 1.7;
            font-family: "Inter", "Segoe UI", system-ui, sans-serif;
        }
        
        body, p, span, li, label, .stMarkdown p {
            font-size: 1.05rem;
            line-height: 1.8;
        }
        
        .stMarkdown h1 {
            font-size: 2.4rem !important;
        }
        
        .stMarkdown h2 {
            font-size: 1.9rem !important;
        }
        
        .stMarkdown h3 {
            font-size: 1.5rem !important;
        }
        
        .stMarkdown h4 {
            font-size: 1.25rem !important;
        }
        
        .stChatMessage p,
        .stChatMessage span,
        .element-container p {
            font-size: 1.05rem !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(30, 60, 114, 0.9);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Main Content Cards */
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            margin-bottom: 1rem;
        }
        
        /* Chat Messages */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px);
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 1rem !important;
        }
        
        .stChatMessage[data-testid="stChatMessageUser"] {
            background: rgba(42, 82, 152, 0.3) !important;
            border-left: 3px solid #2a5298 !important;
        }
        
        .stChatMessage[data-testid="stChatMessageAssistant"] {
            background: rgba(30, 60, 114, 0.3) !important;
            border-left: 3px solid #1e3c72 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(45deg, #2a5298, #1e3c72);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        /* Instructions Card */
        .instructions {
            background: rgba(42, 82, 152, 0.2);
            border-left: 3px solid #2a5298;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUDIO ENGINE ---
def play_ai_voice(text):
    try:
        # Generate audio in memory
        audio_buffer = BytesIO()
        tts = gTTS(text=text, lang='en')
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Store audio in session state for playback
        audio_bytes = audio_buffer.read()
        st.session_state.last_audio = audio_bytes
        st.session_state.should_play_audio = True
        
        return audio_bytes
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None

# --- 3. STATE MANAGEMENT ---
if "messages" not in st.session_state: st.session_state.messages = []
if "practice_mode" not in st.session_state: st.session_state.practice_mode = "chat"
if "last_audio_hash" not in st.session_state: st.session_state.last_audio_hash = None
if "interview_type" not in st.session_state: st.session_state.interview_type = "general"
if "show_feedback" not in st.session_state: st.session_state.show_feedback = False
if "last_audio" not in st.session_state: st.session_state.last_audio = None
if "should_play_audio" not in st.session_state: st.session_state.should_play_audio = False

# --- 4. PROFESSIONAL SIDEBAR ---
with st.sidebar:
    # Header
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="margin: 0; color: #ffffff;">🤖 Practice Partner</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Interview Practice Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Practice Configuration
    st.markdown("### 🎯 Practice Setup")
    role = st.selectbox(
        "🎯 Target Domain",
        [
            "Computer Science & Technology",
            "Sales & Marketing", 
            "Architecture & Design",
            "Finance & Banking",
            "Healthcare & Medicine",
            "Education & Teaching",
            "Business & Management"
        ],
        help="Choose the domain you're preparing for"
    )
    
    st.session_state.practice_mode = st.selectbox(
        "🎭 Practice Mode", 
        ["chat", "mock_interview"],
        format_func=lambda x: "💬 Chat Practice" if x == "chat" else "🎤 Mock Interview"
    )
    
    if st.session_state.practice_mode == "mock_interview":
        st.session_state.interview_type = st.selectbox(
            "📋 Interview Type",
            ["general", "technical", "system_design"],
            format_func=lambda x: x.replace("_", " ").title()
        )
    
    st.divider()
    
    # Practice Stats
    st.markdown("### 📈 Practice Stats")
    st.metric("Questions Practiced", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_feedback = False
        st.rerun()
    
    # End Interview Button (only for mock interviews)
    # Show button after first question (at least 1 user message and 1 assistant message)
    user_message_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    if st.session_state.practice_mode == "mock_interview" and user_message_count >= 1 and not st.session_state.show_feedback:
        if st.button("🏁 End Interview & Get Feedback", use_container_width=True, type="primary"):
            st.session_state.show_feedback = True
            st.rerun()
    
    st.divider()
    
    # Help Section
    with st.expander("📚 Practice Tips"):
        st.markdown("""
        **Chat Mode:**
        - Ask for specific interview questions
        - Get feedback on your answers
        - Practice explaining concepts
        
        **Mock Interview:**
        - Realistic interview simulation
        - Voice responses with feedback
        - Structured question flow
        """)

# --- 5. MAIN INTERFACE ---

# Hero Section
mode_title = "💬 Chat Practice" if st.session_state.practice_mode == "chat" else "🎤 Mock Interview"
st.markdown(f"""
    <div class="main-card" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖 Interview Practice Partner</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; margin: 0;">{mode_title} for {role}</p>
        <p style="opacity: 0.7; margin-top: 0.5rem;">Practice • Learn • Improve</p>
    </div>
""", unsafe_allow_html=True)

# Chat Interface
chat_container = st.container(height=400)
with chat_container:
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            if st.session_state.practice_mode == "chat":
                st.write(f"👋 Hi! I'm your interview practice partner. I'll help you prepare for {role} interviews. Ask me for practice questions, feedback on answers, or help with specific topics!")
            else:
                st.write(f"🎤 Ready for a mock {st.session_state.interview_type} interview in {role}? I'll ask realistic questions and give you feedback. Let's start!")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Play audio if available and flag is set
    if st.session_state.should_play_audio and st.session_state.last_audio:
        # Convert audio bytes to base64 for HTML embedding
        audio_base64 = base64.b64encode(st.session_state.last_audio).decode()
        # Use HTML audio with autoplay that persists across reruns
        audio_html = f"""
        <audio id="ai_voice_player" autoplay controls style="width: 100%; margin-top: 10px;">
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <script>
            // Ensure audio plays even if page reruns
            (function() {{
                var audio = document.getElementById('ai_voice_player');
                if (audio) {{
                    audio.play().catch(function(error) {{
                        console.log('Autoplay prevented:', error);
                    }});
                }}
            }})();
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        st.session_state.should_play_audio = False  # Reset flag after playing

# Input Methods
col1, col2 = st.columns([3, 1])

with col1:
    # Text Input
    if user_input := st.chat_input("💬 Type your message or question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Domain-specific prompts
        domain_contexts = {
            "Computer Science & Technology": "software development, programming, system design, databases, algorithms, and technical problem-solving",
            "Sales & Marketing": "sales strategies, customer relationship management, market analysis, lead generation, and revenue growth",
            "Architecture & Design": "design principles, project management, client relations, building codes, and creative problem-solving",
            "Finance & Banking": "financial analysis, risk management, investment strategies, regulatory compliance, and market knowledge",
            "Healthcare & Medicine": "patient care, medical knowledge, ethical decisions, healthcare systems, and clinical experience",
            "Education & Teaching": "curriculum development, classroom management, student engagement, educational technology, and learning assessment",
            "Business & Management": "leadership, strategic planning, team management, business operations, and organizational development"
        }
        
        domain_context = domain_contexts.get(role, "general professional skills")
        
        # AI Response
        if st.session_state.practice_mode == "chat":
            system_prompt = f"""
            You are a helpful interview practice partner for {role} domain.
            Focus on {domain_context}.
            Help the user practice by:
            - Providing realistic interview questions specific to {role}
            - Giving constructive feedback on answers
            - Explaining domain-specific concepts and best practices
            - Offering tips for success in {role} interviews
            Be encouraging, specific, and helpful.
            IMPORTANT: Keep responses under 50 words. Be concise and direct.
            """
        else:
            # Interview type specific prompts
            if st.session_state.interview_type == "general":
                system_prompt = f"""
                You are conducting a general interview for {role} domain.
                Ask basic questions about background, experience, and behavioral situations.
                Focus on: "Tell me about yourself", "Why this role?", "Describe a challenge", "Strengths/weaknesses".
                IMPORTANT: Keep responses under 30 words. Be concise.
                """
            elif st.session_state.interview_type == "technical":
                system_prompt = f"""
                You are conducting an advanced technical interview for {role} domain.
                Ask complex technical questions about {domain_context}.
                Focus on advanced concepts, problem-solving, coding challenges, architecture decisions.
                IMPORTANT: Keep responses under 30 words. Be concise.
                """
            else:  # system_design
                system_prompt = f"""
                You are conducting a system design interview for {role} domain.
                Ask ONLY system design questions: "Design a messaging app", "Design a URL shortener", "Design a social media feed".
                Focus on scalability, architecture, databases, load balancing.
                IMPORTANT: Keep responses under 30 words. Be concise.
                """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
        )
        
        ai_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        play_ai_voice(ai_response)
        st.rerun()

with col2:
    # Voice Input
    audio_bytes = audio_recorder(
        text="🎤", 
        recording_color="#e74c3c", 
        neutral_color="#2a5298", 
        icon_size="2x"
    )

if audio_bytes:
        current_hash = hashlib.md5(audio_bytes).hexdigest()
        if current_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = current_hash
            
            with st.spinner("Transcribing..."):
                with open("temp.wav", "wb") as f:
                    f.write(audio_bytes)
                try:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-large-v3-turbo",
                        file=open("temp.wav", "rb")
                    )
                    
                    # Add transcribed message
                    st.session_state.messages.append({"role": "user", "content": transcript.text})
                    
                    # Domain-specific prompts for voice input
                    domain_contexts = {
                        "Computer Science & Technology": "software development, programming, system design, databases, algorithms, and technical problem-solving",
                        "Sales & Marketing": "sales strategies, customer relationship management, market analysis, lead generation, and revenue growth",
                        "Architecture & Design": "design principles, project management, client relations, building codes, and creative problem-solving",
                        "Finance & Banking": "financial analysis, risk management, investment strategies, regulatory compliance, and market knowledge",
                        "Healthcare & Medicine": "patient care, medical knowledge, ethical decisions, healthcare systems, and clinical experience",
                        "Education & Teaching": "curriculum development, classroom management, student engagement, educational technology, and learning assessment",
                        "Business & Management": "leadership, strategic planning, team management, business operations, and organizational development"
                    }
                    
                    domain_context = domain_contexts.get(role, "general professional skills")
                    
                    # Generate AI response
                    if st.session_state.practice_mode == "chat":
                        system_prompt = f"""
                        You are a helpful interview practice partner for {role} domain.
                        Focus on {domain_context}.
                        Help the user practice by providing feedback, questions, and tips.
                        Be encouraging and specific.
                        IMPORTANT: Keep responses under 50 words. Be concise and direct.
                        """
                    else:
                        # Interview type specific prompts for voice input
                        if st.session_state.interview_type == "general":
                            system_prompt = f"""
                            You are conducting a general interview for {role} domain.
                            Ask basic questions about background, experience, and behavioral situations.
                            IMPORTANT: Keep responses under 30 words. Be concise.
                            """
                        elif st.session_state.interview_type == "technical":
                            system_prompt = f"""
                            You are conducting an advanced technical interview for {role} domain.
                            Ask complex technical questions about {domain_context}.
                            IMPORTANT: Keep responses under 30 words. Be concise.
                            """
                        else:  # system_design
                            system_prompt = f"""
                            You are conducting a system design interview for {role} domain.
                            Ask ONLY system design questions about scalability and architecture.
                            IMPORTANT: Keep responses under 30 words. Be concise.
                            """
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
                    )
                    
                    ai_response = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    play_ai_voice(ai_response)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Transcription failed: {e}")

# --- INTERVIEW FEEDBACK ---
if st.session_state.show_feedback and st.session_state.practice_mode == "mock_interview":
    st.markdown("""
        <div class="main-card" style="margin-top: 2rem;">
            <h2 style="text-align: center; margin-bottom: 1rem;">📋 Interview Feedback</h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Analyzing your interview performance..."):
        # Create a comprehensive feedback prompt that analyzes the actual conversation
        conversation_summary = "\n".join([
            f"{'Interviewer' if msg['role'] == 'assistant' else 'Candidate'}: {msg['content']}"
            for msg in st.session_state.messages
        ])
        
        user_responses = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user']
        questions_asked = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'assistant']
        
        feedback_prompt = f"""
You are an experienced interviewer providing honest, constructive feedback on a {st.session_state.interview_type} interview for a {role} position.

**Full Interview Conversation:**
{conversation_summary}

**Instructions for Feedback:**
1. Analyze the ACTUAL conversation above. Base your feedback ONLY on what the candidate actually said and did.
2. Be HONEST and REALISTIC. If the candidate didn't answer questions well, didn't provide examples, or gave incomplete answers, reflect that in your feedback.
3. Only mention strengths if the candidate ACTUALLY demonstrated them in their responses.
4. If the candidate didn't answer questions or gave very brief/poor answers, be honest about it.
5. Provide specific examples from their actual responses when mentioning strengths or weaknesses.

**Provide feedback in this format:**

**Overall Performance Rating:** [Rate 1-10 based on actual performance. Format as "X/10" (e.g., "7/10"). Be honest - if they barely answered, rate low]

**Strengths (only if actually demonstrated):**
- [Only list strengths that were ACTUALLY shown in their answers. If they didn't demonstrate any, say "No clear strengths were demonstrated in this interview."]

**Areas for Improvement:**
- [Be specific about what they did wrong or could improve, based on their actual responses]
- [If they didn't answer questions, mention that specifically]

**Recommendations:**
- [Give specific, actionable advice based on their actual performance]

**Important:** 
- If the candidate didn't answer questions properly or gave incomplete answers, be direct about this.
- Don't make up strengths that weren't demonstrated.
- Base everything on the actual conversation above.
- Be constructive but honest.
"""
        
        feedback_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an experienced, honest interviewer providing realistic feedback based on actual interview performance."},
                {"role": "user", "content": feedback_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        feedback = feedback_response.choices[0].message.content
        
        # Format rating to ensure it's in "X/10" format
        # Replace patterns like "Rating: 7" or "7" with "7/10" in the rating section
        rating_pattern = r'(Overall Performance Rating[:\s]*)(\d+)(?!\s*/\s*10)'
        feedback = re.sub(rating_pattern, r'\1\2/10', feedback, flags=re.IGNORECASE)
        # Also handle cases where it might say "Rating: 7 out of 10" or similar
        feedback = re.sub(r'(Overall Performance Rating[:\s]*)(\d+)\s*(out of|/)\s*10', r'\1\2/10', feedback, flags=re.IGNORECASE)
        
        play_ai_voice(feedback)
        
        st.markdown(f"""
            <div class="main-card">
                {feedback}
            </div>
        """, unsafe_allow_html=True)

# --- ELEVENLABS CONVAI WIDGET ---
st.markdown("---")
st.markdown("### 📞 Live Voice Interview Practice")

# Create two columns for the call feature
call_col1, call_col2 = st.columns([1, 1])

with call_col1:
    with st.container():
        st.markdown("#### 🎯 Live Voice Interview Practice")
        st.markdown("""
        Enhance your interview preparation with our **interactive voice conversation feature**. 
        Engage in natural, real-time dialogue with an AI interviewer that adapts to your responses and provides 
        immediate, personalized feedback.
        """)
        
        st.markdown("#### ✨ What You Get:")
        st.markdown("""
        - **Natural Dialogue:** Speak naturally and receive intelligent, contextual responses
        - **Real-Time Feedback:** Get immediate insights and follow-up questions
        - **Flexible Practice:** Practice anywhere, anytime - no typing required
        - **Adaptive Experience:** The AI adjusts to your responses and skill level
        """)
        
        st.info("""
        💡 **Getting Started:** Click the **"Start Call"** button on the right to begin your voice conversation. 
        The AI interviewer will guide you through practice questions tailored to your selected domain and provide 
        real-time feedback to help you improve.
        """)
        
        st.markdown("""
        **💼 Ideal For:** Behavioral interviews, technical discussions, 
        system design conversations, and comprehensive interview practice across all domains.
        """)

with call_col2:
    st.markdown("""
        <div style="margin-bottom: 0.5rem; text-align: center;">
            <p style="background: linear-gradient(45deg, #2a5298, #1e3c72); color: white; padding: 0.8rem 1.5rem; border-radius: 8px; font-weight: 600; font-size: 1rem; margin: 0;">
                📞 Start a live Call here
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.components.v1.html("""
        <style>
            /* Hide the default "Need help?" text if it appears */
            elevenlabs-convai::part(trigger) {
                display: none !important;
            }
        </style>
        <elevenlabs-convai agent-id="agent_3801kaqeykv2f4sag67c3yv7dpxj"></elevenlabs-convai>
        <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
    """, height=400)