# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a customer sentiment analysis project for the Ministry of Energy and Infrastructure. The project uses open source models from Hugging Face for sentiment analysis, leveraging small but effective models that provide excellent performance for this task. The repository is currently empty and ready for initial development.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### Common Commands
- **Run the application**: `streamlit run app.py` or `./run_app.sh`
- **Test Arabic sentiment**: `python3 test_arabic.py`
- **Test data parsing**: `python3 test_data.py`
- **Examine file structure**: `python3 examine_columns.py`
- **Access dashboard**: Open browser to `http://localhost:8501`

### Project Structure
```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── test_data.py          # Data exploration script
├── examine_columns.py    # Column analysis utility
└── CLAUDE.md            # This file
```

## Architecture Notes

**Technology Stack**:
- **Frontend**: Streamlit (rapid prototyping, government-appropriate styling)
- **Data Processing**: Pandas + OpenPyXL for Excel file handling
- **ML Models**: Hugging Face Transformers (cardiffnlp/twitter-roberta-base-sentiment-latest)
- **Visualizations**: Plotly (interactive charts), WordCloud, Matplotlib
- **Deployment**: Local hosting with option to deploy to government cloud

**Data Pipeline Architecture**:
1. **Input**: Excel files (.xlsx) from Customer Pulse surveys
2. **Parsing**: Automatic detection of Q13/Q14 qualitative feedback columns
3. **Processing**: Text cleaning and preprocessing
4. **Analysis**: Sentiment classification using pre-trained models
5. **Output**: Interactive dashboard with metrics, visualizations, and CSV export

**Customer Pulse Data Structure**:
- **Q13**: "هل هناك شيء آخر تود مشاركتنا به؟" (Is there anything else you would like to share with us?)
- **Q14**: Additional qualitative feedback responses
- **Processing**: Handles Arabic and English text, supports bilingual analysis

## Model Recommendations

**Arabic Sentiment Models** (Primary):
- **asafaya/bert-base-arabic-v2**: Primary Arabic model - handles MSA and dialects well
- **nlptown/bert-base-multilingual-uncased-sentiment**: Fallback multilingual model
- **CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment**: Alternative Arabic-specific model

**English Sentiment Models**:
- **cardiffnlp/twitter-roberta-base-sentiment-latest**: Robust for social media-style text
- **distilbert-base-uncased-finetuned-sst-2-english**: Lightweight and fast fallback

**Multilingual Support**:
- Automatic language detection using Unicode character analysis
- Arabic text detection with >30% Arabic characters threshold
- Supports mixed-language documents
- Language-specific model selection for optimal accuracy

## Important Considerations

- This project handles government data - ensure all security and privacy requirements are met
- Follow Ministry of Energy and Infrastructure coding standards and practices
- Consider scalability requirements for processing customer feedback at scale