# Interview Practice Partner 🤖

## AI-Powered Interview Preparation Assistant

A modern, interactive interview practice platform that helps you prepare for technical interviews through AI-powered conversations and mock interviews.

> 📚 **For Technical Details:** See [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)  
> 📋 **For Project Summary:** See [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

### ✨ Key Features
- **Chat Practice Mode**: Interactive Q&A with personalized feedback
- **Mock Interview Mode**: Realistic interview simulations
- **Voice & Text Input**: Flexible communication options
- **Multi-Role Support**: Backend, Frontend, Full-Stack, DevOps preparation
- **Real-Time Feedback**: Instant responses and improvement suggestions
- **Professional UI**: Modern glassmorphism design

## Prerequisites

- Python 3.7 or higher
- Groq API key (for AI and transcription services)

## Setup Instructions

### 1. Activate Virtual Environment

Since you already have a `venv` folder, activate it:

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies (if not already installed)

If the virtual environment doesn't have all packages, install them:

```bash
pip install streamlit openai python-dotenv audio-recorder-streamlit gtts
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key. You can get one from [Groq's website](https://console.groq.com/).

### 4. Run the Application

Once the virtual environment is activated and the `.env` file is set up, run:

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`.

## 🚀 Practice Modes

### 💬 Chat Practice Mode
- **Interactive Learning**: Ask questions and get detailed explanations
- **Custom Questions**: Request specific interview questions for your role
- **Concept Clarification**: Get help understanding technical concepts
- **Best Practices**: Learn industry standards and approaches
- **Flexible Conversation**: Natural dialogue flow

### 🎤 Mock Interview Mode
- **Realistic Simulation**: Experience actual interview conditions
- **Structured Flow**: Professional question progression
- **Immediate Feedback**: Get constructive criticism after each answer
- **Multiple Types**: Behavioral, Technical, and System Design interviews
- **Voice Practice**: Improve your verbal communication skills

### 🎯 Technical Capabilities
- **Voice Recognition**: Advanced speech-to-text with Groq's Whisper model
- **AI-Powered Responses**: Intelligent feedback and question generation
- **Multi-Role Support**: Tailored questions for different positions
- **Session Management**: Track your practice progress
- **Professional UI**: Clean, distraction-free interface

## 💼 How to Use

### Getting Started
1. **Setup**: Configure your target role in the sidebar
2. **Choose Mode**: Select Chat Practice or Mock Interview
3. **Start Practicing**: Begin with text or voice input
4. **Get Feedback**: Receive personalized responses and tips
5. **Track Progress**: Monitor your practice sessions

### Chat Practice Tips
- Ask: "Give me 5 behavioral questions for a senior developer role"
- Request: "Help me explain microservices architecture"
- Practice: "How should I answer 'Tell me about yourself'?"
- Learn: "What are common mistakes in system design interviews?"

### Mock Interview Tips
- Choose your interview type (Behavioral/Technical/System Design)
- Speak naturally and take your time
- Ask for clarification if needed
- Request feedback on specific areas
- Practice regularly for best results

## 🎯 Practice Examples

### Sample Questions You Can Ask
- "Give me technical questions for a Python developer interview"
- "How do I explain my project experience effectively?"
- "What are good questions to ask the interviewer?"
- "Help me practice system design for a messaging app"
- "Mock interview me for a frontend developer position"

## 📚 Documentation

- **[Technical Documentation](./TECHNICAL_DOCUMENTATION.md)** - Comprehensive technical details, architecture, and implementation
- **[Project Summary](./PROJECT_SUMMARY.md)** - Concise overview for presentations and quick reference

## 🛠️ Technical Stack

- **Python 3.7+** - Core application
- **Streamlit** - Web framework
- **Groq API** - LLM inference (Llama 3.3 70B, Llama 3.1 8B)
- **Whisper Large V3 Turbo** - Speech-to-text
- **gTTS** - Text-to-speech
- **OpenAI SDK** - API integration

## 🔧 Key Technical Features

- **Multi-modal AI Integration:** Text, voice input, and voice output
- **Real-time Processing:** Live transcription and TTS
- **State Management:** Session-based persistence
- **Robust Configuration:** Multi-path .env discovery
- **Evidence-Based Feedback:** Conversation analysis for realistic assessment

## Troubleshooting

- **Port already in use**: Streamlit will automatically use the next available port
- **API errors**: Ensure your `GROQ_API_KEY` is correctly set in the `.env` file
- **Audio issues**: Grant microphone permissions in your browser
- **Transcription problems**: Speak clearly and ensure good audio quality
- **.env file not found**: The app searches multiple locations automatically. Ensure the file is in the project root.

## 📝 Project Structure

```
Interview-practice-partner-main/
├── app.py                      # Main application
├── config.py                   # Configuration templates
├── test_backend.py             # API testing
├── requirements.txt             # Dependencies
├── .env                        # Environment variables (create this)
├── README.md                   # This file
├── TECHNICAL_DOCUMENTATION.md  # Technical details
└── PROJECT_SUMMARY.md         # Project overview
```

## 🎓 Skills Demonstrated

- Full-stack development (Python, Streamlit, HTML/CSS)
- AI/ML integration (LLMs, Speech processing)
- API integration (REST APIs)
- State management and session persistence
- Problem-solving and debugging
- UI/UX design
