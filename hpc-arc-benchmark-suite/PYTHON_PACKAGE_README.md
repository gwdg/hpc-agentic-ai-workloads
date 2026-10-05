# HPC-ARC Benchmark Suite - Python Package Installation

## Installation

### Primary Installation Method (Recommended)

The HPC-ARC Benchmark Suite is primarily designed to be used via the **`hpc-arc`** command:

```bash
cd hpc-agentic-ai-workloads/hpc-arc-benchmark-suite

# Step 1: Install package (creates hpc-arc command)
pip install --break-system-packages -e .

# OR with virtual environment (recommended)
python3 -m venv hpc-arc-env
source hpc-arc-env/bin/activate
pip install -e .

# Step 2: Use hpc-arc command
hpc-arc --version
hpc-arc status
hpc-arc benchmark --all
```

### Installation Script (Alternative)

For automatic installation with PATH configuration:

```bash
# Use the installation script
bash install_cli.sh --user

# Or install to system directory (requires sudo)
sudo bash install_cli.sh
```

## Usage

### Primary Method: hpc-arc Command

```bash
# All commands start with hpc-arc
hpc-arc                      # Welcome message & commands
hpc-arc --version          # Version check

# Benchmark Commands
hpc-arc benchmark --all                    # All benchmarks
hpc-arc benchmark --name dgemm              # Specific benchmark
hpc-arc benchmark --name dgemm --size 1024  # Custom size

# Phase Commands
hpc-arc phase execute --task EX-051        # Execute Phase
hpc-arc phase explore                    # Explore Phase

# Analysis Commands
hpc-arc analyze --output results.json      # Complete analysis
hpc-arc analyze --intelligence           # Intelligence scores

# Hardware Profiling
hpc-arc profile --tool likwid              # LIKWID profiling

# GPU Commands
hpc-arc gpu --backend cuda                  # NVIDIA execution

# Examples
hpc-arc example dgemm                     # DGEMM demo
hpc-arc example all                       # All examples
```

### Fallback Methods

If `hpc-arc` command is not available, use:

```bash
# Method 2: Direct script execution
./hpc-arc.py

# Method 3: Module execution (less preferred)
python3 -m hpc_arc
```

## Python API Usage

```python
from hpc_arc import run_cli
from hpc_arc import HPCARCCLI

# Method 1: Run CLI programmatically
run_cli()

# Method 2: Use CLI class
cli = HPCARCCLI()
cli.run()
```

## Installation Verification

```bash
# Primary method check
hpc-arc --version

# Check if hpc-arc is in PATH
which hpc-arc

# Check installed package
pip show hpc-arc-benchmark-suite

# Quick test
hpc-arc status
```

## Troubleshooting

### hpc-arc Command Not Found

```bash
# Option 1: Check if installed
which hpc-arc
pip show hpc-arc-benchmark-suite

# Option 2: Add to PATH manually
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Option 3: Use fallback methods
python3 hpc-arc.py
```

### Module Not Found Errors

```bash
# Ensure package is installed
pip install --break-system-packages -e .

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Verify installation
pip show hpc-arc-benchmark-suite
```

### Path Not Configured

```bash
# Add to ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or add to ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify PATH
echo $PATH | grep -q ".local/bin" && echo "✓ PATH configured" || echo "✗ PATH not configured"
```

## Installation Options

### Development Installation
```bash
pip install -e .
```

### Production Installation
```bash
pip install .
```

### With Development Dependencies
```bash
pip install -e ".[dev]"
```

### With GPU Support
```bash
pip install -e ".[gpu]"
```

## Package Structure

```
hpc_arc/
├── __init__.py              # Package initialization
├── __main__.py              # Main entry point (python -m hpc_arc)
└── cli.py                   # CLI module

core/
├── __init__.py              # Core package
└── hpc_arc_benchmark_suite.py  # Benchmark suite

evaluation/
├── __init__.py              # Evaluation package
└── intelligence_metrics.py     # Intelligence metrics

phases/
├── __init__.py              # Phases package
├── explore_phase.py             # Explore phase
├── hypothesize_phase.py         # Hypothesize phase
├── execute_phase.py             # Execute phase
└── generalize_phase.py          # Generalize phase
```

## Version Information

- **Package Name:** hpc-arc-benchmark-suite
- **Version:** 1.0.0
- **Python:** 3.8+
- **Authors:** Anja Gerbes, HPC-ARC Benchmark Suite Team
- **License:** MIT
- **Primary Command:** hpc-arc

## Additional Resources

- GitHub Repository: https://github.com/HPC-ARC/benchmark-suite
- Documentation: https://github.com/HPC-ARC/benchmark-suite#readme
- CLI README: CLI_README.md
- Implementation Status: IMPLEMENTATION_STATUS.md

## Quick Reference

| Method | Command |
|--------|---------|
| **Primary** | `hpc-arc` ✅ |
| **Fallback 1** | `./hpc-arc.py` |
| **Fallback 2** | `python3 -m hpc_arc` |
| **Python API** | `from hpc_arc import run_cli` |

**Primary usage should always be `hpc-arc` command after installation.**
