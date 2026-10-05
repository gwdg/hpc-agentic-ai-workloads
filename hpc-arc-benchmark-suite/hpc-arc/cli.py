#!/usr/bin/env python3
"""
HPC-ARC CLI Module

This module provides the command-line interface for the HPC-ARC Benchmark Suite.
It can be called directly (./hpc-arc.py) or installed as a system command (hpc-arc).

Main entry point for CLI installation via pip/setuptools.

Primary Usage (after installation):
  hpc-arc                        # Run CLI via installed command
  hpc-arc --version              # Check version
  hpc-arc status                 # System status

Fallback Methods (if hpc-arc not available):
  python3 hpc-arc.py             # Direct script execution
  python3 -m hpc_arc             # Module execution

Available Commands:
  benchmark                  Execute HPC-ARC benchmarks
  phase execute/explore/hypothesize/generalize  # Run specific phase
  analyze                    Analyze results and generate intelligence scores
  profile                    Hardware profiling (LIKWID/perf)
  gpu                        GPU benchmark execution
  example dgemm/fft/all      # Example benchmarks
  status                     System status check
  --version                  Show version
  help                       Display help information

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
    """Main entry point for HPC-ARC CLI
    
    This function is invoked by:
    1. The 'hpc-arc' command (installed by pip via entry_points) - PRIMARY
    2. Direct execution: python3 hpc-arc.py - FALLBACK
    3. Module execution: python3 -m hpc_arc - FALLBACK
    
    Primary usage should be 'hpc-arc' command after installation via pip.
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
        if not sys.argv[0].endswith('hpc-arc'):
            print("\n📝 For installation help: bash install_cli.sh", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ Permission denied: {e}", file=sys.stderr)
        print("\n💡 Ensure file permissions are correct.", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"❌ Import error: {e}", file=sys.stderr)
        print("\n💡 Install dependencies: pip install -r requirements.txt", file=sys.stderr)
        print("\n📝 For installation help: bash install_cli.sh", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ HPC-ARC CLI error: {e}", file=sys.stderr)
        
        # Show traceback in verbose mode
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        else:
            print("\n💡 Run with --verbose for detailed error information", file=sys.stderr)
            if not sys.argv[0].endswith('hpc-arc'):
                print("\n📝 For installation help: bash install_cli.sh", file=sys.stderr)
            
        sys.exit(1)

if __name__ == "__main__":
    main()
