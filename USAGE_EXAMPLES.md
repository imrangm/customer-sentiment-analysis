# Usage Examples

This document provides detailed examples of using the Customer Sentiment Analysis tool.

## Example 1: Using the Dashboard

### Step 1: Launch the Application
```bash
streamlit run app.py
```

### Step 2: Upload Your Data
1. Click the "Browse files" button
2. Select your CSV or XLSX file
3. The data preview will show automatically

### Step 3: Analyze
1. Select the column containing customer feedback
2. Click "Analyze Sentiment"
3. Wait for results to appear

### Step 4: Explore and Download
- View interactive charts
- Filter results by sentiment and confidence
- Download results as CSV or Excel

## Example 2: Using the CLI

### Analyze a CSV file with English reviews
```bash
python cli.py customer_reviews.csv analyzed_reviews.csv --text-column feedback
```

### Analyze an Excel file with Arabic reviews
```bash
python cli.py arabic_feedback.xlsx results.xlsx --text-column تعليقات_العملاء
```

### Quick summary without saving results
```bash
python cli.py reviews.csv --text-column comments --summary-only
```

Output:
```
============================================================
SENTIMENT ANALYSIS SUMMARY
============================================================
Total reviews:           100
Positive:                 65 ( 65.0%)
Neutral:                  20 ( 20.0%)
Negative:                 15 ( 15.0%)
Average confidence:      89.3%
Average star rating:     4.12
============================================================
```

## Example 3: Python API Usage

### Basic sentiment analysis
```python
from sentiment_analyzer import SentimentAnalyzer

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Analyze single text
result = analyzer.analyze_text("This product is amazing!")
print(result)
# Output: {'sentiment': 'positive', 'confidence': 0.95, 'stars': 5}

# Analyze Arabic text
result = analyzer.analyze_text("هذا المنتج رائع جدا")
print(result)
# Output: {'sentiment': 'positive', 'confidence': 0.92, 'stars': 5}
```

### Batch analysis with DataFrame
```python
import pandas as pd
from sentiment_analyzer import SentimentAnalyzer, load_data_file

# Load data
df = load_data_file('customer_reviews.csv')

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Analyze all reviews
result_df = analyzer.analyze_dataframe(df, 'customer_feedback')

# Get summary statistics
summary = analyzer.get_sentiment_summary(result_df)
print(f"Positive: {summary['positive_percent']:.1f}%")
print(f"Negative: {summary['negative_percent']:.1f}%")

# Save results
result_df.to_csv('analyzed_results.csv', index=False)
```

## Example 4: Mixed Language Dataset

The tool automatically handles multiple languages in the same dataset:

```python
reviews = [
    "Excellent service, highly recommended!",
    "خدمة ممتازة، أنصح بها بشدة",
    "Très bon produit",
    "Producto excelente",
    "الجودة رديئة جدا",
    "Poor quality, not worth the price"
]

for review in reviews:
    result = analyzer.analyze_text(review)
    print(f"{review[:30]}... -> {result['sentiment']}")
```

Output:
```
Excellent service, highly rec... -> positive
خدمة ممتازة، أنصح بها بشدة... -> positive
Très bon produit... -> positive
Producto excelente... -> positive
الجودة رديئة جدا... -> negative
Poor quality, not worth the p... -> negative
```

## Example 5: Filtering and Analysis

### Filter by sentiment
```python
# Get only negative reviews for further analysis
negative_reviews = result_df[result_df['sentiment'] == 'negative']
print(f"Found {len(negative_reviews)} negative reviews")

# Get low-confidence predictions for manual review
low_confidence = result_df[result_df['confidence'] < 0.7]
print(f"Found {len(low_confidence)} reviews with low confidence")
```

### Aggregate by date or category
```python
# If your data has a date column
result_df['date'] = pd.to_datetime(result_df['date'])
daily_sentiment = result_df.groupby('date')['sentiment'].value_counts().unstack(fill_value=0)
print(daily_sentiment)

# If your data has product categories
category_summary = result_df.groupby('product_category')['sentiment'].value_counts()
print(category_summary)
```

## Example 6: Advanced Filtering in Dashboard

In the dashboard interface, you can:

1. **Filter by sentiment types**: Select which sentiments to display (positive, neutral, negative)
2. **Filter by confidence**: Use the slider to show only high-confidence predictions
3. **Sort results**: Click column headers to sort
4. **Download filtered data**: The download buttons respect your active filters

## Tips for Best Results

1. **Data Quality**: Ensure your text data is clean and meaningful
2. **Column Names**: Use descriptive column names for easier selection
3. **Text Length**: The model handles texts up to 512 characters (longer texts are truncated)
4. **Empty Values**: Empty or null values are automatically handled as neutral sentiment
5. **Mixed Languages**: You can have multiple languages in the same dataset
6. **Batch Size**: For large datasets (>10,000 rows), the CLI is faster than the dashboard
7. **Confidence Threshold**: Consider reviewing predictions with confidence < 0.7 manually

## Common Use Cases

### E-commerce Reviews
Analyze product reviews to identify customer satisfaction trends

### Customer Support Feedback
Monitor support ticket feedback to improve service quality

### Social Media Monitoring
Track brand sentiment across customer comments

### Survey Responses
Analyze open-ended survey responses at scale

### Market Research
Process focus group feedback and customer interviews

## Troubleshooting

### Model Download Issues
If the model fails to download:
1. Check your internet connection
2. Try running the application again (it will retry)
3. The model is cached after first download (~400MB)

### Memory Issues
For very large datasets (>100,000 rows):
1. Use the CLI instead of the dashboard
2. Process data in chunks
3. Consider using a machine with more RAM

### Encoding Issues
If you see encoding errors:
1. Ensure your CSV/Excel files are UTF-8 encoded
2. Use Excel's "CSV UTF-8" format when exporting

### Wrong Sentiment Detection
If results seem incorrect:
1. Check that you selected the correct text column
2. Verify the text is meaningful and not just IDs or codes
3. Remember that the model may interpret sarcasm literally
