# Personal AI Copilot 🤖

A full-stack conversational AI system inspired by ChatGPT, Gemini, and Perplexity. This project demonstrates an intelligent AI assistant that provides personalized, context-aware responses by combining real-time web intelligence with local LLM processing.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)

## 🌟 Features

### Core Innovation
- **Personalized Conversational AI**: Creates more natural, friend-like interactions
- **Context-Aware Responses**: Maintains conversation history for coherent multi-turn dialogues
- **Privacy-First Architecture**: Uses local LLM processing (Ollama) to protect user data
- **Real-Time Web Intelligence**: Scrapes and processes current information from the web

### Technical Highlights
- **Multi-Stage AI Pipeline**: 5-stage processing (Query Understanding → Web Search → Content Scraping → Filtering → AI Summarization)
- **Advanced NLP**: Intelligent keyword extraction and query understanding using spaCy
- **Scalable Microservices**: Modular backend design for independent component scaling
- **Modern UI/UX**: ChatGPT-style interface with markdown rendering and syntax highlighting

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  • ChatGPT-style UI  • Markdown Rendering  • Syntax Highlight│
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                  Backend (Flask API)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
│   Query      │  │ Web Search  │  │  Content   │
│ Understanding│  │  (Selenium) │  │  Scraping  │
│   (spaCy)    │  └─────────────┘  │(Beautiful  │
└──────────────┘                   │   Soup)    │
                                   └─────┬──────┘
                                         │
                         ┌───────────────▼────────────────┐
                         │  AI Summarization (Ollama)     │
                         │      Local LLM Processing       │
                         └────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Node.js 16+** and npm
- **Ollama** (for local LLM)
- **Google Chrome** (for web scraping)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/Romio1310/PersonalGPT.git
cd PersonalGPT
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv_clean
source venv_clean/bin/activate  # On Windows: venv_clean\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Copy environment template and configure
cp .env.example .env
# Edit .env with your settings (optional)
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template and configure
cp .env.example .env
# Edit .env if needed (default backend URL is already set)
```

#### 4. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

```bash
# Pull the llama3.1 model
ollama pull llama3.1
```

### Running the Application

#### Start Backend (Terminal 1)
```bash
cd backend
source venv_clean/bin/activate
python app.py
```
Backend will run on `http://localhost:5001`

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```
Frontend will run on `http://localhost:3000`

#### Start Ollama (if not running)
```bash
ollama serve
```

### Access the Application

Open your browser and navigate to `http://localhost:3000`

## 💡 Usage Examples

Try these queries to see the AI pipeline in action:

- **"What are the best AI tools for developers in 2025?"**
- **"Top 5 Python frameworks for web development"**
- **"How to deploy a Flask app to production?"**
- **"Explain how web scraping works"**

The system will:
1. Extract keywords using NLP
2. Search the web for relevant information
3. Scrape and process content from multiple sources
4. Filter the most relevant information
5. Generate intelligent, personalized responses using Ollama

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **spaCy** - Natural Language Processing
- **Selenium** - Web automation for search
- **BeautifulSoup4** - HTML parsing
- **Trafilatura** - Content extraction
- **Ollama** - Local LLM integration
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React** - UI framework
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering
- **React Syntax Highlighter** - Code syntax highlighting

## 📁 Project Structure

```
PersonalGPT/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── app_simple.py          # Simple test server
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── modules/
│       ├── __init__.py
│       ├── query_understanding.py   # NLP keyword extraction
│       ├── web_search.py           # Web search functionality
│       ├── content_scraping.py     # Content scraping
│       ├── pre_filtering.py        # Content filtering
│       └── summarization.py        # AI summarization
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── ChatNew.js     # Main chat interface
│   │   │   ├── Message.js     # Message component
│   │   │   └── Input.js       # Input component
│   │   └── ...
│   ├── package.json
│   └── .env.example
├── .gitignore
└── README.md
```

## 🔒 Security & Privacy

- **Local LLM Processing**: All AI processing happens locally using Ollama
- **No API Keys Required**: Works without cloud AI service API keys
- **Environment Variables**: Sensitive data stored in `.env` files (not tracked in git)
- **No Data Storage**: Conversations are not persisted by default

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues & Limitations

- Web scraping may be blocked by some websites
- Search results depend on internet connection
- Response time varies based on web scraping and LLM processing
- Requires Ollama to be running locally

## 🚧 Future Enhancements

- [ ] Add support for multiple LLM models
- [ ] Implement conversation persistence
- [ ] Add user authentication
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Add support for file uploads
- [ ] Implement caching for faster responses
- [ ] Add more NLP features (sentiment analysis, entity recognition)
- [ ] Mobile-responsive improvements

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Gurdeep Singh**
- LinkedIn: [gurdeep-singh0810](https://www.linkedin.com/in/gurdeep-singh0810/)
- GitHub: [@Romio1310](https://github.com/Romio1310)
- Phone: +91-6283376979

## 🙏 Acknowledgments

- Inspired by ChatGPT, Google Gemini, and Perplexity
- Built with open-source technologies
- Thanks to the amazing communities behind Flask, React, spaCy, and Ollama

## 📧 Contact

For questions or feedback, feel free to reach out!

---

**Note**: This project is for educational purposes and demonstrates full-stack AI development skills. It showcases the ability to design and implement scalable, privacy-focused AI systems similar to those used by major tech companies.
