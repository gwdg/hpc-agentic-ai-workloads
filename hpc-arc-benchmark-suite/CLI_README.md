# HPC-ARC Benchmark Suite - Command Line Interface

Complete CLI tool for HPC-ARC benchmark execution, analysis, and intelligence evaluation. The CLI provides a unified interface to all HPC-ARC functionality, similar to PASCIT but adapted for the four-phase intelligence evaluation methodology.

## 🚀 Quick Installation

### Option 1: Using Installation Script (Recommended)
```bash
cd hpc-agentic-ai-workloads/hpc-arc-benchmark-suite
bash install_cli.sh
```

This will create a global `hpc-arc` command that can be called from anywhere.

### Option 2: Manual Installation
```bash
cd hpc-agentic-ai-workloads/hpc-arc-benchmark-suite
chmod +x hpc-arc
# Create symlink to your binary directory
ln -s $(pwd)/hpc-arc ~/.local/bin/hpc-arc
# Add ~/.local/bin to PATH if not already there
export PATH="$HOME/.local/bin:$PATH"
```

### Option 3: Using pip (Optional)
```bash
cd hpc-agentic-ai-workloads/hpc-arc-benchmark-suite
pip install -e .
```

## 📋 Usage

### Basic Commands

```bash
# Show version and welcome message
hpc-arc --version
hpc-arc

# Show help
hpc-arc -h
```

### System Status
```bash
# Check system status and available benchmarks
hpc-arc status

# Detailed system information
hpc-arc status --detailed
```

### Benchmark Execution
```bash
# Run all available benchmarks
hpc-arc benchmark --all

# Run specific benchmark
hpc-arc benchmark --name dgemm

# Run with custom parameters
hpc-arc benchmark --name fft --size 1024 --iterations 10
```

### Phase Execution
```bash
# Run specific phase
hpc-arc phase execute --task EX-051
hpc-arc phase explore
hpc-arc phase hypothesize --task HY-001
hpc-arc phase generalize
```

### Result Analysis
```bash
# Analyze benchmark results
hpc-arc analyze --results benchmark_results/

# Analyze with intelligence scoring
hpc-arc analyze --intelligence --results benchmark_results/

# Save analysis to specific file
hpc-arc analyze --output my_analysis.json
```

### Hardware Profiling
```bash
# Run hardware profiling (LIKWID/perf)
hpc-arc profile --tool likwid --group MEM
hpc-arc profile --tool perf
hpc-arc profile --tool all

# Specific profiling group
hpc-arc profile --likwid CACHE
hpc-arc profile --perf instructions,cycles
```

### GPU Benchmarks
```bash
# Run GPU benchmarks
hpc-arc gpu --backend cuda
hpc-arc gpu --backend hip

# Custom problem size
hpc-arc gpu --size 512
```

### Examples
```bash
# Run HPC-ARC example demonstrations
hpc-arc example dgemm      # DGEMM optimization example
hpc-arc example fft        # 2D FFT analysis example  
hpc-arc example stencil    # GPU 3D stencil example
hpc-arc example all        # Run all examples
```

## 🎯 Command Reference

### benchmark
Execute HPC-ARC benchmarks with specified parameters.

```bash
hpc-arc benchmark [options]
```

**Options:**
- `--name, -n`: Specific benchmark name (dgemm, fft, stencil, etc.)
- `--size, -s`: Problem size (default: 2048)
- `--iterations, -i`: Number of iterations (default: 5)
- `--all, -a`: Run all available benchmarks

**Examples:**
```bash
hpc-arc benchmark --name optimized_dgemm --size 1024 --iterations 10
hpc-arc benchmark --all
```

### phase
Run specific HPC-ARC phase (explore/hypothesize/execute/generalize).

```bash
hpc-arc phase <phase_name> [options]
```

**Phase Names:**
- `explore`: Systematic hardware exploration and profiling
- `hypothesize`: Performance prediction and hypothesis generation
- `execute`: Benchmark execution with iterative optimization
- `generalize`: Cross-domain application and generalization

**Options:**
- `--task, -t`: Task ID (e.g., EX-051, HY-001)
- `--context`: Custom task context

**Examples:**
```bash
hpc-arc phase execute --task EX-051
hpc-arc phase hypothesize --task HY-001
hpc-arc phase explore
```

### analyze
Analyze benchmark results and generate intelligence scores.

```bash
hpc-arc analyze [options]
```

**Options:**
- `--results, -r`: Results file or directory to analyze
- `--output, -o`: Output file (JSON format)
- `--intelligence`: Calculate and show intelligence scores

**Examples:**
```bash
hpc-arc analyze --results benchmark_results/ --intelligence
hpc-arc analyze --output analysis.json
```

### profile
Run hardware profiling and analysis.

```bash
hpc-arc profile [options]
```

**Options:**
- `--tool, -t`: Profiling tool (likwid, perf, all)
- `--group, -g`: Profiling group (MEM, CACHE, FLOPS, etc.)

**Examples:**
```bash
hpc-arc profile --tool likwid --group MEM
hpc-arc profile --tool perf
hpc-arc profile --tool all
```

### gpu
GPU benchmark execution and analysis.

```bash
hpc-arc gpu [options]
```

**Options:**
- `--backend, -b`: GPU backend (cuda, hip, auto)
- `--size, -s`: GPU problem size (default: 256)

**Examples:**
```bash
hpc-arc gpu --backend cuda
hpc-arc gpu --backend hip --size 512
```

### status
Check system status and available benchmarks.

```bash
hpc-arc status [options]
```

**Options:**
- `--detailed, -d`: Show detailed system information

**Examples:**
```bash
hpc-arc status
hpc-arc status --detailed
```

### example
Run HPC-ARC example demonstrations.

```bash
hpc-arc example <example_name>
```

**Example Names:**
- `dgemm` - DGEMM optimization example (EX-051)
- `fft` - 2D FFT analysis example (EX-041, EX-042)
- `stencil` - GPU 3D stencil example (EX-081, EX-082)
- `all` - Run all examples

**Examples:**
```bash
hpc-arc example dgemm
hpc-arc example fft
hpc-arc example all
```

## 🔧 Configuration

### Environment Variables
- `HPC_ARC_CONFIG`: Path to custom configuration file
- `HPC_ARC_VERBOSE`: Enable verbose output (1/0)
- `HPC_ARC_BENCHMARK_DIR`: Custom benchmark directory
- `HPC_ARC_RESULTS_DIR`: Custom results directory

### Configuration File
The CLI can use a JSON configuration file:
```bash
hpc-arc --config custom_config.json benchmark --all
```

## 📊 Output Formats

### Human-Readable Output (default)
```
✓ Command 'benchmark' completed successfully
  Execution Time: 120.45 ms
  Performance: 890.2 MFLOPS
  Intelligence Score: 0.912
  Tier: S_TIER
```

### JSON Output
For automated processing, speciy JSON format:
```bash
hpc-arc analyze --output results.json --format json
```

### YAML Output
```bash
hpc-arc analyze --output results.yaml --format yaml
```

## 🎯 Typical Workflow

### Complete Evaluation Workflow
```bash
# 1. Check system status
hpc-arc status

# 2. Build benchmarks (if needed)
bash build/build_hpc_arc.sh

# 3. Run hardware profiling
hpc-arc profile --tool likwid --group MEM

# 4. Execute benchmarks
hpc-arc benchmark --all

# 5. Analyze results with intelligence scoring
hpc-arc analyze --intelligence --results benchmark_results/

# 6. Run GPU benchmarks
hpc-arc gpu --backend cuda

# 7. Generate comprehensive report
hpc-arc analyze --output final_report.json
```

### Research Workflow
```bash
# 1. Explore Phase - Systematic profiling
hpc-arc phase explore

# 2. Hypothesize Phase - Performance prediction
hpc-arc phase hypothesize --task HY-001

# 3. Execute Phase - Benchmark execution
hpc-arc phase execute --task EX-051

# 4. Generalize Phase - Cross-domain application
hpc-arc phase generalize

# 5. Complete analysis
hpc-arc analyze --intelligence
```

## 🐛 Troubleshooting

### Installation Issues
```bash
# Check if hpc-arc command is available
which hpc-arc

# Test direct execution
cd hpc-agentic-ai-workloads/hpc-arc-benchmark-suite
./hpc-arc --version

# Reinstall using installation script
bash install_cli.sh --force
```

### Python Module Issues
```bash
# Install required dependencies
pip install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.8+

# Verify imports
python3 -c "import numpy; import scipy; print('OK')"
```

### Benchmark Execution Issues
```bash
# Check if benchmarks are compiled
hpc-arc status --detailed

# Rebuild benchmarks if needed
bash build/build_hpc_arc.sh

# Check build logs
ls build/*.log
```

### Hardware Profiling Issues
```bash
# Check if LIKWID is available
likwid-perfcounter --version

# Check if perf is available
perf --version

# Install profiling tools if needed (Linux)
sudo apt-get install likwid linux-tools-generic
```

## 📚 Advanced Usage

### Custom Task Context
```bash
hpc-arc phase execute --task EX-051 --context '{"difficulty": "hard", "research_domain": "linear_algebra"}'
```

### Batch Processing
```bash
# Process multiple result files
for result_file in benchmark_results/*.json; do
  hpc-arc analyze --results "$result_file" --output "analysis_$(basename $result_file .json).json"
done
```

### Integration with CI/CD
```bash
# In CI scripts
hpc-arc benchmark --all --iterations 3
hpc-arc analyze --intelligence --output ci_report.json
```

## 🤝 Contributing

To contribute to the HPC-ARC CLI:
1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Related Projects

- [HPC-ARC Benchmark Suite](https://github.com/HPC-ARC/benchmark-suite)
- [PASCIT Framework](https://github.com/PASCIT/pascit-framework)
- [LIKWID Performance Tools](https://hpc-tutorial.org/likwid/)

## 📞 Support

- GitHub Issues: https://github.com/HPC-ARC/benchmark-suite/issues
- Documentation: https://hpc-arc.readthedocs.io
- Email: hpc-arc@gwdg.de

---

**Version:** 1.0.0  
**Last Updated:** September 12, 2026  
**Framework:** Four-Phase HPC Intelligence Evaluation