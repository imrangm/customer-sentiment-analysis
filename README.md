# Customer Sentiment Analysis 📊

A powerful, open-source customer sentiment analysis engine with **Arabic language support** and interactive dashboard visualization.

## ✨ Features

- 📁 **File Support**: Upload CSV or XLSX files containing customer feedback
- 🌍 **Multilingual**: Support for Arabic, English, and multiple other languages
- 🤖 **Open Source Models**: Uses state-of-the-art Hugging Face Transformers
- 📊 **Interactive Dashboard**: Beautiful Streamlit-based visualization
- 📈 **Comprehensive Analytics**: Sentiment distribution, confidence scores, star ratings
- 💾 **Export Results**: Download analyzed data as CSV or Excel
- 🎯 **High Accuracy**: Powered by BERT-based multilingual models

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/imrangm/customer-sentiment-analysis.git
cd customer-sentiment-analysis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Launch the dashboard:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Dashboard Application (Recommended)

#### 1. Prepare Your Data

Your data file (CSV or XLSX) should contain at least one column with customer feedback text. Example:

| review_id | customer_feedback | date |
|-----------|------------------|------|
| 1 | The product is excellent! | 2024-01-15 |
| 2 | هذا المنتج رائع جدا | 2024-01-16 |
| 3 | Terrible experience | 2024-01-17 |

#### 2. Upload Your File

- Click on "Choose a CSV or XLSX file" button
- Select your data file
- Preview the data to ensure it loaded correctly

#### 3. Select Text Column

- Choose the column containing customer feedback/reviews from the dropdown
- Preview sample text to confirm selection

#### 4. Analyze Sentiment

- Click "Analyze Sentiment" button
- Wait for the model to load and process the data
- View comprehensive results and visualizations

#### 5. Explore Results

The dashboard provides:
- **Key Metrics**: Total reviews, positive/neutral/negative counts and percentages
- **Sentiment Distribution**: Pie chart showing sentiment breakdown
- **Star Ratings**: Bar chart with 1-5 star distribution
- **Confidence Scores**: Histogram of prediction confidence
- **Detailed Table**: Filterable table with all results
- **Download Options**: Export results as CSV or Excel

### Command-Line Interface (CLI)

For batch processing or automation, use the CLI:

```bash
# Basic usage
python cli.py input.csv output.csv --text-column customer_feedback

# Excel files
python cli.py data.xlsx results.xlsx --text-column reviews

# Display summary only (no output file)
python cli.py input.csv --text-column feedback --summary-only

# Short form
python cli.py input.csv output.csv -t feedback
```

After installation with setup.py, you can also use:
```bash
sentiment-cli input.csv output.csv --text-column feedback
```

## 🧪 Testing with Sample Data

A sample data file (`sample_data.csv`) is included with mixed English and Arabic reviews. Use it to test the application:

1. Start the app: `streamlit run app.py`
2. Upload `sample_data.csv`
3. Select "customer_feedback" column
4. Click "Analyze Sentiment"

## 🔧 Technical Details

### Architecture

```
customer-sentiment-analysis/
├── app.py                      # Streamlit dashboard application
├── sentiment_analyzer.py       # Core sentiment analysis engine
├── cli.py                      # Command-line interface
├── test_sentiment_analyzer.py  # Unit tests
├── requirements.txt            # Python dependencies
├── setup.py                    # Installation script
├── sample_data.csv            # Sample data for testing
├── .gitignore                 # Git ignore patterns
└── README.md                  # Documentation
```

### Models

The application uses `nlptown/bert-base-multilingual-uncased-sentiment`, a BERT-based model trained on reviews in multiple languages including:
- English
- Arabic
- Dutch
- German
- French
- Spanish

### Sentiment Classification

Reviews are classified into three categories:
- **Positive**: 4-5 stars
- **Neutral**: 3 stars
- **Negative**: 1-2 stars

Each prediction includes:
- Sentiment label (positive/neutral/negative)
- Confidence score (0-1)
- Star rating (1-5)

## 📦 Dependencies

- **streamlit**: Web dashboard framework
- **transformers**: Hugging Face transformers for NLP models
- **torch**: PyTorch deep learning framework
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file support
- **plotly**: Interactive visualizations
- **scikit-learn**: Machine learning utilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for providing open-source NLP models
- Streamlit for the excellent dashboard framework
- The open-source community for their invaluable tools and libraries

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for better customer insights