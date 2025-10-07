# Installation Guide

## Requirements

- Python 3.8+
- PyTorch 2.0+
- 8GB+ RAM

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/[your-org]/adapt-mad.git
cd adapt-mad
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Download Datasets

```bash
./scripts/download_datasets.sh
```

### 5. Verify Installation

```bash
python quick_start.py
```

## Troubleshooting

### CUDA Issues
```bash
export CUDA_VISIBLE_DEVICES=""  # Use CPU
```

### Import Errors
```bash
pip install -e .
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```
