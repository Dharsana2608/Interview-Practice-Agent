# Interview Practice Partner - Project Description

## Website Overview

**Interview Practice Partner** is an AI-powered web application that helps candidates prepare for interviews. Users can practice through chat conversations or participate in realistic mock interviews, receiving personalized feedback based on their actual performance.

---

## Features Implemented

1. **Chat Practice Mode** - Ask questions and get interview-related explanations
2. **Mock Interview Mode** - Realistic interview simulation (General, Technical, System Design)
3. **Voice Input** - Speak answers that are converted to text
4. **Voice Output** - AI responses converted to speech and played back
5. **Live Voice Conversation** - Real-time voice chat with AI interviewer
6. **Multi-Domain Support** - Practice for 7 job domains (CS, Sales, Finance, Healthcare, Education, Architecture, Business)
7. **Realistic Feedback** - Analyzes conversation to give honest performance ratings and suggestions
8. **Session Tracking** - Saves conversation history and practice stats

---

## Technology Stack

**Frontend:** Streamlit, HTML/CSS, JavaScript  
**Backend:** Python, Streamlit  
**AI Services:** Groq API (Llama models), Whisper (Speech-to-text), gTTS (Text-to-speech), ElevenLabs  
**Libraries:** streamlit, openai, python-dotenv, audio-recorder-streamlit, gtts

---

## Core Logic

**1. State Management** - Uses Streamlit session state to save conversations and prevent data loss on page refresh

**2. Audio Processing** - Converts text to speech in memory, stores in session state, plays via HTML5 audio player

**3. AI Conversation** - Sends messages to AI with role/domain context, maintains conversation history for context

**4. Feedback System** - Analyzes full conversation, only mentions demonstrated strengths, gives honest 1-10 ratings with specific examples

**5. Configuration** - Loads API keys from .env file, searches multiple locations, handles cross-platform compatibility

**6. Voice Input** - Records microphone audio, converts to text via Whisper, processes as user input, prevents duplicates with hash checking

---

## How It Works

User selects domain and mode → Types or speaks input → System processes (voice converted to text) → AI generates role-specific response → Response shown as text and speech → Conversation continues with context → In mock interviews, user can end to get feedback → Feedback analyzes conversation and provides honest assessment
