# Quarto Data Analysis Template (macOS)

A comprehensive template for data analysis projects using Quarto, Python, and modern data tools. Only for macOS. 

It is also recommneded to also install the quarto extension for VScode for some other features (previews etc.)

## 🚀 Quick Start

### Automated Setup

Run the setup script to automatically install all dependencies:

```zsh
chmod +x setup.sh
./setup.sh
```

This will automatically:
- Install Homebrew (if not already installed)
- Install Quarto CLI, uv, and Ruff
- Set up Python dependencies
- Test render the sample report

### Manual Setup (Alternative)

If you prefer manual installation:

1. **Install dependencies:**
   ```bash
   # Install Quarto, uv, and Ruff via Homebrew
   brew install quarto ruff
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install Python dependencies
   uv sync
   ```

2. **Verify installation:**
   ```bash
   quarto render notebooks/report.qmd --to html
   ```

## 📁 Project Structure

```
├── data/
│   ├── 01-bronze/       # Raw, unprocessed data
│   ├── 02-silver/       # Partially processed data
│   └── 03-gold/         # Cleaned, analysis-ready data
├── notebooks/
│   └── report.qmd       # Main Quarto report
├── src/
│   ├── __init__.py
│   └── helper_functions/   # Reusable analysis functions
├── setup.sh             # Automated macOS setup script
├── pyproject.toml       # Project dependencies and metadata
├── uv.lock             # Locked dependencies for reproducibility
└── README.md           # This file
```

## 📈 Example  Workflow

1. **Setup**: Run `./setup.sh` to configure environment
2. **Extract**: Raw data → `data/01-bronze/`
3. **Process**: Clean data → `data/02-silver/` → `data/03-gold/`
4. **Analyse**: Explore patterns in `report.qmd`
5. **Quality**: Check code with `ruff check src/`
6. **Report**: Generate final reports with `quarto render`


### Code Quality
```bash
# Check code quality
ruff check 

# Format code
ruff format 

# Preview report
quarto preview notebooks/report.qmd
```

## 🎯 Output Options

Generate different report formats:

```bash
# HTML report (default)
quarto render notebooks/report.qmd --to html

# PDF report
quarto render notebooks/report.qmd --to pdf

# Live preview with auto-reload
quarto preview notebooks/report.qmd
```

## 📋 Dependencies

Core libraries included:
- **Data Processing**: `polars`, `pandas`, `numpy`
- **Visualisation**: `plotly`, `matplotlib`, `seaborn`
- **Analysis**: `scikit-learn`, `statsmodels`, `scipy`
- **Reports**: `quarto`, `jupyter`, `itables`
- **Quality**: `ruff` for linting and formatting
- **Utilities**: `requests`, modern Python tooling

You can use `uv add` to bring in any addtional dependencies. 

## 🛠️ Customisation

### 1. Update Project Metadata
Edit `pyproject.toml` to change:
- Project name and description
- Author information
- Dependencies (add/remove as needed)

### 2. Add Your Data
- Place raw data in `data/01-bronze/`
- Update data loading paths in `notebooks/report.qmd`
- Create processing scripts in `src/`

### 3. Customize Analysis
- Edit `notebooks/report.qmd` for your specific analysis
- Add helper functions in `src/helper_functions/functions.py`
- Extend visualisations and analysis patterns

## 📈 Example Analysis Workflow

1. **Setup**: Run `./setup.sh` to configure environment
2. **Extract**: Raw data → `data/01-bronze/`
3. **Process**: Clean data → `data/02-silver/` → `data/03-gold/`
4. **Analyse**: Explore patterns in `report.qmd`
5. **Quality**: Check code with `ruff check src/`
6. **Report**: Generate final reports with `quarto render`

## 🔍 Useful Commands

```bash
# Setup and installation
./setup.sh                                  # Full environment setup

# Development
quarto preview notebooks/report.qmd         # Live preview
ruff check src/                             # Code quality check
ruff format src/                            # Format code
uv sync                                     # Update dependencies
uv add                                      # Add dependencies


# Rendering
quarto render notebooks/report.qmd --to html  # HTML output
quarto render notebooks/report.qmd --to pdf   # PDF output
```
