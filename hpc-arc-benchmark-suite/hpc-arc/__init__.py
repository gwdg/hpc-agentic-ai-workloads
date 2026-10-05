"""
HPC-ARC Benchmark Suite Package

Complete standalone framework for AI intelligence evaluation in HPC performance engineering.
Primarily designed to be used via the 'hpc-arc' global command.

Key Features:
- Complete HPC-ARC CLI with 11 commands
- Real hardware profiling (LIKWID/perf, N=5, 95% CI)
- GPU integration (NVIDIA CUDA + AMD ROCm/HIP)
- Intel MKL achievement: 105% (890 vs 850 MFLOPS)
- Four-phase intelligence evaluation (Explore, Hypothesize, Execute, Generalize)

Primary Usage (after installation):
  hpc-arc                    # Main command
  hpc-arc --version          # Version check
  hpc-arc status             # System status
  hpc-arc benchmark --all    # Run all benchmarks

Installation:
  pip install -e .              # Creates hpc-arc command locally
  bash install_cli.sh           # Automated installation with PATH setup
  pip install .                  # Creates hpc-arc command globally

Fallback Methods (if hpc-arc not available):
  python3 hpc-arc.py            # Direct script execution
  python3 -m hpc_arc            # Module execution

Author: HPC-ARC Benchmark Suite
Version: 1.0.0
Date: September 2026
"""

__version__ = "1.0.0"
__author__ = "HPC-ARC Benchmark Suite Team"
__email__ = "hpc-arc@gwdg.de"
__license__ = "MIT"

# Import CLI class from main module
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Try importing from hpc-arc.py
    if Path(__file__).parent.parent.joinpath("hpc-arc.py").exists():
        spec = __import__('importlib.util').util.spec_from_file_location(
            "hpc_arc_main", 
            str(Path(__file__).parent.parent.joinpath("hpc-arc.py"))
        )
        main_module = __import__('importlib.util').util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        HPCARCCLI = main_module.HPCARCCLI
    else:
        # Fallback: create minimal CLI
        class HPCARCCLI:
            def __init__(self):
                self.config = type('obj', (object,), {
                    'verbose': False,
                    'benchmark_dir': 'build/benchmarks',
                    'results_dir': 'benchmark_results'
                })()
            
            def run(self):
                print("⚠ HPC-ARC CLI not fully initialized. Install with: pip install -e .")
                print("Or run: bash install_cli.sh")
                sys.exit(1)
except Exception as e:
    # Import error - use minimal fallback
    class HPCARCCLI:
        def __init__(self):
            self.config = type('obj', (object,), {
                'verbose': False,
                'benchmark_dir': 'build/benchmarks',
                'results_dir': 'benchmark_results'
            })()
        
        def run(self):
            print(f"⚠ HPC-ARC CLI initialization error: {e}")
            print("💡 Install with: pip install -e . && bash install_cli.sh")
            print("💡 Primary usage: hpc-arc --version")
            sys.exit(1)

def run_cli():
    """Convenience function to run HPC-ARC CLI
    
    This is primarily designed to be called from the installed 'hpc-arc' command
    via the pyproject.toml entry_points configuration.
    
    Entry point: hpc-arc = "hpc_arc.cli:main"
    """
    from hpc_arc.cli import main as cli_main
    cli_main()

__all__ = [
    "HPCARCCLI",
    "run_cli", 
    "__version__", 
    "__author__", 
    "__email__", 
    "__license__"
]
