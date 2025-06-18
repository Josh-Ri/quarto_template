#!/bin/bash

# Quarto Data Analysis Template Setup Script (macOS)
# This script installs the necessary tools to get started with Quarto data analysis on macOS
#
# This script will:
# - Install Homebrew automatically if not present
# - Add Homebrew to your ~/.zshrc PATH
# - Install Quarto CLI, uv, and Ruff via Homebrew
# - Set up Python dependencies for the project
# - Test render the sample report

set -e  # Exit on any error

echo "🚀 Setting up Quarto Data Analysis Template for macOS..."
echo "======================================================"
echo "This script will install: Homebrew (if needed), Quarto CLI, uv, Ruff, and Python packages"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install and setup Homebrew
install_homebrew() {
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for current session and future sessions
    echo "🔧 Setting up Homebrew in PATH..."
    
    # For Apple Silicon Macs
    if [[ -d "/opt/homebrew" ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
        echo "✅ Added Homebrew to ~/.zshrc (Apple Silicon)"
    # For Intel Macs
    elif [[ -d "/usr/local/bin/brew" ]]; then
        export PATH="/usr/local/bin:$PATH"
        echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
        echo "✅ Added Homebrew to ~/.zshrc (Intel)"
    fi
    
    # Source the updated profile
    if [[ -f ~/.zshrc ]]; then
        source ~/.zshrc
    fi
}

# Check and install Homebrew if needed
echo ""
echo "🍺 Checking Homebrew installation..."
if command_exists brew; then
    echo "✅ Homebrew already installed: $(brew --version | head -n1)"
else
    install_homebrew
    # Verify installation
    if command_exists brew; then
        echo "✅ Homebrew installed successfully: $(brew --version | head -n1)"
    else
        echo "❌ Homebrew installation failed. Please install manually from https://brew.sh"
        exit 1
    fi
fi

# Install Quarto CLI
echo ""
echo "📝 Installing Quarto CLI..."
if command_exists quarto; then
    echo "✅ Quarto already installed: $(quarto --version)"
else
    echo "Installing Quarto via Homebrew..."
    brew install quarto
fi

# Install uv (modern Python package manager)
echo ""
echo "📦 Installing uv (Python package manager)..."
if command_exists uv; then
    echo "✅ uv already installed: $(uv --version)"
else
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for current session and future sessions
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Check if already in .zshrc to avoid duplicates
    if ! grep -q 'export PATH="$HOME/.cargo/bin:$PATH"' ~/.zshrc 2>/dev/null; then
        echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
        echo "✅ Added uv to ~/.zshrc"
    fi
fi

# Install Ruff (Python linter/formatter)
echo ""
echo "🔍 Installing Ruff..."
if command_exists ruff; then
    echo "✅ Ruff already installed: $(ruff --version)"
else
    echo "Installing Ruff via Homebrew..."
    brew install ruff
fi

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
if command_exists uv; then
    echo "Using uv to install dependencies..."
    uv sync
fi

# Verify installations
echo ""
echo "🔍 Verifying installations..."
echo "=============================================="

if command_exists quarto; then
    echo "✅ Quarto: $(quarto --version)"
else
    echo "❌ Quarto: Not found"
fi

if command_exists uv; then
    echo "✅ uv: $(uv --version)"
else
    echo "⚠️  uv: Not found (optional, can use pip instead)"
fi

if command_exists ruff; then
    echo "✅ Ruff: $(ruff --version)"
else
    echo "❌ Ruff: Not found"
fi

if command_exists python; then
    echo "✅ Python: $(python --version)"
else
    echo "❌ Python: Not found"
fi

# Test Quarto rendering
echo ""
echo "🧪 Testing Quarto rendering..."
if command_exists quarto && [ -f "notebooks/report.qmd" ]; then
    echo "Rendering test report..."
    cd notebooks
    quarto render report.qmd --to html
    cd ..
    echo "✅ Test report generated successfully!"
    echo "📄 Open notebooks/report.html in your browser to view the result"
else
    echo "⚠️  Skipping test render (Quarto not found or report.qmd missing)"
fi

echo ""
echo "🎉 Setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Open notebooks/report.qmd in your editor"
echo "2. Install the Quarto extension for VS Code (if using VS Code)"
echo "3. Start customizing the template for your analysis"
echo ""
echo "Useful commands:"
echo "  quarto render notebooks/report.qmd          # Render to HTML"
echo "  quarto render notebooks/report.qmd --to pdf # Render to PDF"
echo "  quarto preview notebooks/report.qmd         # Live preview"
echo "  ruff check src/                             # Check Python code"
echo "  ruff format src/                            # Format Python code"
echo ""
echo "Happy analysing! 🚀" 