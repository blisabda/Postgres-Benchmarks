#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np

# Configuration details
CONFIGS = {
    1: {"cpu": "1.0", "ram": "1g", "cpu_val": 1.0, "ram_val": 1.0},
    2: {"cpu": "1.0", "ram": "2g", "cpu_val": 1.0, "ram_val": 2.0},
    3: {"cpu": "1.0", "ram": "4g", "cpu_val": 1.0, "ram_val": 4.0},
    4: {"cpu": "1.0", "ram": "8g", "cpu_val": 1.0, "ram_val": 8.0},
    5: {"cpu": "2.0", "ram": "1g", "cpu_val": 2.0, "ram_val": 1.0},
    6: {"cpu": "2.0", "ram": "2g", "cpu_val": 2.0, "ram_val": 2.0},
    7: {"cpu": "2.0", "ram": "4g", "cpu_val": 2.0, "ram_val": 4.0},
    8: {"cpu": "2.0", "ram": "8g", "cpu_val": 2.0, "ram_val": 8.0},
    9: {"cpu": "3.0", "ram": "1g", "cpu_val": 3.0, "ram_val": 1.0},
    10: {"cpu": "3.0", "ram": "2g", "cpu_val": 3.0, "ram_val": 2.0},
    11: {"cpu": "3.0", "ram": "4g", "cpu_val": 3.0, "ram_val": 4.0},
    12: {"cpu": "3.0", "ram": "8g", "cpu_val": 3.0, "ram_val": 8.0},
    13: {"cpu": "4.0", "ram": "1g", "cpu_val": 4.0, "ram_val": 1.0},
    14: {"cpu": "4.0", "ram": "2g", "cpu_val": 4.0, "ram_val": 2.0},
    15: {"cpu": "4.0", "ram": "4g", "cpu_val": 4.0, "ram_val": 4.0},
    16: {"cpu": "4.0", "ram": "8g", "cpu_val": 4.0, "ram_val": 8.0}
}

def parse_pgbench_tps(content):
    """Parse TPS from pgbench output"""
    lines = content.split('\n')
    for line in lines:
        if 'tps =' in line and '(without initial connection time)' in line:
            # Extract the number before the parentheses
            parts = line.split('=')
            if len(parts) > 1:
                tps_part = parts[1].strip().split()[0]
                try:
                    return float(tps_part)
                except ValueError:
                    return 0.0
    return 0.0

def load_version_results(version_path):
    """Load results for a specific PostgreSQL version"""
    results = {'docker': {}, 'k8s': {}}
    
    # Load Docker results
    docker_files = glob.glob(os.path.join(version_path, "results", "docker_config_*.txt"))
    for file_path in docker_files:
        config_num = int(file_path.split('_')[-1].split('.')[0])
        with open(file_path, 'r') as f:
            content = f.read()
            tps = parse_pgbench_tps(content)
            results['docker'][config_num] = tps
    
    # Load Kubernetes results
    k8s_files = glob.glob(os.path.join(version_path, "results", "k8s_config_*.txt"))
    for file_path in k8s_files:
        config_num = int(file_path.split('_')[-1].split('.')[0])
        with open(file_path, 'r') as f:
            content = f.read()
            tps = parse_pgbench_tps(content)
            results['k8s'][config_num] = tps
    
    return results

def create_comparison_plots(pg16_results, pg18_results, output_dir="plots"):
    """Create comparison plots between PG16 and PG18"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get common configs
    pg16_docker_configs = set(pg16_results['docker'].keys())
    pg16_k8s_configs = set(pg16_results['k8s'].keys())
    pg18_docker_configs = set(pg18_results['docker'].keys())
    pg18_k8s_configs = set(pg18_results['k8s'].keys())
    
    docker_common = sorted(pg16_docker_configs & pg18_docker_configs)
    k8s_common = sorted(pg16_k8s_configs & pg18_k8s_configs)
    all_common = sorted(docker_common + k8s_common)
    
    if not all_common:
        print("No common configurations found between versions")
        return
    
    # Calculate improvements
    docker_improvements = []
    k8s_improvements = []
    docker_pg16_tps = []
    docker_pg18_tps = []
    k8s_pg16_tps = []
    k8s_pg18_tps = []
    
    for config in docker_common:
        pg16_tps = pg16_results['docker'][config]
        pg18_tps = pg18_results['docker'][config]
        if pg16_tps > 0:
            improvement = ((pg18_tps - pg16_tps) / pg16_tps) * 100
        else:
            improvement = 0
        docker_improvements.append(improvement)
        docker_pg16_tps.append(pg16_tps)
        docker_pg18_tps.append(pg18_tps)
    
    for config in k8s_common:
        pg16_tps = pg16_results['k8s'][config]
        pg18_tps = pg18_results['k8s'][config]
        if pg16_tps > 0:
            improvement = ((pg18_tps - pg16_tps) / pg16_tps) * 100
        else:
            improvement = 0
        k8s_improvements.append(improvement)
        k8s_pg16_tps.append(pg16_tps)
        k8s_pg18_tps.append(pg18_tps)
    
    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('PostgreSQL 16 vs 18 Performance Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: TPS comparison for Docker
    ax1 = axes[0, 0]
    x_docker = np.arange(len(docker_common))
    width = 0.35
    ax1.bar(x_docker - width/2, docker_pg16_tps, width, label='PG16', alpha=0.8, color='skyblue')
    ax1.bar(x_docker + width/2, docker_pg18_tps, width, label='PG18', alpha=0.8, color='lightcoral')
    ax1.set_xlabel('Configuration')
    ax1.set_ylabel('Transactions per Second (TPS)')
    ax1.set_title('Docker Deployment: TPS by Configuration')
    ax1.set_xticks(x_docker)
    ax1.set_xticklabels([f'Config {c}' for c in docker_common], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: TPS comparison for Kubernetes
    ax2 = axes[0, 1]
    x_k8s = np.arange(len(k8s_common))
    ax2.bar(x_k8s - width/2, k8s_pg16_tps, width, label='PG16', alpha=0.8, color='skyblue')
    ax2.bar(x_k8s + width/2, k8s_pg18_tps, width, label='PG18', alpha=0.8, color='lightcoral')
    ax2.set_xlabel('Configuration')
    ax2.set_ylabel('Transactions per Second (TPS)')
    ax2.set_title('Kubernetes Deployment: TPS by Configuration')
    ax2.set_xticks(x_k8s)
    ax2.set_xticklabels([f'Config {c}' for c in k8s_common], rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Performance improvement percentage for Docker
    ax3 = axes[1, 0]
    ax3.bar(docker_common, docker_improvements, color='green', alpha=0.7)
    ax3.set_xlabel('Configuration')
    ax3.set_ylabel('Performance Improvement (%)')
    ax3.set_title('Docker: PG18 vs PG16 Improvement')
    ax3.set_xticks(docker_common)
    ax3.set_xticklabels([f'Config {c}' for c in docker_common], rotation=45)
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Plot 4: Performance improvement percentage for Kubernetes
    ax4 = axes[1, 1]
    ax4.bar(k8s_common, k8s_improvements, color='green', alpha=0.7)
    ax4.set_xlabel('Configuration')
    ax4.set_ylabel('Performance Improvement (%)')
    ax4.set_title('Kubernetes: PG18 vs PG16 Improvement')
    ax4.set_xticks(k8s_common)
    ax4.set_xticklabels([f'Config {c}' for c in k8s_common], rotation=45)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'version_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create summary statistics
    docker_avg_improvement = np.mean(docker_improvements)
    k8s_avg_improvement = np.mean(k8s_improvements)
    docker_max_improvement = np.max(docker_improvements)
    k8s_max_improvement = np.max(k8s_improvements)
    
    print(".1f")
    print(".1f")
    print(".1f")
    print(".1f")
    
    return {
        'docker_avg_improvement': docker_avg_improvement,
        'k8s_avg_improvement': k8s_avg_improvement,
        'docker_max_improvement': docker_max_improvement,
        'k8s_max_improvement': k8s_max_improvement
    }

def main():
    """Main function to run the comparison"""
    print("Loading PostgreSQL 16 results...")
    pg16_results = load_version_results("PG16")
    
    print("Loading PostgreSQL 18 results...")
    pg18_results = load_version_results("PG18")
    
    print("Creating comparison plots...")
    stats = create_comparison_plots(pg16_results, pg18_results)
    
    print("Comparison complete! Check the plots/version_comparison.png file.")

if __name__ == "__main__":
    main()