# Contributing to PersonalGPT 🤝

Thank you for your interest in contributing to PersonalGPT! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [What We're Looking For](#what-were-looking-for)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Community Guidelines](#community-guidelines)

## 🎯 About the Project

**PersonalGPT** is a full-stack conversational AI system that combines:
- Real-time web intelligence (search & scraping)
- Advanced NLP processing (spaCy)
- Local LLM integration (Ollama)
- Modern React UI with ChatGPT-style interface

**Goal:** Create a privacy-first, personalized AI assistant that provides context-aware responses by intelligently processing web information.

## 🔍 What We're Looking For

We welcome contributions in these areas:

### High Priority 🔥
- [ ] **Performance Optimization** - Faster web scraping and response times
- [ ] **Caching System** - Redis/memory caching for repeated queries
- [ ] **Error Handling** - Better error messages and fallback mechanisms
- [ ] **Mobile Responsiveness** - Improve UI for mobile devices
- [ ] **Testing** - Unit tests, integration tests, end-to-end tests
- [ ] **Documentation** - Code comments, API docs, tutorials

### Medium Priority 🎯
- [ ] **Multi-LLM Support** - Support for different AI models (GPT-4, Claude, etc.)
- [ ] **Conversation Persistence** - Save and restore chat history
- [ ] **User Authentication** - Login system with user profiles
- [ ] **Voice Input/Output** - Speech-to-text and text-to-speech
- [ ] **Source Citation** - Better tracking and display of information sources
- [ ] **Dark/Light Theme** - UI theme switcher

### Advanced Features 🚀
- [ ] **Cloud Deployment** - Docker, Kubernetes, AWS/Azure/GCP guides
- [ ] **API Rate Limiting** - Prevent abuse and manage resources
- [ ] **Advanced NLP** - Sentiment analysis, entity recognition, summarization
- [ ] **File Upload Support** - Process documents, PDFs, images
- [ ] **Multi-language Support** - Internationalization (i18n)
- [ ] **Analytics Dashboard** - Usage statistics and insights

## 🚀 How to Contribute

### 1. Fork the Repository
```bash
# Click "Fork" button on GitHub, then:
git clone https://github.com/YOUR_USERNAME/PersonalGPT.git
cd PersonalGPT
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# Or for bug fixes:
git checkout -b fix/bug-description
```

### 3. Make Your Changes
- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 4. Test Your Changes
```bash
# Backend tests (if you add them)
cd backend
source venv_clean/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: Add amazing new feature

- Detailed description of what changed
- Why the change was needed
- Any breaking changes or dependencies"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request!

## 💻 Development Setup

### Prerequisites
- Python 3.12+
- Node.js 16+
- Ollama installed
- Google Chrome (for Selenium)

### Backend Setup
```bash
cd backend
python3 -m venv venv_clean
source venv_clean/bin/activate  # Windows: venv_clean\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

### Ollama Setup
```bash
# Install from https://ollama.ai
ollama pull llama3.1
ollama serve
```

## 📝 Coding Standards

### Python (Backend)
- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions small and focused
- Use meaningful variable names

```python
def extract_keywords(query: str) -> list[str]:
    """
    Extract relevant keywords from user query using NLP.
    
    Args:
        query: User's search query
        
    Returns:
        List of extracted keywords
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)
- Use **functional components** with hooks
- Follow **ESLint** rules
- Use **camelCase** for variables and functions
- Use **PascalCase** for components
- Add **PropTypes** or TypeScript types

```javascript
const MessageComponent = ({ text, sender }) => {
  // Implementation
};

MessageComponent.propTypes = {
  text: PropTypes.string.isRequired,
  sender: PropTypes.string.isRequired
};
```

### General
- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple, Stupid)
- **SOLID** principles
- Write self-documenting code

## 🔄 Pull Request Process

1. **Ensure your PR:**
   - Has a clear title and description
   - Links to related issues (if any)
   - Includes tests (if applicable)
   - Updates documentation (if needed)
   - Passes all checks and tests

2. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   How has this been tested?
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] No new warnings generated
   ```

3. **Review Process:**
   - Maintainer will review within 2-3 days
   - Address any requested changes
   - Once approved, PR will be merged

## 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check if the bug has already been reported
- Ensure you're using the latest version
- Try to reproduce the bug

**Bug Report Template:**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots
If applicable

## Environment
- OS: [e.g., macOS 13.0]
- Browser: [e.g., Chrome 120]
- Python version: [e.g., 3.12]
- Node version: [e.g., 18.0]

## Additional Context
Any other relevant information
```

## 💡 Suggesting Features

**Feature Request Template:**
```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should it work?

## Alternatives Considered
What other solutions did you consider?

## Additional Context
Mockups, examples, references
```

## 🤝 Community Guidelines

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Harassment, trolling, or insulting comments
- Personal or political attacks
- Publishing others' private information
- Any conduct inappropriate in a professional setting

### Enforcement

Project maintainers will:
- Clarify standards of acceptable behavior
- Take appropriate action for unacceptable behavior
- Remove, edit, or reject contributions that don't align with guidelines

## 📞 Contact

- **Project Maintainer:** Gurdeep Singh
- **Email:** Sharymann1329@gmail.com
- **LinkedIn:** [gurdeep-singh0810](https://www.linkedin.com/in/gurdeep-singh0810/)
- **GitHub:** [@Romio1310](https://github.com/Romio1310)

## 🎓 Learning Resources

New to contributing? Here are some helpful resources:

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Contributions Tutorial](https://github.com/firstcontributions/first-contributions)
- [Git and GitHub Tutorial](https://guides.github.com/)
- [Python Best Practices](https://docs.python-guide.org/)
- [React Documentation](https://react.dev/)

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated! Together, we can build an amazing AI assistant that helps people access information in a personalized, privacy-focused way.

Happy coding! 🚀
