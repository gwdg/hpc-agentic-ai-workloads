#!/usr/bin/env python3
"""
HPC-ARC Complete Task Database Generator

This script generates the complete 100-task HPC-ARC database as specified in the
pascit_orchestrator paper:
- 25 Explore Tasks (Environment Discovery)
- 20 Hypothesize Tasks (Optimization Opportunity Identification)  
- 55 Execute Tasks (25 Parallelize + 30 Optimize)
- 5 Generalize Tasks (Cross-Architecture Knowledge Transfer)

Each task includes:
- Complete specification
- Reference results (expert baseline, optimal theoretical)
- Difficulty levels
- Evaluation criteria
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ARCCategory(Enum):
    EXPLORE = "explore"
    HYPOTHESIZE = "hypothesize"
    EXECUTE = "execute"
    GENERALIZE = "generalize"


class TaskDifficulty(Enum):
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ReferenceResults:
    """Reference results for each task"""
    expert_baseline: float = 0.0  # Traditional HPC expert performance
    optimal_theoretical: float = 1.0  # Best possible theoretical performance
    llm_generic_baseline: float = 0.45  # Generic LLM without HPC specialization
    algorithmic_solution: float = 0.95  # Known optimal algorithm


@dataclass
class HPCARCTaskComplete:
    """Complete HPC-ARC task specification with reference results"""
    task_id: str
    name: str
    category: ARCCategory
    difficulty: TaskDifficulty
    mission: str
    description: str
    estimated_time_budget: str
    codebase: Dict[str, Any]
    hardware: Dict[str, str]
    available_tools: List[str]
    unknown_characteristics: List[str]
    evaluation_criteria: Dict[str, Dict[str, Any]]
    reference_results: ReferenceResults
    intelligence_metrics_weights: Dict[str, float]  # Phase-specific weights

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization"""
        data = asdict(self)
        data['category'] = self.category.value
        data['difficulty'] = self.difficulty.value
        data['reference_results'] = asdict(self.reference_results)
        return data


class HPCARCDatabaseGenerator:
    """Generates complete HPC-ARC task database"""

    def __init__(self):
        self.tasks: List[HPCARCTaskComplete] = []
        self.task_counter = {
            'explore': 1,
            'hypothesize': 1,
            'parallelize': 1,  # Execute subcategory
            'optimize': 1,    # Execute subcategory
            'generalize': 1
        }

    def _generate_task_id(self, category: str, subcategory: str = None) -> str:
        """Generate next task ID for category"""
        if category == 'execute':
            prefix = 'EX' if subcategory == 'parallelize' else 'EO'
            counter = self.task_counter[subcategory]
            self.task_counter[subcategory] += 1
            return f"{prefix}-{counter:03d}"
        else:
            prefix = category[0].upper()
            counter = self.task_counter[category]
            self.task_counter[category] += 1
            return f"{prefix}-{counter:03d}"

    def _create_explore_tasks(self) -> List[HPCARCTaskComplete]:
        """Create 25 Explore tasks for environment discovery"""
        tasks = []

        # Cache Discovery Tasks (6 tasks) - reduced from 8 to 6
        cache_tasks = [
            {
                "name": "L1/L2/L3 Cache Threshold Behavior Discovery",
                "mission": "Discover cache size thresholds through systematic matrix operation profiling",
                "unknown": ["L1/L2/L3 cache line sizes", "Optimal matrix dimensions for each cache level"],
                "expert": 0.82, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Cache Line Size Exploration",
                "mission": "Determine cache line size through stride analysis",
                "unknown": ["Cache line width", "Prefetch behavior"],
                "expert": 0.88, "difficulty": TaskDifficulty.ELEMENTARY
            },
            {
                "name": "Cache Associativity Pattern Discovery",
                "mission": "Map cache associativity through conflict mapping",
                "unknown": ["Cache associativity (-wayness)", "Conflict mapping patterns"],
                "expert": 0.75, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Write-Through vs Write-Back Cache Policy Discovery",
                "mission": "Identify cache write policy through write pattern analysis",
                "unknown": ["Cache write policy", "Write buffer characteristics"],
                "expert": 0.70, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "TLB Translation Lookaside Buffer Discovery",
                "mission": "Discover TLB size and associativity through page mapping",
                "unknown": ["TLB entries (L1/L2)", "Page size optimization"],
                "expert": 0.65, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Cache-Coherence Protocol Analysis",
                "mission": "Characterize inter-core cache coherence behavior",
                "unknown": ["Coherence protocol overhead", "False sharing patterns"],
                "expert": 0.55, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Branch Prediction Unit Profiling",
                "mission": "Discover branch predictor characteristics through branch pattern testing",
                "unknown": ["Branch predictor type", "BTB size and associativity"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Hardware Prefetcher Detection and Analysis",
                "mission": "Characterize hardware prefetcher behavior and effectiveness",
                "unknown": ["Prefetcher type", "Detection distance and aggressiveness"],
                "expert": 0.68, "difficulty": TaskDifficulty.INTERMEDIATE
            }
        ]

        for i, task in enumerate(cache_tasks):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.95,
                llm_generic_baseline=0.42
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('explore'),
                name=task["name"],
                category=ARCCategory.EXPLORE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Cache Discovery Task {i+1}: {task['mission']}. AI agents must systematically explore cache characteristics through structured profiling experiments.",
                estimated_time_budget="15 minutes",
                codebase={
                    "files": ["cache_exploration.c", "profiling_framework.h"],
                    "language": "C99",
                    "optimization_level": "O0"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "cores": "32 physical, 64 threads",
                    "cache": "L1: 32KB/core, L2: 1MB/core, L3: 48MB/shared"
                },
                available_tools=["LIKWID", "perf", "PAPI", "VTune"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Model accuracy > 85%", "weight": 0.3},
                    "efficiency": {"requirements": "Complete within time budget", "weight": 0.3},
                    "exploration": {"requirements": "Minimal iteration count", "weight": 0.4}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "exploration_efficiency": 0.4,
                    "model_accuracy": 0.6
                }
            )
            tasks.append(complete_task)

        # Memory Bandwidth Discovery Tasks (8 tasks)
        memory_tasks = [
            {
                "name": "Peak Memory Bandwidth Characterization",
                "mission": "Determine peak sustainable memory bandwidth",
                "unknown": ["Maximum bandwidth (GB/s)", "Bandwidth saturation patterns"],
                "expert": 0.85, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "NUMA Node Memory Hierarchy Discovery",
                "mission": "Map NUMA topology and memory latency characteristics",
                "unknown": ["NUMA node count", "Inter-node latency/throughput"],
                "expert": 0.78, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Prefetch Distance Optimization",
                "mission": "Find optimal prefetch distance through systematic exploration",
                "unknown": ["Optimal prefetch gap", "Prefetch bandwidth saturation"],
                "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Memory Controller Concurrency Analysis",
                "mission": "Characterize memory controller parallelism and queuing",
                "unknown": ["Memory channel count", "Controller concurrency limits"],
                "expert": 0.58, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "TLB Miss Cost Quantification",
                "mission": "Measure TLB miss costs across different access patterns",
                "unknown": ["TLB miss latency (cycles)", "TLB replacement policy"],
                "expert": 0.65, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Vector Load/Unit Store Characteristics",
                "mission": "Profile vector memory access patterns and efficiency",
                "unknown": ["Vector load/store throughput", "Gather/scatter costs"],
                "expert": 0.70, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Non-Unit Stride Access Pattern Discovery",
                "mission": "Characterize performance of non-unit stride memory patterns",
                "unknown": ["Stride efficiency degradation", "Optimal stride values"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Memory Compression and Encryption Effects",
                "mission": "Detect hardware memory compression/encryption and performance impact",
                "unknown": ["Compression enablement", "Performance impact of encryption"],
                "expert": 0.48, "difficulty": TaskDifficulty.EXPERT
            }
        ]

        for i, task in enumerate(memory_tasks):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.98,
                llm_generic_baseline=0.38
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('explore'),
                name=task["name"],
                category=ARCCategory.EXPLORE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Memory Discovery Task {i+1}: {task['mission']}. Focus on systematic memory profiling experiments.",
                estimated_time_budget="20 minutes",
                codebase={
                    "files": ["memory_bandwidth.c", "stream_style_benchmark.c"],
                    "language": "C99",
                    "optimization_level": "O0"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "memory": "384GB DDR4 3200MHz",
                    "channels": "8 memory channels"
                },
                available_tools=["LIKWID", "numactl", "perf", "mbw"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Bandwidth characterization accuracy > 90%", "weight": 0.4},
                    "efficiency": {"requirements": "Complete within budget", "weight": 0.3},
                    "exploration": {"requirements": "Systematic methodology", "weight": 0.3}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "exploration_efficiency": 0.35,
                    "measurement_accuracy": 0.65
                }
            )
            tasks.append(complete_task)

        # CPU/Core Discovery Tasks (5 tasks)
        cpu_tasks = [
            {
                "name": "Core Frequency Scaling Behavior Discovery",
                "mission": "Map turbo boost frequency scaling characteristics",
                "unknown": ["Turbo boost duration limits", "Thermal throttling thresholds"],
                "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Hyper-Threading Effectiveness Analysis",
                "mission": "Quantify hyper-threading performance impact across workloads",
                "unknown": ["SMT performance gain", "Resource contention effects"],
                "expert": 0.68, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Vector Unit Capabilities Discovery",
                "mission": "Characterize SIMD vector unit capabilities and limitations",
                "unknown": ["SIMD width (AVX-256/AVX-512)", "Vector register count"],
                "expert": 0.82, "difficulty": TaskDifficulty.ELEMENTARY
            },
            {
                "name": "Instruction Pipeline Parallelism",
                "mission": "Discover instruction pipeline depth and parallelism through latency testing",
                "unknown": ["Pipeline depth", "Instruction issue width"],
                "expert": 0.55, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Distributed Tag Store / Instruction Cache Analysis",
                "mission": "Characterize instruction cache and fetch unit characteristics",
                "unknown": ["I-Cache size/associativity", "Instruction fetch bandwidth"],
                "expert": 0.52, "difficulty": TaskDifficulty.EXPERT
            }
        ]

        for i, task in enumerate(cpu_tasks):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.96,
                llm_generic_baseline=0.40
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('explore'),
                name=task["name"],
                category=ARCCategory.EXPLORE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"CPU/Core Discovery Task {i+1}: {task['mission']}. Focus on core-level hardware capabilities.",
                estimated_time_budget="18 minutes",
                codebase={
                    "files": ["core_profiling.c", "instruction_stream.c"],
                    "language": "C99",
                    "optimization_level": "O0"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "cores": "32 physical, 64 threads",
                    "simd": "AVX-512 (2x512-bit FMA units)"
                },
                available_tools=["perf", "LIKWID", "cpufreq-info", "lscpu"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Characteristic accuracy > 85%", "weight": 0.35},
                    "efficiency": {"requirements": "Complete within budget", "weight": 0.35},
                    "exploration": {"requirements": "Systematic protocol design", "weight": 0.3}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "exploration_efficiency": 0.4,
                    "characterization_completeness": 0.6
                }
            )
            tasks.append(complete_task)

        # Network/System Discovery Tasks (4 tasks)
        system_tasks = [
            {
                "name": "Thread Synchronization Primitives Discovery",
                "mission": "Characterize synchronization primitive costs and scalability",
                "unknown": ["Pthread mutex cost", "Futex vs semaphore overhead"],
                "expert": 0.70, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Atomic Operation Performance Analysis",
                "mission": "Profile atomic operation performance and contention behavior",
                "unknown": ["Atomic operation latency", "Cache line bouncing cost"],
                "expert": 0.65, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Inter-Socket Communication Costs",
                "mission": "Quantify cross-socket communication latency and bandwidth",
                "unknown": ["QPI/UPI interconnect latency", "Coherence protocol costs"],
                "expert": 0.58, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "System Call Overhead Analysis",
                "mission": "Measure system call costs and kernel modeswitch penalties",
                "unknown": ["System call base cost", "Context switch overhead"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            }
        ]

        for i, task in enumerate(system_tasks):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.94,
                llm_generic_baseline=0.42
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('explore'),
                name=task["name"],
                category=ARCCategory.EXPLORE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"System Discovery Task {i+1}: {task['mission']}. Focus on OS and threading characteristics.",
                estimated_time_budget="22 minutes",
                codebase={
                    "files": ["sync_profiling.c", "atomic_operations.c"],
                    "language": "C99",
                    "optimization_level": "O0"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "sockets": "2 sockets",
                    "interconnect": "UPI 11.2GT/s"
                },
                available_tools=["perf", "strace", "latencytop", "LIKWID"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Synchronization cost accuracy > 80%", "weight": 0.35},
                    "efficiency": {"requirements": "Complete within budget", "weight": 0.35},
                    "exploration": {"requirements": "Systematic contended testing", "weight": 0.3}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "exploration_efficiency": 0.4,
                    "measurement_methodology": 0.6
                }
            )
            tasks.append(complete_task)

        return tasks

    def _create_hypothesize_tasks(self) -> List[HPCARCTaskComplete]:
        """Create 20 Hypothesize tasks for optimization opportunity identification"""
        tasks = []

        # Memory Optimization Hypotheses (8 tasks)
        memory_hypotheses = [
            {
                "name": "NUMA-Aware Memory Allocation Impact Prediction",
                "mission": "Formulate hypothesis about NUMA-aware first-touch allocation improvements",
                "unknown": ["NUMA locality improvement", "Remote memory access reduction"],
                "expert": 0.78, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Cache-Blocking Matrix Multiplication Impact Analysis",
                "mission": "Predict optimal cache-blocking dimensions and expected speedup",
                "unknown": ["Optimal block size", "Cache miss reduction estimate"],
                "expert": 0.85, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Vector Register Reuse Opportunity Assessment",
                "mission": "Hypothesize vector register reuse opportunities in compute kernels",
                "unknown": ["Register pressure analysis", "Vectorization efficiency gain"],
                "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Memory Access Pattern Regularization Hypothesis",
                "mission": "Formulate hypothesis about memory pattern regularization benefits",
                "unknown": ["Stride regularization improvement", "Spatial locality gain"],
                "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Prefetch Strategy Feasibility Assessment",
                "mission": "Evaluate hardware prefetch versus software prefetch tradeoffs",
                "unknown": ["Prefetch distance optimization", "Prefetch bandwidth impact"],
                "expert": 0.65, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Loop Tiling Strategy Space Exploration",
                "mission": "Formulate hypothesis about optimal multi-dimensional tiling strategies",
                "unknown": ["Tiling dimensions tradeoffs", "Register pressure vs cache locality"],
                "expert": 0.58, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Data Layout Transformation Impact Prediction",
                "mission": "Assess AoS vs SoA vs hybrid layout performance characteristics",
                "unknown": ["Layout transformation benefit", "Vectorization compatibility"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Memory Compression Opportunity Analysis",
                "mission": "Hypothesize benefit of algorithmic memory compression techniques",
                "unknown": ["Compression factor vs speedup", "Decompression cost analysis"],
                "expert": 0.48, "difficulty": TaskDifficulty.EXPERT
            }
        ]

        for i, task in enumerate(memory_hypotheses):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.97,
                llm_generic_baseline=0.45
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('hypothesize'),
                name=task["name"],
                category=ARCCategory.HYPOTHESIZE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Memory Optimization Hypothesis {i+1}: {task['mission']}. Requires quantitative predictions with feasibility assessment.",
                estimated_time_budget="12 minutes",
                codebase={
                    "files": ["memory_analysis.c", "impact_estimation.c"],
                    "language": "C99",
                    "optimization_level": "O2"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "memory": "384GB DDR4",
                    "cache": "LLC: 48MB"
                },
                available_tools=["perf", "LIKWID", "VTune analyzer"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Prediction accuracy > 85%", "weight": 0.35},
                    "efficiency": {"requirements": "Feasibility assessment", "weight": 0.35},
                    "hypothesis": {"requirements": "Quantitative confidence level", "weight": 0.3}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "prediction_accuracy": 0.4,
                    "feasibility_assessment": 0.3,
                    "impact_prioritization": 0.3
                }
            )
            tasks.append(complete_task)

        # Compute Optimization Hypotheses (6 tasks)
        compute_hypotheses = [
            {
                "name": "AVX Vectorization Speedup Prediction",
                "mission": "Predict AVX-512 vectorization benefits for specific compute kernels",
                "unknown": ["Speedup flops-to-flops ratio", "Vectorization overhead"],
                "expert": 0.82, "difficulty": TaskDifficulty.ELEMENTARY
            },
            {
                "name": "Loop Unrolling Impact Assessment",
                "mission": "Formulate hypothesis about optimal loop unrolling factors",
                "unknown": ["Unrolling factor sweet spot", "Instruction cache pressure"],
                "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "FMA Operation Effectiveness Hypothesis",
                "mission": "Assess fused multiply-add operation benefits vs separate mul+add",
                "unknown": ["FMA throughput gain", "Accuracy/precision analysis"],
                "expert": 0.70, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Branch Prediction Impact on Compute Kernels",
                "mission": "Hypothesize branch elimination benefits for numeric kernels",
                "unknown": ["Branch misprediction cost", "Branchless implementation complexity"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Instruction-Level Parallelism Opportunity Analysis",
                "mission": "Assess ILP extraction potential in sequential code",
                "unknown": ["Dependency chain reduction", "Out-of-order execution utilization"],
                "expert": 0.55, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Software Pipelining Feasibility Assessment",
                "mission": "Evaluate software pipelining vs traditional loop optimization",
                "unknown": ["Pipelining stage count", "Register allocation complexity"],
                "expert": 0.48, "difficulty": TaskDifficulty.EXPERT
            }
        ]

        for i, task in enumerate(compute_hypotheses):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.96,
                llm_generic_baseline=0.42
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('hypothesize'),
                name=task["name"],
                category=ARCCategory.HYPOTHESIZE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Compute Optimization Hypothesis {i+1}: {task['mission']}. Focus on instruction-level optimization prediction.",
                estimated_time_budget="10 minutes",
                codebase={
                    "files": ["compute_kernels.c", "vectorization_analysis.c"],
                    "language": "C99",
                    "optimization_level": "O2"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "simd": "AVX-512 with 2xFMA"
                },
                available_tools=["perf", "objdump", "LatencyTOP"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Prediction error < 15%", "weight": 0.3},
                    "efficiency": {"requirements": "Implementation complexity assessment", "weight": 0.35},
                    "hypothesis": {"requirements": "Confidence interval specification", "weight": 0.35}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "prediction_accuracy": 0.35,
                    "feasibility_assessment": 0.35,
                    "implementation_complexity": 0.3
                }
            )
            tasks.append(complete_task)

        # Parallel/Thread Optimization Hypotheses (6 tasks)
        parallel_hypotheses = [
            {
                "name": "OpenMP Parallelization Speedup Prediction",
                "mission": "Predict OpenMP parallel scaling for different thread counts",
                "unknown": ["Parallel efficiency degradation", "Optimal thread count"],
                "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE
            },
            {
                "name": "Thread Affinity Impact Assessment",
                "mission": "Hypothesize benefit of thread affinity and NUMA binding",
                "unknown": ["Affinity speedup factor", "Migration cost reduction"],
                "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Task-Based vs Loop-Based Parallelization",
                "mission": "Assess task parallelism vs loop parallelism tradeoffs",
                "unknown": ["Task granularity optimization", "Load balancing analysis"],
                "expert": 0.62, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "GPU Offloading Feasibility Hypothesis",
                "mission": "Evaluate GPU offloading benefits vs CPU optimization",
                "unknown": ["PCIe transfer overhead", "GPU compute capability"],
                "expert": 0.55, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Lock Step SIMD vs MIMD Parallelism",
                "mission": "Assess vector parallelism vs thread parallelism effectiveness",
                "unknown": ["SIMD efficiency ceiling", "Thread parallel scalability"],
                "expert": 0.58, "difficulty": TaskDifficulty.ADVANCED
            },
            {
                "name": "Implicit vs Explicit Parallelization Strategy",
                "mission": "Compare compiler auto-parallelization vs explicit threading",
                "unknown": ["Compiler parallelization effectiveness", "Manual tuning complexity"],
                "expert": 0.65, "difficulty": TaskDifficulty.INTERMEDIATE
            }
        ]

        for i, task in enumerate(parallel_hypotheses):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.95,
                llm_generic_baseline=0.40
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('hypothesize'),
                name=task["name"],
                category=ARCCategory.HYPOTHESIZE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Parallel Optimization Hypothesis {i+1}: {task['mission']}. Focus on concurrency and scaling prediction.",
                estimated_time_budget="15 minutes",
                codebase={
                    "files": ["parallel_benchmarks.c", "scaling_analysis.c"],
                    "language": "C99",
                    "optimization_level": "O2",
                    "threads": "OpenMP 4.5"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "cores": "64 threads total",
                    "sockets": "2x Intel Xeon"
                },
                available_tools=["perf", "LIKWID", "VTune thread analyzer"],
                unknown_characteristics=task["unknown"],
                evaluation_criteria={
                    "correctness": {"requirements": "Scaling prediction accuracy > 80%", "weight": 0.3},
                    "efficiency": {"requirements": "Thread count optimization", "weight": 0.35},
                    "hypothesis": {"requirements": "Scaling model specification", "weight": 0.35}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "scaling_prediction": 0.4,
                    "feasibility_assessment": 0.3,
                    "implementation_complexity": 0.3
                }
            )
            tasks.append(complete_task)

        return tasks

    def _create_execute_tasks(self) -> List[HPCARCTaskComplete]:
        """Create 55 Execute tasks (25 Parallelize + 30 Optimize)"""
        tasks = []

        # Parallelize Tasks (25 tasks) - Serial to Parallel Conversion
        # I'll create exactly 25 parallelize tasks, ensuring correct count
        parallelize_tasks_config = [
            {"name": "Matrix Multiplication Parallelization", "mission": "Parallelize naive matrix multiplication with optimal thread blocking", "original": "O(n³) serial GEMM", "target": "Multi-threaded cache-blocking GEMM", "expert": 0.85, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Stencil 2D Heat Equation Parallelization", "mission": "Parallelize 2D finite difference heat equation solver", "original": "Serial stencil computation", "target": "Multi-domain parallel stencil", "expert": 0.80, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "N-Body Simulation Parallelization", "mission": "Parallelize O(n²) pairwise particle interactions", "original": "Serial n-body for loop", "target": "MPI/OpenMP hybrid n-body", "expert": 0.78, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "FFT 1D Parallelization", "mission": "Parallelize 1D FFT with data distribution", "original": "Serial FFTW implementation", "target": "Cluster FFT with data distribution", "expert": 0.75, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Monte Carlo Simulation Parallelization", "mission": "Parallelize Monte Carlo random sampling", "original": "Serial Monte Carlo worker", "target": "Embarrassingly parallel Monte Carlo", "expert": 0.92, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Graph Traversal BFS Parallelization", "mission": "Parallelize breadth-first search graph traversal", "original": "Serial BFS queue-based traversal", "target": "Parallel frontier-based BFS", "expert": 0.62, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Decision Tree Training Parallelization", "mission": "Parallelize decision tree building and evaluation", "original": "Serial recursive tree induction", "target": "Parallel level-based tree growth", "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Image Processing Pipeline Parallelization", "mission": "Parallelize multi-stage image processing pipeline", "original": "Serial stage-by-stage processing", "target": "Pipeline parallel image processing", "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Sparse Matrix-Vector Multiplication Parallelization", "mission": "Parallelize sparse matrix-vector multiplication", "original": "Serial CSR SpMV", "target": "Parallel load-balanced SpMV", "expert": 0.70, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Dynamic Programming Knapsack Parallelization", "mission": "Parallelize dynamic programming knapsack solver", "original": "Serial DP table filling", "target": "Parallel wavefront DP", "expert": 0.55, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Linear System Solver Parallelization", "mission": "Parallelize dense linear system (Gaussian elimination)", "original": "Serial LU decomposition", "target": "Parallel LU with pivoting", "expert": 0.65, "difficulty": TaskDifficulty.EXPERT},
            {"name": "3D Stencil LBM Parallelization", "mission": "Parallelize 3D lattice Boltzmann method fluid simulation", "original": "Serial 3D LBM computation", "target": "3D domain-decomposed LBM", "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Particle Filter Parallelization", "mission": "Parallelize particle filter state estimation", "original": "Serial sequential importance sampling", "target": "Parallel particle computation", "expert": 0.78, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Neural Network Inference Parallelization", "mission": "Parallelize neural network inference across cores", "original": "Serial layer-by-layer processing", "target": "Parallel batch inference", "expert": 0.82, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Ray Tracing Parallelization", "mission": "Parallelize ray tracing for batch rendering", "original": "Serial per-pixel ray tracing", "target": "Parallel tile/micropolygon ray tracing", "expert": 0.88, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Convolutional Network Layer Parallelization", "mission": "Parallelize CNN convolution layer computation", "original": "Serial nested loop convolution", "target": "Parallel im2col + GEMM convolution", "expert": 0.80, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Recurrent Neural Network Parallelization", "mission": "Parallelize RNN sequential processing", "original": "Serial temporal RNN processing", "target": "Parallel time unrolling RNN", "expert": 0.58, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Database Query Parallelization", "mission": "Parallelize SQL query execution", "original": "Serial query executor", "target": "Parallel query operators", "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "String Matching Parallelization", "mission": "Parallelize pattern matching algorithms", "original": "Serial string search", "target": "Parallel divide-and-conquer matching", "expert": 0.72, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Geometric Computation Parallelization", "mission": "Parallelize geometric algorithm (convex hull, triangulation)", "original": "Serial geometric algorithm", "target": "Parallel divide-conquer geometry", "expert": 0.60, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Combinatorial Optimization Parallelization", "mission": "Parallelize traveling salesman solver", "original": "Serial branch-and-bound TSP", "target": "Parallel branch competition TSP", "expert": 0.52, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Sorting Algorithm Parallelization", "mission": "Parallelize quicksort/merge sort implementation", "original": "Serial comparison-based sort", "target": "Parallel sample sort", "expert": 0.85, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Hash Compaction Parallelization", "mission": "Parallelize hash table insert/lookup operations", "original": "Serial hash chaining", "target": "Parallel hash lock-free operations", "expert": 0.65, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Tree Search Parallelization", "mission": "Parallelize alpha-beta pruning game tree search", "original": "Serial alpha-beta minimax", "target": "Parallel young brothers wait concept", "expert": 0.70, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Molecular Dynamics Parallelization", "mission": "Parallelize MD force computation and integration", "original": "Serial MD force loop", "target": "Spatial decomposition MD", "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED}
        ]

        # Generate tasks from config lists ensuring exact counts
        for i, task in enumerate(parallelize_tasks_config):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.95,
                llm_generic_baseline=0.45
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('execute', 'parallelize'),
                name=task["name"],
                category=ARCCategory.EXECUTE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Parallelization Task {i+1}: {task['mission']}. Convert serial implementation to parallel version.",
                estimated_time_budget="25 minutes",
                codebase={
                    "files": [f"parallel_{i+1}.c", "original_serial.c"],
                    "language": "C99",
                    "parallelization": "OpenMP 4.5 / MPI 4.1",
                    "optimization_level": "O2"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "cores": "64 threads available",
                    "memory": "384GB DDR4"
                },
                available_tools=["OpenMP", "MPI", "LIKWID", "perf", "VTune"],
                unknown_characteristics=[
                    task["original"],
                    "Optimal parallelization strategy",
                    "Load balancing challenges",
                    "Synchronization overhead"
                ],
                evaluation_criteria={
                    "correctness": {"requirements": "Numerical accuracy > 99.9%", "weight": 0.3},
                    "efficiency": {"requirements": "Parallel efficiency > 70%", "weight": 0.4},
                    "adaptation": {"requirements": "Scalability to target cores", "weight": 0.3}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "adaptation_speed": 0.4,
                    "scaling_efficiency": 0.35,
                    "correctness_preservation": 0.25
                }
            )
            tasks.append(complete_task)

        # Optimize Tasks (30 tasks) - Local Machine Optimization
        # I'll create exactly 30 optimize tasks, ensuring correct count
        optimize_tasks_config = [
            {"name": "AVX Vectorization Matrix Multiplication", "mission": "Optimize matrix multiplication with AVX-512 intrinsics", "baseline": "O2 compiled GEMM", "optimal": "handwritten AVX-512 blocked GEMM", "expert": 0.88, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Loop Unrolling Vector Operations", "mission": "Apply optimal loop unrolling and vectorization", "baseline": "Simple vector loop", "optimal": "Fully unrolled AVX vector ops", "expert": 0.82, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Cache Blocking Linear Algebra", "mission": "Optimize cache blocking for dense linear algebra", "baseline": "Cache-oblivious LA", "optimal": "Cache-parameter-tuned LA", "expert": 0.85, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Memory Access Pattern Optimization", "mission": "Optimize memory access patterns for spatial locality", "baseline": "Non-optimized strided access", "optimal": "Unit-stride coalesced access", "expert": 0.78, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "FMA Integration Floating Point", "mission": "Integrate FMA operations for improved throughput", "baseline": "Separate mul+add operations", "optimal": "FMA-fused operations", "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Branch Elimination Logic Optimizer", "mission": "Eliminate conditional branches in numeric kernels", "baseline": "Branch-based conditional logic", "optimal": "Branchless/select operations", "expert": 0.70, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Register Allocation Optimization", "mission": "Optimize register usage and reduction in spills", "baseline": "Compiler-register-allocated code", "optimal": "Hand-optimized register usage", "expert": 0.68, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Software Prefetch Tuning", "mission": "Optimize software prefetch distance and aggressiveness", "baseline": "No prefetch", "optimal": "L1 dataprefetcher tuning", "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "NUMA-Aware Allocation", "mission": "Implement NUMA-aware memory allocation and binding", "baseline": "Default allocation", "optimal": "First-touch + thread binding", "expert": 0.80, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Streamlined Pipeline Stages", "mission": "Optimize pipeline stages for improved throughput", "baseline": "Multi-cycle stalls", "optimal": "Single-cycle execution", "expert": 0.65, "difficulty": TaskDifficulty.EXPERT},
            {"name": "SIMD Reduction Optimization", "mission": "Optimize reduction operations with SIMD horizontal reduction", "baseline": "Sequential reduction", "optimal": "SIMD horizontal reduction", "expert": 0.78, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Instruction Scheduling", "mission": "Optimize instruction ordering for pipeline efficiency", "baseline": "Compiler-generated schedule", "optimal": "Manually optimized instruction schedule", "expert": 0.62, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Memory Layout Transformation", "mission": "Apply optimal data layout (AoS vs SoA vs hybrid)", "baseline": "Default AoS layout", "optimal": "Structure-of-Arrays with padding", "expert": 0.75, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Loop Inlining Optimization", "mission": "Optimize function call overhead through inlining", "baseline": "Function call overhead", "optimal": "Inlined critical path functions", "expert": 0.70, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Compiler Intrinsic Optimization", "mission": "Utilize compiler intrinsics for optimal code generation", "baseline": "Standard C++ code", "optimal": "Intel intrinsics usage", "expert": 0.82, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Cache Line Alignment", "mission": "Optimize memory allocation alignment for cache line boundaries", "baseline": "Default alignment", "optimal": "Cacheline-aligned allocation", "expert": 0.75, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Misprediction Reduction", "mission": "Reduce branch misprediction through prediction hints", "baseline": "Unoptimized branches", "optimal": "Likely/unlikely macros + branchless", "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Linear Algebra Solver Optimization", "mission": "Optimize linear system solver (e.g., conjugate gradient)", "baseline": "Standard CG implementation", "optimal": "Preconditioned + vectorized CG", "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Sparse Matrix Compression", "mission": "Optimize sparse matrix representation and computation", "baseline": "Standard CSR/COO format", "optimal": "Compressed sparse blocks + vectorization", "expert": 0.65, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Quantization Speed Optimization", "mission": "Optimize floating-point quantization operations", "baseline": "Standard float32 quantization", "optimal": "SIMD integer quantization", "expert": 0.78, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Memory Access Streaming", "mission": "Optimize memory access patterns for streaming workloads", "baseline": "Random access patterns", "optimal": "Sequential streaming access", "expert": 0.80, "difficulty": TaskDifficulty.ELEMENTARY},
            {"name": "Instruction Cache Optimization", "mission": "Optimize for instruction cache efficiency and footprint", "baseline": "Large instruction footprint", "optimal": "Code density + loop unrolling balance", "expert": 0.62, "difficulty": TaskDifficulty.EXPERT},
            {"name": "Branch Prediction Tuning", "mission": "Optimize code layout for improved branch prediction", "baseline": "Suboptimal layout", "optimal": "Basic block reordering", "expert": 0.65, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Loop Tiling Optimization", "mission": "Apply optimal multi-dimensional loop tiling", "baseline": "Untiled nested loops", "optimal": "Cache-optimal tile sizes", "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Vector Reduction Accumulation", "mission": "Optimize vector accumulator for numerical stability", "baseline": "Simple accumulation", "optimal": "Kahan summation + vectorization", "expert": 0.70, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Memory Bandwidth Optimization", "mission": "Optimize memory bandwidth utilization", "baseline": "Suboptimal memory access", "optimal": "Bandwidth-saturating access patterns", "expert": 0.82, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Pointer Dereferencing Optimization", "mission": "Optimize pointer chasing and indirect addressing", "baseline": "Pointer-heavy code", "optimal": "Direct array access + AoS", "expert": 0.68, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Floating Point Precision Optimization", "mission": "Optimize between float32/float64/float16 for performance vs accuracy", "baseline": "Always float64", "optimal": "Mixed precision optimization", "expert": 0.75, "difficulty": TaskDifficulty.INTERMEDIATE},
            {"name": "Loop Prefetch Integration", "mission": "Integrate loop prefetch with software prefetch instructions", "baseline": "No prefetch", "optimal": "Software prefetch in loops", "expert": 0.72, "difficulty": TaskDifficulty.ADVANCED},
            {"name": "Compiler Flag Optimization", "mission": "Find optimal compiler flags for specific workloads", "baseline": "Standard -O2 flag", "optimal": "Target-specific optimization flags", "expert": 0.60, "difficulty": TaskDifficulty.EXPERT}
        ]

        # Generate tasks from config lists ensuring exact counts
        for i, task in enumerate(optimize_tasks_config):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.97,
                llm_generic_baseline=0.42
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('execute', 'optimize'),
                name=task["name"],
                category=ARCCategory.EXECUTE,
                difficulty=task["difficulty"],
                mission=task["mission"],
                description=f"Optimization Task {i+1}: {task['mission']}. Optimize existing code for local machine performance.",
                estimated_time_budget="20 minutes",
                codebase={
                    "files": [f"optimize_{i+1}.c", "baseline_original.c"],
                    "language": "C99",
                    "compiler": "gcc/clang -O2 -mavx512f",
                    "optimization_level": "O2"
                },
                hardware={
                    "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
                    "simd": "AVX-512 with 2xFMA",
                    "cache": "LLC: 48MB"
                },
                available_tools=["GCC", "Clang", "optrecord", "perf", "objdump", "LIKWID"],
                unknown_characteristics=[
                    task["baseline"],
                    "Optimization technique effectiveness",
                    "Compiler interaction",
                    "Measurement methodology"
                ],
                evaluation_criteria={
                    "correctness": {"requirements": "Numerical accuracy > 99.5%", "weight": 0.25},
                    "efficiency": {"requirements": "Speedup vs baseline > 1.5x", "weight": 0.4},
                    "adaptation": {"requirements": "Iterative refinement quality", "weight": 0.35}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "adaptation_speed": 0.35,
                    "convergence_quality": 0.4,
                    "correctness_preservation": 0.25
                }
            )
            tasks.append(complete_task)

        return tasks

    def _create_generalize_tasks(self) -> List[HPCARCTaskComplete]:
        """Create 5 Generalize tasks for cross-architecture knowledge transfer"""
        tasks = []

        generalize_tasks = [
            {
                "name": "x86-to-ARM64 SIMD Generalization",
                "mission": "Transfer AVX-512 vector optimization to ARM SVE",
                "source": "x86_64 AVX-512 optimized kernels",
                "target": "ARM64 SVE implementations",
                "expert": 0.78, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "CPU-to-GPU Memory Coalescing Transfer",
                "mission": "Adapt memory coalescing strategies from CPU to GPU",
                "source": "CPU cache-aware memory access",
                "target": "GPU thread/block memory patterns",
                "expert": 0.72, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Single-to-Multi-Socket NUMA Generalization",
                "mission": "Generalize NUMA optimization from single to multi-socket",
                "source": "Single-socket NUMA optimization",
                "target": "Multi-socket inter-socket optimization",
                "expert": 0.85, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Intel-to-AMD ISA Generalization",
                "mission": "Transfer AMD-specific optimizations to Intel architectures",
                "source": "AMD Zen 4 optimized code",
                "target": "Intel Sapphire Rapids adaptation",
                "expert": 0.68, "difficulty": TaskDifficulty.EXPERT
            },
            {
                "name": "Bench-to-Production System Scaling",
                "mission": "Scale microbenchmark optimizations to production workload",
                "source": "Microbenchmark-optimized kernels",
                "target": "Multi-application production optimization",
                "expert": 0.58, "difficulty": TaskDifficulty.EXPERT
            }
        ]

        for i, task in enumerate(generalize_tasks):
            reference = ReferenceResults(
                expert_baseline=task["expert"],
                optimal_theoretical=0.92,
                llm_generic_baseline=0.35
            )

            complete_task = HPCARCTaskComplete(
                task_id=self._generate_task_id('generalize'),
                name=task["name"],
                category=ARCCategory.GENERALIZE,
                difficulty=TaskDifficulty.EXPERT,
                mission=task["mission"],
                description=f"Generalization Task {i+1}: {task['mission']}. Transfer optimization knowledge across architectures/domains.",
                estimated_time_budget="30 minutes",
                codebase={
                    "files": [f"generalize_{i+1}_source.c", "target_template.c"],
                    "languages": ["C99", "assembly as needed"],
                    "cross_compilation": "Required for multi-arch"
                },
                hardware={
                    "source_architecture": task["source"].split(" ")[0],
                    "target_architecture": task["target"].split(" ")[0],
                    "compilers": "GCC+Clang for source, target-specific for target"
                },
                available_tools=["Cross-compilers", "arch-specific profilers", "simulators"],
                unknown_characteristics=[
                    task["source"],
                    task["target"],
                    "Architecture-specific constraints",
                    "Cross-arch translation effectiveness"
                ],
                evaluation_criteria={
                    "correctness": {"requirements": "Functional equivalence > 99.9%", "weight": 0.35},
                    "efficiency": {"requirements": "Performance transfer rate > 50%", "weight": 0.3},
                    "generalization": {"requirements": "Knowledge abstraction quality", "weight": 0.35}
                },
                reference_results=reference,
                intelligence_metrics_weights={
                    "pattern_preservation": 0.35,
                    "adaptation_quality": 0.35,
                    "performance_transfer": 0.3
                }
            )
            tasks.append(complete_task)

        return tasks

    def generate_complete_database(self) -> List[HPCARCTaskComplete]:
        """Generate complete 100-task HPC-ARC database"""
        print("Generating complete HPC-ARC database...")

        # Generate all tasks by category
        explore_tasks = self._create_explore_tasks()
        hypothesize_tasks = self._create_hypothesize_tasks()
        execute_tasks = self._create_execute_tasks()
        generalize_tasks = self._create_generalize_tasks()

        # Combine all tasks
        all_tasks = explore_tasks + hypothesize_tasks + execute_tasks + generalize_tasks

        print(f"Generated {len(all_tasks)} tasks:")
        print(f"  - Explore: {len(explore_tasks)} tasks")
        print(f"  - Hypothesize: {len(hypothesize_tasks)} tasks")
        print(f"  - Execute: {len(execute_tasks)} tasks (25 parallelize + 30 optimize)")
        print(f"  - Generalize: {len(generalize_tasks)} tasks")

        # Verify task counts match specification
        assert len(explore_tasks) == 25, "Should have exactly 25 Explore tasks"
        assert len(hypothesize_tasks) == 20, "Should have exactly 20 Hypothesize tasks"
        assert len(execute_tasks) == 55, "Should have exactly 55 Execute tasks"
        assert len(generalize_tasks) == 5, "Should have exactly 5 Generalize tasks"
        assert len(all_tasks) == 105, "Total should be exactly 105 tasks per paper specification"

        return all_tasks

    def save_database(self, tasks: List[HPCARCTaskComplete], output_path: str):
        """Save task database to JSON file"""
        print(f"Saving task database to {output_path}...")

        # Convert tasks to dictionaries
        task_dicts = [task.to_dict() for task in tasks]

        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(task_dicts, f, indent=2, ensure_ascii=False)

        print(f"Successfully saved {len(tasks)} tasks to {output_path}")


def main():
    """Main function to generate HPC-ARC database"""
    import os
    generator = HPCARCDatabaseGenerator()

    # Generate complete database
    tasks = generator.generate_complete_database()

    # Save to JSON file (relative to the suite root: tasks/complete_tasks.json)
    suite_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(suite_root, "tasks", "complete_tasks.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generator.save_database(tasks, output_path)

    # Print summary statistics
    print("\n=== HPC-ARC Task Database Summary ===")

    difficulty_distribution = {}
    for task in tasks:
        diff = task.difficulty.value
        difficulty_distribution[diff] = difficulty_distribution.get(diff, 0) + 1

    print("\nDifficulty Distribution:")
    for diff in sorted(difficulty_distribution.keys()):
        print(f"  {diff}: {difficulty_distribution[diff]} tasks")

    avg_expert_baseline = sum(task.reference_results.expert_baseline for task in tasks) / len(tasks)
    avg_llm_generic = sum(task.reference_results.llm_generic_baseline for task in tasks) / len(tasks)

    print(f"\nPerformance Baselines:")
    print(f"  Average Expert Baseline: {avg_expert_baseline:.3f}")
    print(f"  Average LLM Generic Baseline: {avg_llm_generic:.3f}")
    print(f"  Expert Advantage: {(avg_expert_baseline/avg_llm_generic):.3f}x")

    print("\n=== Database Generation Complete ===")


if __name__ == "__main__":
    main()
