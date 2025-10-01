#!/bin/bash
# Launch script for Customer Sentiment Analysis Dashboard

echo "🏛️  MOEI Customer Sentiment Analysis Dashboard"
echo "=============================================="
echo ""

# Find and use the correct Python with streamlit installed
PYTHON_CMD="python3"

# Check if we're in a virtualenv
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_CMD="$VIRTUAL_ENV/bin/python3"
# Check for pipenv virtualenv
elif [ -d "$HOME/.local/share/virtualenvs" ]; then
    # Try to find the virtualenv for this project
    VENV_PATH=$(find "$HOME/.local/share/virtualenvs" -name "*Lesson2*" -o -name "*customer-sentiment*" 2>/dev/null | head -1)
    if [ -n "$VENV_PATH" ] && [ -f "$VENV_PATH/bin/python3" ]; then
        PYTHON_CMD="$VENV_PATH/bin/python3"
    fi
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

echo "🚀 Starting the application..."
echo "📊 Dashboard will open at: http://localhost:8501"
echo "⚡ To stop the application, press Ctrl+C"
echo ""

# Launch with the correct python
$PYTHON_CMD -m streamlit run app.py