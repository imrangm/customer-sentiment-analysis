# Quick Start Guide

Get started with Customer Sentiment Analysis in 5 minutes!

## 📋 Prerequisites

- Python 3.8 or higher installed
- Internet connection (for first-time model download)
- Your customer feedback data in CSV or XLSX format

## 🚀 Installation Steps

### 1. Get the Code

```bash
# Clone the repository
git clone https://github.com/imrangm/customer-sentiment-analysis.git
cd customer-sentiment-analysis
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

This will install:
- Streamlit (web dashboard)
- Transformers (AI models)
- PyTorch (deep learning)
- Pandas (data processing)
- Plotly (visualizations)
- Other utilities

**Note**: First-time installation may take a few minutes as it downloads ML libraries.

## 🎯 Quick Test with Sample Data

### Option A: Dashboard (Recommended for Beginners)

1. **Start the dashboard**:
   ```bash
   streamlit run app.py
   ```

2. **Your browser will open automatically** at `http://localhost:8501`

3. **Upload the sample data**:
   - Click "Browse files"
   - Select `sample_data.csv`
   - Preview shows your data ✓

4. **Select column**:
   - Choose "customer_feedback" from dropdown
   - Preview shows sample text ✓

5. **Analyze**:
   - Click "🚀 Analyze Sentiment"
   - Wait ~30 seconds for first-time model download
   - See results! 📊

### Option B: Command Line (For Advanced Users)

```bash
# Quick analysis with summary
python cli.py sample_data.csv --text-column customer_feedback --summary-only
```

Expected output:
```
============================================================
SENTIMENT ANALYSIS SUMMARY
============================================================
Total reviews:           20
Positive:                10 ( 50.0%)
Neutral:                  4 ( 20.0%)
Negative:                 6 ( 30.0%)
Average confidence:      87.5%
Average star rating:     3.25
============================================================
```

## 📁 Prepare Your Own Data

### CSV Format
Create a CSV file with at least one column containing text:

```csv
id,feedback,date
1,Great product!,2024-01-15
2,هذا المنتج رائع,2024-01-16
3,Not satisfied,2024-01-17
```

### Excel Format
Create an Excel file with similar structure:

| ID | Customer Feedback | Date |
|----|-------------------|------|
| 1  | Amazing quality   | 2024-01-15 |
| 2  | خدمة ممتازة      | 2024-01-16 |

### Data Tips

✅ **DO:**
- Include meaningful text in feedback column
- Use UTF-8 encoding for non-English text
- Have column headers in first row
- Keep feedback text under 512 characters for best results

❌ **DON'T:**
- Use empty or null values (they'll be marked as neutral)
- Mix feedback with system codes or IDs
- Forget column headers

## 🎨 Understanding the Dashboard

### Main Sections

**1. File Upload Area**
- Drag & drop or browse for your file
- Supported: CSV, XLSX, XLS
- Preview appears after upload

**2. Configuration**
- Select text column from dropdown
- Preview sample text
- Click "Analyze Sentiment" button

**3. Results Dashboard**
- **Top Metrics**: Quick overview (total, positive, neutral, negative)
- **Charts**: Visual representations
  - Pie chart: Sentiment distribution
  - Bar chart: Star ratings
  - Histogram: Confidence scores
- **Data Table**: Detailed results with filters
- **Download Buttons**: Export as CSV or Excel

### Interactive Features

- **Filter by sentiment**: Show only positive/negative/neutral
- **Filter by confidence**: Adjust slider for minimum confidence
- **Sort columns**: Click headers to sort
- **Download**: Get results in your preferred format

## 🌍 Supported Languages

The system supports **100+ languages** including:

- **Arabic** (العربية) ✓
- **English** ✓
- **French** (Français)
- **German** (Deutsch)
- **Spanish** (Español)
- **Dutch** (Nederlands)
- **Italian** (Italiano)
- **Portuguese** (Português)
- **Russian** (Русский)
- **Chinese** (中文)
- And many more!

**Mixed language support**: You can have reviews in different languages in the same file.

## 📊 Understanding Results

### Sentiment Labels
- **Positive**: Customer is satisfied (4-5 stars)
- **Neutral**: Customer is indifferent (3 stars)
- **Negative**: Customer is dissatisfied (1-2 stars)

### Confidence Score
- **0.9-1.0**: Very confident (90-100%)
- **0.7-0.9**: Confident (70-90%)
- **0.5-0.7**: Moderate confidence (50-70%)
- **<0.5**: Low confidence (review manually)

### Star Rating
- **5 stars**: Extremely positive
- **4 stars**: Positive
- **3 stars**: Neutral/Mixed
- **2 stars**: Negative
- **1 star**: Extremely negative

## 🔧 Troubleshooting

### Issue: Model won't download
**Solution**: 
- Check internet connection
- Wait and retry (HuggingFace may be temporarily busy)
- Model is ~400MB, may take a few minutes

### Issue: "Column not found" error
**Solution**:
- Verify column name spelling
- Check for hidden characters or spaces
- Ensure file has headers

### Issue: Results seem incorrect
**Solution**:
- Verify you selected correct text column
- Check that text is actual feedback (not IDs or codes)
- Note: Sarcasm may be interpreted literally

### Issue: Out of memory
**Solution**:
- Use CLI instead of dashboard for large files
- Process data in smaller batches
- Close other applications

### Issue: Encoding errors with Arabic/special characters
**Solution**:
- Save CSV as "UTF-8" encoding
- Use Excel's "CSV UTF-8" format
- Verify text displays correctly before upload

## 💡 Next Steps

1. **Try with your data**: Upload your customer feedback file
2. **Explore visualizations**: Understand trends in your data
3. **Export results**: Download analyzed data for further processing
4. **Automate**: Use CLI for batch processing
5. **Integrate**: Import the Python module in your own scripts

## 🆘 Need Help?

- **Documentation**: See README.md for detailed info
- **Examples**: Check USAGE_EXAMPLES.md for code samples
- **Issues**: Report bugs on GitHub Issues
- **Questions**: Open a discussion on GitHub

## 🎉 Success Checklist

After following this guide, you should be able to:

- [x] Install the application
- [x] Run the dashboard
- [x] Upload a data file
- [x] Analyze sentiment
- [x] View and interpret results
- [x] Download analyzed data
- [x] Use the CLI for batch processing

**Congratulations! You're ready to analyze customer sentiment! 🎊**
