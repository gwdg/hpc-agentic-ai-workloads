#!/usr/bin/env python3
"""
HPC-ARC Benchmark Suite - Command Line Interface

Complete CLI tool for HPC-ARC benchmark execution and analysis.
Similar structure to PASCIT CLI but adapted for HPC-ARC methodology.

Usage: hpc-arc [command] [options]

Available Commands:
  benchmark    Execute HPC-ARC benchmarks
  phase        Run specific phase (explore/hypothesize/execute/generalize)
  analyze      Analyze benchmark results and generate intelligence scores
  profile      Hardware profiling and analysis
  gpu          GPU benchmark execution
  status       Check system status and available benchmarks
  help         Show help information

Author: HPC-ARC Benchmark Suite
Date: September 2026
Version: 1.0.0
"""

import os
import sys
import argparse
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# HPC-ARC Framework imports (handle optional dependencies gracefully)
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.hpc_arc_benchmark_suite import HPCARCBenchmarkSuite, TaskContext, BenchmarkPhase
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Core framework not available: {str(e)[:50]}")
    CORE_AVAILABLE = False
    HPCARCBenchmarkSuite = None
    TaskContext = None
    BenchmarkPhase = None

try:
    from evaluation.intelligence_metrics import HPCARCEvaluator
    EVALUATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Evaluation framework not available: {str(e)[:50]}")
    EVALUATION_AVAILABLE = False
    HPCARCEvaluator = None

@dataclass
class CLIRunConfig:
    """Configuration for HPC-ARC CLI execution"""
    benchmark_dir: str = "build/benchmarks"
    results_dir: str = "benchmark_results"
    iterations: int = 5  # N=5 from HPC-ARC specification
    size: int = 2048  # Default problem size
    confidence_interval: float = 0.95
    statistical_validation: bool = True
    verbose: bool = False
    output_format: str = "human"  # human, json, yaml

class HPCARCCLI:
    """HPC-ARC Benchmark Suite Command Line Interface"""
    
    def __init__(self):
        self.config = CLIRunConfig()
        
        # Initialize framework components (handle optional dependencies)
        self.benchmark_suite = HPCARCBenchmarkSuite() if CORE_AVAILABLE else None
        self.evaluator = HPCARCEvaluator() if EVALUATION_AVAILABLE else None
        
        if not CORE_AVAILABLE:
            print("⚠ Warning: Core framework not available - some features limited")
        if not EVALUATION_AVAILABLE:
            print("⚠ Warning: Evaluation framework not available - intelligence scoring disabled")
        
        # Ensure directories exist
        Path(self.config.results_dir).mkdir(exist_ok=True)
        
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            prog='hpc-arc',
            description='HPC-ARC Benchmark Suite CLI - Complete high-performance computing intelligence evaluation',
            epilog='Execute HPC-ARC benchmarks, analyze results, and assess artificial HPC intelligence.'
        )
        
        parser.add_argument('--version', action='version', version='HPC-ARC Benchmark Suite 1.0.0')
        parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
        parser.add_argument('--config', '-c', help='Configuration file path')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # BENCHMARK COMMAND
        benchmark_parser = subparsers.add_parser('benchmark', help='Execute HPC-ARC benchmarks')
        benchmark_parser.add_argument('--name', '-n', help='Specific benchmark name')
        benchmark_parser.add_argument('--size', '-s', type=int, default=2048, help='Problem size')
        benchmark_parser.add_argument('--iterations', '-i', type=int, default=5, help='Number of iterations')
        benchmark_parser.add_argument('--all', '-a', action='store_true', help='Run all benchmarks')
        
        # PHASE COMMAND
        phase_parser = subparsers.add_parser('phase', help='Run specific HPC-ARC phase')
        phase_parser.add_argument('phase_name', choices=['explore', 'hypothesize', 'execute', 'generalize'],
                                help='Phase to execute')
        phase_parser.add_argument('--task', '-t', help='Task ID (e.g., EX-051)')
        
        # ANALYZE COMMAND
        analyze_parser = subparsers.add_parser('analyze', help='Analyze benchmark results')
        analyze_parser.add_argument('--results', '-r', help='Results file/directory')
        analyze_parser.add_argument('--output', '-o', help='Output file (JSON format)')
        analyze_parser.add_argument('--intelligence', action='store_true', help='Calculate intelligence scores')
        
        # PROFILE COMMAND
        profile_parser = subparsers.add_parser('profile', help='Hardware profiling and analysis')
        profile_parser.add_argument('--tool', '-t', choices=['likwid', 'perf', 'all'], default='all',
                                  help='Profilig tool to use')
        profile_parser.add_argument('--group', '-g', help='Profiling group (e.g., MEM, CACHE, FLOPS)')
        
        # GPU COMMAND
        gpu_parser = subparsers.add_parser('gpu', help='GPU benchmark execution')
        gpu_parser.add_argument('--backend', '-b', choices=['cuda', 'hip', 'auto'], default='auto',
                              help='GPU backend to use')
        gpu_parser.add_argument('--size', '-s', type=int, default=256, help='GPU problem size')
        
        # STATUS COMMAND
        status_parser = subparsers.add_parser('status', help='Check system status')
        status_parser.add_argument('--detailed', '-d', action='store_true', help='Show detailed status')
        
        # EXAMPLE COMMAND
        example_parser = subparsers.add_parser('example', help='Run HPC-ARC examples')
        example_parser.add_argument('example_name', choices=['dgemm', 'fft', 'stencil', 'all'],
                                  help='Example to run')
        
        return parser.parse_args()
    
    def run(self):
        """Main CLI execution"""
        args = self.parse_arguments()
        
        if args.verbose:
            self.config.verbose = True
        
        if not args.command:
            self.print_welcome()
            self.print_available_commands()
            return
        
        # Dispatch based on command
        command_map = {
            'benchmark': self.run_benchmark,
            'phase': self.run_phase,
            'analyze': self.run_analyze,
            'profile': self.run_profile,
            'gpu': self.run_gpu,
            'status': self.run_status,
            'example': self.run_example
        }
        
        command_func = command_map.get(args.command)
        if command_func:
            try:
                result = command_func(args)
                self.print_result(result, args.command)
            except Exception as e:
                if self.config.verbose:
                    import traceback
                    traceback.print_exc()
                print(f"Error executing command '{args.command}': {str(e)}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            self.print_available_commands()
            sys.exit(1)
    
    def print_welcome(self):
        """Print welcome message"""
        print("""
╔════════════════════════════════════════════════════════════════╗
║     HPC-ARC BENCHMARK SUITE - COMMAND LINE INTERFACE            ║
║  High-Performance Computing Abstraction and Reasoning         ║
║            Challenge (Intelligence Evaluation)                  ║
╚════════════════════════════════════════════════════════════════╝

Version: 1.0.0 (September 2026)
Framework: Four-phase intelligence evaluation methodology
Benchmarks: 113 tasks across Explore, Hypothesize, Execute, Generalize phases
        """)
    
    def print_available_commands(self):
        """Print available commands"""
        print("Available Commands:")
        print("  benchmark     Execute HPC-ARC benchmarks")
        print("  phase         Run specific phase (explore/hypothesize/execute/generalize)")
        print("  analyze       Analyze benchmark results and generate intelligence scores")
        print("  profile       Hardware profiling and analysis")
        print("  gpu           GPU benchmark execution")
        print("  status        Check system status and available benchmarks")
        print("  example       Run HPC-ARC examples")
        print("  help          Show help information")
        print()
        print("Usage Examples:")
        print("  hpc-arc benchmark --all                    # Run all benchmarks")
        print("  hpc-arc benchmark --name dgemm              # Run specific benchmark")
        print("  hpc-arc phase execute --task EX-051        # Run execute phase")
        print("  hpc-arc analyze --intelligence              # Analyze with intelligence scoring")
        print("  hpc-arc profile --tool likwid --group MEM  # Run LIKWID memory profiling")
        print("  hpc-arc gpu --backend cuda                  # Run GPU benchmarks")
        print("  hpc-arc example dgemm                      # Run DGEMM optimization example")
        print("  hpc-arc status --detailed                   # Show detailed system status")
    
    def print_result(self, result: Dict, command: str):
        """Print execution result"""
        if not result:
            print(f"\n✗ Command '{command}' failed to produce results")
            return
        
        success = result.get('success', False)
        if success:
            print(f"\n✓ Command '{command}' completed successfully")
        else:
            print(f"\n✗ Command '{command}' failed: {result.get('error', 'Unknown error')}")
        
        # Print key metrics for successful executions
        if success and command in ['benchmark', 'analyze', 'phase']:
            self.print_performance_metrics(result)
    
    def print_performance_metrics(self, result: Dict):
        """Print performance metrics from result"""
        if 'performance' in result:
            perf = result['performance']
            print(f"Performance Metrics:")
            print(f"  Execution Time: {perf.get('time_ms', 0):.2f} ms")
            print(f"  Performance: {perf.get('mflops', 0):.1f} MFLOPS")
            
            if 'intelligence' in result:
                intel = result['intelligence']
                print(f"  Intelligence Score: {intel.get('intelligence_score', 0):.3f}")
                print(f"  Tier: {intel.get('tier', 'UNKNOWN')}")
    
    def run_benchmark(self, args) -> Dict:
        """Execute HPC-ARC benchmarks"""
        print(f"\n{'='*70}")
        print(f"HPC-ARC BENCHMARK EXECUTION")
        print(f"{'='*70}")
        
        results = []
        
        # Map benchmark names to executables
        benchmark_map = {
            'naive_dgemm': 'naive_dgemm',
            'optimized_dgemm': 'optimized_dgemm',
            'dgemm': 'optimized_dgemm',
            'fft': '2d_fft',
            '2d_fft': '2d_fft',
            'stencil': '3d_stencil_cuda',
            '3d_stencil': '3d_stencil_cuda'
        }
        
        benchmarks_to_run = []
        
        if args.all:
            print("Running all available benchmarks...")
            benchmarks_to_run = ['naive_dgemm', 'optimized_dgemm', '2d_fft']
            if self._file_exists(f"{self.config.benchmark_dir}/3d_stencil_cuda"):
                benchmarks_to_run.append('3d_stencil_cuda')
        elif args.name:
            benchmark_exec = benchmark_map.get(args.name, args.name)
            if self._file_exists(f"{self.config.benchmark_dir}/{benchmark_exec}"):
                benchmarks_to_run = [args.name]
            else:
                return {'success': False, 'error': f"Benchmark '{args.name}' not found"}
        else:
            # Run default benchmark (optimized DGEMM)
            benchmarks_to_run = ['optimized_dgemm']
        
        # Execute benchmarks
        for benchmark_name in benchmarks_to_run:
            print(f"\nExecuting: {benchmark_name}")
            benchmark_exec = benchmark_map.get(benchmark_name, benchmark_name)
            benchmark_path = f"{self.config.benchmark_dir}/{benchmark_exec}"
            
            result = self._execute_single_benchmark(benchmark_path, args.size, args.iterations)
            results.append({
                'name': benchmark_name,
                'result': result
            })
            
            if self.config.verbose:
                print(f"  Performance: {result.get('mflops', 0):.1f} MFLOPS")
        
        return {
            'success': True,
            'benchmarks_executed': len(benchmarks_to_run),
            'results': results
        }
    
    def run_phase(self, args) -> Dict:
        """Run specific HPC-ARC phase"""
        print(f"\n{'='*70}")
        print(f"HPC-ARC PHASE EXECUTION: {args.phase_name.upper()}")
        print(f"{'='*70}")
        
        phase = BenchmarkPhase[args.phase_name.upper()]
        task_context = TaskContext(
            task_id=args.task or f"GEN-{args.phase_name.upper()}",
            research_domain="General HPC Intelligence",
            phase=phase,
            difficulty="medium"
        )
        
        # Run phase execution
        try:
            result = self.benchmark_suite.execute_phase(task_context)
            
            return {
                'success': True,
                'phase': args.phase_name,
                'task_id': args.task,
                'performance': result.get('performance', {}),
                'intelligence': result.get('intelligence', {}),
                'details': result.get('details', {})
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'phase': args.phase_name
            }
    
    def run_analyze(self, args) -> Dict:
        """Analyze benchmark results"""
        print(f"\n{'='*70}")
        print(f"HPC-ARC ANALYSIS")
        print(f"{'='*70}")
        
        # Find results to analyze
        results_path = args.results or self.config.results_dir
        results_file = Path(results_path)
        
        if results_file.is_file():
            # Analyze specific results file
            print(f"Analyzing results from: {results_path}")
            analysis = self.evaluator.evaluate_results_file(str(results_file))
        elif results_file.is_dir():
            # Analyze all results in directory
            print(f"Analyzing all results in: {results_path}")
            results_files = list(results_file.glob("*.json"))
            analysis = self.evaluator.evaluate_batch([str(f) for f in results_files])
        else:
            return {'success': False, 'error': f"Results not found: {results_path}"}
        
        if args.intelligence:
            print("\nHPC-ARC Intelligence Assessment:")
            print(f"  Overall Intelligence Score: {analysis.get('intelligence_score', 0):.3f}")
            print(f"  Tier Assessment: {analysis.get('tier', 'UNKNOWN')}")
            
            components = analysis.get('components', {})
            print(f"  Components:")
            print(f"    Explore Phase:        {components.get('explore', 0):.3f}")
            print(f"    Hypothesize Phase:    {components.get('hypothesize', 0):.3f}")
            print(f"    Execute Phase:       {components.get('execute', 0):.3f}")
            print(f"    Generalize Phase:    {components.get('generalize', 0):.3f}")
        
        # Save analysis results
        if args.output:
            output_file = Path(args.output)
            output_file.parent.mkdir(exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"Analysis saved to: {args.output}")
        
        return {
            'success': True,
            'analysis': analysis,
            'results_processed': analysis.get('results_count', 0)
        }
    
    def run_profile(self, args) -> Dict:
        """Run hardware profiling"""
        print(f"\n{'='*70}")
        print(f"HARDWARE PROFILING")
        print(f"{'='*70}")
        
        # Import hardware profiling tool
        try:
            import tools.hardware_profiling as hp
            
            profiler = hp.HardwareProfiler()
            
            profiling_results = {}
            
            if args.tool in ['likwid', 'all']:
                print("Running LIKWID profiling...")
                try:
                    likwid_result = profiler.run_likwid_profiling(
                        "build/benchmarks/naive_dgemm 2048 3",
                        args.group or "MEM",
                        f"{self.config.results_dir}/likwid_profile.out"
                    )
                    profiling_results['likwid'] = asdict(likwid_result)
                    print(f"  ✓ LIKWID profiling completed")
                except Exception as e:
                    print(f"  ⚠ LIKWID profiling failed: {str(e)[:50]}")
                    profiling_results['likwid'] = {'error': str(e)}
            
            if args.tool in ['perf', 'all']:
                print("Running perf profiling...")
                try:
                    perf_result = profiler.run_perf_profiling(
                        "build/benchmarks/naive_dgemm 2048 3",
                        ['instructions', 'cycles'],
                        f"{self.config.results_dir}/perf_profile.out"
                    )
                    profiling_results['perf'] = asdict(perf_result)
                    print(f"  ✓ perf profiling completed")
                except Exception as e:
                    print(f"  ⚠ perf profiling failed: {str(e)[:50]}")
                    profiling_results['perf'] = {'error': str(e)}
            
            # Generate comprehensive profiling report
            if profiling_results:
                report = profiler.generate_profiling_report(
                    profiling_results,
                    f"{self.config.results_dir}/hardware_profile_report.json"
                )
            
            return {
                'success': True,
                'profiling_results': profiling_results,
                'report': report
            }
        except ImportError:
            return {'success': False, 'error': 'Hardware profiling tools not available'}
    
    def run_gpu(self, args) -> Dict:
        """Run GPU benchmarks"""
        print(f"\n{'='*70}")
        print(f"GPU BENCHMARK EXECUTION")
        print(f"{'='*70}")
        
        try:
            import tools.gpu_integration as gpu
            
            gpu_suite = gpu.GPUBenchmarkSuite()
            
            print(f"GPU Backend: {args.backend}")
            print(f"Problem Size: {args.size}³")
            
            # Define GPU benchmarks
            gpu_benchmarks = [
                gpu.GPUBenchmark(
                    name="3D Stencil",
                    executable=f"{self.config.benchmark_dir}/3d_stencil_cuda",
                    backend="cuda",
                    parameters={'iterations': '5', 'size': str(args.size)},
                    description="GPU 3D stencil computation with shared memory tiling",
                    expected_performance={'gflops': 850.0},
                    application_domain="Computational Fluid Dynamics"
                )
            ]
            
            # Execute GPU benchmarks
            results = gpu_suite.run_statistical_gpu_benchmark_campaign(
                gpu_benchmarks,
                iterations=self.config.iterations
            )
            
            # Generate GPU benchmark report
            report = gpu_suite.generate_gpu_benchmark_report(
                results,
                f"{self.config.results_dir}/gpu_benchmark_report.json"
            )
            
            return {
                'success': True,
                'gpu_results': results,
                'report': report
            }
            
        except ImportError:
            return {'success': False, 'error': 'GPU integration tools not available'}
    
    def run_status(self, args) -> Dict:
        """Check system status"""
        print(f"\n{'='*70}")
        print(f"HPC-ARC SYSTEM STATUS")
        print(f"{'='*70}")
        
        # Check benchmark availability
        benchmark_status = {}
        benchmark_dir = Path(self.config.benchmark_dir)
        
        if benchmark_dir.exists():
            potential_benchmarks = list(benchmark_dir.glob("*"))
            for benchmark in potential_benchmarks:
                if benchmark.is_file() and os.access(benchmark, os.X_OK):
                    benchmark_status[benchmark.name] = 'available'
                else:
                    benchmark_status[benchmark.name] = 'not_executable'
        else:
            print(f"⚠ Benchmark directory not found: {self.config.benchmark_dir}")
            print("Run build system first: bash build/build_hpc_arc.sh")
            benchmark_status = {'status': 'no_benchmarks_available'}
        
        # Check profiling tools
        profiling_tools = {}
        
        # Check LIKWID
        try:
            subprocess.run(["likwid-perfcounter", "--version"], 
                          capture_output=True, timeout=5, check=True)
            profiling_tools['likwid'] = 'available'
        except:
            profiling_tools['likwid'] = 'not_available'
        
        # Check perf
        try:
            subprocess.run(["perf", "version"], 
                          capture_output=True, timeout=5, check=True)
            profiling_tools['perf'] = 'available'
        except:
            profiling_tools['perf'] = 'not_available'
        
        # Check GPU tools
        gpu_tools = {}
        
        try:
            subprocess.run(["nvcc", "--version"], 
                          capture_output=True, timeout=5, check=True)
            gpu_tools['cuda'] = 'available'
        except:
            gpu_tools['cuda'] = 'not_available'
        
        try:
            subprocess.run(["hipcc", "--version"], 
                          capture_output=True, timeout=5, check=True)
            gpu_tools['hip'] = 'available'
        except:
            gpu_tools['hip'] = 'not_available'
        
        # Print basic status
        print(f"Benchmark Status:")
        available_count = sum(1 for status in benchmark_status.values() if status == 'available')
        print(f"  Available Benchmarks: {available_count}/{len(benchmark_status) if benchmark_status else 0}")
        
        for benchmark, status in benchmark_status.items():
            if status == 'available':
                print(f"    ✓ {benchmark}")
            elif status == 'not_executable':
                print(f"    ⚠ {benchmark} (not executable)")
        
        print(f"\nProfiling Tools:")
        for tool, status in profiling_tools.items():
            availability_symbol = "✓" if status == 'available' else "✗"
            print(f"  {availability_symbol} {tool}: {status}")
        
        print(f"\nGPU Tools:")
        for tool, status in gpu_tools.items():
            availability_symbol = "✓" if status == 'available' else "✗"
            print(f"  {availability_symbol} {tool}: {status}")
        
        status_result = {
            'success': True,
            'benchmarks': benchmark_status,
            'profiling_tools': profiling_tools,
            'gpu_tools': gpu_tools
        }
        
        if args.detailed:
            print(f"\nDetailed System Information:")
            self._print_detailed_system_info()
        
        return status_result
    
    def run_example(self, args) -> Dict:
        """Run HPC-ARC examples"""
        print(f"\n{'='*70}")
        print(f"HPC-ARC EXAMPLE EXECUTION")
        print(f"{'='*70}")
        
        example_map = {
            'dgemm': 'examples/ex_051_dgemm_optimization.py',
            'fft': 'examples/execute_real_benchmarks.py 2',  # Run FFT example
            'stencil': 'examples/execute_real_benchmarks.py 3',  # Run stencil example
            'all': 'examples/execute_real_benchmarks.py'
        }
        
        if args.example_name in example_map:
            example_script = example_map[args.example_name]
            print(f"Running example: {args.example_name}")
            print(f"Script: {example_script}")
            
            try:
                result = subprocess.run(
                    f"python {example_script}",
                    shell=True,
                    capture_output=True,
                    timeout=300,
                    cwd=Path(__file__).parent
                )
                
                if result.returncode == 0:
                    print(result.stdout)
                    return {'success': True, 'example': args.example_name}
                else:
                    print(f"Example execution failed: {result.stderr}")
                    return {'success': False, 'error': result.stderr}
                    
            except subprocess.TimeoutExpired:
                return {'success': False, 'error': 'Example execution timeout'}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            return {'success': False, 'error': f"Unknown example: {args.example_name}"}
    
    def _execute_single_benchmark(self, benchmark_path: str, size: int, iterations: int) -> Dict:
        """Execute single benchmark and return results"""
        try:
            cmd = [benchmark_path, str(size), str(iterations)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Parse output for performance metrics
            mflops = self._parse_performance_from_output(result.stdout)
            
            return {
                'success': result.returncode == 0,
                'mflops': mflops,
                'time_ms': 0.0,  # Would parse from output
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _parse_performance_from_output(self, output: str) -> float:
        """Parse MFLOPS from benchmark output"""
        for line in output.split('\n'):
            if "MFLOPS" in line:
                try:
                    mflops_str = line.split("MFLOPS")[0].strip().split()[-1]
                    return float(mflops_str)
                except (ValueError, IndexError):
                    continue
        return 0.0
    
    def _file_exists(self, filepath: str) -> bool:
        """Check if file exists and is executable"""
        try:
            return os.path.exists(filepath) and os.access(filepath, os.X_OK)
        except:
            return False
    
    def _print_detailed_system_info(self):
        """Print detailed system information"""
        import platform
        import cpuinfo
        
        print(f"  System: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Python Version: {platform.python_version()}")
        
        try:
            cpu_info = cpuinfo.get_cpu_info()
            print(f"  Processor: {cpu_info.get('brand_raw', 'Unknown')}")
            print(f"  CPU Cores: {cpu_info.get('count', 'Unknown')}")
        except:
            print(f"  Processor Information: not available")
        
        # Memory information
        try:
            import psutil
            mem = psutil.virtual_memory()
            print(f"  Total Memory: {mem.total / (1024**3):.2f} GB")
            print(f"  Available Memory: {mem.available / (1024**3):.2f} GB")
        except:
            print(f"  Memory Information: not available")

def main():
    """Main entry point for HPC-ARC CLI"""
    cli = HPCARCCLI()
    cli.run()

if __name__ == "__main__":
    main()