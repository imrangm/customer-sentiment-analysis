"""Setup script for customer sentiment analysis"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="customer-sentiment-analysis",
    version="1.0.0",
    author="imrangm",
    description="Customer sentiment analysis engine with Arabic language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imrangm/customer-sentiment-analysis",
    py_modules=["sentiment_analyzer", "cli"],
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "sentiment-cli=cli:main",
        ],
    },
)
