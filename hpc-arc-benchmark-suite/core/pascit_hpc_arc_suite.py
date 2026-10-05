"""
HPC-ARC: HPC Automated Reasoning Benchmark Suite

This module implements the HPC-ARC Interactive Reasoning Benchmark Suite as described in the
pascit_orchestrator paper. It extends PASCIT with ARC-AGI-3 inspired interactive reasoning
methodology for measuring AI systems' HPC performance engineering intelligence.

Key Features:
- Interactive exploration-based tasks (Explore, Hypothesize, Execute, Generalize phases)
- Tri-correlated evaluation framework (correctness, efficiency, intelligence)
- Skill-acquisition measurement and learning curve analysis
- Cross-architecture knowledge transfer evaluation
- Iterative optimization with feedback loops
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from abc import ABC, abstractmethod
import time
import random
import math


# ==============================================================================
# CORE ENUMS AND DATA STRUCTURES
# ==============================================================================

class ARCCategory(Enum):
    """ ARC-inspired task categories for HPC performance engineering """
    EXPLORE = "explore"          # Environment discovery through interactive profiling
    HYPOTHESIZE = "hypothesize"  # Optimization opportunity identification
    EXECUTE = "execute"          # Adaptive optimization implementation
    GENERALIZE = "generalize"    # Cross-architecture knowledge transfer


class TaskDifficulty(Enum):
    """ Difficulty levels for HPC-ARC tasks """
    ELEMENTARY = "elementary"    # Basic exploration/hypothesis tasks
    INTERMEDIATE = "intermediate" # Standard optimization challenges
    ADVANCED = "advanced"        # Complex multi-stage optimization
    EXPERT = "expert"           # Expert-level cross-architecture tasks


class DifficultyLevel(Enum):
    """ Numerical difficulty levels for scoring """
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


@dataclass
class EvaluationResultV2:
    """
    Extended evaluation result with HPC-ARC Intelligence Metrics
    
    Incorporates dual metrics (correctness + efficiency) plus novel intelligence metrics
    for comprehensive HPC performance engineering assessment.
    """
    # Task identification
    task_id: str
    approach: str
    
    # Bestehende Dual Metrics (erhalten)
    correctness_score: float        # 0.0-1.0 (Working Solution)
    efficiency_percentage: float     # 0.0-100.0 (vs Optimum)
    overall_score: float             # 0.0-100.0 (Weighted combo)
    
    # Neue HPC-ARC Metrics (addiert)
    exploration_efficiency: float    # 0.0-1.0 (Iterative Discovery Speed)
    hypothesis_quality: float        # 0.0-1.0 (Prediction Accuracy)
    adaptation_speed: float          # 0.0-1.0 (Convergence Rate)
    generalization_success: float    # 0.0-1.0 (Cross-Architecture Transfer)
    
    # Aggregierte HPC-ARC Intelligence Score
    intelligence_score: float        # 0.0-1.0 (ARC-inspired measurement)
    
    # Extensive Performance Metrics
    execution_time_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    
    # Iterative Process Data
    iterations_used: int = 1        # Number of optimization iterations
    time_to_convergence: float = 0.0 # Zeit in Sekunden bis optimal
    learning_curve_development: List[float] = field(default_factory=list)  # Skill-acquisition über Iterationen
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    hardware_platform: str = "generic_x86_64"
    
    @classmethod
    def from_base_result(cls, result: 'EvaluationResult') -> 'EvaluationResultV2':
        """Convert basic EvaluationResult to extended version with default intelligence metrics"""
        return cls(
            task_id=result.task_id,
            approach=result.approach,
            correctness_score=result.correctness_score,
            efficiency_percentage=result.efficiency_percentage,
            overall_score=result.overall_score,
            exploration_efficiency=0.5,  # Default middle value
            hypothesis_quality=0.5,
            adaptation_speed=0.5,
            generalization_success=0.5,
            intelligence_score=0.5,
            execution_time_seconds=getattr(result, 'execution_time_seconds', 0.0),
            iterations_used=1,
            time_to_convergence=getattr(result, 'execution_time_seconds', 0.0),
            learning_curve_development=[0.5]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "task_id": self.task_id,
            "approach": self.approach,
            "correctness_score": self.correctness_score,
            "efficiency_percentage": self.efficiency_percentage,
            "overall_score": self.overall_score,
            "exploration_efficiency": self.exploration_efficiency,
            "hypothesis_quality": self.hypothesis_quality,
            "adaptation_speed": self.adaptation_speed,
            "generalization_success": self.generalization_success,
            "intelligence_score": self.intelligence_score,
            "execution_time_seconds": self.execution_time_seconds,
            "memory_usage_mb": self.memory_usage_mb,
            "iterations_used": self.iterations_used,
            "time_to_convergence": self.time_to_convergence,
            "learning_curve_development": self.learning_curve_development,
            "timestamp": self.timestamp,
            "hardware_platform": self.hardware_platform
        }


@dataclass
class HPCARCTaskSpec:
    """
    HPC-ARC Task Specification
    
    Defines comprehensive task specifications with ARC-inspired methodology for interactive
    reasoning benchmarks in HPC performance engineering.
    """
    # Basic identification
    task_id: str
    name: str
    category: ARCCategory
    difficulty: TaskDifficulty
    version: str = "3.0"
    
    # Task description and objectives
    mission: str = ""
    description: str = ""
    estimated_time_budget: str = "20 minutes"
    
    # Code context
    codebase: Dict[str, Any] = field(default_factory=dict)
    hardware: Dict[str, Any] = field(default_factory=dict)
    available_tools: List[str] = field(default_factory=list)
    
    # Unknown characteristics to discover
    unknown_characteristics: List[str] = field(default_factory=list)
    exploration_objectives: Dict[str, Any] = field(default_factory=dict)
    
    # Interactive constraints
    interactive_budget: int = 1260  # seconds (21 minutes default)
    max_iterations: int = 3
    time_per_iteration: int = 420   # seconds (7 minutes default)
    memory_limit: int = 32000       # MB
    allowed_operations: List[str] = field(default_factory=list)
    
    # Evaluation criteria
    evaluation_criteria: Dict[str, Any] = field(default_factory=dict)
    success_thresholds: Dict[str, float] = field(default_factory=dict)
    
    # Initial feedback and context
    initial_feedback: Dict[str, Any] = field(default_factory=dict)
    
    # ARC-specific attributes
    learning_objectives: List[str] = field(default_factory=list)
    exploration_tools: List[str] = field(default_factory=list)
    intelligence_metrics: Dict[str, float] = field(default_factory=dict)
    generalization_targets: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HPCARCTaskSpec':
        """Create task specification from dictionary"""
        category_map = {
            "explore": ARCCategory.EXPLORE,
            "hypothesize": ARCCategory.HYPOTHESIZE,
            "execute": ARCCategory.EXECUTE,
            "generalize": ARCCategory.GENERALIZE
        }
        
        difficulty_map = {
            "elementary": TaskDifficulty.ELEMENTARY,
            "intermediate": TaskDifficulty.INTERMEDIATE,
            "advanced": TaskDifficulty.ADVANCED,
            "expert": TaskDifficulty.EXPERT
        }
        
        return cls(
            task_id=data.get("task_id", "unknown"),
            name=data.get("name", "Unknown Task"),
            category=category_map.get(data.get("category", "explore"), ARCCategory.EXPLORE),
            difficulty=difficulty_map.get(data.get("difficulty", "intermediate"), TaskDifficulty.INTERMEDIATE),
            version=data.get("version", "3.0"),
            mission=data.get("mission", ""),
            description=data.get("description", ""),
            estimated_time_budget=data.get("estimated_time_budget", "20 minutes"),
            codebase=data.get("initial_context", {}).get("codebase", {}),
            hardware=data.get("initial_context", {}).get("hardware", {}),
            available_tools=data.get("initial_context", {}).get("available_tools", {}).get("profiling", []),
            unknown_characteristics=data.get("unknown_characteristics", []),
            exploration_objectives=data.get("exploration_objectives", {}),
            interactive_budget=data.get("interactive_constraints", {}).get("time_budget_total", 1260),
            max_iterations=data.get("interactive_constraints", {}).get("iteration_limit", 3),
            time_per_iteration=data.get("interactive_constraints", {}).get("time_per_iteration", 420),
            memory_limit=data.get("interactive_constraints", {}).get("memory_limit", 32000),
            allowed_operations=data.get("interactive_constraints", {}).get("allowed_operations", []),
            evaluation_criteria=data.get("evaluation_criteria", {}),
            success_thresholds=data.get("success_thresholds", {}),
            initial_feedback=data.get("initial_feedback", {}),
            learning_objectives=data.get("learning_objectives", []),
            exploration_tools=data.get("exploration_tools", []),
            intelligence_metrics=data.get("intelligence_metrics", {}),
            generalization_targets=data.get("generalization_targets", {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task specification to dictionary"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "category": self.category.value,
            "difficulty": self.difficulty.value,
            "version": self.version,
            "mission": self.mission,
            "description": self.description,
            "estimated_time_budget": self.estimated_time_budget,
            "initial_context": {
                "codebase": self.codebase,
                "hardware": self.hardware,
                "available_tools": {"profiling": self.available_tools}
            },
            "unknown_characteristics": self.unknown_characteristics,
            "exploration_objectives": self.exploration_objectives,
            "interactive_constraints": {
                "time_budget_total": self.interactive_budget,
                "iteration_limit": self.max_iterations,
                "time_per_iteration": self.time_per_iteration,
                "memory_limit": self.memory_limit,
                "allowed_operations": self.allowed_operations
            },
            "evaluation_criteria": self.evaluation_criteria,
            "success_thresholds": self.success_thresholds,
            "initial_feedback": self.initial_feedback,
            "learning_objectives": self.learning_objectives,
            "exploration_tools": self.exploration_tools,
            "intelligence_metrics": self.intelligence_metrics,
            "generalization_targets": self.generalization_targets
        }


class CalculationResult:
    """Mithilfeklasse für Berechnungsergebnisse für Kompatibilität"""
    def __init__(self, checksum: float, execution_time: float, gflops: float = 0.0):
        self.checksum = checksum
        self.execution_time = execution_time
        self.gflops = gflops

    def to_dict(self) -> Dict[str, float]:
        return {"checksum": self.checksum, "execution_time": self.execution_time, "gflops": self.gflops}

    @property
    def execution_time_seconds(self) -> float:
        return self.execution_time


class EvaluationResult:
    """Mithilfeklasse für Evaluierungsergebnisse für Kompatibilität"""
    def __init__(self, task_id: str, approach: str, correctness_score: float = 0.0, 
                 efficiency_percentage: float = 0.0, overall_score: float = 0.0):
        self.task_id = task_id
        self.approach = approach
        self.correctness_score = correctness_score
        self.efficiency_percentage = efficiency_percentage
        self.overall_score = overall_score


@dataclass
class TaskFeedback:
    """
    Interactive feedback provided to AI agents during task execution
    
    Implements the ARC-inspired feedback system for iterative learning
    and skill development.
    """
    iteration: int
    arc_phase: str
    current_intelligence_score: float
    
    # Performance diagnostics
    performance_diagnostics: Dict[str, Any] = field(default_factory=dict)
    
    # Learning opportunities
    learning_opportunities: List[str] = field(default_factory=list)
    
    # Actionable recommendations
    recommendations: List[str] = field(default_factory=list)
    
    # Next steps guidance
    next_steps: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "iteration": self.iteration,
            "arc_phase": self.arc_phase,
            "current_intelligence_score": self.current_intelligence_score,
            "performance_diagnostics": self.performance_diagnostics,
            "learning_opportunities": self.learning_opportunities,
            "recommendations": self.recommendations,
            "next_steps": self.next_steps
        }


# ==============================================================================
# INTELLIGENCE METRICS CALCULATION
# ==============================================================================

class HPCARCCalculator:
    """
    Calculate HPC-ARC Intelligence Scores based on ARC-AGI-3 methodology
    
    Implements tri-correlated evaluation framework with intelligence skill-acquisition metrics
    """
    
    @staticmethod
    def calculate_exploration_efficiency(iterations_used: int, max_iterations: int) -> float:
        """
        Calculate exploration efficiency metric
        
        Measures how quickly agents discover performance characteristics:
        Exploration_Score = 1 - (Iterations_Used / Allowed_Iterations)
        
        Args:
            iterations_used: Number of iterations actually used
            max_iterations: Maximum allowed iterations
            
        Returns:
            Exploration efficiency score (0.0-1.0)
        """
        if max_iterations <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (iterations_used / max_iterations)))
    
    @staticmethod
    def calculate_hypothesis_quality(prediction_accuracy: float, feasibility_score: float) -> float:
        """
        Calculate hypothesis quality metric
        
        Measures accuracy of predicted performance improvements:
        Hypothesis_Score = (Prediction_Accuracy + Feasibility_Score) / 2
        
        Args:
            prediction_accuracy: How close predictions were to actual results (0.0-1.0)
            feasibility_score: Implementation feasibility assessment (0.0-1.0)
            
        Returns:
            Hypothesis quality score (0.0-1.0)
        """
        return (max(0.0, min(1.0, prediction_accuracy)) + 
                max(0.0, min(1.0, feasibility_score))) / 2.0
    
    @staticmethod
    def calculate_adaptation_speed(time_to_optimal: float, allowed_time: float) -> float:
        """
        Calculate adaptation speed metric
        
        Measures how quickly agents reach optimal solutions:
        Adaptation_Score = 1 - (Time_to_Optimal / Allowed_Time)
        
        Args:
            time_to_optimal: Time taken to reach optimal solution in seconds
            allowed_time: Maximum allowed time budget in seconds
            
        Returns:
            Adaptation speed score (0.0-1.0)
        """
        if allowed_time <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (time_to_optimal / allowed_time)))
    
    @staticmethod
    def calculate_generalization_success(pattern_preservation: float, performance_maintenance: float) -> float:
        """
        Calculate generalization success metric
        
        Measures transferability of learned patterns:
        Generalization_Score = (Pattern_Preservation + Performance_Maintenance) / 2
        
        Args:
            pattern_preservation: Core optimization principles maintained (0.0-1.0)
            performance_maintenance: Performance maintained in new context (0.0-1.0)
            
        Returns:
            Generalization success score (0.0-1.0)
        """
        return (max(0.0, min(1.0, pattern_preservation)) + 
                max(0.0, min(1.0, performance_maintenance))) / 2.0
    
    @staticmethod
    def calculate_intelligence_score(
        exploration_efficiency: float,
        hypothesis_quality: float, 
        adaptation_speed: float,
        generalization_success: float
    ) -> float:
        """
        Calculate cumulative HPC-ARC Intelligence Score
        
        Implements weighted combination based on ARC-AGI-3 methodology:
        Intelligence_Score = 0.25×(Exploration_Score) + 0.25×(Hypothesis_Score) + 
                           0.30×(Adaptation_Score) + 0.20×(Generalization_Score)
        
        Args:
            exploration_efficiency: Exploration efficiency metric
            hypothesis_quality: Hypothesis quality metric
            adaptation_speed: Adaptation speed metric
            generalization_success: Generalization success metric
            
        Returns:
            Overall intelligence score (0.0-1.0)
        """
        intelligence_score = (
            0.25 * max(0.0, min(1.0, exploration_efficiency)) +
            0.25 * max(0.0, min(1.0, hypothesis_quality)) +
            0.30 * max(0.0, min(1.0, adaptation_speed)) +
            0.20 * max(0.0, min(1.0, generalization_success))
        )
        return intelligence_score
    
    @staticmethod
    def calculate_overall_score(
        correctness_score: float,
        efficiency_percentage: float,
        intelligence_score: float,
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Calculate overall tri-correlated score
        
        Combines dual metrics (correctness, efficiency) with intelligence score
        for comprehensive evaluation.
        
        Args:
            correctness_score: Correctness metric (0.0-1.0)
            efficiency_percentage: Efficiency percentage (0.0-100.0)
            intelligence_score: Intelligence score (0.0-1.0)
            weights: Optional custom weights
            
        Returns:
            Overall score (0.0-100.0)
        """
        if weights is None:
            weights = {
                "correctness": 0.4,
                "efficiency": 0.35,
                "intelligence": 0.25
            }
        
        normalized_efficiency = max(0.0, min(1.0, efficiency_percentage / 100.0))
        
        overall_score = (
            weights["correctness"] * max(0.0, min(1.0, correctness_score)) +
            weights["efficiency"] * normalized_efficiency +
            weights["intelligence"] * max(0.0, min(1.0, intelligence_score))
        ) * 100.0
        
        return overall_score
    
    @staticmethod
    def interpret_intelligence_score(score: float) -> Tuple[str, str]:
        """
        Provide human-interpretable classification for intelligence scores
        
        Args:
            score: Intelligence score (0.0-1.0)
            
        Returns:
            Tuple of (tier_name, description)
        """
        if score >= 0.8:
            return ("S-TIER (Expert)", "Expert HPC engineer level performance")
        elif score >= 0.6:
            return ("A-TIER (Advanced)", "Advanced HPC practitioner level")
        elif score >= 0.4:
            return ("B-TIER (Developing)", "Developing HPC knowledge")
        elif score >= 0.2:
            return ("C-TIER (Basic)", "Basic pattern matching capabilities")
        else:
            return ("D-TIER (Novice)", "Random/brute-force approach")


class HPCARCBenchmarkSuite:
    """
    Comprehensive benchmark suite with HPC-ARC phase assignment and management
    """
    
    def __init__(self, benchmark_dir: Optional[Path] = None):
        self.benchmark_dir = Path(benchmark_dir) if benchmark_dir else Path("hpc_arc_benchmarks")
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)
        self.tasks: Dict[str, HPCARCTaskSpec] = {}
        self.arc_phase_mapping = {
            "analyze": "Explore",
            "detect": "Hypothesize", 
            "parallelize": "Execute",
            "optimize": "Execute",
            "generalize": "Generalize"
        }
        self._initialize_tasks()
    
    def _initialize_tasks(self):
        """Initialize all benchmark tasks from specification files"""
        try:
            # First try to load from individual task files
            task_spec_files = list(self.benchmark_dir.glob("**/task_*.json"))
            
            for spec_file in task_spec_files:
                with open(spec_file, 'r') as f:
                    task_data = json.load(f)
                    task_spec = HPCARCTaskSpec.from_dict(task_data)
                    self.tasks[task_spec.task_id] = task_spec
            
            # If no individual files found, try to load from all_tasks.json
            if not self.tasks:
                all_tasks_file = self.benchmark_dir / "all_tasks.json"
                if all_tasks_file.exists():
                    with open(all_tasks_file, 'r') as f:
                        tasks_data = json.load(f)
                        for task_data in tasks_data:
                            task_spec = HPCARCTaskSpec.from_dict(task_data)
                            self.tasks[task_spec.task_id] = task_spec
            
            # If still no tasks, create defaults
            if not self.tasks:
                print(f"Note: Using default task specifications (no specification files found in {self.benchmark_dir})")
                self._create_default_tasks()
                    
        except Exception as e:
            print(f"Note: Using default task specifications (loading failed: {e})")
            # Create default tasks if no specification files found
            self._create_default_tasks()
    
    def _create_default_tasks(self):
        """Create default HPC-ARC task specifications"""
        # Explore tasks (25)
        explore_tasks = [
            (f"E{i:03d}", "Cache Behavior Discovery", ARCCategory.EXPLORE, TaskDifficulty.INTERMEDIATE)
            for i in range(1, 26)
        ]
        
        # Hypothesize tasks (20)
        hypothesize_tasks = [
            (f"H{i:03d}", "Optimization Hypothesis Formulation", ARCCategory.HYPOTHESIZE, TaskDifficulty.INTERMEDIATE)
            for i in range(1, 21)
        ]
        
        # Execute tasks (55)
        execute_tasks = [
            (f"EX{i:03d}", "Adaptive Optimization Implementation", ARCCategory.EXECUTE, TaskDifficulty.ADVANCED)
            for i in range(1, 56)
        ]
        
        # Generalize tasks (20)
        generalize_tasks = [
            (f"G{i:03d}", "Cross-Architecture Knowledge Transfer", ARCCategory.GENERALIZE, TaskDifficulty.EXPERT)
            for i in range(1, 21)
        ]
        
        all_tasks = explore_tasks + hypothesize_tasks + execute_tasks + generalize_tasks
        
        for task_id, name, category, difficulty in all_tasks:
            self.tasks[task_id] = HPCARCTaskSpec(
                task_id=task_id,
                name=name,
                category=category,
                difficulty=difficulty,
                mission=f"Perform {category.value} task: {name.lower()}",
                description=f"Interactive reasoning task for HPC performance engineering in {category.value} phase",
                estimated_time_budget="20 minutes",
                interactive_budget=1260,
                max_iterations=3,
                time_per_iteration=420,
                evaluation_criteria={
                    "correctness": {"requirements": f"Correct solution for {category.value}", "weight": 0.4},
                    "efficiency": {"requirements": "Efficient within time budget", "weight": 0.35},
                    "generalization": {"requirements": "Applicable patterns", "weight": 0.25}
                },
                success_thresholds={
                    "overall_score": 0.75,
                    "minimum_correctness": 0.8,
                    "maximum_iterations_used": 3
                }
            )
    
    def get_task(self, task_id: str) -> Optional[HPCARCTaskSpec]:
        """Get specific task by ID"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_arc_phase(self, arc_phase: str) -> List[HPCARCTaskSpec]:
        """Get tasks based on ARC phase"""
        phase_mapping = {
            "Explore": ARCCategory.EXPLORE,
            "Hypothesize": ARCCategory.HYPOTHESIZE,
            "Execute": ARCCategory.EXECUTE,
            "Generalize": ARCCategory.GENERALIZE
        }
        
        target_category = phase_mapping.get(arc_phase)
        if target_category is None:
            return []
            
        return [task for task in self.tasks.values() 
                if task.category == target_category]
    
    def get_tasks_by_category(self, category: ARCCategory) -> List[HPCARCTaskSpec]:
        """Get tasks by HPC-ARC category"""
        return [task for task in self.tasks.values() if task.category == category]
    
    def get_all_tasks(self) -> List[HPCARCTaskSpec]:
        """Get all tasks"""
        return list(self.tasks.values())
    
    def save_tasks(self, output_path: Optional[Path] = None):
        """Save all task specifications to JSON"""
        if output_path is None:
            output_path = self.benchmark_dir / "all_tasks.json"
        
        tasks_data = [task.to_dict() for task in self.tasks.values()]
        
        with open(output_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)
        
        print(f"Saved {len(self.tasks)} task specifications to {output_path}")
    
    def load_tasks(self, input_path: Path):
        """Load task specifications from JSON"""
        if not input_path.exists():
            raise FileNotFoundError(f"Task specification file not found: {input_path}")
        
        with open(input_path, 'r') as f:
            tasks_data = json.load(f)
        
        self.tasks = {}
        for task_data in tasks_data:
            task_spec = HPCARCTaskSpec.from_dict(task_data)
            self.tasks[task_spec.task_id] = task_spec
        
        print(f"Loaded {len(self.tasks)} task specifications from {input_path}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get benchmark suite statistics"""
        stats = {
            "total_tasks": len(self.tasks),
            "by_category": {
                "explore": len(self.get_tasks_by_arc_phase("Explore")),
                "hypothesize": len(self.get_tasks_by_arc_phase("Hypothesize")),
                "execute": len(self.get_tasks_by_arc_phase("Execute")),
                "generalize": len(self.get_tasks_by_arc_phase("Generalize"))
            },
            "by_difficulty": {},
            "estimated_total_time": "0 hours"
        }
        
        # Count by difficulty
        for task in self.tasks.values():
            difficulty = task.difficulty.value
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
        
        # Estimate total time (20 minutes per task)
        total_tasks = len(self.tasks)
        total_minutes = total_tasks * 20
        hours = total_minutes // 60
        minutes = total_minutes % 60
        stats["estimated_total_time"] = f"{hours} hours {minutes} minutes"
        
        return stats


class InteractiveTaskEvaluator:
    """
    Interactive task evaluator with HPC-ARC iterations management and feedback loops
    
    Implements ARC-inspired interactive evaluation with feedback for iterative learning
    and skill development.
    """
    
    def __init__(self, benchmark_suite: HPCARCBenchmarkSuite):
        self.benchmark_suite = benchmark_suite
        self.calculator = HPCARCCalculator()
        self.arc_phase_mapping = {
            "explore": "Explore",
            "hypothesize": "Hypothesize",
            "execute": "Execute",
            "generalize": "Generalize"
        }
    
    def evaluate_task_interactive(
        self,
        task_spec: HPCARCTaskSpec,
        approach: str,
        max_iterations: Optional[int] = None,
        iteration_budget: Optional[int] = None
    ) -> EvaluationResultV2:
        """
        Interactive evaluation with iterations management like ARC-AGI-3
        
        Args:
            task_spec: Task specification
            approach: Approach/method being evaluated
            max_iterations: Maximum iterations (overrides task spec)
            iteration_budget: Time budget per iteration in seconds
            
        Returns:
            Extended evaluation result with intelligence metrics
        """
        # Use task defaults if not specified
        if max_iterations is None:
            max_iterations = task_spec.max_iterations
        if iteration_budget is None:
            iteration_budget = task_spec.time_per_iteration
        
        iteration_results = []
        learning_curve = []
        total_execution_time = 0.0
        
        arc_phase = self.arc_phase_mapping.get(task_spec.category.value, "Execute")
        
        for iteration in range(1, max_iterations + 1):
            iteration_start = time.time()
            
            # Simulate base evaluation for this iteration
            # In practice, this would run the actual optimization approach
            base_result = self._simulate_base_evaluation(task_spec, approach, iteration)
            
            # Calculate HPC-ARC metrics for this iteration
            iteration_intelligence = self._calculate_iteration_intelligence(
                base_result, arc_phase, iteration
            )
            
            # Generate ARC-inspired feedback
            feedback = self._generate_arc_feedback(task_spec, base_result, arc_phase, iteration)
            
            iteration_time = time.time() - iteration_start
            total_execution_time += iteration_time
            
            iteration_results.append({
                'iteration': iteration,
                'result': base_result,
                'intelligence': iteration_intelligence,
                'feedback': feedback,
                'time_used': iteration_time
            })
            
            learning_curve.append(iteration_intelligence)
            
            # Check for convergence (ARC: "skill-acquisition efficiency")
            if self._has_converged(iteration_results):
                break
        
        # Create aggregated result with learning curve data
        final_result = EvaluationResultV2.from_base_result(iteration_results[-1]['result'])
        
        # Update with aggregated metrics
        final_result.iterations_used = len(iteration_results)
        final_result.learning_curve_development = learning_curve
        final_result.time_to_convergence = total_execution_time
        final_result.execution_time_seconds = total_execution_time
        
        # Calculate final HPC-ARC intelligence scores
        final_result = self._calculate_final_intelligence(final_result, arc_phase, iteration_results)
        
        return final_result
    
    def _simulate_base_evaluation(
        self,
        task_spec: HPCARCTaskSpec,
        approach: str,
        iteration: int
    ) -> EvaluationResult:
        """
        Simulate base evaluation for given task and iteration
        
        In a real implementation, this would run the actual optimization approach
        and measure performance. This is a placeholder for simulation purposes.
        """
        # Simulate improving results over iterations
        base_correctness = 0.7 + (0.1 * iteration) if iteration <= 3 else 0.95
        base_efficiency = 40.0 + (15.0 * iteration) if iteration <= 4 else 90.0
        
        result = EvaluationResult(
            task_id=task_spec.task_id,
            approach=approach,
            correctness_score=min(base_correctness, 1.0),
            efficiency_percentage=min(base_efficiency, 100.0),
        )
        
        # Calculate overall score
        result.overall_score = (
            0.6 * result.correctness_score +
            0.4 * (result.efficiency_percentage / 100.0)
        ) * 100.0
        
        return result
    
    def _calculate_iteration_intelligence(
        self,
        base_result: EvaluationResult,
        arc_phase: str,
        iteration: int
    ) -> float:
        """
        Calculate intelligence score for specific iteration
        
        Applies phase-specific weights based on ARC methodology
        """
        # Simulate exploration efficiency (fewer iterations = better)
        exploration_efficiency = 1.0 - (0.1 * iteration) if iteration <= 10 else 0.0
        
        # Simulate hypothesis quality based on correctness
        hypothesis_quality = base_result.correctness_score * 0.9
        
        # Simulate adaptation speed based on efficiency
        adaptation_speed = (base_result.efficiency_percentage / 100.0) * (1.0 - (0.05 * iteration))
        
        # Simulate generalization success (random but correlated to other metrics)
        generalization_success = (exploration_efficiency + hypothesis_quality + adaptation_speed) / 3.0
        
        # Calculate intelligence score with phase-specific weighting
        intelligence_score = self.calculator.calculate_intelligence_score(
            exploration_efficiency,
            hypothesis_quality,
            adaptation_speed,
            generalization_success
        )
        
        return intelligence_score
    
    def _generate_arc_feedback(
        self,
        task_spec: HPCARCTaskSpec,
        base_result: EvaluationResult,
        arc_phase: str,
        iteration: int
    ) -> TaskFeedback:
        """
        Generate ARC-AGI-3 inspired feedback for iterative improvement
        
        Provides actionable feedback and learning opportunities to guide
        agents toward better solutions.
        """
        feedback = TaskFeedback(
            iteration=iteration,
            arc_phase=arc_phase,
            current_intelligence_score=self._calculate_iteration_intelligence(base_result, arc_phase, iteration),
            learning_opportunities=[],
            recommendations=[],
            next_steps=[]
        )
        
        # Phase-specific feedback generation
        if arc_phase == "Explore":
            if base_result.efficiency_percentage < 60.0:
                feedback.learning_opportunities.append(
                    "Cache behavior model needs refinement - consider register pressure effects"
                )
                feedback.recommendations.append(
                    "Implement targeted cache microbenchmarking experiments"
                )
            else:
                feedback.learning_opportunities.append(
                    "Good exploration patterns - consider memory bandwidth saturation analysis"
                )
        
        elif arc_phase == "Hypothesize":
            if base_result.correctness_score < 0.90:
                feedback.learning_opportunities.append(
                    "Hypothesis feasibility assessment requires deeper performance model understanding"
                )
                feedback.recommendations.append(
                    "Incorporate quantitative prediction accuracy measurement"
                )
            else:
                feedback.learning_opportunities.append(
                    "Strong hypothesis formulation - consider cross-architecture applicability"
                )
        
        elif arc_phase == "Execute":
            if base_result.efficiency_percentage < 80.0:
                feedback.learning_opportunities.append(
                    "Optimization convergence can be accelerated through iterative adaptation strategies"
                )
                feedback.recommendations.append(
                    "Apply architecture-specific SIMD and vectorization techniques"
                )
                feedback.next_steps.append(
                    "Implement advanced loop optimizations and memory layout improvements"
                )
            else:
                feedback.learning_opportunities.append(
                    "Excellent adaptation speed - consider cross-platform optimization"
                )
        
        elif arc_phase == "Generalize":
            if base_result.efficiency_percentage < 70.0:
                feedback.learning_opportunities.append(
                    "Cross-architecture pattern understanding requires deeper abstraction of optimization principles"
                )
                feedback.recommendations.append(
                    "Separate core optimization principles from architecture-specific details"
                )
            else:
                feedback.learning_opportunities.append(
                    "Strong generalization capabilities - consider multi-architecture deployment"
                )
        
        # Add general next steps
        if iteration < 3:
            feedback.next_steps.append(
                f"Proceed to iteration {iteration + 1} with refined optimization strategy"
            )
        else:
            feedback.next_steps.append(
                "Consider converging to current solution or exploring alternative approaches"
            )
        
        return feedback
    
    def _has_converged(self, iteration_results: List[Dict[str, Any]]) -> bool:
        """
        Check if the solution has converged (ARC: "skill-acquisition efficiency")
        
        Returns True if further iterations are unlikely to provide significant improvement.
        """
        if len(iteration_results) < 2:
            return False
        
        # Check if intelligence improvement between last two iterations is minimal
        latest_intelligence = iteration_results[-1]['intelligence']
        previous_intelligence = iteration_results[-2]['intelligence']
        
        improvement = abs(latest_intelligence - previous_intelligence)
        
        # Converged if improvement is less than 2%
        return improvement < 0.02
    
    def _calculate_final_intelligence(
        self,
        result: EvaluationResultV2,
        arc_phase: str,
        iteration_results: List[Dict[str, Any]]
    ) -> EvaluationResultV2:
        """
        Calculate final intelligence scores based on all iterations
        
        Aggregates intelligence metrics across all iterations with emphasis
        on final performance and learning curve characteristics.
        """
        # Extract intelligence scores from all iterations
        intelligence_scores = [iteration['intelligence'] for iteration in iteration_results]
        
        # Calculate aggregate metrics
        result.exploration_efficiency = self.calculator.calculate_exploration_efficiency(
            result.iterations_used, 
            max(1, len(iteration_results))
        )
        
        result.hypothesis_quality = self.calculator.calculate_hypothesis_quality(
            iteration_results[-1]['result'].correctness_score * 0.9,
            0.85  # Simulated feasibility score
        )
        
        result.adaptation_speed = self.calculator.calculate_adaptation_speed(
            result.time_to_convergence,
            result.iterations_used * 420  # Assume 7 min per iteration
        )
        
        result.generalization_success = (result.exploration_efficiency + 
                                         result.hypothesis_quality + 
                                         result.adaptation_speed) / 3.0
        
        # Calculate final intelligence score
        result.intelligence_score = self.calculator.calculate_intelligence_score(
            result.exploration_efficiency,
            result.hypothesis_quality,
            result.adaptation_speed,
            result.generalization_success
        )
        
        # Update learning curve
        result.learning_curve_development = intelligence_scores
        
        # Calculate overall score with tri-correlated metrics
        result.overall_score = self.calculator.calculate_overall_score(
            result.correctness_score,
            result.efficiency_percentage,
            result.intelligence_score
        )
        
        return result


def create_sample_tasks():
    """Create sample HPC-ARC task specifications for testing"""
    print("HPC-ARC: Creating sample task specifications...")
    
    benchmark_suite = HPCARCBenchmarkSuite()
    
    # Create sample Explore task
    explore_task = HPCARCTaskSpec(
        task_id="E001",
        name="Systematic Cache Behavior Discovery",
        category=ARCCategory.EXPLORE,
        difficulty=TaskDifficulty.INTERMEDIATE,
        mission="Systematically discover cache behavior characteristics through interactive experimentation",
        description="AI agents learn performance characteristics through structured experimentation",
        estimated_time_budget="20 minutes",
        codebase={
            "files": ["matrix_operations.c", "test_data.h"],
            "language": "C99",
            "optimization_level": "O0"
        },
        hardware={
            "cpu": "Intel Xeon Gold 6348 @ 2.8GHz",
            "cores": "32 physical, 64 threads",
            "cache": "L1: 32KB/core, L2: 1MB/core, L3: 48MB/shared"
        },
        available_tools=["LIKWI", "perf", "PASCIT profiler"],
        unknown_characteristics=[
            "Cache sensitivity of different matrix operations",
            "Optimal data layout for cache utilization",
            "Memory bandwidth saturation points"
        ],
        evaluation_criteria={
            "correctness": {"requirements": "Cache model error < 10%", "weight": 0.4},
            "efficiency": {"requirements": "Complete within budget", "weight": 0.35},
            "generalization": {"requirements": "Accuracy > 80% on unseen data", "weight": 0.25}
        }
    )
    
    # Create sample Hypothesize task
    hypothesize_task = HPCARCTaskSpec(
        task_id="H001",
        name="NUMA-Awareness Hypothesis Formulation",
        category=ARCCategory.HYPOTHESIZE,
        difficulty=TaskDifficulty.ADVANCED,
        mission="Generate testable hypotheses about NUMA optimization opportunities",
        description="Based on exploration findings, formulate quantitative optimization hypotheses",
        estimated_time_budget="15 minutes",
        evaluation_criteria={
            "correctness": {"requirements": "Valid hypothesis structure", "weight": 0.3},
            "efficiency": {"requirements": "Accurate impact prediction", "weight": 0.4},
            "generalization": {"requirements": "Feasible implementation plan", "weight": 0.3}
        }
    )
    
    # Create sample Execute task
    execute_task = HPCARCTaskSpec(
        task_id="EX001",
        name="Iterative SIMD Vectorization with Feedback",
        category=ARCCategory.EXECUTE,
        difficulty=TaskDifficulty.EXPERT,
        mission="Implement adaptive SIMD vectorization with iterative refinement",
        description="Apply modern SIMD techniques with architecture-specific optimizations",
        estimated_time_budget="30 minutes",
        available_tools=["AVX-512F", "AVX-512BW", "AVX-512DQ", "SVE intrinsics"],
        evaluation_criteria={
            "correctness": {"requirements": "Maintain numerical accuracy", "weight": 0.4},
            "efficiency": {"requirements": "≥85% theoretical peak", "weight": 0.4},
            "generalization": {"requirements": "Maintain ≥80% performance across sizes", "weight": 0.2}
        }
    )
    
    # Create sample Generalize task
    generalize_task = HPCARCTaskSpec(
        task_id="G001",
        name="Cross-Architecture MPI Communication Pattern Transfer",
        category=ARCCategory.GENERALIZE,
        difficulty=TaskDifficulty.EXPERT,
        mission="Transfer learned optimization patterns to different hardware architectures",
        description="Apply optimization knowledge from x86 to ARM64 SVE architecture",
        estimated_time_budget="25 minutes",
        evaluation_criteria={
            "correctness": {"requirements": "Pattern preservation", "weight": 0.4},
            "efficiency": {"requirements": "≥70% of x86 performance", "weight": 0.35},
            "generalization": {"requirements": "Demonstrate principle understanding", "weight": 0.25}
        }
    )
    
    # Add tasks to benchmark suite
    benchmark_suite.tasks.update({
        explore_task.task_id: explore_task,
        hypothesize_task.task_id: hypothesize_task,
        execute_task.task_id: execute_task,
        generalize_task.task_id: generalize_task
    })
    
    # Save sample tasks
    output_dir = Path("hpc_arc_benchmarks")
    output_dir.mkdir(exist_ok=True)
    benchmark_suite.save_tasks(output_dir / "sample_tasks.json")
    
    # Display statistics
    stats = benchmark_suite.get_statistics()
    print(f"HPC-ARC: Created sample benchmark suite:")
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  By category: {stats['by_category']}")
    print(f"  Estimated time: {stats['estimated_total_time']}")
    
    return benchmark_suite


# Standalone execution for testing
if __name__ == "__main__":
    print("=== HPC-ARC: HPC Automated Reasoning Benchmark Suite ===")
    print("Initializing PASCIT HPC-ARC integration...")
    
    # Create sample tasks
    benchmark_suite = create_sample_tasks()
    
    # Initialize interactive evaluator
    evaluator = InteractiveTaskEvaluator(benchmark_suite)
    
    # Test evaluation with sample task
    sample_task = benchmark_suite.get_task("E001")
    if sample_task:
        print("\n--- Testing Interactive Evaluation ---")
        result = evaluator.evaluate_task_interactive(
            task_spec=sample_task,
            approach="Test Approach",
            max_iterations=3
        )
        
        print(f"Evaluation Results for {sample_task.name}:")
        print(f"  Overall Score: {result.overall_score:.2f}")
        print(f"  Correctness: {result.correctness_score:.3f}")
        print(f"  Efficiency: {result.efficiency_percentage:.1f}%")
        print(f"  Intelligence Score: {result.intelligence_score:.3f}")
        
        # Interpret intelligence tier
        tier, description = HPCARCCalculator.interpret_intelligence_score(result.intelligence_score)
        print(f"  Performance Tier: {tier}")
        print(f"  Description: {description}")
        
        print(f"\nLearning Curve: {[f'{score:.3f}' for score in result.learning_curve_development]}")
        print(f"Iterations Used: {result.iterations_used}")
        print(f"Time to Convergence: {result.time_to_convergence:.1f}s")
    
    print("\n=== HPC-ARC: Initialization Complete ===")