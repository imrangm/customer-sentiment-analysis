# Contributing to Customer Sentiment Analysis

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Sample data (if applicable)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- Clear description of the feature
- Use case and benefits
- Example of how it would work

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests**:
   ```bash
   pytest test_sentiment_analyzer.py
   ```
6. **Ensure code quality**:
   ```bash
   python -m py_compile *.py
   ```
7. **Commit your changes**:
   ```bash
   git commit -m "Add: description of your changes"
   ```
8. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/customer-sentiment-analysis.git
cd customer-sentiment-analysis

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_sentiment_analyzer.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

## Testing

- Add unit tests for new features
- Ensure all tests pass before submitting PR
- Test with both English and Arabic text
- Include edge cases

## Documentation

- Update README.md if adding features
- Add examples to USAGE_EXAMPLES.md
- Update QUICK_START.md if changing installation
- Comment complex code sections

## Areas for Contribution

### High Priority
- Additional language support
- Performance optimizations
- More visualization options
- Export formats (PDF, JSON)
- Real-time analysis API

### Medium Priority
- Batch processing improvements
- Custom model support
- Sentiment intensity scoring
- Topic extraction
- Comparative analysis

### Low Priority
- UI/UX improvements
- Additional chart types
- Dark mode
- Mobile responsiveness
- Integration examples

## Questions?

Feel free to open an issue for any questions or clarifications!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the project goals
- Help others learn and grow

Thank you for contributing! 🙏
