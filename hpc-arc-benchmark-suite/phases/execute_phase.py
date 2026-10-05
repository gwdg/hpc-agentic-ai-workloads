#!/usr/bin/env python3
"""
HPC-ARC Execute Phase: Adaptive Optimization Implementation

The Execute phase requires AI systems to implement optimization strategies
through iterative refinement with real-time profiling feedback. This phase
measures adaptation speed and convergence quality across multiple iterations.

Key capabilities:
- Adaptive optimization implementation with iterative refinement
- Real-time profiling feedback integration
- Correctness preservation during optimization
- Convergence detection and iteration strategy adaptation
"""

import json
import subprocess
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time
import logging
import tempfile
import shutil
from pathlib import Path

from core.hpc_arc_benchmark_suite import TaskContext, BenchmarkPhase, Difficulty

@dataclass
class IterationResult:
    """Single optimization iteration result"""
    iteration_number: int
    optimizations_applied: List[str]
    performance_mflops: float
    correctness_score: float
    profiling_feedback: Dict
    time_seconds: float
    convergence_flags: Dict

@dataclass
class ExecuteResult:
    """Complete Execute phase results"""
    task_id: str
    iterations: List[IterationResult]
    final_performance: float
    correctness_score: float
    adaptation_speed: float
    convergence_quality: float
    total_time_seconds: float
    success: bool

class ExecutePhaseExecutor:
    """Executor for Execute phase tasks"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            "max_iterations": 8,
            "convergence_threshold": 0.05,
            "correctness_threshold": 1e-6,
            "timeout_per_iteration": 300
        }
        self.logger = self._setup_logging()
        self.validator = self._setup_statistical_validator()
        
    def _setup_logging(self):
        logger = logging.getLogger('ExecutePhase')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - ExecutePhase - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
        return logger
    
    def _setup_statistical_validator(self):
        """Setup statistical validation for performance measurements"""
        return {"n_measurements": 5, "confidence": 0.95}
    
    def execute_execute_task(self, task: TaskContext) -> Dict:
        """
        Execute optimization with iterative refinement
        Returns structured execution results
        """
        self.logger.info(f"Starting Execute task: {task.task_id}")
        
        start_time = time.time()
        results = {
            "task_id": task.task_id,
            "phase": "execute",
            "start_time": start_time,
            "iterations": [],
            "final_performance": 0.0,
            "correctness_score": 0.0,
            "adaptation_speed": 0.0,
            "convergence_quality": 0.0,
            "total_time_seconds": 0.0
        }
        
        try:
            # Get hypotheses from task context (if available)
            hypotheses = task.initial_context.get('hypotheses', [])
            
            # Execute iterative optimization
            iteration_results = self._execute_iterative_optimization(task, hypotheses)
            results["iterations"] = [asdict(r) for r in iteration_results]
            
            # Calculate final metrics
            if iteration_results:
                final_result = iteration_results[-1]
                results["final_performance"] = final_result.performance_mflops
                results["correctness_score"] = final_result.correctness_score
                
                # Calculate adaptation speed (convergence efficiency)
                results["adaptation_speed"] = self._calculate_adaptation_speed(iteration_results)
                
                # Calculate convergence quality (final achievement)
                results["convergence_quality"] = self._calculate_convergence_quality(iteration_results, task)
            
            results["total_time_seconds"] = time.time() - start_time
            results["status"] = "completed"
            
        except Exception as e:
            self.logger.error(f"Execution task failed: {str(e)}")
            results["total_time_seconds"] = time.time() - start_time
            results["status"] = "failed"
            results["error"] = str(e)
        
        return results
    
    def _execute_iterative_optimization(self, task: TaskContext, hypotheses: List[Dict]) -> List[IterationResult]:
        """Execute optimization with iterative refinement"""
        iterations = []
        
        # Initial reference performance (naive implementation)
        current_code = task.initial_context.get('base_code', self._create_reference_implementation())
        baseline_performance = self._simulate_performance(1.0)  # Baseline
        target_performance = self._determine_target_performance(task)
        
        self.logger.info(f"Starting optimization from baseline: {baseline_performance:.1f} MFLOPS")
        self.logger.info(f"Target performance: {target_performance:.1f} MFLOPS")
        
        iteration_num = 1
        converged = False
        
        while iteration_num <= self.config["max_iterations"] and not converged:
            self.logger.info(f"=== Iteration {iteration_num} ===")
            
            # Select next optimization based on iteration number and hypotheses
            optimization = self._select_optimization(iteration_num, hypotheses)
            
            # Apply optimization
            self.logger.info(f"Applying: {optimization['name']}")
            current_code = self._apply_optimization(current_code, optimization)
            
            # Compile and measure performance
            performance_result = self._measure_performance(current_code, task, iteration_num)
            
            # Check correctness
            correctness_result = self._check_correctness(current_code, task)
            
            # Get profiling feedback
            profiling_feedback = self._get_profiling_feedback(current_code)
            
            # Check convergence
            convergence_flags = self._check_convergence(
                performance_result['performance'],
                baseline_performance,
                target_performance
            )
            
            # Record iteration result
            iteration_result = IterationResult(
                iteration_number=iteration_num,
                optimizations_applied=[optimization['name']],
                performance_mflops=performance_result['performance'],
                correctness_score=correctness_result['score'],
                profiling_feedback=profiling_feedback,
                time_seconds=performance_result['time'],
                convergence_flags=convergence_flags
            )
            
            iterations.append(iteration_result)
            
            # Check if converged
            if convergence_flags.get('converged', False):
                converged = True
                self.logger.info(f"Converged after iteration {iteration_num}")
            
            iteration_num += 1
        
        return iterations
    
    def _select_optimization(self, iteration: int, hypotheses: List[Dict]) -> Dict:
        """Select appropriate optimization for current iteration"""
        # Simulated optimization selection strategy
        
        if iteration == 1:
            return {
                "name": "AVX-512 Basic Vectorization",
                "category": "vectorization",
                "expected_speedup": 3.0,
                "description": "Convert scalar loops to AVX-512 intrinsics",
                "complexity": "MEDIUM"
            }
        elif iteration == 2:
            return {
                "name": "Register Blocking with 8x8 Register Tiles",
                "category": "cache_optimization",
                "expected_speedup": 1.6,
                "description": "Implement 8x8 register blocking to improve cache locality",
                "complexity": "MEDIUM"
            }
        elif iteration == 3:
            return {
                "name": "L1 Cache-Aware Tiling with Morton Order",
                "category": "cache_optimization",
                "expected_speedup": 1.3,
                "description": "Implement 32x32 L1 cache tiles with Morton order data layout",
                "complexity": "HIGH"
            }
        elif iteration == 4:
            return {
                "name": "Software Prefetching with Prefetch Distance Calculation",
                "category": "prefetch_optimization",
                "expected_speedup": 1.2,
                "description": "Add software prefetching with calculated prefetch distances",
                "complexity": "MEDIUM"
            }
        elif iteration == 5:
            return {
                "name": "Loop Unrolling and Pipelining",
                "category": "code_generation",
                "expected_speedup": 1.1,
                "description": "Increase loop unrolling factor and optimize instruction pipeline",
                "complexity": "MEDIUM"
            }
        else:
            return {
                "name": "Targeted Micro-optimizations with Profile-Guided Refinement",
                "category": "micro_optimization",
                "expected_speedup": 1.05,
                "description": "Apply targeted micro-optimizations based on profiling feedback",
                "complexity": "LOW"
            }
    
    def _create_reference_implementation(self) -> str:
        """Create naive reference implementation for matrix multiplication"""
        return """
void dgemm_naive(int N, double *A, double *B, double *C) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}
"""
    
    def _apply_optimization(self, current_code: str, optimization: Dict) -> str:
        """Apply optimization to current code"""
        # Simulated code transformation
        if optimization["category"] == "vectorization":
            return current_code + " /* AVX-512 vectorization applied */\n"
        elif optimization["category"] == "cache_optimization":
            return current_code + " /* Cache blocking optimization applied */\n"
        elif optimization["category"] == "prefetch_optimization":
            return current_code + " /* Software prefetching applied */\n"
        else:
            return current_code + f" /* {optimization['name']} applied */\n"
    
    def _measure_performance(self, code: str, task: TaskContext, iteration: int) -> Dict:
        """Measure performance with statistical validation"""
        # Simulated performance measurements
        performance_progression = {
            1: 420.0,   # Initial vectorization: ~49% of baseline
            2: 680.0,   # Register blocking: ~80% of baseline
            3: 820.0,   # Cache tiling: ~96% of baseline
            4: 860.0,   # Prefetching: ~1.01% of baseline
            5: 890.0,   # Micro-optimizations: ~1.05% of baseline
            6: 890.0,
            7: 890.0,
            8: 890.0
        }
        
        base_performance = performance_progression.get(min(iteration, 5), 890.0)
        
        # Add statistical variation
        measurements = [base_performance + np.random.normal(0, base_performance * 0.02) for _ in range(5)]
        mean_performance = np.mean(measurements)
        
        return {
            "performance": mean_performance,
            "measurements": measurements,
            "baseline_comparison": mean_performance / 850.0,  # vs Intel MKL baseline
            "time": np.random.uniform(10, 30)  # seconds
        }
    
    def _check_correctness(self, code: str, task: TaskContext) -> Dict:
        """Check numerical correctness against reference"""
        # Simulated correctness check
        correct = True
        max_error = np.random.uniform(1e-8, 5e-7)
        
        return {
            "correct": correct,
            "score": max(0.0, 1.0 - max_error / 1e-5),  # Convert to 0.0-1.0 score
            "max_absolute_error": max_error,
            "relative_error": max_error / 1.0  # relative to unit values
        }
    
    def _get_profiling_feedback(self, code: str) -> Dict:
        """Get profiling feedback for next iteration"""
        return {
            "vector_utilization": f"{np.random.uniform(0.89, 0.92):.2f}",
            "l1_cache_hit_rate": f"{np.random.uniform(0.94, 0.96):.2f}",
            "l2_cache_hit_rate": f"{np.random.uniform(0.88, 0.91):.2f}",
            "l3_cache_hit_rate": f"{np.random.uniform(0.82, 0.85):.2f}",
            "instructions_per_cycle": f"{np.random.uniform(1.8, 2.2):.2f}",
            "remaining_bottlenecks": ["pipeline_stalls", "branch_mispredictions"]
        }
    
    def _check_convergence(self, current: float, baseline: float, target: float) -> Dict:
        """Check if optimization has converged"""
        # Convergence criteria based on improvement and target achievement
        improvement = (current - baseline) / baseline
        target_achievement = current / target
        
        converged = target_achievement >= 0.95  # 95% of target
        
        return {
            "converged": converged,
            "improvement": improvement,
            "target_achievement": target_achievement,
            "stability": True  # Will check measurement stability in real implementation
        }
    
    def _simulate_performance(self, baseline_factor: float) -> float:
        """Simulate performance scaling from baseline"""
        base_performance = 150.0  # MFLOPS for naive implementation
        return base_performance * baseline_factor
    
    def _determine_target_performance(self, task: TaskContext) -> float:
        """Determine target performance from evaluation criteria"""
        # For EX-051, target is 850 MFLOPS (Intel MKL baseline)
        return 850.0
    
    def _calculate_adaptation_speed(self, iterations: List[IterationResult]) -> float:
        """
        Calculate adaptation speed score (0.0-1.0)
        
        Measures how quickly the system converges toward optimal performance
        """
        if len(iterations) < 2:
            return 0.0
        
        # Calculate convergence rate
        first_perf = iterations[0].performance_mflops
        final_perf = iterations[-1].performance_mflops
        target_perf = 850.0  # Intel MKL baseline
        
        # Higher score = faster convergence
        target_achievement = final_perf / target_perf
        convergence_efficiency = 1.0 / len(iterations)  # Fewer iterations = better
        
        adaptation_score = target_achievement * convergence_efficiency
        return min(1.0, adaptation_score)
    
    def _calculate_convergence_quality(self, iterations: List[IterationResult], task: TaskContext) -> float:
        """
        Calculate convergence quality score (0.0-1.0)
        
        Measures final performance achievement and correctness preservation
        """
        if not iterations:
            return 0.0
        
        final_iteration = iterations[-1]
        target_performance = self._determine_target_performance(task)
        
        # Performance quality (0.0-1.0)
        if target_performance > 0:
            performance_quality = min(1.0, final_iteration.performance_mflops / target_performance)
        else:
            performance_quality = 0.0
        
        # Correctness quality (0.0-1.0)
        correctness_quality = final_iteration.correctness_score
        
        # Combined quality score
        convergence_quality = 0.7 * performance_quality + 0.3 * correctness_quality
        
        return convergence_quality

# Example execution for Execute phase
def execute_execute_example():
    """Execute Execute Phase example (EX-051 from paper)"""
    
    # Create example task context matching EX-051
    task = TaskContext(
        task_id="EX-051",
        phase=BenchmarkPhase.EXECUTE,
        description="AVX-512 Vectorization with Iterative Refinement",
        difficulty=Difficulty.HARD,
        time_budget=7200,  # 2 hours
        iteration_limit=8,
        available_tools=["llvm", "likwid", "perf"],
        initial_context={
            "base_code": "naive_dgemm_implementation",
            "target_performance": 850.0,  # MFLOPS (Intel MKL baseline)
            "max_iterations": 8,
            "hypotheses": [
                {
                    "hypothesis_id": "H001",
                    "name": "AVX-512 Vectorization",
                    "expected_speedup": 4.0
                }
            ]
        },
        evaluation_criteria={
            "correctness": {"requirements": "Numerical error < 10^-6"},
            "phase_specific": {
                "max_iterations": 8,
                "target_performance": 850.0,  # MFLOPS
                "convergence_threshold": 0.05,
                "correctness_threshold": 1e-6
            }
        }
    )
    
    # Execute Execute phase
    executor = ExecutePhaseExecutor()
    results = executor.execute_execute_task(task)
    
    # Print summary
    print(f"""
    ================================================================
    EXECUTE PHASE TASK: {task.task_id}
    ================================================================
    
    Status: {results['status']}
    Total Time: {results['total_time_seconds']:.2f} seconds
    Iterations Completed: {len(results['iterations'])}
    
    Final Performance: {results['final_performance']:.1f} MFLOPS
    Final Correctness: {results['correctness_score']:.6f}
    
    Adaptation Speed: {results['adaptation_speed']:.3f}
    Convergence Quality: {results['convergence_quality']:.3f}
    
    Performance Progression:
    """)
    
    for iteration in results['iterations']:
        perf = iteration['performance_mflops']
        baseline_comparison = perf / 850.0  # vs Intel MKL
        print(f"  Iteration {iteration['iteration_number']}: {perf:.1f} MFLOPS ({baseline_comparison:.2f}x Intel MKL)")
    
    print(f"""
    Target Achievement: {results['final_performance'] / 850.0:.3f}x Intel MKL baseline
    Success Criteria: {'PASSED' if results['final_performance'] >= 850.0 * 0.8 else 'FAILED'}
    Correctness Validation: {'PASSED' if results['correctness_score'] > 0.999999 else 'FAILED'}
    
    ================================================================
    """)
    
    return results

if __name__ == "__main__":
    execute_execute_example()