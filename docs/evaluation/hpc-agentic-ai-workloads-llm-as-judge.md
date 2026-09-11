# HPC Agentic AI Workloads - LLM as Judge

## Executive Summary

This document explains how to use Large Language Models (LLMs) as judges in the HPC Agentic AI Workloads system. LLMs provide intelligent, context-aware evaluation of optimization quality, code correctness, performance improvements, and overall task success. This approach adds a layer of AI-powered assessment complementing traditional metrics and statistical validation.

---

## 1. Why Use LLMs as Judges?

### 1.1 Advantages of AI-Powered Judging

**Context-Aware Assessment:**

- Understand optimization intent and constraints
- Evaluate trade-offs between different approaches
- Assess code complexity and maintainability
- Recognize domain-specific optimization patterns

**Qualitative Evaluation:**

- Assess code quality beyond raw performance
- Identify potential issues not captured by metrics
- Evaluate optimization elegance and sophistication
- Provide actionable feedback and explanations

**Multi-Criteria Decision Making:**

- Balance performance vs. maintainability
- Weigh optimization benefits against complexity
- Consider architectural constraints
- Evaluate suitability for target hardware

**Consistency and Scalability:**

- Consistent evaluation across different tasks
- Scalable to large volumes of optimizations
- Available for on-demand assessment
- Can be trained on successful optimization patterns

### 1.2 Complementing Traditional Evaluation

**Traditional Metrics:**

- Quantitative performance measurements (GFLOPS, speedup)
- Statistical validation (confidence intervals, significance)
- Hardware counter analysis (cache behavior, vectorization)
- Numerical correctness testing

**LLM Judge Enhancements:**

- Qualitative code assessment (elegance, maintainability)
- Optimization strategy evaluation (appropriateness, effectiveness)
- Code pattern recognition (known optimization techniques)
- Architectural fit assessment (hardware compatibility)

**Combined Evaluation Framework:**

```
COMPREHENSIVE EVALUATION:

Traditional Metrics (70% weight):
├─ Performance Improvement (30%)
├─ Statistical Validation (20%)
├─ Numerical Correctness (10%)
└─ Resource Efficiency (10%)

LLM Judge Assessment (30% weight):
├─ Code Quality Evaluation (10%)
├─ Optimization Strategy Assessment (8%)
├─ Maintainability Assessment (7%)
└─ Innovation and Elegance (5%)
```

---

## 2. LLM Judge Categories and Responsibilities

### 2.1 Performance Judge

**Role:** Evaluate the effectiveness of performance optimizations

**Assessment Criteria:**

1. **Speedup Magnitude**: Is the speedup reasonable for the complexity?
2. **Optimization Appropriateness**: Do the optimizations match the identified bottlenecks?
3. **Efficiency Gains**: Are the improvements efficient relative to code complexity?
4. **Hardware Utilization**: Does the optimization properly target hardware capabilities?
5. **Scalability**: Will the optimization scale to larger problem sizes?

**Example Prompt:**

```python
PERFORMANCE_JUDGE_PROMPT = """
You are an expert HPC performance engineer evaluating code optimization quality.

CONTEXT:
Original Code: {original_code}
Optimized Code: {optimized_code}
Performance Metrics:
- Baseline GFLOPS: {baseline_gflops}
- Optimized GFLOPS: {optimized_gflops}
- Speedup: {speedup}x
- Hardware: {hardware_context}

PROFILING DATA:
Bottlenecks Identified: {bottlenecks}
Cache Behavior: {cache_behavior}
Vectorization Status: {vectorization_status}

OPTIMIZATIONS APPLIED:
{optimization_details}

TASK:
Evaluate the performance optimization effectiveness on a scale of 1-10 for each criterion:

1. SPEEDUP_MAGNITUDE (1-10):
   - Is the speedup reasonable for the optimization complexity?
   - Consider: optimization type, hardware capabilities, problem size

2. BOTTLENECK_ALIGNMENT (1-10):
   - Do optimizations target the identified bottlenecks?
   - Consider: cache misses, memory bandwidth, CPU utilization

3. HARDWARE_UTILIZATION (1-10):
   - Does optimization leverage hardware capabilities?
   - Consider: vector units, cache hierarchy, instruction-level parallelism

4. EFFICIENCY_RATIONALE (1-10):
   - Are the improvements justified by code complexity?
   - Consider: code size, maintainability cost vs. performance gain

5. SCALABILITY_POTENTIAL (1-10):
   - Will optimizations scale to larger problem sizes?
   - Consider: memory access patterns, algorithmic complexity

Provide:
- Individual criterion scores with reasoning
- Overall performance score (weighted average)
- Specific strengths and weaknesses
- Recommendations for further improvement

RESPONSE FORMAT:
{
  "individual_scores": {
    "speedup_magnitude": {"score": 8, "reasoning": "..."},
    "bottleneck_alignment": {"score": 9, "reasoning": "..."},
    "hardware_utilization": {"score": 7, "reasoning": "..."},
    "efficiency_rationale": {"score": 9, "reasoning": "..."},
    "scalability_potential": {"score": 8, "reasoning": "..."}
  },
  "overall_score": 8.2,
  "strengths": [
    "Excellent cache blocking strategy",
    "Good alignment with identified memory bottleneck"
  ],
  "weaknesses": [
    "Could benefit from loop unrolling",
    "Prefetching not utilized for large patterns"
  ],
  "recommendations": [
    "Consider prefetching for loops with non-linear access",
    "Add loop unrolling to the inner-most loop"
  ]
}
"""
```

### 2.2 Code Quality Judge

**Role:** Assess the quality, maintainability, and elegance of optimized code

**Assessment Criteria:**

1. **Code Readability**: Is the code clear and understandable?
2. **Maintainability**: Can the code be easily modified and extended?
3. **Documentation Quality**: Are optimizations well-documented?
4. **Safe Patterns**: Are optimization patterns safe and robust?
5. **Portability**: Will the code work across different environments?

**Example Prompt:**

```python
CODE_QUALITY_JUDGE_PROMPT = """
You are an expert software engineer specialized in HPC code quality assessment.

CONTEXT:
Original Code: {original_code}
Optimized Code: {optimized_code}
Optimization Type: {optimization_type}
Target Architecture: {target_architecture}

CHANGES MADE:
{changes_summary}

COMPLEXITY METRICS:
- Lines Added: {lines_added}
- Lines Removed: {lines_removed}
- Cyclomatic Complexity Increase: {complexity_increase}

TASK:
Evaluate code quality on a scale of 1-10 for each criterion:

1. CODE_CLARITY (1-10):
   - Are variable names descriptive?
   - Is control flow understandable?
   - Are optimizations clearly explained?

2. MAINTAINABILITY (1-10):
   - Can modifications be made without breaking optimizations?
   - Are optimization parameters configurable?
   - Is the code modular?

3. DOCUMENTATION_QUALITY (1-10):
   - Are optimization strategies explained?
   - Are performance-critical sections annotated?
   - Is the rationale for changes clear?

4. SAFETY_AND_ROBUSTNESS (1-10):
   - Are edge cases handled?
   - Are bounds checks preserved?
   - Are floating-point concerns addressed?

5. PORTABILITY (1-10):
   - Will code work on different compilers?
   - Is architecture-specific code properly isolated?
   - Are standard coding practices followed?

Provide comprehensive assessment with specific examples from both code versions.

RESPONSE FORMAT:
{
  "individual_scores": {
    "code_clarity": {"score": 7, "reasoning": "Variable names are clear but optimization logic could use comments", "examples": ["Good: 'tile_size' vs Bad: 't'"]},
    "maintainability": {"score": 8, "reasoning": "Modular structure allows easy modification of tile size", "examples": ["Const TILE_SIZE enables easy tuning"]},
    "documentation_quality": {"score": 6, "reasoning": "Limited inline comments explaining blocking strategy", "examples": ["Missing cache fit rationale"]},
    "safety_and_robustness": {"score": 9, "reasoning": "Bounds checks preserved, edge cases handled", "examples": ["Remainder handling for non-multiple sizes"]},
    "portability": {"score": 7, "reasoning": "Architecture-specific code but properly isolated", "examples": ["AVX-512 in dedicated function"]}
  },
  "overall_score": 7.4,
  "strengths": [
    "Modular design prevents optimization breakage",
    "Safety mechanisms well-maintained"
  ],
  "weaknesses": [
    "Limited documentation of optimization rationale",
    some hardcoded values could be parameterized"
  ],
  "improvement_suggestions": [
    "Add detailed comments explaining cache blocking rationale",
    "Consider making TILE_SIZE a configuration parameter",
    "Add inline documentation for vectorization patterns"
  ]
}
"""
```

### 2.3 Correctness Judge

**Role:** Evaluate the correctness and safety of optimizations

**Assessment Criteria:**

1. **Numerical Accuracy**: Does the optimization preserve numerical fidelity?
2. **Algorithmic Correctness**: Is the algorithm fundamentally correct?
3. **Edge Case Handling**: Are boundary conditions properly addressed?
4. **Memory Safety**: Are there memory access violations?
5. **Floating-Point Considerations**: Are floating-point issues addressed?

**Example Prompt:**

```python
CORRECTNESS_JUDGE_PROMPT = """
You are an expert in numerical computing and algorithm verification.

CONTEXT:
Original Code: {original_code}
Optimized Code: {optimized_code}
Algorithm: {algorithm_type}
Data Type: {float_precision}

NUMERICAL TESTS:
- Maximum Error: {max_error}
- Error Distribution: {error_distribution}
- Edge Cases Tested: {edge_cases}

PROFILING DATA:
{profiling_data}

TASK:
Evaluate optimization correctness on a scale of 1-10 for each criterion:

1. NUMERICAL_FIDELITY (1-10):
   - Does optimization preserve numerical accuracy within tolerance?
   - Are there any precision losses?
   - Are cancellation patterns properly handled?

2. ALGORITHMIC_CORRECTNESS (1-10):
   - Is the core algorithm logic preserved?
   - Are loop transformations mathematically equivalent?
   - Are boundary conditions correctly handled?

3. EDGE_CASE_ROBUSTNESS (1-10):
   - Are small/large arrays handled correctly?
   - Are divisibility issues (non-multiple sizes) addressed?
   - Are pathological inputs handled?

4. MEMORY_SAFETY (1-10):
   - Are array bounds respected?
   - Are there potential buffer overflows?
   - Are pointer arithmetic operations safe?

5. FLOATING_POINT_AWARENESS (1-10):
   - Are associativity concerns addressed?
   - Are division-by-zero checks preserved?
   - Are numerical stability issues mitigated?

Analyze the code for specific correctness issues and provide detailed reasoning.

RESPONSE FORMAT:
{
  "individual_scores": {
    "numerical_fidelity": {"score": 9, "reasoning": "Error within 1e-7 tolerance, no precision loss", "concerns": []},
    "algorithmic_correctness": {"score": 10, "reasoning": "Loop reordering perfectly preserves computation", "concerns": []},
    "edge_case_robustness": {"score": 8, "reasoning": "Non-multiple sizes handled with remainder loops", "concerns": ["Potential performance degradation on small tail elements"]},
    "memory_safety": {"score": 10, "reasoning": "All bounds checks preserved, no unsafe operations", "concerns": []},
    "floating_point_awareness": {"score": 7, "reasoning": "No dangerous associativity changes, but could improve", "concerns": ["Parallel reduction order might affect rounding"]}
  },
  "overall_score": 8.8,
  "correctness_verification": "PASSED",
  "critical_issues": [],
  "minor_concerns": [
    "Small non-multiple array tails handled serially",
    "Parallel reduction order might slightly affect rounding"
  ],
  "recommendations": [
    "Consider vectorized remainder handling for tails",
    "Document floating-point rounding behavior"
  ]
}
"""
```

### 2.4 Optimization Strategy Judge

**Role:** Evaluate the appropriateness and effectiveness of optimization strategies

**Assessment Criteria:**

1. **Strategy Appropriateness**: Is the optimization strategy suitable for the problem?
2. **Bottleneck Targeting**: Do optimizations target the actual bottlenecks?
3. **Complexity-Benefit Trade-off**: Are the results worth the added complexity?
4. **Architecture Alignment**: Do optimizations target the right hardware features?
5. **Innovation Quality**: Are the optimizations innovative or standard?

**Example Prompt:**

```python
STRATEGY_JUDGE_PROMPT = """
You are an expert HPC optimization strategist with deep knowledge of performance analysis.

CONTEXT:
Original Code: {original_code}
Optimized Code: {optimized_code}
Hardware Context: {hardware_context}

PROFILING ANALYSIS:
{profiling_analysis}

BOTTLENECKS IDENTIFIED:
{bottlenecks}

OPTIMIZATION STRATEGY:
{optimization_strategy}

EXPECTED vs ACHIEVED:
- Expected Speedup: {expected_speedup}
- Achieved Speedup: {achieved_speedup}
- Target Achievement: {achievement_percentage}%

TASK:
Evaluate optimization strategy on a scale of 1-10 for each criterion:

1. STRATEGY_APPROPRIATENESS (1-10):
   - Is the chosen optimization technique suitable for this problem?
   - Are alternative strategies that would be more effective?
   - Does the strategy match the identified bottleneck?

2. BOTTLENECK_TARGETING (1-10):
   - Do optimizations address the actual performance limitations?
   - Are there untapped optimization opportunities?
   - Is the bottleneck analysis accurate?

3. COMPLEXITY_BENEFIT_RATIO (1-10):
   - Is the performance gain justified by code complexity?
   - Could simpler optimizations achieve similar results?
   - Is the maintainability cost acceptable?

4. ARCHITECTURE_ALIGNMENT (1-10):
   - Do optimizations leverage hardware capabilities?
   - Are the right instruction sets utilized?
   - Is memory hierarchy properly exploited?

5. INNOVATION_AND_ELEGANCE (1-10):
   - Are the optimizations creative or standard?
   - Is there evidence of sophisticated understanding?
   - Do optimizations show insight beyond simple patterns?

Provide detailed strategic analysis with specific recommendations.

RESPONSE FORMAT:
{
  "individual_scores": {
    "strategy_appropriateness": {"score": 9, "reasoning": "Cache blocking perfectly addresses memory bandwidth limitation", "alternatives_considered": ["Register blocking", "Prefetching-only"]},
    "bottleneck_targeting": {"score": 10, "reasoning": "Directly targets 60% L1 cache miss rate", "untapped_opportunities": ["Loop unrolling", "Prefetching"]},
    "complexity_benefit_ratio": {"score": 8, "reasoning": "3.5× speedup for moderate complexity increase", "alternatives": ["SIMD-only would give 8× but much more complex"]},
    "architecture_alignment": {"score": 9, "reasoning": "Tile size optimized for L1 cache (32KB)", "architecture_features": ["AVX-512 vectorization", "Cache hierarchy"]},
    "innovation_and_elegance": {"score": 7, "reasoning": "Solid application of standard blocking patterns", "innovation": ["Tile size selection shows hardware understanding"]}
  },
  "overall_score": 8.6,
  "strategic_assessment": "EXCELLENT",
  "strengths": [
    "Perfectly matches memory bandwidth bottleneck",
    "Tile size demonstrates hardware knowledge",
    "Reasonable complexity for achieved performance"
  ],
  "potential_improvements": [
    "Consider adding prefetching for larger patterns",
    "Loop unrolling could provide additional 20-30% improvement"
  ],
  "strategic_recommendations": [
    "Strategy is well-suited for current hardware",
    "Consider multi-level blocking for different cache levels",
    "Prefetching should be next optimization step"
  ]
}
"""
```

---

## 3. LLM Judge Implementation

### 3.1 Judge Architecture

```python
class LLMJudgeFramework:
    """
    Comprehensive LLM judging framework for HPC workload evaluation
    """

    def __init__(self, llm_provider: LLMProvider, config: JudgeConfig):
        self.llm = llm_provider
        self.config = config
        self.judges = {
            'performance': PerformanceJudge(llm_provider),
            'code_quality': CodeQualityJudge(llm_provider),
            'correctness': CorrectnessJudge(llm_provider),
            'strategy': StrategyJudge(llm_provider)
        }

    def evaluate_optimization(
        self,
        optimization_result: OptimizationResult,
        judge_types: List[str] = None
    ) -> EvaluationResult:
        """
        Comprehensive evaluation using multiple LLM judges
        """

        if judge_types is None:
            judge_types = list(self.judges.keys())

        evaluation = EvaluationResult(
            optimization_id=optimization_result.task_id,
            evaluation_timestamp=datetime.utcnow()
        )

        for judge_type in judge_types:
            try:
                judge = self.judges[judge_type]
                judge_result = judge.evaluate(optimization_result)
                evaluation.add_judge_result(judge_type, judge_result)
            except Exception as e:
                evaluation.add_judge_error(judge_type, str(e))

        # Calculate composite score
        evaluation.calculate_composite_score()

        return evaluation

    def evaluate_batch(
        self,
        optimization_results: List[OptimizationResult],
        parallel: bool = True
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple optimizations efficiently
        """

        if parallel and self.config.parallel_evaluation:
            return self._evaluate_parallel(optimization_results)
        else:
            return self._evaluate_sequential(optimization_results)

    def _evaluate_parallel(self, results: List[OptimizationResult]) -> List[EvaluationResult]:
        """Parallel evaluation using concurrent threads"""
        with ThreadPoolExecutor(max_workers=self.config.max_parallel_judges) as executor:
            futures = {
                executor.submit(self.evaluate_optimization, result): result
                for result in results
            }

            evaluation_results = []
            for future in as_completed(futures):
                result = futures[future]
                try:
                    evaluation_results.append(future.result())
                except Exception as e:
                    # Create failed evaluation result
                    evaluation_results.append(
                        EvaluationResult.failed(result.task_id, str(e))
                    )

        return evaluation_results
```

### 3.2 Base Judge Class

```python
class BaseLLMJudge:
    """
    Base class for LLM judges providing common functionality
    """

    def __init__(self, llm_provider: LLMProvider, judge_config: dict):
        self.llm = llm_provider
        self.config = judge_config
        self.prompt_template = self._load_prompt_template()
        self.response_parser = self._create_response_parser()

    def evaluate(self, optimization_result: OptimizationResult) -> JudgeResult:
        """
        Main evaluation method
        """
        # Build evaluation context
        context = self._build_evaluation_context(optimization_result)

        # Generate prompt from template
        prompt = self._generate_prompt(context)

        # Get LLM response
        llm_response = self._get_llm_response(prompt)

        # Parse and validate response
        parsed_result = self._parse_response(llm_response)

        # Validate result quality
        validated_result = self._validate_result(parsed_result, optimization_result)

        return validated_result

    def _build_evaluation_context(self, result: OptimizationResult) -> dict:
        """Build comprehensive evaluation context"""
        context = {
            # Code information
            'original_code': result.original_code,
            'optimized_code': result.optimized_code,
            'code_file': result.code_file,
            'language': result.language,

            # Performance metrics
            'baseline_gflops': result.baseline_performance.gflops,
            'optimized_gflops': result.optimized_performance.gflops,
            'speedup': result.speedup,
            'execution_time_reduction': result.execution_time_reduction,

            # Profiling data
            'profiling_data': result.profiling_data,
            'bottlenecks': result.bottlenecks,
            'cache_behavior': result.cache_behavior,
            'vectorization_status': result.vectorization_status,

            # Optimization details
            'optimizations_applied': result.optimizations_applied,
            'optimization_strategy': result.optimization_strategy,
            'changes_made': result.changes_summary,

            # Hardware context
            'hardware_context': result.hardware_context,
            'target_architecture': result.target_architecture,

            # Validation data
            'numerical_tests': result.numerical_tests,
            'correctness_validation': result.correctness_validation,
            'edge_cases': result.edge_cases_tested,

            # Metadata
            'task_id': result.task_id,
            'user_id': result.user_id,
            'timestamp': result.timestamp
        }

        return context

    def _generate_prompt(self, context: dict) -> str:
        """Generate evaluation prompt from template"""
        prompt = self.prompt_template.format(**context)
        return prompt

    def _get_llm_response(self, prompt: str) -> str:
        """Get response from LLM with retry logic"""
        max_retries = self.config.get('max_retries', 3)
        retry_delay = self.config.get('retry_delay', 2)

        for attempt in range(max_retries):
            try:
                response = self.llm.generate(
                    prompt=prompt,
                    temperature=0.0,
                    max_tokens=4000,
                    top_p=0.95
                )
                return response.text
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                else:
                    raise JudgeException(f"LLM evaluation failed after {max_retries} attempts: {str(e)}")

    def _parse_response(self, response: str) -> dict:
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: structured parsing
                return self._parse_structured_response(response)
        except json.JSONDecodeError:
            # Fallback: structured parsing
            return self._parse_structured_response(response)

    def _validate_result(self, parsed_result: dict, optimization_result: OptimizationResult) -> JudgeResult:
        """Validate and create final judge result"""
        # Check for required fields
        required_fields = ['individual_scores', 'overall_score']
        for field in required_fields:
            if field not in parsed_result:
                raise JudgeValidationException(f"Missing required field: {field}")

        # Validate score ranges
        for score_name, score_data in parsed_result['individual_scores'].items():
            if not 1 <= score_data['score'] <= 10:
                raise JudgeValidationException(f"Score {score_name} out of range: {score_data['score']}")

        # Create judge result
        judge_result = JudgeResult(
            judge_type=self.__class__.__name__,
            individual_scores=parsed_result['individual_scores'],
            overall_score=parsed_result['overall_score'],
            strengths=parsed_result.get('strengths', []),
            weaknesses=parsed_result.get('weaknesses', []),
            recommendations=parsed_result.get('recommendations', []),
            reasoning_data=parsed_result
        )

        return judge_result
```

### 3.3 Specific Judge Implementations

#### Performance Judge Implementation

```python
class PerformanceJudge(BaseLLMJudge):
    """
    Performance-specific LLM judge implementation
    """

    def __init__(self, llm_provider: LLMProvider):
        config = {
            'max_retries': 3,
            'retry_delay': 2,
            'scoring_weights': {
                'speedup_magnitude': 0.25,
                'bottleneck_alignment': 0.25,
                'hardware_utilization': 0.20,
                'efficiency_rationale': 0.15,
                'scalability_potential': 0.15
            }
        }
        super().__init__(llm_provider, config)
        self.prompt_template = PERFORMANCE_JUDGE_PROMPT

    def _calculate_weighted_score(self, scores: dict) -> float:
        """Calculate weighted performance score"""
        weighted_sum = 0.0
        total_weight = 0.0

        for criterion, score_data in scores.items():
            weight = self.config['scoring_weights'].get(criterion, 0.0)
            weighted_sum += score_data['score'] * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _validate_result(self, parsed_result: dict, optimization_result: OptimizationResult) -> JudgeResult:
        """Performance-specific validation"""
        # Base validation
        judge_result = super()._validate_result(parsed_result, optimization_result)

        # Additional performance validation
        if optimization_result.speedup < 1.0 and judge_result.individual_scores['speedup_magnitude']['score'] > 7:
            # Adjust score if performance actually degraded
            judge_result.individual_scores['speedup_magnitude']['score'] = 3
            judge_result.individual_scores['speedup_magnitude']['reasoning'] += " [ADJUSTED: Actual performance decreased]"
            judge_result.overall_score = self._calculate_weighted_score(judge_result.individual_scores)

        return judge_result
```

#### Code Quality Judge Implementation

```python
class CodeQualityJudge(BaseLLMJudge):
    """
    Code quality-specific LLM judge implementation
    """

    def __init__(self, llm_provider: LLMProvider):
        config = {
            'max_retries': 3,
            'retry_delay': 2,
            'scoring_weights': {
                'code_clarity': 0.25,
                'maintainability': 0.25,
                'documentation_quality': 0.20,
                'safety_and_robustness': 0.20,
                'portability': 0.10
            }
        }
        super().__init__(llm_provider, config)
        self.prompt_template = CODE_QUALITY_JUDGE_PROMPT

    def _validate_result(self, parsed_result: dict, optimization_result: OptimizationResult) -> JudgeResult:
        """Code quality-specific validation"""
        # Base validation
        judge_result = super()._validate_result(parsed_result, optimization_result)

        # Check for common code quality indicators
        if len(optimization_result.optimizations_applied) == 0:
            # If no optimizations applied, maintainability should be high
            judge_result.individual_scores['maintainability']['score'] = 10
            judge_result.individual_scores['maintainability']['reasoning'] = "No code changes means perfect maintainability"

        return judge_result
```

---

## 4. Evaluation Integration Strategy

### 4.1 Integration with Optimization Workflow

```python
class JudgeIntegratedWorkflow:
    """
    HPC optimization workflow with integrated LLM judging
    """

    def __init__(self, harness_client: HarnessClient, judge_framework: LLMJudgeFramework):
        self.harness = harness
        self.judges = judge_framework
        self.workflow_engine = harness.get_workflow_engine()

    def execute_judged_optimization_workflow(self, task_spec: dict) -> JudgedWorkflowResult:
        """
        Execute optimization workflow with continuous LLM assessment
        """

        workflow_result = JudgedWorkflowResult(
            task_id=task_spec['task_id'],
            evaluation_timeline=[]
        )

        # Step 1: Profiling (no judging needed)
        profiling_result = self._execute_profiling(task_spec)
        workflow_result.add_step_result('profiling', profiling_result)

        # Step 2: LLM Strategy Judge (evaluate optimization plan)
        strategy_result = self._execute_strategy_analysis(task_spec, profiling_result)
        strategy_evaluation = self.judges.evaluate(
            type='strategy', data=strategy_result)
        workflow_result.add_step_result('strategy_analysis', strategy_result, strategy_evaluation)

        # Step 3: Code Generation with Quality Judge
        code_result = self._execute_code_generation(task_spec, strategy_result)
        code_quality_evaluation = self.judges.evaluate(
            type='code_quality', data=code_result)
        workflow_result.add_step_result('code_generation', code_result, code_quality_evaluation)

        # Step 4: Correctness Evaluation
        correctness_result = self._execute_correctness_validation(task_spec, code_result)
        correctness_evaluation = self.judges.evaluate(
            type='correctness', data=correctness_result)
        workflow_result.add_step_result('correctness_validation', correctness_result, correctness_evaluation)

        # Step 5: Performance Evaluation
        performance_result = self._execute_performance_testing(task_spec, correctness_result)
        performance_evaluation = self.judges.evaluate(
            type='performance', data=performance_result)
        workflow_result.add_step_result('performance_testing', performance_result, performance_evaluation)

        # Calculate final comprehensive score
        workflow_result.calculate_comprehensive_score()

        return workflow_result
```

### 4.2 Real-Time Feedback Loop

```python
class FeedbackLoopIntegration:
    """
    Integrate LLM judge feedback into optimization iteration
    """

    def __init__(self, llm_optimizer: LLMOptimizer, judge_framework: LLMJudgeFramework):
        self.optimizer = llm_optimizer
        self.judges = judge_framework
        self.feedback_processor = FeedbackProcessor()

    def execute_iterative_judged_optimization(
        self,
        original_task: OptimizationTask,
        max_iterations: int = 3
    ) -> IterativeOptimizationResult:
        """
        Execute optimization iterations with judge feedback
        """

        current_code = original_task.source_code
        improvements_log = []

        for iteration in range(1, max_iterations + 1):
            # Execute optimization for this iteration
            optimization_result = self.optimizer.optimize(
                source_code=current_code,
                context=original_task.context
            )

            # Get comprehensive evaluation
            evaluation = self.judges.evaluate(
                type='comprehensive',
                data=optimization_result
            )

            # Process judge feedback for next iteration
            feedback = self._process_judge_feedback(evaluation)

            # Log this iteration
            improvements_log.append({
                'iteration': iteration,
                'optimization_result': optimization_result,
                'evaluation': evaluation,
                'judge_feedback': feedback
            })

            # Check if we should continue iterating
            if not self._should_continue_iterating(evaluation, iteration, max_iterations):
                break

            # Apply judge recommendations for next iteration
            current_code = self._incorporate_judge_recommendations(current_code, feedback)

        return IterativeOptimizationResult(
            original_task=original_task,
            iterations=improvements_log,
            final_code=current_code,
            final_evaluation=evaluation
        )

    def _process_judge_feedback(self, evaluation: EvaluationResult) -> JudgeFeedback:
        """Process and prioritize judge feedback"""
        feedback = JudgeFeedback()

        # Collect all recommendations from all judges
        all_recommendations = []
        for judge_type, judge_result in evaluation.judge_results.items():
            all_recommendations.extend(judge_result.recommendations)

        # Prioritize by frequency and impact
        prioritized_recommendations = self.feedback_processor.prioritize(
            recommendations=all_recommendations,
            evaluation_scores=evaluation.judge_results
        )

        feedback.recommendations = prioritized_recommendations
        feedback.weaknesses = self._collect_weaknesses(evaluation)
        feedback.strengths = self._collect_strengths(evaluation)

        return feedback

    def _should_continue_iterating(
        self,
        evaluation: EvaluationResult,
        current_iteration: int,
        max_iterations: int
    ) -> bool:
        """Determine if optimization should continue"""
        # Check iteration limit
        if current_iteration >= max_iterations:
            return False

        # Check if significant improvements possible
        composite_score = evaluation.composite_score
        if composite_score > 8.5:  # High threshold for optimization quality
            return False

        # Check if judges recommend further improvements
        has_improvement_recommendations = any(
            judge_result.overall_score < 8.0
            and len(judge_result.recommendations) > 0
            for judge_result in evaluation.judge_results.values()
        )

        return has_improvement_recommendations
```

---

## 5. Judge Training and Calibration

### 5.1 Judge Training

```python
class LLMJudgeTrainer:
    """
    Train and calibrate LLM judges using expert evaluations
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.training_data = JudgeTrainingDataset()
        self.calibration_method = "expert_feedback"

    def train_judge(
        self,
        judge_type: str,
        training_examples: List[JudgeTrainingExample]
    ) -> JudgeTrainingResult:
        """
        Train specific judge type using expert evaluations
        """

        # Prepare training data
        prepared_data = self._prepare_training_data(training_examples)

        # Create fine-tuning dataset
        fine_tuning_prompt = self._create_fine_tuning_prompt(judge_type, prepared_data)

        # Configure training parameters
        training_config = self._get_training_config(judge_type)

        # Execute fine-tuning
        fine_tuned_model = self._fine_tune_model(
            base_model=self.llm.model_name,
            training_data=fine_tuning_prompt,
            config=training_config
        )

        # Validate trained judge
        validation_results = self._validate_judge(
            judge_type=judge_type,
            trained_model=fine_tuned_model,
            validation_examples=self._get_validation_examples(judge_type)
        )

        # Create trained judge instance
        trained_judge = self._create_judge_instance(
            judge_type=judge_type,
            model=fine_tuned_model
        )

        return JudgeTrainingResult(
            judge_type=judge_type,
            trained_model=fine_tuned_model,
            validation_score=validation_results.accuracy,
            training_examples=len(training_examples),
            calibration_metadata=validation_results.metadata
        )

    def _create_fine_tuning_prompt(
        self,
        judge_type: str,
        training_data: List[JudgeTrainingExample]
    ) -> str:
        """Create fine-tuning training prompt"""
        system_prompt = self._get_judge_system_prompt(judge_type)

        training_samples = []
        for example in training_data:
            training_samples.append({
                "context": example.evaluation_context,
                "expert_evaluation": example.expert_evaluation,
                "reasoning": example.expert_reasoning
            })

        fine_tuning_data = {
            "system_prompt": system_prompt,
            "training_examples": training_samples,
            "output_format": "consistent_json_evaluation"
        }

        return json.dumps(fine_tuning_data, indent=2)

    def _fine_tune_model(
        self,
        base_model: str,
        training_data: str,
        config: dict
    ) -> str:
        """
        Execute model fine-tuning
        """
        # This would interface with the actual fine-tuning API
        # Implementation depends on the LLM provider

        fine_tuning_request = {
            "base_model": base_model,
            "training_data": training_data,
            "hyperparameters": {
                "learning_rate": config.get("learning_rate", 1e-5),
                "batch_size": config.get("batch_size", 4),
                "epochs": config.get("epochs", 3),
                "warmup_steps": config.get("warmup_steps", 100)
            },
            "validation_split": 0.2,
            "output_prefix": f"fine_tuned_{base_model}"
        }

        # Submit fine-tuning job
        fine_tuned_model_id = self.llm.fine_tune(**fine_tuning_request)

        return fine_tuned_model_id
```

### 5.2 Judge Calibration

```python
class JudgeCalibration:
    """
    Calibrate LLM judges against expert human evaluations
    """

    def __init__(self, judge_framework: LLMJudgeFramework):
        self.judges = judge_framework
        self.calibration_database = CalibrationDatabase()

    def calibrate_judge(
        self,
        judge_type: str,
        calibration_examples: List[CalibrationExample]
    ) -> CalibrationResult:
        """
        Calibrate specific judge against expert evaluations
        """

        calibration_metrics = []

        for example in calibration_examples:
            # Get judge evaluation
            judge_evaluation = self.judges.evaluate(
                type=judge_type,
                data=example.optimization_result
            )

            # Compare with expert evaluation
            comparison = self._compare_evaluations(
                judge_evaluation=judge_evaluation,
                expert_evaluation=example.expert_evaluation
            )

            calibration_metrics.append(comparison)

        # Calculate calibration statistics
        calibration_stats = self._calculate_calibration_statistics(calibration_metrics)

        # Determine if calibration is needed
        calibration_needed = self._assess_calibration_need(calibration_stats)

        calibration_result = CalibrationResult(
            judge_type=judge_type,
            calibration_metrics=calibration_metrics,
            calibration_statistics=calibration_stats,
            calibration_needed=calibration_needed,
            calibration_adjustments=self._generate_calibrations(calibration_stats)
        )

        return calibration_result

    def _compare_evaluations(
        self,
        judge_evaluation: EvaluationResult,
        expert_evaluation: ExpertEvaluation
    ) -> CalibrationMetrics:
        """
        Compare judge evaluation with expert evaluation
        """

        # Compare overall scores
        overall_difference = abs(
            judge_evaluation.composite_score -
            expert_evaluation.overall_score
        )

        # Compare individual criterion scores
        criterion_differences = {}
        for criterion in judge_evaluation.judge_results.keys():
            judge_score = judge_evaluation.judge_results[criterion].overall_score
            expert_score = expert_evaluation.detailed_scores.get(criterion, {}).get('score', judge_score)
            criterion_differences[criterion] = abs(judge_score - expert_score)

        # Compare qualitative assessments
        qualitative_similarity = self._compare_qualitative_assessments(
            judge_evaluation.judge_results,
            expert_evaluation.qualitative_feedback
        )

        return CalibrationMetrics(
            overall_difference=overall_difference,
            criterion_differences=criterion_differences,
            qualitative_similarity=qualitative_similarity,
            calibration_example_id=expert_evaluation.example_id
        )

    def _calculate_calibration_statistics(
        self,
        calibration_metrics: List[CalibrationMetrics]
    ) -> dict:
        """
        Calculate statistical calibration metrics
        """

        overall_differences = [m.overall_difference for m in calibration_metrics]

        return {
            "mean_difference": np.mean(overall_differences),
            "std_difference": np.std(overall_differences),
            "max_difference": np.max(overall_differences),
            "min_difference": np.min(overall_differences),
            "within_tolerance": sum(1 for d in overall_differences if d < 1.0) / len(overall_differences),
            "correlation_with_expert": self._calculate_correlation(calibration_metrics)
        }

    def _generate_calibrations(
        self,
        calibration_stats: dict
    ) -> List[CalibrationAdjustment]:
        """
        Generate calibration adjustments based on statistics
        """

        adjustments = []

        # If consistent bias detected
        if abs(calibration_stats["mean_difference"]) > 0.5:
            adjustments.append(
                CalibrationAdjustment(
                    adjustment_type="bias_correction",
                    value=-calibration_stats["mean_difference"],
                    reason="Consistent scoring bias detected"
                )
            )

        # If high variability detected
        if calibration_stats["std_difference"] > 1.5:
            adjustments.append(
                CalibrationAdjustment(
                    adjustment_type="precision_improvement",
                    action="reduce_scoring_range",
                    value=calibration_stats["std_difference"],
                    reason="High scoring variability detected"
                )
            )

        # If poor correlation with experts
        if calibration_stats["correlation_with_expert"] < 0.7:
            adjustments.append(
                CalibrationAdjustment(
                    adjustment_type="expert_feedback_integration",
                    action="increase_exert_weight",
                    value=1.0 - calibration_stats["correlation_with_expert"],
                    reason="Poor correlation with expert evaluations"
                )
            )

        return adjustments
```

---

## 6. Practical Usage Examples

### 6.1 Single Optimization Evaluation

```python
# Example: Evaluate a single optimization
judge_framework = LLMJudgeFramework(llm_provider=llm_provider)

optimization_result = OptimizationResult(
    task_id="TASK-OPT-001",
    original_code=GEMM_ORIGINAL_CODE,
    optimized_code=GEMM_OPTIMIZED_CODE,
    baseline_performance={'gflops': 2.1},
    optimized_performance={'gflops': 7.8},
    profiling_data={'l1_miss_rate': 0.45, 'vectorization_rate': 0.92},
    optimizations_applied=['loop_tiling', 'vectorization'],
    hardware_context={'processor': 'Intel Xeon Gold 6348', 'cores': 48}
)

# Get comprehensive evaluation
evaluation = judge_framework.evaluate_optimization(
    optimization_result=optimization_result
)

print(f"Overall Score: {evaluation.composite_score:.2f}/10")
print(f"Performance Judge: {evaluation.judge_results['performance'].overall_score:.2f}/10")
print(f"Code Quality Judge: {evaluation.judge_results['code_quality'].overall_score:.2f}/10")

# Get specific feedback
print("\nStrengths:")
for strength in evaluation.judge_results['performance'].strengths:
    print(f"  - {strength}")

print("\nWeaknesses:")
for weakness in evaluation.judge_results['performance'].weaknesses:
    print(f"  - {weakness}")

print("\nRecommendations:")
for recommendation in evaluation.judge_results['performance'].recommendations:
    print(f"  - {recommendation}")
```

### 6.2 Iterative Optimization with Judge Feedback

```python
# Example: Iterative optimization with judge feedback
feedback_loop = FeedbackLoopIntegration(
    llm_optimizer=optimizer,
    judge_framework=judge_framework
)

original_task = OptimizationTask(
    task_id="TASK-ITER-001",
    source_code=ORIGINAL_CODE,
    context={'hardware': 'Intel Xeon', 'optimization_target': 'speed'}
)

# Execute iterative judged optimization
iterative_result = feedback_loop.execute_iterative_judged_optimization(
    original_task=original_task,
    max_iterations=3
)

print("Optimization Progress:")
for i, iteration in enumerate(iterative_result.iterations, 1):
    print(f"\nIteration {i}:")
    print(f"  Score: {iteration['evaluation'].composite_score:.2f}/10")
    print(f"  Judge Feedback: {len(iteration['judge_feedback'].recommendations)} recommendations")

print(f"\nFinal Score: {iterative_result.final_evaluation.composite_score:.2f}/10")
print(f"Total Improvements: {len(iterative_result.iterations)} iterations")
```

### 6.3 Benchmark Comparison Judging

```python
# Example: Judge multiple optimization approaches
judge_framework = LLMJudgeFramework(llm_provider=llm_provider)

optimization_approaches = [
    {
        'name': 'Loop Tiling',
        'result': OptimizationResult(tiling_code, performance_data)
    },
    {
        'name': 'Vectorization',
        'result': OptimizationResult(vectorized_code, performance_data)
    },
    {
        'name': 'Combined Tiling+Vectorization',
        'result': OptimizationResult(combined_code, performance_data)
    }
]

# Evaluate all approaches
evaluations = []
for approach in optimization_approaches:
    evaluation = judge_framework.evaluate_optimization(approach['result'])
    evaluations.append({
        'name': approach['name'],
        'evaluation': evaluation
    })

# Compare results
print("Optimization Approach Comparison:")
print(f"{'Approach':<30} {'Overall Score':<15} {'Performance':<15} {'Code Quality':<15}")
print("-" * 75)

for eval_result in sorted(evaluations, key=lambda x: -x['evaluation'].composite_score):
    print(f"{eval_result['name']:<30} "
          f"{eval_result['evaluation'].composite_score:<15.2f} "
          f"{eval_result['evaluation'].judge_results['performance'].overall_score:<15.2f} "
          f"{eval_result['evaluation'].judge_results['code_quality'].overall_score:<15.2f}")
```

---

## 7. Integration Benefits and Limitations

### 7.1 Key Benefits

**Enhanced Evaluation Depth:**

- Qualitative assessment beyond quantitative metrics
- Context-aware optimization evaluation
- Multi-criteria scoring frameworks

**Continuous Improvement:**

- Feedback loops enable iterative optimization
- Judge recommendations guide next steps
- Calibration ensures consistency over time

**Scalability:**

- Automated evaluation at scale
- Consistent judgments across tasks
- Integration with workflow automation

**Domain Expertise:**

- Specialized judges for different aspects
- HPC-specific evaluation criteria
- Architecture-aware assessment

### 7.2 Limitations and Mitigations

**LLM Limitations:**

- **Knowledge Cutoff:** May not be aware of recent hardware developments
  - Mitigation: Regular training updates, expert supervision
- **Hallucination Risk:** May generate incorrect assessments
  - Mitigation: Validation against metrics, expert review
- **Bias Potential:** May carry training data biases
  - Mitigation: Diverse training data, regular bias audits

**Evaluation Consistency:**

- **Score Variance:** Similar optimizations may receive different scores
  - Mitigation: Calibration, multiple judge consensus, temperature control
- **Context Sensitivity:** Judgments may vary with presentation
  - Mitigation: Standardized prompts, consistent context formatting

**Computational Cost:**

- **API Latency:** LLM evaluation adds to optimization time
  - Mitigation: Caching, parallelization, batch evaluation
- **Service Costs:** LLM API usage costs
  - Mitigation: Local models, efficient prompting, result caching

---

## 8. Best Practices for LLM Judging

### 8.1 Prompt Engineering Guidelines

**Clear Instructions:**

- Specify exact scoring criteria and ranges
- Provide concrete examples for each score level
- Define response format precisely

**Rich Context:**

- Include complete code before and after
- Provide profiling data and metrics
- Describe hardware context and constraints

**Structured Output:**

- Request JSON-formatted responses
- Specify required fields and types
- Include reasoning for each score

**Validation Checklist:**

- Scores within specified range (1-10)
- All required fields present
- Reasoning provided for scores
- Recommendations specific to context

### 8.2 Evaluation Safety

**Multiple Judge Consensus:**

```python
# Use multiple LLM judges for important evaluations
def get_consensus_evaluation(optimization_result: OptimizationResult) -> EvaluationResult:
    # Get evaluations from multiple LLM providers/models
    evaluations = []
    for provider in ['llama3', 'gpt-4', 'claude']:
        judge_framework = LLMJudgeFramework(get_llm_provider(provider))
        evaluation = judge_framework.evaluate_optimization(optimization_result)
        evaluations.append(evaluation)

    # Calculate consensus
    return calculate_consensus(evaluations)
```

**Fallback to Metrics:**

```python
def safe_judge_evaluation(optimization_result: OptimizationResult) -> EvaluationResult:
    try:
        # Try LLM judge evaluation
        return judge_framework.evaluate_optimization(optimization_result)
    except Exception as e:
        # Fallback to metric-based evaluation
        return metric_fallback_evaluation(optimization_result)
```

**Human Review Override:**

```python
def human_review_evaluation(evaluation: EvaluationResult) -> EvaluationResult:
    # Flag low-confidence evaluations for human review
    if evaluation.confidence < 0.7:
        evaluation.requires_human_review = True
        evaluation.human_reviewer = "pending_assignment"

    return evaluation
```

---

## 9. Future Enhancements

### 9.1 Advanced Judge Capabilities

**Adaptive Judges:**

- Learn from actual optimization outcomes
- Adjust scoring based on success rates
- Incorporate user feedback loops

**Specialized Domain Judges:**

- NUMA optimization judges
- Memory hierarchy specialists
- Floating-point precision experts
- Parallel programming judges

**Multi-Modal Judges:**

- Analyze visualization files
- Process performance plots
- Understand profiling diagrams
- Evaluate algorithm animations

### 9.2 Integration Advances

**Real-time Judge Integration:**

- Continuous monitoring during optimization
- Live feedback during code generation
- Dynamic strategy adjustment based on judge feedback

**Judge Ensemble:**

- Combine multiple specialized judges
- Weighted consensus mechanisms
- Hierarchical judge structures

**Self-Improving Judges:**

- Analyze their evaluation patterns
- Identify biases and correct them
- Improve consistency over time

---

## Conclusion

Using LLMs as judges in HPC optimization workflows provides a powerful layer of intelligent evaluation that complements traditional quantitative metrics. The framework demonstrates how multiple specialized judges can assess different aspects of optimization quality, providing comprehensive, context-aware feedback that guides iterative improvement.

The key success factors are:

1. **Specialized Judge Design** - Tailored prompts and criteria for each evaluation aspect
2. **Integration with Workflows** - Seamless integration into optimization processes
3. **Calibration and Training** - Continuous improvement through expert feedback
4. **Validation and Safety** - Fallback mechanisms and human oversight
5. **Scalability** - Efficient batch evaluation and caching strategies

This approach enables more nuanced, comprehensive evaluation of HPC optimizations while maintaining scalability and consistency across diverse optimization tasks.
