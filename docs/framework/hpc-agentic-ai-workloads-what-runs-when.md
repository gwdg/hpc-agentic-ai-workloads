# HPC Agentic AI Workloads - What Runs When

## Executive Summary

This document explains what actually runs in the HPC Agentic AI Workloads system - from task submission through execution to final results. It provides a clear, step-by-step explanation of what happens when you use the system, what gets processed, and what outputs are generated.

---

## 1. The Big Picture: System Overview

### What the System Does

The HPC Agentic AI Workloads system automates the process of optimizing high-performance computing code through AI-driven analysis and implementation. Think of it as having a team of HPC performance engineers working together automatically:

1. **Profiling Agents**: Analyze code performance and identify bottlenecks
2. **Optimization Agents**: Suggest and apply code improvements
3. **Validation Agents**: Test that optimizations work correctly
4. **Orchestration Agents**: Coordinate everything in the right order

### High-Level Workflow

```
USER SUBMITS CODE
         ↓
    PROFILING (What is slow?)
         ↓
    ANALYSIS (Why is it slow?)
         ↓
    OPTIMIZATION (How to make it faster?)
         ↓
    VALIDATION (Does it still work correctly?)
         ↓
    MEASUREMENT (How much faster is it?)
         ↓
    RESULTS (Report + improved code)
```

---

## 2. User Perspective: What You Submit

### 2.1 Simple Task Submission

**What you provide:**

```bash
# Command line submission
pascit optimize \
  --source my_gemm_code.c \
  --task "make this faster" \
  --provider ollama \
  --model llama3

# Or via web interface
{
  "source_code": "my_gemm_code.c",
  "objective": "maximize FLOPS performance",
  "constraints": {
    "max_memory": "512GB",
    "time_limit": "8 hours"
  }
}
```

**What the system receives:**

- Source code file(s) in C/C++, Fortran, Python, etc.
- Optimization objective (speed, memory, energy, etc.)
- Hardware context (which CPU/GPU are we targeting?)
- Any constraints or preferences
- Authentication/authorization information

### 2.2 Complex Workflow Submission

**What you provide:**

```json
{
  "workflow": {
    "steps": [
      {
        "action": "profile_baseline",
        "tools": ["likwid", "perf"],
        "duration": "5 minutes"
      },
      {
        "action": "llm_analysis",
        "focus": ["cache_bottleneck", "vectorization_lack"],
        "iterations": 3
      },
      {
        "action": "apply_optimizations",
        "types": ["loop_tiling", "simd_vectorization"]
      },
      {
        "action": "validate_correctness",
        "tests": ["numerical", "regression"]
      },
      {
        "action": "benchmark_comparison",
        "baseline": "MKL"
      }
    ]
  }
}
```

**What the system receives:**

- Multi-step workflow definition
- Configuration for each step
- Dependencies between steps
- Success criteria for the entire workflow

---

## 3. What Runs: Step-by-Step Execution

### Phase 1: Profiling (Performance Measurement)

#### What Happens
The system measures how your current code performs to establish a baseline.

#### What Gets Executed

**1. LIKWID Profiling** (Hardware Counter Collection)

```bash
# Command that runs
likwid-perfctr -C 2 -g FLOPS_DP ./my_gemm_code

# What it does:
# - Monitors specific CPU hardware events
# - Counts floating point operations
# - Measures cache behavior
# - Tracks memory bandwidth usage
```

**Input:**

- Compiled binary from your source code
- Configuration for what to measure (FLOPS, CACHE, MEMORY)
- Hardware context information

**Output:**

```json
{
  "baseline_performance": {
    "gflops": 2.1,
    "execution_time_seconds": 15.2,
    "cache_efficiency": {
      "l1_miss_rate": 0.45,
      "l2_miss_rate": 0.22
    },
    "hardware_counters": {
      "cpu_cycles": 42630000,
      "instructions": 68507000,
      "l1_dcache_misses": 749,
      "l2_cache_misses": 312
    }
  }
}
```

**2. Prof Analysis** (Alternative Hardware Monitoring)

```bash
# Command that runs
perf stat -e cycles,instructions,cache-references,cache-misses ./my_gemm_code

# What it does:
# - Uses Linux kernel performance counters
# - Shows CPU cycle efficiency
# - Measures instruction throughput
# - Tracks cache behavior
```

**Result:**

- Complete performance baseline established
- Bottleneck identification (e.g., "memory bandwidth limited")
- Quantitative measurements stored in database
- Profiling data saved as Evidence Artifact

---

### Phase 2: LLM Analysis (Intelligent Code Analysis)

#### What Happens
AI agents analyze your code and profiling data to understand what optimizations would help.

#### What Gets Executed

**1. Code Analysis Agent**

```python
# What runs internally
agent = CodeAnalysisAgent(llm_provider="ollama", model="llama3")

# Analysis performed:
# - Parse source code structure
# - Identify loop patterns and data structures
# - Detect optimization opportunities
# - Evaluate complexity and potential gains

analysis_result = agent.analyze(
    source_code="my_gemm_code.c",
    profiling_data=baseline_results,
    hardware_context=IntelXeonGold6348
)
```

**Input:**

- Source code (text analysis)
- Baseline profiling results
- Hardware specifications
- Historical optimization data

**Output:**

```json
{
  "analysis": {
    "code_structure": "triple-nested loops, row-major access",
    "detected_issues": [
      "no vectorization detected (0%)",
      "high cache miss rate (45% L1)",
      "memory bandwidth limited"
    ],
    "optimization_opportunities": [
      {
        "type": "loop_tiling",
        "expected_improvement": "2-3x speedup",
        "complexity": "low",
        "description": "Break matrix into blocks to fit in cache"
      },
      {
        "type": "avx512_vectorization",
        "expected_improvement": "8-12x speedup",
        "complexity": "medium",
        "description": "Use SIMD instructions for parallel processing"
      }
    ],
    "recommended_approach": "Combine loop tiling with AVX-512 vectorization"
  }
}
```

**2. Optimization Strategy Agent**

```python
# What runs internally
strategy_agent = OptimizationStrategyAgent()

# Strategy development:
# - Prioritize optimization opportunities
# - Estimate implementation complexity
# - Plan optimization sequence
# - Allocate resources appropriately

strategy = strategy_agent.plan_optimization(
    analysis_results=analysis_result,
    constraints={"time_budget": "30 minutes"},
    success_criteria={"minimum_speedup": 1.5}
)
```

**Input:**

- Code analysis results
- Available optimization techniques
- Resource constraints
- Performance targets

**Output:**

```json
{
  "optimization_plan": {
    "iterations": 3,
    "step_1": {
      "order": 1,
      "technique": "loop_tiling",
      "tile_size": 32,
      "priority": "high",
      "estimated_time": "5 minutes"
    },
    "step_2": {
      "order": 2,
      "technique": "avx512_vectorization",
      "vector_width": 512,
      "priority": "high",
      "estimated_time": "10 minutes"
    },
    "step_3": {
      "order": 3,
      "technique": "prefetching",
      "prefetch_distance": 4,
      "priority": "medium",
      "estimated_time": "5 minutes"
    },
    "total_expected_speedup": "3.5x",
    "total_estimated_time": "20 minutes"
  }
}
```

**Result:**

- Detailed understanding of code performance issues
- Prioritized optimization strategies
- Implementation plan with time estimates
- Resource allocation for execution

---

### Phase 3: Code Optimization (Implementation)

#### What Happens
The AI agents actually modify your source code to implement the optimizations.

#### What Gets Executed

**1. Code Generation Agent**

```python
# What runs internally
code_agent = CodeGenerationAgent(llm_provider="ollama", model="llama3")

# Code generation:
# - Transforms source code based on optimization strategy
# - Applies specific optimization patterns
# - Maintains code correctness and functionality
# - Preserves comments and structure

optimized_code = code_agent.optimize(
    original_code="my_gemm_code.c",
    optimization_plan=optimization_strategy,
    optimization_step=step_1  # loop_tiling
)
```

**Input:**

- Original source code
- Specific optimization to apply
- Code context and structure
- Implementation constraints

**Output:**

```c
// What gets generated and saved as my_gemm_code_tiled.c
void gemm_optimized(float* A, float* B, float* C, int N) {
    const int TILE_SIZE = 32;  // Optimized for L1 cache

    for (int ii = 0; ii < N; ii += TILE_SIZE) {
        for (int jj = 0; jj < N; jj += TILE_SIZE) {
            for (int kk = 0; kk < N; kk += TILE_SIZE) {
                // Process 32x32 blocks
                for (int i = ii; i < ii + TILE_SIZE; i++) {
                    for (int j = jj; j < jj + TILE_SIZE; j++) {
                        float sum = 0.0f;
                        for (int k = kk; k < kk + TILE_SIZE; k++) {
                            sum += A[i*N + k] * B[k*N + j];
                        }
                        C[i*N + j] = sum;
                    }
                }
            }
        }
    }
}
```

**2. Compilation Agent**

```bash
# Command that runs
gcc -march=native -O3 -ffast-math -mavx512f \
    my_gemm_code_tiled.c -o my_gemm_code_tiled

# What it does:
# - Compiles optimized code
# - Applies architecture-specific optimizations
# - Uses advanced compiler features
# - Generates optimized machine code
```

**Input:**

- Optimized source code
- Compiler flags and options
- Target architecture specifications
- Optimization level settings

**Output:**

```json
{
  "compilation": {
    "status": "success",
    "warnings": 0,
    "binary_size": "45KB",
    "compilation_time": "3.2s",
    "compiler_flags": "-march=native -O3 -ffast-math -mavx512f",
    "generated_binary": "my_gemm_code_tiled"
  }
}
```

**Result:**

- Modified source code with optimizations applied
- Compiled binary ready for testing
- Compilation logs saved
- Intermediate artifacts stored

---

### Phase 4: Validation (Correctness Testing)

#### What Happens
The system verifies that the optimized code still produces correct results.

#### What Gets Executed

**1. Numerical Correctness Test**

```python
# What runs internally
correctness_tester = CorrectnessValidator()

# Testing performed:
# - Run original and optimized with same inputs
# - Compare numerical results within tolerance
# - Check for NaN, infinity, or overflow
# - Verify pathological cases

correctness_result = correctness_tester.validate(
    baseline_binary="my_gemm_code_original",
    optimized_binary="my_gemm_code_tiled",
    test_inputs=[
        {"size": 256, "hal_seed": 42},
        {"size": 512, "hal_seed": 123},
        {"size": 1024, "hal_seed": 456}
    ],
    tolerance="1e-6"
)
```

**Input:**

- Baseline and optimized binaries
- Test input matrices
- Tolerance thresholds
- Edge case specifications

**Output:**

```json
{
  "correctness_validation": {
    "status": "passed",
    "tests_performed": 3,
    "tests_passed": 3,
    "maximum_error": "3.2e-7",
    "tolerance": "1e-6",
    "numerical_stability": "good",
    "no_nan_or_inf": true,
    "edge_cases": [
      {"case": "small_matrix", "status": "passed"},
      {"case": "large_matrix", "status": "passed"},
      {"case": " pathological_values", "status": "passed"}
    ]
  }
}
```

**2. Regression Test**

```bash
# Command that runs
./regression_test_suite --baseline=./my_gemm_code_original \
                        --optimized=./my_gemm_code_tiled \
                        --test_cases=100

# What it does:
# - Runs comprehensive test suite
# - Checks for functional equivalence
# - Validates memory access patterns
# - Verifies consistent behavior
```

**Result:**

- Confirmation that optimized code works correctly
- Detailed test results saved
- Error margins quantified
- Approval for performance testing

---

### Phase 5: Performance Measurement (Speed Comparison)

#### What Happens
The system measures how much faster the optimized code is compared to the original.

#### What Gets Executed

**1. Performance Benchmark**

```bash
# Command that runs (for both baseline and optimized)
likwid-perfctr -C 2 -g FLOPS_DP ./my_gemm_code_tiled

# Measured over N=5 runs for statistical significance:
# Run 1: 7.2 GFLOPS
# Run 2: 7.4 GFLOPS
# Run 3: 7.1 GFLOPS
# Run 4: 7.3 GFLOPS
# Run 5: 7.2 GFLOPS
```

**Input:**
- Optimized binary
- Same measurement configuration as baseline
- Statistical requirements (N=5 measurements)

**Output:**

```json
{
  "performance_measurement": {
    "optimized_performance": {
      "mean_gflops": 7.24,
      "std_deviation": 0.12,  # 1.6% coefficient of variation
      "confidence_interval_95": "[7.1, 7.4]",
      "measurements": [7.2, 7.4, 7.1, 7.3, 7.2]
    },
    "comparison": {
      "baseline_gflops": 2.1,
      "speedup": 3.45,
      "improvement_percentage": 245.2,
      "performance_rank": "excellent",
      "vs_mkl_baseline": "10.8% of MKL performance (67.3 GFLOPS)"
    },
    "cache_improvement": {
      "l1_miss_rate": 0.18,  // was 0.45
      "l2_miss_rate": 0.12,  // was 0.22
      "memory_bandwidth_utilization": 0.82  // was 0.56
    },
    "statistical_significance": {
      "t_statistic": 42.3,
      "p_value": "<0.0001",
      "significance_level": "***",
      "result": "highly_significant"
    }
  }
}
```

**2. Vectorization Analysis**

```bash
# Command that runs
perf stat -e metrics,instructions,vectors ./my_gemm_code_tiled

# What it measures:
# - SIMD instruction utilization
# - Vector efficiency rates
# - Instruction throughput
# - Pipeline efficiency
```

**Output:**

```json
{
  "vectorization_analysis": {
    "vectorization_rate": 0.92,  // 92% of operations vectorized
    "simd_efficiency": "excellent",
    "avx512_utilization": "high",
    "vector_width": 512,
    "floating_point_throughput": "maximized"
  }
}
```

**Result:**

- Quantified performance improvement
- Statistical validation of improvement
- Detailed analysis of optimization effectiveness
- Comparison against industry baselines (Intel MKL)

---

### Phase 6: Results Delivery (Final Output)

#### What Gets Produced

**1. Optimized Source Code**

```c
// File saved: my_gemm_code_optimized.c
// Contains all optimizations applied with comments explaining changes

void gemm_optimized(float* A, float* B, float* C, int N) {
    const int TILE_SIZE = 32;  // OPTIMIZATION: Cache blocking for L1 cache
                                // Changed from 256 to 32 based on profiling

    for (int ii = 0; ii < N; ii += TILE_SIZE) {
        for (int jj = 0; jj < N; jj += TILE_SIZE) {
            for (int kk = 0; kk < N; kk += TILE_SIZE) {
                // OPTIMIZATION: Process 32x32 blocks to improve cache locality
                for (int i = ii; i < ii + TILE_SIZE; i++) {
                    for (int j = jj; j < jj + TILE_SIZE; j++) {
                        float sum = 0.0f;

                        // OPTIMIZATION: Inner loop can be vectorized by AVX-512
                        for (int k = kk; k < kk + TILE_SIZE; k++) {
                            sum += A[i*N + k] * B[k*N + j];
                        }
                        C[i*N + j] = sum;
                    }
                }
            }
        }
    }
}
```

**2. Performance Report** (PDF/Markdown)

```markdown
# Performance Optimization Report

## Executive Summary
Successfully optimized matrix multiplication kernel with **3.45× speedup**

## Performance Comparison
| Metric | Baseline | Optimized | Improvement |
|--------|----------|-----------|-------------|
| GFLOPS | 2.1 | 7.24 | **+245%** |
 Execution Time | 15.2s | 4.4s | **-71%** |
| L1 Cache Misses | 45% | 18% | **-60%** |
| L2 Cache Misses | 22% | 12% | **-45%** |

## Optimizations Applied
1. **Loop Tiling** (32×32 blocks)
   - Reduced cache misses by 60%
   - Improved memory locality

2. **AVX-512 Vectorization**
   - 92% vectorization rate achieved
   - Utilized SIMD instructions efficiently

## Statistical Validation
- **95% Confidence Interval**: [7.1, 7.4] GFLOPS
- **Coe cient of Variation**: 1.6% (excellent reproducibility)
- **Statistical Significance**: *** p < 0.0001

## Recommendations
- Further improvement possible with loop unrolling
- Consider prefetching for large matrices
- Multi-threading could provide additional 2-4× speedup
```

**3. Evidence Artifacts Package**

```
artifacts/
├── task_id/
│   ├── profiling/
│   │   ├── likwid_baseline.json
│   │   ├── likwid_optimized.json
│   │   └── perf_counters.csv
│   ├── code/
│   │   ├── my_gemm_code_original.c
│   │   ├── my_gemm_code_tiled.c
│   │   └── my_gemm_code_optimized.c
│   ├── compilation/
│   │   ├── gcc_baseline.log
│   │   └── gcc_optimized.log
│   ├── testing/
│   │   ├── correctness_tests.txt
│   │   ├── regression_tests.txt
│   │   └── numerical_errors.csv
│   ├── visualization/
│   │   ├── performance_comparison.png
│   │   ├── cache_behavior.png
│   │   └── speedup_chart.png
│   └── documentation/
│       ├── optimization_decision_log.txt
│       ├── llm_conversation_history.json
│       └── implementation_notes.md
```

**4. Database Records**

- Task execution log in PostgreSQL
- Performance metrics stored for future analysis
- Optimization strategies catalogued
- LLM interaction traces archived

---

## 4. What Concurrent Processes Run

### Parallel Execution (When Multiple Tasks)

**Independent Tasks Run Simultaneously:**

```
Task Queue:
├── [PRIORIYY HIGH] User A: GEMM optimization → Profiling → LLM → Optimization
├── [PRIORITY MEDIUM] User B: FFT optimization → Profiling → LLM → Optimization
└── [PRIORITY LOW] User C: Code analysis → Profiling → Analysis

Concurrent Execution:
┌─ Worker 1: User A - LIKWID profiling (5 min)
├─ Worker 2: User B - LIKWID profiling (5 min)
└─ Worker 3: User C - Code analysis (8 min)

After profiling completes:
┌─ Worker 1: User A - LLM optimization analysis (10 min)
├─ Worker 2: User B - LLM optimization analysis (10 min)
└─ Worker 3: User C - Analysis report generation (2 min)
```

**Dependent Steps Run Sequentially:**

```
Single Workflow (Must wait for completion):
Baseline Profiling (5 min) ► LLM Analysis (10 min) ► Code Optimization (5 min) ►
Compilation (2 min) ► Validation (5 min) ► Performance Testing (8 min)

Total: 35 minutes sequential execution
```

### Background Processes

**Continuous Monitoring:**

```
Monitor Process:
├─ Check active task completion status (every 30 seconds)
├─ Monitor resource utilization (CPU, memory, queue length)
├─ Scale worker nodes up/down based on load
└─ Alert on failed tasks or resource exhaustion

Maintenance Process:
├─ Archive completed task data (daily)
├─ Clean up temporary files (hourly)
├─ Update statistics and metrics (every 5 minutes)
└─ Backup database and artifacts (nightly)
```

---

## 5. Different Task Types: What Runs When

### Type 1: Simple Optimization (RUN directly)

**What happens:**

```
User submits: "optimize my_gemm.c for speed"

System runs:
1. Baseline profiling (5 min)
2. Single LLM analysis (10 min)
3. Code generation (5 min)
4. Compilation (2 min)
5. Validation (5 min)
6. Performance testing (8 min)

Total: ~35 minutes fully automated
```

### Type 2: Iterative Optimization (RUN with feedback)

**What happens:**

```
User submits: "optimize my_gemm.c, multiple iterations"

System runs (iteration 1):
1. Baseline profiling (5 min)
2. LLM analysis (10 min)
3. Code optimization #1 (5 min)
4. Validation (5 min)
5. Performance test #1 (8 min)

Review results: 2.1 → 3.2 GFLOPS (+52%)

System runs (iteration 2):
6. New profiling (5 min)
7. Revised LLM analysis (10 min)
8. Code optimization #2 (5 min)
9. Validation (5 min)
10. Performance test #2 (8 min)

Review results: 3.2 → 5.1 GFLOPS (+59%)

System runs (iteration 3):
11. Final profiling (5 min)
12. Final LLM refinement (10 min)
13. Code optimization #3 (5 min)
14. Validation (5 min)
15. Final performance test (8 min)

Final results: 5.1 GFLOPS (+143% total)
Total: ~1.5 hours with multiple optimization cycles
```

### Type 3: Debugging Task (RUN with error correction)

**What happens:**

```
User submits: "my FFT code gives wrong results"

System runs:
1. Compile and run error detection (5 min)
2. Analyze crash log/error output (3 min)
3. LLM code analysis (10 min)
4. Identify potential causes (e.g., division by zero) (5 min)
5. Generate fix code (5 min)
6. Compile fix (2 min)
7. Test correctness (5 min)
8. Verify numerical accuracy (5 min)

Total: ~40 minutes to diagnose and fix bug
```

### Type 4: Benchmark Comparison (RUN multiple tests)

**What happens:**

```
User submits: "compare my GEMM against MKL baseline"

System runs:
1. Compile user code (2 min)
2. Profile user code (5 min)
3. Compile MKL reference (2 min)
4. Profile MKL reference (5 min)
5. Statistical comparison analysis (10 min)
6. Generate comparison report (5 min)
7. Visual comparison charts (5 min)

Total: ~35 minutes for comprehensive analysis
```

---

## 6. Resource Utilization: What Uses What

### During Profiling Phase

```
CPU: High (running benchmarks, collecting counters)
Memory: High (profiling data, large matrices)
Storage: Low (temporary files)
Network: Low (local execution)
LLM API: None (no AI involved yet)

Resource Budget:
├─ 2 CPU cores (for profiling)
├─ 4 GB RAM (for matrices)
├─ 100 MB temporary storage
└─ 5 minutes execution time
```

### During LLM Analysis Phase

```
CPU: Low (API calls, text processing)
Memory: Medium (context storage, parsing)
Storage: Low (conversation history)
Network: High (LLM API calls)
LLM API: High (analysis queries)

Resource Budget:
├─ 0.5 CPU cores (for orchestration)
├─ 1 GB RAM (context management)
├─ 50 MB storage (conversation logs)
└─ 10 minutes (API latency + processing)
```

### During Code Generation Phase

```
CPU: Medium (code generation, parsing)
Memory: Medium (code storage, parsing)
Storage: Low (source files)
Network: Medium (LLM API calls)
LLM API: Medium (code generation queries)

Resource Budget:
├─ 1 CPU core (for orchestration)
├─ 2 GB RAM (code storage)
├─ 500 KB storage (source files)
└─ 5 minutes (code generation + validation)
```

### During Compilation Phase

```
CPU: Very High (compiler optimization)
Memory: High (intermediate compilation)
Storage: Medium (object files, binaries)
Network: Low (local compilation)
LLM API: None

Resource Budget:
├─ 4 CPU cores (compilation)
├─ 8 GB RAM (intermediate code)
├─ 2 GB storage (object files)
└─ 2-5 minutes compilation time
```

### During Testing Phase

```
CPU: High (running test cases)
Memory: Medium (test data storage)
Storage: Low (test results)
Network: Low (local testing)
LLM API: None

Resource Budget:
├─ 2-4 CPU cores (parallel testing)
├─ 4 GB RAM (test matrices)
├─ 100 MB storage (test results)
└─ 5-15 minutes comprehensive testing
```

---

## 7. What Gets Logged and Tracked

### Execution Logs (What happened and when)

```
2026-09-11 14:30:45 INFO Task TASK-0001 submitted by user johndoe
2026-09-11 14:30:45 INFO Task scheduled with priority HIGH
2026-09-11 14:32:15 INFO Profiling started on my_gemm_code.c
2026-09-11 14:37:15 INFO Profiling completed: baseline 2.1 GFLOPS
2026-09-11 14:38:30 INFO LLM analysis started with ollama/llama3
2026-09-11 14:48:30 INFO LLM analysis completed: loop tiling recommended
2026-09-11 14:50:15 INFO Code generation completed
2026-09-11 14:52:30 INFO Compilation successful (0 warnings)
2026-09-11 14:57:45 INFO Validation passed: numerical accuracy 1e-7
2026-09-11 15:05:45 INFO Performance testing completed: 7.2 GFLOPS
2026-09-11 15:07:30 INFO Task TASK-0001 completed successfully
2026-09-11 15:07:30 INFO Results package generated and archived
```

### Performance Metrics (Quantitative results)

```
# Database records for analysis
{
  "task_id": "TASK-0001",
  "user_id": "johndoe",
  "timestamp": "2026-09-11T14:30:45Z",
  "category": "OPTIMIZATION",
  "complexity": " intermediate",
  "duration": "36.75 minutes",

  "metrics": {
    "baseline_gflops": 2.1,
    "optimized_gflops": 7.2,
    "speedup": 3.43,
    "improvement": "243%",

    "cache_improvement": {
      "l1_reduction": "60%",
      "l2_reduction": "45%"
    },

    "statistical_confidence": {
      "confidence_interval": "[7.1, 7.3]",
      "coefficient_of_variation": 0.016,
      "significance": "*** p < 0.0001"
    }
  }
}
```

### LLM Interaction Logs (AI reasoning)

```
# Conversation history for transparency
{
  "turn": 1,
  "user_request": "Optimize this GEMM code for maximum FLOPS",
  "llm_analysis": {
    "thought_process": [
      "Analyzing loop structure: triple nested loops observed",
      "Profiling data shows 45% L1 cache miss rate - major bottleneck",
      "No vectorization detected (0%) - missed AVX-512 opportunity",
      "Memory bandwidth utilization only 56% of theoretical"
    ],
    "recommendation": "Implement loop tiling with 32×32 blocks to improve cache locality",
    "expected_improvement": "2-3× speedup with minimal complexity"
  }
}
```

---

## 8. Error Handling: What Goes Wrong and How It's Fixed

### Common Issues and Automatic Recovery

**1. Compilation Errors**

```
Error: "undefined reference to _mm512_mul_ps"
Cause: Missing AVX-512 library compilation flag

Automatic Fix:
├─ LLM detects compilation error pattern
├─ Analyzes error message
├─ Generates fix: Add "-mavx512f -march=native" flag
├─ Re-compiles with corrected flags
└─ Continues workflow
```

**2. LLM API Timeout**

```
Error: "Ollama API request timeout after 120 seconds"
Cause: Overloaded local model or network issue

Automatic Fix:
├─ Detects timeout in API call
├─ Retries with exponential backoff (10s, 30s, 90s)
├─ Falls back to alternative provider (e.g., OpenAI)
├─ Resubmits analysis request
└─ Continues workflow
```

**3. Numerical Incorrectness**

```
Error: "Correctness test failed: maximum error 1.2e-4 exceeds tolerance 1e-6"
Cause: Optimization introduced numerical instability

Automatic Fix:
├─ LLM analyzes numerical error locations
├─ Identifies problematic transformation
├─ Generates conservative alternative (e.g., safer division)
├─ Re-compiles and re-tests
└─ Continues workflow if corrected
```

**4. Resource Exhaustion**

```
Error: "Insufficient memory for 4096×4096 matrix test"
Cause: Test case larger than available memory

Automatic Fix:
├─ Detects memory exhaustion
├─ Reduces test size to fit memory
├─ Uses representative smaller test cases
├─ Estimates large-scale performance with extrapolation
└─ Continues workflow
```

---

## 9. Summary: The End-to-End Flow

### What Runs in Sequence (30-60 minutes typical)

```
START
 ↓
[5 min] Profiling: Measure baseline performance
 ↓
[10 min] LLM Analysis: AI analyzes code + profiling data
 ↓
[5 min] Code Generation: AI modifies source code
 ↓
[2 min] Compilation: Compile optimized code
 ↓
[5 min] Validation: Test correctness
 ↓
[8 min] Performance Testing: Measure improvement
 ↓
[5 min] Report Generation: Create deliverables
 ↓
[End] Results: Code + Report + Evidence Artifacts

Total: ~40 minutes fully automated
```

### What You Get at the End

1. **Faster Code** - Optimized source code you can use immediately
2. **Performance Report** - Detailed analysis of improvements
3. **Evidence Package** - All data for scientific reproducibility
4. **Optimization Recommendations** - Suggestions for further work
5. **Documentation** - Explains what was changed and why

### Key System Characteristics

- **Fully Automated**: No manual intervention required
- **Scientifically Sound**: Statistical validation, reproducible results
- **Transparent**: Complete logs and traceability
- **Scalable**: Handles multiple concurrent requests
- **Intelligent**: AI-driven optimization decisions
- **Robust**: Automatic error handling and recovery

---

## 10. Real-World Example: What Actually Happens

### User Submits: "my calculation is too slow, make it faster"

**Behind the scenes, this is what runs:**

```
0. User uploads: inefficient_heat_equation_solver.c (15KB file)

1. [System Runs] Compilation of user code
   └─ Command: gcc -O2 inefficient_heat_equation_solver.c -o slow_solver
   └─ Output: runnable binary (maybe with warnings)

2. [System Runs] Baseline profiling
   └─ Command: likwid-perfctr -C 2 -g FLOPS_DP, CACHE, MEM ./slow_solver 2048
   └─ Results: 1.3 GFLOPS, 58% L1 cache misses, memory bandwidth limited

3. [System Runs] LLM code analysis
   └─ API Call: Send code + profiling data to Ollama LLaMA-3
   └─ Analysis: "High cache misses in stencil loops, no SIMD vectorization"
   └─ Recommendation: "Apply 3D blocking + AVX-512 vectorization"

4. [System Runs] Code optimization
   └─ AI generates: optimized_heat_equation_solver.c (18KB file)
   └─ Changes: Added 8×8×8 tiling, AVX-512 intrinsics in inner loops

5. [System Runs] Compilation of optimized code
   └─ Command: gcc -march=native -O3 -ffast-math -mavx512f \
                  optimized_heat_equation_solver.c -o fast_solver
   └─ Output: optimized binary (no warnings)

6. [System Runs] Correctness validation
   └─ Test: Compare results for 256³, 512³, 1024³ grids
   └─ Result: Maximum error 2.1e-7 within 1e-6 tolerance ✓

7. [System Runs] Performance measurement
   └─ Command: likwid-perfctr -C 2 -g FLOPS_DP ./fast_solver 2048
   └─ Results: 4.8 GFLOPS, 19% L1 cache misses, efficient bandwidth usage
   └─ Speedup: 3.7× improvement, 87% memory bandwidth utilization

8. [System Runs] Report generation
   └─ Create: performance_report.pdf with charts and tables
   └─ Package: evidence_artifacts.zip with all data

9. [User Receives]
   └─ optimized_heat_equation_solver.c (ready to use)
   └─ performance_report.pdf (detailed analysis)
   └─ evidence_artifacts.zip (scientific documentation)
   └─ Summary email: "Your code is now 3.7× faster and scientifically validated"

Total time: ~42 minutes automated processing
```

This is what actually runs when you use the system - a complete, automated pipeline from code submission to optimized, validated results.
