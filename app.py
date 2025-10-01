"""
Customer Sentiment Analysis Dashboard
Streamlit app for analyzing customer feedback with Arabic support
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analyzer import SentimentAnalyzer, load_data_file
import io

# Page configuration
st.set_page_config(
    page_title="Customer Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load sentiment analysis model (cached)"""
    return SentimentAnalyzer()


def main():
    # Header
    st.markdown('<div class="main-header">📊 Customer Sentiment Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("""
        ### About
        This application analyzes customer feedback sentiment using open-source multilingual models.
        
        **Features:**
        - ✅ Support for CSV and XLSX files
        - ✅ Multilingual support (including Arabic)
        - ✅ Interactive visualizations
        - ✅ Detailed sentiment analysis
        
        ### Instructions
        1. Upload your data file (CSV or XLSX)
        2. Select the column containing customer feedback
        3. Click "Analyze Sentiment"
        4. Explore the results!
        """)
    
    # File upload
    st.header("📁 Upload Customer Feedback Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV or XLSX file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a file containing customer feedback/reviews"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
            
            # Show preview
            with st.expander("📋 Preview Data", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Column selection
            st.header("🔍 Select Text Column")
            text_column = st.selectbox(
                "Select the column containing customer feedback/reviews:",
                options=df.columns.tolist(),
                help="Choose the column that contains the text you want to analyze"
            )
            
            # Sample preview
            if text_column:
                st.markdown("**Sample text from selected column:**")
                sample_text = df[text_column].dropna().iloc[0] if not df[text_column].dropna().empty else ""
                st.info(sample_text)
            
            # Analyze button
            if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
                with st.spinner("Loading model and analyzing sentiment... This may take a few moments."):
                    try:
                        # Load model
                        analyzer = load_model()
                        
                        # Analyze sentiment
                        result_df = analyzer.analyze_dataframe(df, text_column)
                        
                        # Get summary
                        summary = analyzer.get_sentiment_summary(result_df)
                        
                        # Store in session state
                        st.session_state['result_df'] = result_df
                        st.session_state['summary'] = summary
                        st.session_state['text_column'] = text_column
                        
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        return
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return
    
    # Display results if available
    if 'result_df' in st.session_state:
        st.markdown("---")
        display_results(
            st.session_state['result_df'],
            st.session_state['summary'],
            st.session_state['text_column']
        )


def display_results(result_df: pd.DataFrame, summary: dict, text_column: str):
    """Display analysis results with visualizations"""
    
    st.header("📈 Sentiment Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Reviews",
            f"{summary['total_reviews']:,}",
            help="Total number of reviews analyzed"
        )
    
    with col2:
        st.metric(
            "Positive",
            f"{summary['positive']:,}",
            f"{summary['positive_percent']:.1f}%",
            delta_color="normal",
            help="Number and percentage of positive reviews"
        )
    
    with col3:
        st.metric(
            "Neutral",
            f"{summary['neutral']:,}",
            f"{summary['neutral_percent']:.1f}%",
            delta_color="off",
            help="Number and percentage of neutral reviews"
        )
    
    with col4:
        st.metric(
            "Negative",
            f"{summary['negative']:,}",
            f"{summary['negative_percent']:.1f}%",
            delta_color="inverse",
            help="Number and percentage of negative reviews"
        )
    
    # Additional metrics
    col5, col6 = st.columns(2)
    with col5:
        st.metric(
            "Average Confidence",
            f"{summary['average_confidence']:.2%}",
            help="Average confidence score of predictions"
        )
    with col6:
        st.metric(
            "Average Rating",
            f"{summary['average_stars']:.2f} ⭐",
            help="Average star rating (1-5 scale)"
        )
    
    st.markdown("---")
    
    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 Sentiment Distribution")
        
        # Pie chart
        sentiment_counts = result_df['sentiment'].value_counts()
        colors = {'positive': '#2ecc71', 'neutral': '#f39c12', 'negative': '#e74c3c'}
        color_sequence = [colors.get(sent, '#95a5a6') for sent in sentiment_counts.index]
        
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color=sentiment_counts.index,
            color_discrete_map=colors,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_chart2:
        st.subheader("⭐ Star Rating Distribution")
        
        # Bar chart for star ratings
        star_counts = result_df['stars'].value_counts().sort_index()
        fig_bar = px.bar(
            x=star_counts.index,
            y=star_counts.values,
            labels={'x': 'Star Rating', 'y': 'Count'},
            title="Star Rating Distribution",
            color=star_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Confidence distribution
    st.subheader("📉 Confidence Score Distribution")
    fig_hist = px.histogram(
        result_df,
        x='confidence',
        nbins=30,
        title="Distribution of Confidence Scores",
        labels={'confidence': 'Confidence Score', 'count': 'Frequency'},
        color_discrete_sequence=['#3498db']
    )
    fig_hist.update_layout(showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Detailed results table
    st.markdown("---")
    st.subheader("📋 Detailed Results")
    
    # Filter options
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        sentiment_filter = st.multiselect(
            "Filter by sentiment:",
            options=['positive', 'neutral', 'negative'],
            default=['positive', 'neutral', 'negative']
        )
    with col_filter2:
        min_confidence = st.slider(
            "Minimum confidence:",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05
        )
    
    # Apply filters
    filtered_df = result_df[
        (result_df['sentiment'].isin(sentiment_filter)) &
        (result_df['confidence'] >= min_confidence)
    ]
    
    st.write(f"Showing {len(filtered_df)} of {len(result_df)} reviews")
    
    # Display table
    display_columns = [text_column, 'sentiment', 'confidence', 'stars']
    st.dataframe(
        filtered_df[display_columns].style.background_gradient(
            subset=['confidence'],
            cmap='YlGn'
        ),
        use_container_width=True,
        height=400
    )
    
    # Download results
    st.markdown("---")
    st.subheader("💾 Download Results")
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        # CSV download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="sentiment_analysis_results.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_download2:
        # Excel download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name='Results')
            
            # Add summary sheet
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, index=False, sheet_name='Summary')
        
        excel_data = output.getvalue()
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name="sentiment_analysis_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
