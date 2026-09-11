# HPC Agentic AI Workloads - Structure Framework

## Overview

This document defines a comprehensive structure for HPC (High-Performance Computing) Agentic AI workloads, providing standardized task definitions, input/output specifications, and workflow management for AI-driven performance optimization tasks.

---

## Core Structure Definition

### 1. Task Identifier and Classification

```json
{
  "task_id": "TASK-<CATEGORY>-<NUMBER>",
  "task_name": "Human-readable task name",
  "category": "optimization|profiling|debugging|benchmarking|comparison",
  "complexity": "elementary|intermediate|advanced|expert",
  "estimated_duration_minutes": 15,
  "hpc_arc_phase": "E|H|EX|G",
  "priority": "high|medium|low",
  "automated": true,
  "requires_llm": true
}
```

### 2. Input Specification

```json
{
  "input_spec": {
    "source_code": {
      "files": ["path/to/source.c", "path/to/headers.h"],
      "language": "C|C++|Fortran|Python|CUDA|OpenCL",
      "architecture_target": "x86_64|ARM64|GPU",
      "optimization_level": "O0|O1|O2|O3|Ofast"
    },
    "profiling_data": {
      "baseline_results": "path/to/baseline.json",
      "hardware_counters": "likwid|perf|oprofile",
      "measurements": 5,
      "confidence_interval": 0.95
    },
    "hardware_context": {
      "processor": "Intel Xeon Gold 6348|AMD EPYC 7742|ARM Neoverse-N1",
      "cores": 48,
      "cache_topology": {
        "L1_KB": 384,
        "L2_MB": 1.5,
        "L3_MB": 105
      },
      "vector_capabilities": ["AVX-512", "SVE-256"],
      "memory_bandwidth_GB_s": 3.2
    },
    "constraints": {
      "memory_limit_GB": 512,
      "time_limit_hours": 8,
      "thread_limit": 48,
      "energy_constraints": false
    },
    "llm_config": {
      "provider": "opencode|ollama|openai|gwdg-saia",
      "model": "llama-3-8b|gpt-4|devstral-2",
      "temperature": 0.0,
      "max_tokens": 4096,
      "context_window": 3
    }
  }
}
```

### 3. Output Specification

```json
{
  "output_spec": {
    "optimized_code": {
      "path": "path/to/optimized.c",
      "modifications": {
        "changes_count": 3,
        "lines_added": 42,
        "lines_removed": 18,
        "modifications": ["loop tiling", "vectorization", "prefetching"]
      }
    },
    "performance_metrics": {
      "baseline_gflops": 2.1,
      "optimized_gflops": 7.8,
      "speedup": 3.71,
      "cache_efficiency": {
        "l1_miss_rate_before": 0.45,
        "l1_miss_rate_after": 0.18,
        "l2_miss_rate_before": 0.22,
        "l2_miss_rate_after": 0.12
      },
      "vectorization_rate": 0.92,
      "memory_bandwidth_utilization": 0.85
    },
    "validation": {
      "correctness_test": "passed",
      "regression_test": "passed",
      "numerical_accuracy": "1e-6",
      "reproducibility": {
        "coefficient_of_variation": 0.059,
        "confidence_interval_95": "[6.8, 8.8]"
      }
    },
    "analysis": {
      "bottleneck_identified": "memory bandwidth",
      "optimization_strategy": "cache blocking + vectorization",
      "efficiency_vs_baseline": 0.85,
      "architectural_fit": "excellent"
    },
    "evidence_artifacts": {
      "profiling_data": "path/to/profile_data.json",
      "compilation_logs": "path/to/compilation.log",
      "test_results": "path/to/test_results.txt",
      "monitoring_trace": "path/to/monitoring.json"
    }
  }
}
```

### 4. Task Definition and Workflow

```json
{
  "task_definition": {
    "objective": "Maximize FLOPS performance for GEMM 2048x2048 matrix multiplication",
    "steps": [
      {
        "step_number": 1,
        "action": "profiling",
        "description": "Collect baseline performance metrics using LIKWID",
        "command": "pascit profile likwid --benchmark gemm_2048 --group FLOPS_DP",
        "expected_output": "baseline_performance.json"
      },
      {
        "step_number": 2,
        "action": "analysis",
        "description": "Identify performance bottlenecks from profiling data",
        "llm_analysis": true,
        "diagnosis_focus": ["cache behavior", "vectorization", "memory bandwidth"]
      },
      {
        "step_number": 3,
        "action": "optimization",
        "description": "Apply LLM-suggested optimizations to source code",
        "optimization_types": ["loop tiling", "AVX-512 vectorization", "prefetching"],
        "automated": true
      },
      {
        "step_number": 4,
        "action": "compilation",
        "description": "Compile optimized version with appropriate flags",
        "command": "gcc -march=native -O3 -ffast-math optimized.c -o optimized"
      },
      {
        "step_number": 5,
        "action": "profiling",
        "description": "Measure optimized performance",
        "command": "pascit profile likwid --benchmark optimized --group FLOPS_DP"
      },
      {
        "step_number": 6,
        "action": "validation",
        "description": "Verify correctness and measure improvement",
        "tests": ["numerical correctness", "performance comparison", "reproducibility"]
      }
    ],
    "success_criteria": {
      "minimum_speedup": 1.5,
      "correctness_required": true,
      "statistical_significance": true,
      "cache_miss_reduction": 0.2
    },
    "failure_modes": [
      "compilation_error",
      "runtime_crash",
      "incorrect_results",
      "performance_degradation",
      "insufficient_improvement"
    ]
  }
}
```

---

## Task Categories and Templates

### Category 1: Performance Optimization (OPT)

#### OPT-001: Basic Loop Optimization
```json
{
  "task_id": "OPT-001",
  "task_name": "Basic scalar loop vectorization",
  "category": "optimization",
  "complexity": "elementary",
  "hpc_arc_phase": "EX",
  "input": {
    "code_pattern": "simple nested loops without vectorization",
    "bottleneck": "scalar execution, low CPU utilization",
    "target_architecture": "x86_64 with AVX-512"
  },
  "output": {
    "optimized_pattern": "AVX-512 vectorized loop",
    "expected_speedup": "8-12×",
    "vectorization_rate": ">0.8"
  },
  "steps": [
    "profile baseline with LIKWID FLOPS_DP",
    "analyze scalar execution pattern",
    "apply AVX-512 intrinsics",
    "compile with -mavx512f",
    "measure improvement"
  ]
}
```

#### OPT-002: Cache Blocking for GEMM
```json
{
  "task_id": "OPT-002", 
  "task_name": "GEMM cache blocking optimization",
  "category": "optimization",
  "complexity": "intermediate",
  "hpc_arc_phase": "EX",
  "input": {
    "code_pattern": "naive GEMM multiplication",
    "matrix_size": "2048×2048",
    "current_performance": "2.1 GFLOPS",
    "cache_issues": "45% L1 miss rate"
  },
  "output": {
    "optimized_pattern": "32×32 tiled GEMM",
    "target_performance": "7.2+ GFLOPS",
    "improvement": "3.4× speedup",
    "cache_efficiency": "<20% L1 miss rate"
  },
  "steps": [
    "profile cache behavior with CACHE group",
    "determine optimal tile size for L1 cache",
    "implement tiling with TILE_SIZE=32",
    "optimize memory access patterns",
    "validate correctness and measure improvement"
  ]
}
```

### Category 2: Profiling and Analysis (PRF)

#### PRF-001: Comprehensive Performance Profiling
```json
{
  "task_id": "PRF-001",
  "task_name": "Full hardware counter profiling",
  "category": "profiling", 
  "complexity": "elementary",
  "hpc_arc_phase": "E",
  "input": {
    "target_code": "any HPC kernel",
    "profiling_tools": ["likwid", "perf", "oprofile"],
    "hardware_events": ["cycles", "instructions", "cache-misses", "branch-misses"]
  },
  "output": {
    "profiling_report": "detailed performance analysis",
    "bottleneck_identification": "specific limiting factors",
    "optimization_recommendations": "priority-ranked suggestions",
    "baseline_metrics": "performance baseline for comparison"
  },
  "steps": [
    "compile with profiling flags",
    "run benchmarks with multiple profiler groups",
    "collect comprehensive hardware counter data",
    "analyze cache hierarchy behavior",
    "identify vectorization efficiency",
    "generate detailed bottleneck analysis"
  ]
}
```

#### PRF-002: Memory Bandwidth Analysis
```json
{
  "task_id": "PRF-002",
  "task_name": "Memory bandwidth bottleneck identification", 
  "category": "profiling",
  "complexity": "intermediate",
  "hpc_arc_phase": "E",
  "input": {
    "application_type": "memory-bound workloads",
    "theoretical_bandwidth": "3.2 GB/s (DDR4-3200)",
    "current_bandwidth": "1.8 GB/s"
  },
  "output": {
    "bandwidth_utilization": "percentage of theoretical maximum",
    "bottleneck_type": "specific memory bandwidth limitation",
    "optimization_strategy": "bandwidth-aware optimization approach",
    "expected_improvement": "projected bandwidth increase"
  },
  "steps": [
    "profile with MEM counter group",
    "analyze memory access patterns",
    "calculate bandwidth utilization ratio",
    "identify inefficient memory accesses",
    "recommend bandwidth-optimizing transformations"
  ]
}
```

### Category 3: Debugging and Error Resolution (DBG)

#### DBG-001: Numerical Stability Fix
```json
{
  "task_id": "DBG-001",
  "task_name": "Numerical instability correction",
  "category": "debugging",
  "complexity": "intermediate", 
  "hpc_arc_phase": "EX",
  "input": {
    "symptom": "incorrect results in frequency domain",
    "potential_cause": "division by small values",
    "current_accuracy": "failed validation tests"
  },
  "output": {
    "corrected_code": "numerically stable implementation",
    "test_status": "all validation tests passed",
    "accuracy_threshold": "within 1e-6 tolerance",
    "error_elimination": "zero numerical errors"
  },
  "steps": [
    "identify numerical instability locations",
    "analyze division by small values",
    "implement clamping/stabilization mechanisms",
    "verify numerical correctness",
    "measure accuracy improvement"
  ]
}
```

### Category 4: Benchmarking and Comparison (BNK)

#### BNK-001: Cross-Architecture Performance Comparison
```json
{
  "task_id": "BNK-001",
  "task_name": "x86_64 vs ARM64 performance comparison",
  "category": "benchmarking",
  "complexity": "advanced",
  "hpc_arc_phase": "G",
  "input": {
    "kernel": "GEMM implementation",
    "architectures": ["Intel Xeon (AVX-512)", "ARM Neoverse-N1 (SVE-256)"],
    "code_variants": ["platform-specific optimizations"]
  },
  "output": {
    "performance_comparison": "side-by-side analysis",
    "transfer_efficiency": "ARM64 performance as % of x86 baseline",
    "optimization_adaptations": "ISA-specific changes",
    "portability_assessment": "code portability metrics"
  },
  "steps": [
    "implement x86_64 AVX-512 version",
    "implement ARM64 SVE-256 version",
    "compile for both architectures",
    "run comparative benchmarks",
    "analyze transfer efficiency",
    "document architecture-specific optimizations"
  ]
}
```

### Category 5: Profile-Guided Optimization (PGO)

#### PGO-001: Complete PGO Pipeline
```json
{
  "task_id": "PGO-001",
  "task_name": "Full profile-guided optimization workflow",
  "category": "benchmarking",
  "complexity": "advanced",
  "hpc_arc_phase": "EX",
  "input": {
    "source_code": "performance-critical kernel",
    "training_workload": "representative input data",
    "compilers": ["gcc", "clang"]
  },
  "output": {
    "pgo_optimized_binary": "profile-guided compiled executable",
    "improvement_metrics": "speedup vs standard optimization",
    "profile_analysis": "training data utilization report",
    "compiler_comparison": "GCC vs Clang PGO effectiveness"
  },
  "steps": [
    "build instrumented version",
    "execute with representative workload",
    "collect profile data",
    "merge profiles from multiple runs",
    "build PGO-optimized version",
    "compare with baseline",
    "analyze optimization effectiveness"
  ]
}
```

---

## Validation and Quality Assurance

### Validation Framework

```json
{
  "validation_framework": {
    "correctness_verification": {
      "numerical_accuracy_test": "compare against reference implementation",
      "regression_test": "ensure no functional changes",
      "boundary_condition_test": "handle edge cases",
      "precision_verification": "FP32/FP64 accuracy validation"
    },
    "performance_validation": {
      "statistical_significance": "N=5 measurements with 95% CI",
      "reproducibility_test": "CV < 5% across runs",
      "baseline_comparison": "compare against Intel MKL baseline",
      "scaling_analysis": "verify expected scaling behavior"
    },
    "architectural_validation": {
      "cache_behavior": "verify cache usage improvements",
      "vectorization_verify": "SIMD instruction utilization",
      "memory_efficiency": "memory bandwidth optimization",
      "cross_architecture": "portability across ISAs"
    }
  }
}
```

### Quality Assurance Criteria

```json
{
  "quality_assurance": {
    "code_quality": {
      "compilation_warnings": "zero warnings with -Wall -Wextra",
      "code_style": "consistent formatting and naming",
      "documentation": "meaningful comments and documentation",
      "maintainability": "clear structure and modularity"
    },
    "performance_quality": {
      "minimum_speedup": "1.5× vs baseline",
      "cache_efficiency": "<30% miss rate on critical loops",
      "vectorization_rate": ">80% for vectorizable code",
      "stability": "consistent performance across runs"
    },
    "correctness_quality": {
      "test_coverage": "100% correctness test pass",
      "numerical_precision": "within 1e-6 of reference",
      "edge_case_handling": "proper boundary condition handling",
      "error_handling": "graceful degradation on errors"
    }
  }
}
```

---

## Evidence and Artifact Management

### Artifact Collection

```json
{
  "evidence_artifacts": {
    "profiling_data": {
      "likwid_results": "JSON files with hardware counters",
      "perf_statistics": "Linux perf output",
      "oprofile_data": "sample-based profiling results"
    },
    "build_artifacts": {
      "compilation_logs": "detailed compiler output",
      "object_files": "intermediate compilation products",
      "linker_information": "library and dependency details"
    },
    "runtime_artifacts": {
      "execution_log": "detailed runtime information",
      "memory_footprint": "tss memory usage patterns",
      "cpu_utilization": "core usage and threading behavior"
    },
    "validation_artifacts": {
      "test_results": "correctness test outputs",
      "performance_measurements": "timing and throughput results",
      "statistical_analysis": "confidence intervals and significance"
    }
  }
}
```

### Artifact Structure

```
/artifacts/
├── TASK-XXX/
│   ├── input/
│   │   └── source_code/
│   ├── profiling/
│   │   ├── likwid/
│   │   ├── perf/
│   │   └── oprofile/
│   ├── build/
│   │   ├── baseline/
│   │   └── optimized/
│   ├── validation/
│   │   ├── correctness/
│   │   └── performance/
│   └── output/
│       ├── optimized_code/
│       └── analysis_reports/
```

---

## Task Dependencies and Workflows

### Dependency Graph

```json
{
  "task_dependencies": {
    "prerequisite_tasks": {
      "profiling_required": ["PRF-001"],
      "analysis_required": ["PRF-001", "PRF-002"],
      "optimization_builds_on": ["PRF-001", "OPT-001"],
      "benchmarks_require": ["OPT-001", "OPT-002", "PGO-001"]
    },
    "task_sequence": {
      "start": "PRF-001 → PRF-002",
      "optimization_flow": "PRF → OPT → DBG (if needed)",
      "validation_flow": "BNK → PGO → BNK",
      "cross_architecture": "OPT x86 → BNK comparison → OPT ARM → BNK"
    }
  }
}
```

---

## Metadata and Documentation

### Task Documentation Template

```json
{
  "documentation": {
    "task_summary": "Brief description of task purpose and goals",
    "theoretical_background": "Relevant HPC theory and principles",
    "implementation_details": "Technical implementation approach",
    "expected_results": "Quantitative and qualitative expectations",
    "common_issues": "Frequently encountered problems and solutions",
    "references": "Academic papers, documentation, benchmarks"
  }
}
```

---

## Extensibility and Future Work

### Extensible Categories

- **Energy Optimization**: Power-aware performance optimization
- **Thermal Management**: Temperature-constrained optimization
- **Multi-Objective**: Pareto-optimal solutions
- **Real-time Requirements**: Latency-sensitive optimizations
- **Fault Tolerance**: Error-resilient computing
- **Quantum Computing**: Future architecture support

---

## Usage Guidelines

### Task Execution Workflow

1. **Task Selection**: Choose appropriate task based on complexity and requirements
2. **Input Preparation**: Gather required source code, profiling data, and contexts
3. **Configuration**: Set up environment, tools, and LLM parameters
4. **Execution**: Follow defined steps, monitoring intermediate results
5. **Validation**: Verify correctness and performance improvements
6. **Documentation**: Record results, evidence artifacts, and analysis
7. **Archival**: Store complete task results for reproducibility

### Best Practices

- Start with profiling tasks (PRF) to establish baselines
- Build complexity gradually from elementary to expert tasks
- Always validate correctness after modifications
- Use statistical measurements for performance claims
- Maintain comprehensive evidence artifacts
- Document all decisions and rationale
- Follow reproducibility principles with N=5 measurements

---

*This framework provides a standardized structure for HPC Agentic AI workloads, enabling systematic exploration of AI-driven performance optimization with reproducible, scientifically sound methodology.*