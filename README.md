# Markaz - Interactive Finance Assistant

An AI-powered real estate analysis tool that provides insights from the KFH Real Estate Report 2025 Q1.

## 🔧 Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment Variables
Create a `.env` file:
```env
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=your-embedding-deployment
```

### Run Locally
```bash
# Web Interface
streamlit run knowledge/docling/5-chat.py

# Command Line Interface
python knowledge/docling/5-chat-cli.py
```

## 📊 Features

- **AI-Powered Analysis**: Get insights from real estate reports
- **Smart Context Retrieval**: Relevant information from your database
- **Interactive Visualizations**: Charts and graphs when requested
- **Concise Responses**: Focused, to-the-point answers
- **Multiple Interfaces**: Web UI and command-line options

## 📝 Usage Examples

- "What are the rental rates in Salmiya?"
- "Create a chart of property prices"
- "Summarize market trends for 2025"
