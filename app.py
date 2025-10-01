import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
import re
from datetime import datetime
import warnings
import base64
from pathlib import Path

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Configure page
st.set_page_config(
    page_title="Customer Sentiment Analysis - MOEI",
    page_icon="🏛️",
    layout="wide"
)

# MOEI Color Scheme (from official branding - lightened for charts)
MOEI_COLORS = {
    'primary': '#DAA520',      # Goldenrod (lighter gold)
    'secondary': '#CD853F',    # Peru (lighter brown)
    'green': '#4CAF50',        # Material Green (lighter, more vibrant)
    'red': '#EF5350',          # Material Red (lighter, softer)
    'accent': '#FFC107',       # Amber (for highlights)
    'background': '#FAFAF8',   # Cream/Off-white
    'text': '#333333'          # Dark Gray
}

# Custom CSS matching MOEI branding
st.markdown(f"""
<style>
    .stApp {{
        background: {MOEI_COLORS['background']};
    }}

    .moei-header {{
        background: white;
        padding: 2rem 1rem;
        border-bottom: 4px solid {MOEI_COLORS['primary']};
        margin-bottom: 2rem;
        text-align: center;
    }}

    .moei-header h1 {{
        color: {MOEI_COLORS['primary']};
        text-align: center;
        margin: 1rem 0 0.5rem 0;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        font-size: 2rem;
    }}

    .moei-header h2 {{
        color: {MOEI_COLORS['text']};
        text-align: center;
        margin: 0;
        font-family: 'Arial', sans-serif;
        font-weight: 400;
        font-size: 1.3rem;
    }}

    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {MOEI_COLORS['primary']};
    }}

    .stMetric {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    /* Update button and elements colors */
    .stButton>button {{
        background-color: {MOEI_COLORS['primary']};
        color: white;
    }}

    .stProgress > div > div {{
        background-color: {MOEI_COLORS['primary']};
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_sentiment_models():
    """Load sentiment analysis models for English and Arabic"""
    models = {}

    with st.spinner('Loading models...'):
        # English model
        try:
            models['english'] = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
        except:
            models['english'] = None

        # Arabic model - using a proven reliable model
        try:
            models['arabic'] = pipeline(
                "sentiment-analysis",
                model="citizenlab/twitter-xlm-roberta-base-sentiment-finetunned",
                device=-1,
                truncation=True,
                max_length=512
            )
        except:
            # Fallback to multilingual model
            try:
                models['arabic'] = pipeline(
                    "sentiment-analysis",
                    model="nlptown/bert-base-multilingual-uncased-sentiment",
                    device=-1,
                    truncation=True,
                    max_length=512
                )
            except:
                models['arabic'] = models['english']

    return models

def detect_language(text):
    """Detect if text is Arabic or English"""
    if pd.isna(text) or not text.strip():
        return 'unknown'

    text = str(text).strip()
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')

    return 'arabic' if arabic_chars > len(text) * 0.3 else 'english'

def analyze_sentiment(text, models):
    """Sentiment analysis with language-specific models"""
    if not text or len(str(text).strip()) < 3:
        return {'label': 'NEUTRAL', 'score': 0.5, 'language': 'unknown'}

    language = detect_language(text)
    text_sample = str(text)[:512]  # More text for better accuracy

    # Choose the right model
    model = models.get(language) or models.get('english')
    if not model:
        return {'label': 'NEUTRAL', 'score': 0.5, 'language': language}

    try:
        result = model(text_sample, truncation=True, max_length=512)[0]
        label = result['label'].upper()
        score = result['score']

        # Normalize labels (handle different model outputs)
        # Handle star ratings (1-5 stars from nlptown model)
        if '5' in label or '4' in label:
            label = 'POSITIVE'
        elif '1' in label or '2' in label:
            label = 'NEGATIVE'
        elif '3' in label:
            # For Arabic, if score is high on 3 stars, check if it's more positive/negative
            if language == 'arabic':
                if score < 0.6:  # Low confidence on neutral, reclassify
                    # Check for positive/negative keywords in Arabic
                    positive_keywords = ['شكر', 'ممتاز', 'جيد', 'رائع', 'مبدع', 'شاكر', 'أحسنت', 'جزيل']
                    negative_keywords = ['سيء', 'مشكل', 'صعب', 'بطيء', 'خطأ', 'فشل']

                    text_lower = text_sample.lower()
                    has_positive = any(word in text_sample for word in positive_keywords)
                    has_negative = any(word in text_sample for word in negative_keywords)

                    if has_positive and not has_negative:
                        label = 'POSITIVE'
                    elif has_negative and not has_positive:
                        label = 'NEGATIVE'
                    else:
                        label = 'NEUTRAL'
                else:
                    label = 'NEUTRAL'
            else:
                label = 'NEUTRAL'
        # Handle standard labels
        elif 'POS' in label or label == 'POSITIVE':
            label = 'POSITIVE'
        elif 'NEG' in label or label == 'NEGATIVE':
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'

        return {'label': label, 'score': score, 'language': language}
    except:
        return {'label': 'NEUTRAL', 'score': 0.5, 'language': language}

def parse_excel_file(file):
    """Parse uploaded Excel file and extract relevant data"""
    try:
        # Try to read all sheets
        excel_file = pd.ExcelFile(file)

        # Look for sheets that might contain feedback data
        feedback_data = []

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet_name)

            # Look for columns that might contain qualitative feedback
            text_columns = []
            for col in df.columns:
                col_lower = str(col).lower()
                # Check for standard feedback keywords
                if any(keyword in col_lower for keyword in
                      ['feedback', 'comment', 'suggestion', 'improvement', 'experience', 'opinion']):
                    text_columns.append(col)
                # Check for Arabic/English Q13 and Q14 patterns (customer pulse specific)
                elif ('q13' in col_lower or 'q14' in col_lower or
                      'anything else' in col_lower or 'تود مشاركتنا' in col or
                      'no-trans' in col_lower):
                    text_columns.append(col)

            if text_columns:
                for col in text_columns:
                    valid_responses = df[df[col].notna() & (df[col] != '')][col].tolist()
                    feedback_data.extend(valid_responses)

        return feedback_data, excel_file.sheet_names
    except Exception as e:
        st.error(f"Error parsing Excel file: {str(e)}")
        return [], []

def get_base64_image(image_path):
    """Convert image to base64 for embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    # Header with logo
    logo_path = Path(__file__).parent / "UAE_MOI.png"

    if logo_path.exists():
        logo_base64 = get_base64_image(logo_path)
        st.markdown(f"""
        <div class="moei-header">
            <img src="data:image/png;base64,{logo_base64}"
                 alt="MOEI Logo"
                 style="max-width: 700px; width: 100%; margin: 0 auto; display: block;">
            <h2 style="margin-top: 1.5rem; color: #333; font-weight: 400;">Customer Sentiment Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="moei-header">
            <h1 style="color: #DAA520; margin: 0;">Ministry of Energy & Infrastructure</h1>
            <h2 style="margin-top: 1rem; color: #333; font-weight: 400;">Customer Sentiment Analysis</h2>
        </div>
        """, unsafe_allow_html=True)

    # File upload section
    st.subheader("📁 Upload Customer Pulse Data")
    uploaded_file = st.file_uploader(
        "Choose an Excel file (.xlsx)",
        type=['xlsx'],
        help="Upload your customer pulse survey data file"
    )

    if uploaded_file is not None:
        with st.spinner('Processing file and analyzing sentiments...'):
            # Parse the uploaded file
            feedback_data, sheet_names = parse_excel_file(uploaded_file)

            if not feedback_data:
                st.warning("No feedback text found in the uploaded file.")
                return

            # Load sentiment models
            models = load_sentiment_models()

            # Process feedback
            results = []
            progress_bar = st.progress(0)

            for i, text in enumerate(feedback_data):
                if text and str(text).strip():
                    sentiment = analyze_sentiment(text, models)
                    results.append({
                        'text': str(text)[:200],
                        'original_text': str(text),
                        'sentiment': sentiment['label'],
                        'confidence': sentiment['score'],
                        'language': sentiment['language'],
                        'length': len(str(text).split())
                    })
                progress_bar.progress((i + 1) / len(feedback_data))

            st.success(f"✅ Processed {len(results)} entries")

            if not results:
                st.warning("No valid feedback text found for analysis.")
                return

            # Create results DataFrame
            df_results = pd.DataFrame(results)

            # Display key metrics
            st.subheader("📊 Key Sentiment Metrics")

            col1, col2, col3, col4 = st.columns(4)

            total_responses = len(df_results)
            positive_count = len(df_results[df_results['sentiment'] == 'POSITIVE'])
            negative_count = len(df_results[df_results['sentiment'] == 'NEGATIVE'])
            neutral_count = total_responses - positive_count - negative_count

            with col1:
                st.metric("Total Responses", total_responses)
            with col2:
                st.metric("Positive", positive_count, f"{positive_count/total_responses*100:.1f}%")
            with col3:
                st.metric("Negative", negative_count, f"{negative_count/total_responses*100:.1f}%")
            with col4:
                st.metric("Neutral", neutral_count, f"{neutral_count/total_responses*100:.1f}%")

            # Combined Sentiment Distribution Section
            st.subheader("📈 Sentiment Distribution")

            # Calculate language counts
            arabic_count = len(df_results[df_results['language'] == 'arabic'])
            english_count = len(df_results[df_results['language'] == 'english'])
            unknown_count = len(df_results[df_results['language'] == 'unknown'])

            # Create three columns for charts
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Overall Sentiment**")
                sentiment_counts = {
                    'Positive': positive_count,
                    'Negative': negative_count,
                    'Neutral': neutral_count
                }
                fig_overall = px.pie(
                    values=list(sentiment_counts.values()),
                    names=list(sentiment_counts.keys()),
                    color_discrete_sequence=[MOEI_COLORS['green'], MOEI_COLORS['red'], MOEI_COLORS['primary']]
                )
                fig_overall.update_layout(
                    font=dict(family="Inter, Arial, sans-serif"),
                    height=300,
                    showlegend=True,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_overall, use_container_width=True)

            with col2:
                st.markdown(f"**Arabic Sentiment** ({arabic_count} responses)")
                arabic_df = df_results[df_results['language'] == 'arabic']
                if len(arabic_df) > 0:
                    ar_pos = len(arabic_df[arabic_df['sentiment'] == 'POSITIVE'])
                    ar_neg = len(arabic_df[arabic_df['sentiment'] == 'NEGATIVE'])
                    ar_neu = len(arabic_df) - ar_pos - ar_neg

                    fig_ar = px.pie(
                        values=[ar_pos, ar_neg, ar_neu],
                        names=['Positive', 'Negative', 'Neutral'],
                        color_discrete_sequence=[MOEI_COLORS['green'], MOEI_COLORS['red'], MOEI_COLORS['primary']]
                    )
                    fig_ar.update_layout(
                        font=dict(family="Inter, Arial, sans-serif"),
                        height=300,
                        showlegend=False,
                        margin=dict(t=0, b=0, l=0, r=0)
                    )
                    st.plotly_chart(fig_ar, use_container_width=True)
                else:
                    st.info("No Arabic responses")

            with col3:
                st.markdown(f"**English Sentiment** ({english_count} responses)")
                english_df = df_results[df_results['language'] == 'english']
                if len(english_df) > 0:
                    en_pos = len(english_df[english_df['sentiment'] == 'POSITIVE'])
                    en_neg = len(english_df[english_df['sentiment'] == 'NEGATIVE'])
                    en_neu = len(english_df) - en_pos - en_neg

                    fig_en = px.pie(
                        values=[en_pos, en_neg, en_neu],
                        names=['Positive', 'Negative', 'Neutral'],
                        color_discrete_sequence=[MOEI_COLORS['green'], MOEI_COLORS['red'], MOEI_COLORS['primary']]
                    )
                    fig_en.update_layout(
                        font=dict(family="Inter, Arial, sans-serif"),
                        height=300,
                        showlegend=False,
                        margin=dict(t=0, b=0, l=0, r=0)
                    )
                    st.plotly_chart(fig_en, use_container_width=True)
                else:
                    st.info("No English responses")

            # Confidence distribution
            st.subheader("🎯 Analysis Confidence")
            fig_hist = px.histogram(
                df_results,
                x='confidence',
                nbins=20,
                title="Confidence Score Distribution",
                color_discrete_sequence=[MOEI_COLORS['primary']]
            )
            fig_hist.update_layout(
                font=dict(family="Inter, Arial, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)


            # Sample feedback by sentiment with language info
            st.subheader("💬 Sample Feedback by Sentiment")

            tab1, tab2, tab3 = st.tabs(["Positive", "Negative", "Neutral"])

            with tab1:
                positive_df = df_results[df_results['sentiment'] == 'POSITIVE']
                # Get unique samples by removing duplicate text
                positive_unique = positive_df.drop_duplicates(subset=['original_text']).head(8)
                if len(positive_unique) > 0:
                    st.markdown(f"**{len(positive_unique)} sample positive responses (unique):**")
                    for _, row in positive_unique.iterrows():
                        lang_flag = "🇸🇦" if row['language'] == 'arabic' else "🇬🇧" if row['language'] == 'english' else "🌐"
                        st.success(f"{lang_flag} **Confidence: {row['confidence']:.2f} | Language: {row['language'].title()}**  \n{row['text']}")
                else:
                    st.info("No positive feedback found.")

            with tab2:
                negative_df = df_results[df_results['sentiment'] == 'NEGATIVE']
                # Get unique samples by removing duplicate text
                negative_unique = negative_df.drop_duplicates(subset=['original_text']).head(8)
                if len(negative_unique) > 0:
                    st.markdown(f"**{len(negative_unique)} sample negative responses (unique):**")
                    for _, row in negative_unique.iterrows():
                        lang_flag = "🇸🇦" if row['language'] == 'arabic' else "🇬🇧" if row['language'] == 'english' else "🌐"
                        st.error(f"{lang_flag} **Confidence: {row['confidence']:.2f} | Language: {row['language'].title()}**  \n{row['text']}")
                else:
                    st.info("No negative feedback found.")

            with tab3:
                neutral_df = df_results[df_results['sentiment'] == 'NEUTRAL']
                # Get unique samples by removing duplicate text
                neutral_unique = neutral_df.drop_duplicates(subset=['original_text']).head(8)
                if len(neutral_unique) > 0:
                    st.markdown(f"**{len(neutral_unique)} sample neutral responses (unique):**")
                    for _, row in neutral_unique.iterrows():
                        lang_flag = "🇸🇦" if row['language'] == 'arabic' else "🇬🇧" if row['language'] == 'english' else "🌐"
                        st.info(f"{lang_flag} **Confidence: {row['confidence']:.2f} | Language: {row['language'].title()}**  \n{row['text']}")
                else:
                    st.info("No neutral feedback found.")

            # Export results
            st.subheader("💾 Export Results")

            # Prepare export data
            export_df = df_results.copy()
            export_df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"sentiment_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()