# ⚖️ Legal Document Review Assistant

A comprehensive AI-powered legal document analysis and review system that helps legal professionals analyze contracts, extract clauses, assess risks, and get intelligent suggestions for improvement.

## 🌟 Features

### 📄 Document Management
- **Multi-format Support**: Upload PDF, DOCX, and TXT documents
- **Automatic Text Extraction**: Intelligent extraction of text from various document formats
- **Document Organization**: Categorize and manage multiple legal documents
- **Batch Processing**: Upload and analyze multiple documents simultaneously

### 🤖 AI-Powered Analysis
- **Clause Extraction**: Automatically identify and extract legal clauses from documents
- **Risk Assessment**: AI-powered risk analysis with scoring (0-10 scale)
- **Clause Classification**: Categorize clauses by type (Indemnity, Liability, Termination, Payment, etc.)
- **Plain English Explanations**: Convert complex legal language into understandable terms
- **Smart Suggestions**: AI recommendations for improving clause clarity and legal protection

### 📊 Interactive Analytics Dashboard
- **Visual Analytics**: Interactive charts and graphs using Plotly
- **Risk Distribution**: Visualize risk levels across documents and clauses
- **Clause Type Analysis**: Distribution and analysis of different clause types
- **Temporal Trends**: Track document analysis over time
- **Document Comparison**: Compare clauses across different documents

### ✏️ Advanced Clause Editor
- **Rich Text Editing**: Full editing capabilities for clause text
- **Real-time Validation**: Instant feedback on changes and improvements
- **Bulk Editing**: Edit multiple clauses simultaneously
- **Version Control**: Track changes and maintain edit history
- **Export Options**: Export edited clauses and analysis data

### 🔍 Smart Search & Insights
- **Semantic Search**: Find relevant clauses using natural language queries
- **Advanced Filtering**: Filter by risk level, clause type, document, and date
- **Search Analytics**: Visualize search results and patterns
- **Similarity Analysis**: Find similar clauses across documents

### 🎨 Modern User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Professional Styling**: Clean, corporate design suitable for legal professionals
- **Interactive Components**: Smooth animations and hover effects
- **Accessibility**: WCAG compliant design for inclusive access

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # SQLAlchemy database configuration
├── models.py               # Pydantic models and SQLAlchemy schemas
├── routes/
│   ├── health.py           # Health check endpoints
│   ├── upload.py           # Document upload endpoints
│   ├── analyze.py          # Clause analysis endpoints
│   └── search.py           # Semantic search endpoints
└── services/
    ├── clause_extractor.py # Clause extraction logic
    ├── llm_service.py      # AI/LLM integration
    ├── risk_analyzer.py    # Risk assessment algorithms
    └── semantic_search.py  # Search functionality
```

### Frontend (Streamlit)
```
frontend/
├── app.py                  # Main Streamlit application
├── api_client.py           # Backend API client
└── components/
    ├── charts.py           # Data visualization components
    ├── clause_editor.py    # Clause editing interface
    └── sidebar.py          # Navigation and filtering
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested on Python 3.11)
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd legal-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the template and add your real API key
   cp backend/.env.example backend/.env
   # Then edit backend/.env and replace the placeholder with your key
   ```

5. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

6. **Start the frontend application**
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501
   ```
   The web interface will be available at `http://localhost:8501`

## 📖 Usage Guide

### 1. Document Upload
- Navigate to the "Document Upload & Analysis" page
- Select PDF, DOCX, or TXT files to upload
- The system will automatically extract text and analyze the documents
- View upload progress and analysis results

### 2. Clause Review
- Go to the "Clause Review & Analysis" page
- Select a document to review
- Choose view mode: Plain English, Technical, or Both
- Review individual clauses with AI explanations and suggestions
- Edit clauses using the advanced editor

### 3. Analytics Dashboard
- Access the "Interactive Analytics Dashboard"
- View comprehensive analytics and visualizations
- Use filters to analyze specific documents or time periods
- Export analytics data and charts

### 4. Search & Insights
- Use the "Smart Search & Insights" page
- Enter natural language queries to find relevant clauses
- Apply advanced filters for precise results
- View search analytics and patterns

## 🔧 Configuration

### Environment Variables
Copy `backend/.env.example` to `backend/.env` and fill in your values:

```env
# Required — get yours at https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here
```

> ⚠️ **Never commit `.env` to version control.** The `.gitignore` already blocks it.

### API Keys
- **Gemini API**: Required for AI-powered analysis. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Development

### Backend Development
```bash
cd backend
python main.py
```

### Frontend Development
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Database Management
The application uses SQLite by default. Database files are created automatically:
- `legal_docs.db` - Main database file
- Tables are created automatically on first run

### API Documentation
Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📊 API Endpoints

### Health Check
- `GET /health` - Service health status

### Document Upload
- `POST /api/upload` - Upload and process documents
- `GET /api/documents` - List all uploaded documents

### Analysis
- `POST /api/analyze/{document_id}` - Analyze document for clauses
- `GET /api/clauses` - Get all extracted clauses
- `PUT /api/clauses/{clause_id}` - Update clause information

### Search
- `POST /api/search` - Semantic search across clauses

## 🎯 Key Features Explained

### AI-Powered Clause Extraction
The system uses advanced NLP techniques to:
- Identify legal clause boundaries
- Classify clause types automatically
- Extract key terms and conditions
- Assess risk levels using machine learning

### Risk Assessment Algorithm
Our proprietary risk scoring system evaluates:
- Language complexity and ambiguity
- Liability exposure levels
- Missing protective clauses
- Industry-standard compliance

### Plain English Translation
Converts complex legal language into:
- Simple, understandable explanations
- Key points and implications
- Actionable insights
- Contextual examples

### Smart Suggestions Engine
Provides intelligent recommendations for:
- Risk reduction strategies
- Clarity improvements
- Legal compliance enhancements
- Best practice implementations

## 🔒 Security & Privacy

### Data Protection
- All uploaded documents are processed locally
- No data is sent to external services except for AI analysis
- Database is encrypted and secure
- User sessions are managed securely

### API Security
- CORS protection configured
- Input validation and sanitization
- Rate limiting (configurable)
- Error handling without data exposure

## 🚀 Deployment

### Production Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Set up reverse proxy (nginx recommended)
4. Configure SSL certificates
5. Set up monitoring and logging

### Docker Deployment
```dockerfile
# Example Dockerfile for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation for new features
- Ensure backward compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language model capabilities
- **Streamlit** for the excellent web framework
- **FastAPI** for the high-performance API framework
- **Plotly** for interactive data visualizations
- **SQLAlchemy** for robust database management

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation and FAQ

## 🔄 Version History

### v1.0.0 (Current)
- Initial release with core functionality
- AI-powered clause extraction and analysis
- Interactive dashboard and analytics
- Advanced clause editor with suggestions
- Semantic search capabilities
- Plain English explanations
- Bulk editing and export features

---

**Built with ❤️ for the legal community**

*Empowering legal professionals with AI-driven document analysis and review tools.*