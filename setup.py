"""ADAPT-MAD Setup Script"""
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="adapt-mad",
    version="1.0.0",
    author="Minav Suresh Patel, Rohit Dhawan, Ankush Dhar",
    author_email="contact@adapt-mad.org",
    description="Adaptive Multi-Agent Detection for Performance Anomaly Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adapt-mad/adapt-mad",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "torch>=2.0.1",
        "scikit-learn>=1.3.0",
        "pyyaml>=6.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0", "black>=23.7.0"],
        "docs": ["sphinx>=7.1.0"],
    },
    entry_points={
        "console_scripts": [
            "adapt-mad=quick_start:main",
        ],
    },
)
