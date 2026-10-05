#!/bin/bash
# HPC-ARC CLI Global Installation Script
# This script installs the hpc-arc CLI as a global command: hpc-arc

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        HPC-ARC BENCHMARK SUITE - CLI INSTALLATION                ║"
echo "║   Global installation: hpc-arc command (primary usage)         ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Detect installation directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Installation directory: $SCRIPT_DIR"
echo ""

# Installation options
USE_VENV=false
AUTO_PATH_SETUP=true
SKIP_INSTALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --venv)
            USE_VENV=true
            shift
            ;;
        --no-path-setup)
            AUTO_PATH_SETUP=false
            shift
            ;;
        --skip-install)
            SKIP_INSTALL=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --venv              Create and activate virtual environment"
            echo "  --no-path-setup     Skip automatic PATH configuration"
            echo "  --skip-install      Skip pip install (use existing installation)"
            echo "  --help              Show this help message"
            echo ""
            echo "Primary Usage (after installation):"
            echo "  hpc-arc              # Run HPC-ARC CLI"
            echo "  hpc-arc --version   # Check version"
            echo "  hpc-arc status      # System status"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Virtual environment setup
if [ "$USE_VENV" = true ]; then
    echo "────────────────────────────────────────────────────────────────"
    echo "Setting up virtual environment..."
    echo "────────────────────────────────────────────────────────────────"
    
    VENV_DIR="$SCRIPT_DIR/hpc-arc-env"
    
    if [ -d "$VENV_DIR" ]; then
        echo "✓ Virtual environment already exists: $VENV_DIR"
        source "$VENV_DIR/bin/activate"
    else
        echo "Creating virtual environment: $VENV_DIR"
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
    fi
    
    echo "✓ Virtual environment activated: $(which python3)"
    echo ""
fi

# Python package installation
if [ "$SKIP_INSTALL" = false ]; then
    echo "────────────────────────────────────────────────────────────────"
    echo "Installing HPC-ARC Python package..."
    echo "────────────────────────────────────────────────────────────────"
    
    # Check if pyproject.toml exists
    if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
        echo "ERROR: pyproject.toml not found in $SCRIPT_DIR"
        exit 1
    fi
    
    # Install package in development mode
    echo "Installing package..."
    pip install --break-system-packages -e "$SCRIPT_DIR" || {
        echo "✗ Installation failed!"
        echo "   Make sure you have Python 3.8+ and pip installed"
        exit 1
    }
    
    echo "✓ Package installed successfully"
    echo ""
fi

# Check installation
echo "────────────────────────────────────────────────────────────────"
echo "Verifying installation..."
echo "────────────────────────────────────────────────────────────────"

# Check if package is installed
if pip show hpc-arc-benchmark-suite > /dev/null 2>&1; then
    VERSION=$(pip show hpc-arc-benchmark-suite | grep Version | awk '{print $2}')
    echo "✓ Package installed: hpc-arc-benchmark-suite v$VERSION"
else
    echo "✗ Package not found in pip list"
    exit 1
fi

# Check if hpc-arc command is available
HPC_ARC_FOUND=false
AVAILABLE_LOCATIONS=()

# Check common installation locations
CHECK_DIRS=(
    "$HOME/.local/bin"
    "/usr/local/bin"
    "/usr/bin"
    "$HOME/.local/bin"
)

for dir in "${CHECK_DIRS[@]}"; do
    if [ -f "$dir/hpc-arc" ]; then
        AVAILABLE_LOCATIONS+=("$dir/hpc-arc")
        HPC_ARC_FOUND=true
        break
    fi
done

if [ "$HPC_ARC_FOUND" = true ]; then
    echo "✓ hpc-arc found at: ${AVAILABLE_LOCATIONS[0]}"
else
    echo "⚠ hpc-arc command not found in standard locations"
    echo "  This is normal if PATH is not configured yet"
fi

echo ""

# PATH configuration
if [ "$AUTO_PATH_SETUP" = true ]; then
    echo "────────────────────────────────────────────────────────────────"
    echo "Configuring PATH..."
    echo "────────────────────────────────────────────────────────────────"
    
    # Detect shell type
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
        SHELL_TYPE="zsh"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
        SHELL_TYPE="bash"
    else
        SHELL_CONFIG="$HOME/.profile"
        SHELL_TYPE="generic"
    fi
    
    LOCAL_BIN="$HOME/.local/bin"
    
    # Check if PATH is already configured
    if grep -q "$LOCAL_BIN" "$SHELL_CONFIG" 2>/dev/null; then
        echo "✓ PATH already configured in $SHELL_CONFIG"
    else
        echo "Adding $LOCAL_BIN to PATH in $SHELL_CONFIG"
        
        echo "" >> "$SHELL_CONFIG"
        echo "# HPC-ARC Benchmark Suite" >> "$SHELL_CONFIG"
        echo "export PATH=\"$LOCAL_BIN:\$PATH\"" >> "$SHELL_CONFIG"
        
        echo "✓ PATH configuration added to $SHELL_CONFIG"
        echo "  Please restart your shell or run: source $SHELL_CONFIG"
    fi
    
    # Test PATH (current session)
    if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
        echo ""
        echo "⚠ Current session PATH not yet updated"
        echo "  Adding $LOCAL_BIN to current PATH for immediate use"
        export PATH="$LOCAL_BIN:$PATH"
    else
        echo "✓ Current session PATH already includes $LOCAL_BIN"
    fi
    
    echo ""
fi

# Final verification
echo "────────────────────────────────────────────────────────────────"
echo "Testing hpc-arc command..."
echo "────────────────────────────────────────────────────────────────"

# Try to run hpc-arc
if command -v hpc-arc &> /dev/null; then
    echo "✓ hpc-arc command available"
    
    # Test version command
    VERSION_OUTPUT=$(hpc-arc --version 2>&1)
    if [ $? -eq 0 ]; then
        echo "✓ Version check successful:"
        echo "  $VERSION_OUTPUT"
    else
        echo "⚠ Version check failed, but command is available"
    fi
else
    echo "⚠ hpc-arc command not found in current PATH"
    echo "  This is normal if you just installed"
    echo "  Please restart your shell or source your config file"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              HPC-ARC CLI INSTALLATION COMPLETE                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Installation Summary:"
echo "  ✓ Package: hpc-arc-benchmark-suite"
echo "  ✓ Primary command: hpc-arc"
echo "  ✓ Installation method: pip install -e ."
echo "  ✓ Virtual environment: $([ "$USE_VENV" = true ] && echo "yes ($VENV_DIR)" || echo "no")"
echo "  ✓ PATH configured: $([ "$AUTO_PATH_SETUP" = true ] && echo "yes" || echo "no")"
echo ""
echo "Primary Usage (recommended):"
echo "  hpc-arc              # Run HPC-ARC CLI"
echo "  hpc-arc --version   # Check version"
echo "  hpc-arc status      # System status"
echo "  hpc-arc --help      # Show help"
echo ""
echo "Available Commands:"
echo "  hpc-arc benchmark           # Execute benchmarks"
echo "  hpc-arc phase execute       # Run execute phase"
echo "  hpc-arc analyze             # Analyze results"
echo "  hpc-arc profile             # Hardware profiling"
echo "  hpc-arc gpu                 # GPU benchmarks"
echo "  hpc-arc example dgemm       # Run examples"
echo ""
if [ ! command -v hpc-arc &> /dev/null ]; then
    echo "⚠ IMPORTANT: Restart your shell or run:"
    echo "  source ~/$([ "$SHELL_TYPE" = "bash" ] && echo ".bashrc" || echo ".zshrc")"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi
echo "Happy Benchmarking with HPC-AI!"
