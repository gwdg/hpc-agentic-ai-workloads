#!/bin/bash
# hpc-arc wrapper script for global installation
# This wrapper ensures proper Python environment and paths

# Determine the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find the benchmark suite directory
# First check if we're in the same directory as the main python script
if [ -f "$SCRIPT_DIR/hpc-arc.py" ]; then
    HPC_ARC_PYTHON="$SCRIPT_DIR/hpc-arc.py"
    BENCHMARK_DIR="$SCRIPT_DIR"
else
    # Try to find the benchmark suite in parent directories
    CURRENT_DIR="$SCRIPT_DIR"
    while [ "$CURRENT_DIR" != "/" ]; do
        if [ -f "$CURRENT_DIR/hpc-arc.py" ]; then
            HPC_ARC_PYTHON="$CURRENT_DIR/hpc-arc.py"
            BENCHMARK_DIR="$CURRENT_DIR"
            break
        fi
        CURRENT_DIR="$(dirname "$CURRENT_DIR")"
    done
    
    if [ -z "$HPC_ARC_PYTHON" ]; then
        echo "ERROR: hpc-arc.py not found in expected locations"
        exit 1
    fi
fi

# Change to benchmark directory to ensure proper Python path
cd "$BENCHMARK_DIR"

# Determine which Python to use
if [ -n "$HPC_ARC_PYTHON" ]; then
    # Use the same Python interpreter that was used to install
    PYTHON_CMD="python3"
else
    # Try different Python versions
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "ERROR: Python not found"
        exit 1
    fi
fi

# Execute the main HPC-ARC Python script with all arguments
exec "$PYTHON_CMD" "$HPC_ARC_PYTHON" "$@"