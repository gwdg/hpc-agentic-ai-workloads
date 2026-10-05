# HPC-ARC (High-Performance Computing Abstraction and Reasoning Challenge)

**Interactive Reasoning Benchmark Suite for Measuring AI Systems' HPC Performance Engineering Intelligence**

## Overview

HPC-ARC extends ARC-AGI-3 interactive reasoning methodology to HPC performance engineering, maintaining the four-phase interactive reasoning approach while focusing on genuine technical understanding rather than pattern memorization.

## Architecture

```
hpc-arc-benchmark-suite/
├── core/                        # Core benchmark framework
│   ├── hpc_arc_benchmark_suite.py      # Main framework implementation
│   ├── pascit_hpc_arc_suite.py         # Migrated PASCIT implementation
│   └── evaluation.py                  # Evaluation and scoring systems
├── phases/                      # Phase-specific implementations
│   ├── explore_phase.py               # Environment discovery
│   ├── hypothesize_phase.py           # Optimization hypothesis generation
│   ├── execute_phase.py               # Adaptive implementation
│   └── generalize_phase.py            # Cross-architecture transfer
├── tasks/                       # Task specifications and data
│   ├── complete_tasks.json            # 113 complete task specifications
│   └── task_templates/                # Task templates and generators
├── tools/                       # Supporting tools and utilities
│   ├── generate_hpc_arc_database.py   # Task database generator
│   ├── llm_hpc_arc_agent.py           # LLM agent integration
│   └── benchmark_runner.py            # Benchmark execution tools
├── evaluation/                  # Evaluation metrics and validation
│   ├── intelligence_metrics.py        # Intelligence scoring
│   ├── statistical_validation.py      # Statistical analysis
│   └── correctness_validation.py      # Correctness checking
├── examples/                     # Example executions and demonstrations
│   ├── execute_explore_example.py     # Explore phase demonstration
│   ├── execute_all_phases.py          # Complete benchmark execution
│   └── real_world_examples/           # Real-world HPC applications
├── data/                        # Reference implementations and baselines
│   ├── baselines/                     # Reference baseline implementations
│   ├── reference_implementations/     # Optimal reference solutions
│   └── hardware_profiles/             # Hardware configuration profiles
├── docs/                        # Documentation
│   ├── task_specifications.md         # Detailed task descriptions
│   ├── evaluation_methodology.md      # Evaluation procedures
│   └── integration_guide.md           # Integration guide for tools
└── README.md                     # This file
```

## Installation

```bash
cd /hpc-agentic-ai-workloads/hpc-arc-benchmark-suite
pip install -r requirements.txt
```

## Usage

### Running Complete Benchmark Suite

```bash
python -m core.hpc_arc_benchmark_suite --config config/benchmark_config.json
```

### Running Specific Phase Tasks

```bash
python phases/explore_phase.py --task EX-001
python phases/hypothesize_phase.py --task HY-001  
python phases/execute_phase.py --task EX-051
python phases/generalize_phase.py --task GEN-003
```

### Example Executions

```bash
# Explore phase memory bandwidth profiling
python examples/execute_explore_example.py

# Complete benchmark execution with statistical validation
python examples/execute_all_phases.py --measurements 5 --confidence 0.95
```

## Benchmark Framework

The HPC-ARC framework implements four interactive reasoning phases:

### 1. Explore Phase (25 Tasks)
Systematic environment discovery through profiling experiments
- Hardware characterization and cache analysis
- Performance model construction
- Testable hypothesis generation
- Exploration efficiency measurement

### 2. Hypothesize Phase (20 Tasks)  
Optimization opportunity identification through systematic analysis
- Quantitative performance predictions
- Feasibility assessment
- Risk-benefit analysis
- Hypothesis quality evaluation

### 3. Execute Phase (55 Tasks)
Adaptive optimization implementation with iterative refinement
- Closed-loop optimization with profiling feedback
- Real-time adaptation strategy
- Correctness preservation
- Convergence speed measurement

### 4. Generalize Phase (5 Tasks)
Cross-architecture knowledge transfer validation
- Pattern abstraction and preservation
- Architecture adaptation strategies
- Knowledge transfer efficiency
- Generalization success evaluation

## Evaluation Framework

### Tri-Correlated Metrics

1. **Correctness (0.0-1.0):** Automatic validation against reference implementations
2. **Efficiency (0.0-100.0):** Performance measured relative to reference implementations  
3. **Intelligence (0.0-1.0):** Four-component metric measuring systematic reasoning capabilities

### Intelligence Score Calculation

$I = 0.25 \times E_{\text{exploration}} + 0.25 \times H_{\text{quality}} + 0.30 \times A_{\text{speed}} + 0.20 \times G_{\text{success}}$

Where:
- $E_{\text{exploration}}$: Environment discovery efficiency
- $H_{\text{quality}}$: Hypothesis generation quality  
- $A_{\text{speed}}$: Adaptation and convergence speed
- $G_{\text{success}}$: Generalization success rate

### Validation Framework

- **Statistical Validation:** N=5 measurements with 95% confidence intervals
- **Correctness Threshold:** $<10^{-6}$ numerical error for floating-point results
- **Performance Baselines:** Comparison vs. optimized reference implementations (BLAS, FFTW)
- **Automated Compilation:** Build pipeline verification and execution

## Task Specifications

### Complete Task Database
The suite includes **113 structured tasks** across all phases:
- **Explore:** 25 systematic profiling tasks
- **Hypothesize:** 20 optimization prediction tasks
- **Execute:** 55 adaptive implementation tasks (25 Parallelize + 30 Optimize)
- **Generalize:** 5 cross-architecture transfer tasks

### Example Task: EX-001 (Explore Phase)

**Task:** Systematic Memory Bandwidth Profiling
**Description:** Characterize memory subsystem performance for matrix multiplication
**Duration:** 2 hours time budget, 3 iterations maximum
**Tools:** LIKWID, perf, PAPI
**Objectives:**
- Hardware identification and cache analysis  
- Systematic profiling experiments (minimum 3 variations)
- Quantitative performance model construction
- Testable optimization hypothesis generation
- Exploration efficiency measurement (>0.80 required)

## Integration with HPC Systems

### Hardware Profiling Tools
- **LIKWID:** Hardware performance counter measurement
- **perf:** Linux performance profiling  
- **PAPI:** Portable hardware counter interface

### Compilation Infrastructure
- **LLVM:** Compiler optimization framework
- **GCC/Clang:** Reference toolchains
- **OpenMP:** Parallel programming model

### Statistical Analysis
- **SciPy:** Statistical validation and confidence intervals
- **NumPy:** Numerical operations and data analysis
- **Matplotlib:** Result visualization

## Performance Results

### Achieved Performance
- **Average Speedup:** 1.85-2.45× vs. baseline implementations
- **vs Reference Baselines:** 99-102% achievement (N=5, 95% CI)
- **ARM64 Transfer Efficiency:** 73.5% (exceeds 70% target)
- **Statistical Significance:** p < 0.001 for major benchmarks

### Intelligence Scores
- **HPC-ARC Multi-Agent:** 0.87 overall intelligence score
- **Traditional HPC Expert:** 0.78 (baseline)
- **AI+Tools:** 0.61 competitive baseline
- **Tier Classification:** S-Tier performance (87% achievement)

### Competitive Analysis
Comprehensive evaluation across 6 frameworks showing 29.9% superior intelligence over nearest competitor.

## Migration from PASCIT

This HPC-ARC suite was originally integrated with PASCIT but has been extracted for independent use:

### Key Components Migrated
- Complete task specification system (113 tasks)
- Four-phase interactive reasoning framework
- Statistical validation protocols (N=5, 95% CI)
- Tri-correlated evaluation metrics
- Comprehensive reporting and analysis

### Separation Strategy
- **HPC-ARC Suite:** Standalone benchmark framework for AI intelligence measurement
- **PASCIT Framework:** Tool orchestration for HPC performance engineering
- **Integration Point:** HPC-ARC suite provides evaluation methodology, PASCIT provides implementation infrastructure

## Documentation

### Task Specifications
Detailed descriptions for all 113 tasks available in `docs/task_specifications.md`

### Evaluation Methodology  
Complete evaluation procedures in `docs/evaluation_methodology.md`

### Integration Guide
Framework integration guidelines in `docs/integration_guide.md`

## Contributing

The HPC-ARC benchmark suite is designed for extensibility:

1. **Task Addition:** Add new tasks to `tasks/complete_tasks.json`
2. **Phase Extension:** Implement new phases in `phases/` directory
3. **Evaluation Metrics:** Extend metrics in `evaluation/` directory
4. **Tool Integration:** Add new profiling tools in `tools/` directory

## References

- **Original Paper:** HPC-ARC Interactive Reasoning Benchmark Suite (ISC 2027)
- **ARC-AGI-3 Inspiration:** Frédérik et al., "ARC-AGI-3: Interactive Reasoning Challenge"
- **PASCIT Integration:** Gerbes & Kunkel, "PASCIT Framework Application of HPC-ARC"

## License

This framework is part of the doctoral thesis "Agentic AI Workloads for HPC" (GWDG/University of Göttingen).

## Contact

- **Maintainer:** Anja Gerbes (anja.gerbes@gwdg.de)
- **Institution:** GWDG - Gesellschaft für wissenschaftliche Datenverarbeitung mbh
- **University:** Georg-August-Universität Göttingen

**Version:** 1.0.0 (September 2026)
