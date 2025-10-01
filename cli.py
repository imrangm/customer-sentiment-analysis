#!/usr/bin/env python3
"""
Command-line interface for sentiment analysis
Usage: python cli.py input.csv output.csv --text-column customer_feedback
"""

import argparse
import sys
from sentiment_analyzer import SentimentAnalyzer, load_data_file


def main():
    parser = argparse.ArgumentParser(
        description='Analyze customer sentiment from CSV/XLSX files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze CSV file
  python cli.py input.csv output.csv --text-column feedback
  
  # Analyze Excel file
  python cli.py data.xlsx results.xlsx --text-column reviews
  
  # Display summary only
  python cli.py input.csv --text-column feedback --summary-only
        """
    )
    
    parser.add_argument('input_file', help='Input CSV or XLSX file')
    parser.add_argument('output_file', nargs='?', help='Output file (CSV or XLSX)')
    parser.add_argument(
        '--text-column',
        '-t',
        required=True,
        help='Name of column containing text to analyze'
    )
    parser.add_argument(
        '--summary-only',
        '-s',
        action='store_true',
        help='Display summary only without saving results'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.summary_only and not args.output_file:
        parser.error('output_file is required unless --summary-only is specified')
    
    try:
        # Load data
        print(f"Loading data from {args.input_file}...")
        df = load_data_file(args.input_file)
        print(f"✓ Loaded {len(df)} rows\n")
        
        # Initialize analyzer
        print("Loading sentiment analysis model...")
        analyzer = SentimentAnalyzer()
        print("✓ Model loaded\n")
        
        # Analyze sentiment
        print(f"Analyzing sentiment in column '{args.text_column}'...")
        result_df = analyzer.analyze_dataframe(df, args.text_column)
        print("✓ Analysis complete\n")
        
        # Get summary
        summary = analyzer.get_sentiment_summary(result_df)
        
        # Display summary
        print("=" * 60)
        print("SENTIMENT ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Total reviews:        {summary['total_reviews']}")
        print(f"Positive:             {summary['positive']:4d} ({summary['positive_percent']:5.1f}%)")
        print(f"Neutral:              {summary['neutral']:4d} ({summary['neutral_percent']:5.1f}%)")
        print(f"Negative:             {summary['negative']:4d} ({summary['negative_percent']:5.1f}%)")
        print(f"Average confidence:   {summary['average_confidence']:5.1%}")
        print(f"Average star rating:  {summary['average_stars']:.2f}")
        print("=" * 60)
        
        # Save results
        if not args.summary_only:
            print(f"\nSaving results to {args.output_file}...")
            if args.output_file.endswith('.csv'):
                result_df.to_csv(args.output_file, index=False)
            else:
                result_df.to_excel(args.output_file, index=False)
            print("✓ Results saved successfully")
        
        print("\n✓ Done!")
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
