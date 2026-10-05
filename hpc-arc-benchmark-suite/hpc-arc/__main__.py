#!/usr/bin/env python3
"""
HPC-ARC Benchmark Suite - Main Entry Point

This module serves as the main entry point for the HPC-ARC Benchmark Suite.
Primarily designed to be called via the installed 'hpc-arc' command.

Installation:
  pip install -e .              # Creates hpc-arc command in ~/.local/bin/
  pip install .                  # Creates hpc-arc command in system bin/
  
Usage:
  hpc-arc                        # Primary method: using installed command
  hpc-arc --version              # Check version
  hpc-arc status                 # System status
  hpc-arc benchmark --all        # Run all benchmarks

Fallback Methods:
  python3 hpc-arc.py             # Direct script execution
  python3 -m hpc_arc             # Module execution (if PATH not configured)

Available Commands:
  benchmark                      # Execute benchmarks
  phase execute/explore/hypothesize/generalize  # Run specific phases
  analyze                        # Analyze results and generate intelligence scores
  profile                        # Hardware profiling (LIKWID/perf)
  gpu                            # GPU benchmarks
  example dgemm/fft/all          # Examples
  status                         # System status
  --version                      # Show version
  help                           # Display help information

Author: HPC-ARC Benchmark Suite
Version: 1.0.0
Date: September 2026
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Main entry point for HPC-ARC Benchmark Suite
    
    This function is invoked by:
    1. The 'hpc-arc' command (installed by pip via entry_points)
    2. Direct execution: python3 hpc-arc.py
    3. Module execution: python3 -m hpc_arc
    
    Primary usage should be 'hpc-arc' command after installation.
    """
    try:
        # Import the CLI class from the main module
        from hpc_arc import HPCARCCLI
        
        # Create CLI instance
        cli = HPCARCCLI()
        
        # Execute CLI
        cli.run()
        
    except KeyboardInterrupt:
        print("\n\nHPC-ARC Benchmark Suite interrupted by user.")
        sys.exit(130)
    except FileNotFoundError as e:
        print(f"❌ System file not found: {e}", file=sys.stderr)
        print("\n💡 Try running 'hpc-arc status' to check system setup.", file=sys.stderr)
        print("\n📝 For installation help: python3 hpc-arc.py --help", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ Permission denied: {e}", file=sys.stderr)
        print("\n💡 Ensure file permissions are correct.", file=sys.stderr)
        print("\n📝 For installation help: python3 hpc-arc.py --help", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"❌ Import error: {e}", file=sys.stderr)
        print("\n💡 Install dependencies: pip install -r requirements.txt", file=sys.stderr)
        print("\n📝 For installation help: python3 hpc-arc.py --help", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ HPC-ARC CLI error: {e}", file=sys.stderr)
        
        # Show traceback in verbose mode
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        else:
            print("\n💡 Run with --verbose for detailed error information", file=sys.stderr)
            print("\n📝 For installation help: python3 hpc-arc.py --help", file=sys.stderr)
            
        sys.exit(1)

if __name__ == "__main__":
    main()
