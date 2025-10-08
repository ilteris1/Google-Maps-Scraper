from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="google-maps-scraper",
    version="1.0.0",
    author="Your Name",
    description="A professional Google Maps scraper for extracting business data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Google-Maps-Scraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.16.0",
        "webdriver-manager>=4.0.1",
        "pandas>=2.1.4",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
        "tqdm>=4.66.1",
    ],
)
