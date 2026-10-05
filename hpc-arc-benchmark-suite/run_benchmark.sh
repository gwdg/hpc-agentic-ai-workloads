#!/bin/bash

# HPC-ARC Benchmark Suite Automated Execution Script
# This script provides a complete automated execution framework for all HPC-ARC phases

CONFIG="config/benchmark_config.json"
RESULTS_DIR="results/"
REPORTS_DIR="reports/"
LOGS_DIR="logs/"
N_MEASUREMENTS=5
CONFIDENCE_INTERVAL=0.95

# Create necessary directories
mkdir -p "$RESULTS_DIR" "$REPORTS_DIR" "$LOGS_DIR"

echo "=========================================="
echo "HPC-ARC Benchmark Suite Automated Execution"
echo "=========================================="
echo "Configuration: $CONFIG"
echo "Measurements per task: $N_MEASUREMENTS"
echo "Confidence interval: $CONFIDENCE_INTERVAL"
echo ""

# Function to execute a single phase
execute_phase() {
    local phase=$1
    echo ""
    echo "=========================================="
    echo "Executing Phase: $phase"
    echo "=========================================="
    
    # Create phase-specific result directory
    local phase_results_dir="$RESULTS_DIR${phase}/"
    mkdir -p "$phase_results_dir"
    
    # Execute the phase with the main framework
    python3 -m core.hpc_arc_benchmark_suite \
        --config "$CONFIG" \
        --phase "$phase" \
        --measurements "$N_MEASUREMENTS" \
        --confidence "$CONFIDENCE_INTERVAL" \
        --output_dir "$phase_results_dir" \
        --verbose
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Phase $phase execution failed"
        echo "Check logs in $LOGS_DIR for details"
        exit 1
    fi
    
    echo "[OK] Phase $phase completed successfully"
}

# Function to aggregate results
aggregate_results() {
    echo ""
    echo "=========================================="
    echo "Aggregating Results Across Phases"
    echo "=========================================="
    
    python3 core/evaluation/aggregate_intelligence_scores.py \
        --input_dir "$RESULTS_DIR" \
        --output "$REPORTS_DIR/intelligence_report.json" \
        --with_validation \
        --generate_plots
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Results aggregation failed"
        exit 1
    fi
    
    echo "[OK] Results aggregation completed"
}

# Function to generate final reports
generate_reports() {
    echo ""
    echo "=========================================="
    echo "Generating Benchmark Reports"
    echo "=========================================="
    
    python3 tools/generate_reports.py \
        --input "$REPORTS_DIR/intelligence_report.json" \
        --output "$REPORTS_DIR/" \
        --formats "json,html,pdf" \
        --include_detailed_metrics
    
    if [ $? -ne 0 ]; then
        echo "WARNING: Report generation failed, continuing with existing results"
    else
        echo "[OK] Reports generated successfully"
    fi
}

# Function to display summary
display_summary() {
    echo ""
    echo "=========================================="
    echo "BENCHMARK EXECUTION COMPLETED"
    echo "=========================================="
    
    if [ -f "$REPORTS_DIR/intelligence_report.json" ]; then
        # Extract key metrics from the report
        python3 -c "
import json
with open('$REPORTS_DIR/intelligence_report.json', 'r') as f:
    report = json.load(f)
    score = report['intelligence_score']
    print(f'Overall Intelligence Score: {score[\"overall\"]:.3f}')
    print(f'Exploration Efficiency: {score[\"exploration_efficiency\"]:.3f}')
    print(f'Hypothesis Quality: {score[\"hypothesis_quality\"]:.3f}')
    print(f'Adaptation Speed: {score[\"adaptation_speed\"]:.3f}')
    print(f'Generalization Success: {score[\"generalization_success\"]:.3f}')
    print(f'Performance Tier: {score[\"tier\"][\"name\"]}')
    print(f'Tasks Completed: {report[\"completed_tasks\"]}/{report[\"total_tasks\"]}')
        "
    else
        echo "Intelligence report not found. Check execution logs."
    fi
    
    echo ""
    echo "Results directory: $RESULTS_DIR"
    echo "Reports directory: $REPORTS_DIR"
    echo "Logs directory: $LOGS_DIR"
    echo "=========================================="
}

# Main execution flow
main() {
    local phases=("explore" "hypothesize" "execute" "generalize")
    
    echo "Starting HPC-ARC benchmark execution..."
    echo "This will execute all four phases systematically."
    echo ""
    
    # Execute each phase
    for phase in "${phases[@]}"; do
        execute_phase "$phase"
    done
    
    # Aggregate results
    aggregate_results
    
    # Generate reports
    generate_reports
    
    # Display summary
    display_summary
    
    echo ""
    echo "✅ HPC-ARC Benchmark Suite execution completed successfully!"
}

# Command line argument parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --only-phase)
            phase="$2"
            execute_phase "$phase"
            display_summary
            exit 0
            ;;
        --measurements)
            N_MEASUREMENTS="$2"
            shift 2
            ;;
        --confidence)
            CONFIDENCE_INTERVAL="$2"
            shift 2
            ;;
        --skip-reports)
            SKIP_REPORTS=true
            shift
            ;;
        --help)
            echo "HPC-ARC Benchmark Suite Automated Execution"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --config PATH              Path to configuration file (default: config/benchmark_config.json)"
            echo "  --only-phase PHASE         Execute only specified phase (explore|hypothesize|execute|generalize)"
            echo "  --measurements N           Number of measurements per task (default: 5)"
            echo "  --confidence FLOAT         Confidence interval (default: 0.95)"
            echo "  --skip-reports            Skip report generation"
            echo "  --help                    Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                      # Execute complete benchmark suite"
            echo "  $0 --only-phase explore  # Execute only explore phase"
            echo "  $0 --measurements 10     # Execute with 10 measurements per task"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main execution
main