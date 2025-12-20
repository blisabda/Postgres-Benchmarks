#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime

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

def load_results():
    """Load all config results into a dictionary organized by mode"""
    results = {'docker': {}, 'k8s': {}}
    
    # Load Docker results
    docker_files = glob.glob("results/docker_config_*.txt")
    for file_path in docker_files:
        config_num = int(file_path.split('_')[-1].split('.')[0])
        with open(file_path, 'r') as f:
            content = f.read()
            tps = parse_pgbench_tps(content)
            df = pd.DataFrame({'operation': ['tps'], 'time_seconds': [tps]})
            results['docker'][config_num] = df
    
    # Load Kubernetes results
    k8s_files = glob.glob("results/k8s_config_*.txt")
    for file_path in k8s_files:
        config_num = int(file_path.split('_')[-1].split('.')[0])
        with open(file_path, 'r') as f:
            content = f.read()
            tps = parse_pgbench_tps(content)
            df = pd.DataFrame({'operation': ['tps'], 'time_seconds': [tps]})
            results['k8s'][config_num] = df

    return results

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

def create_plots(results, output_dir="plots"):
    """Create performance plots and save them"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get common configs that exist in both modes
    docker_configs = set(results['docker'].keys())
    k8s_configs = set(results['k8s'].keys())
    common_configs = sorted(docker_configs & k8s_configs)
    
    if not common_configs:
        print("No common configurations found between Docker and Kubernetes results")
        return

    # Create subplots for comparison
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('PostgreSQL 18 Performance: Docker vs Kubernetes', fontsize=16)

    # CPU values for x-axis
    cpu_vals = [CONFIGS[c]['cpu_val'] for c in common_configs]

    # Get TPS values for both modes
    docker_tps = [results['docker'][c][results['docker'][c]['operation'] == 'tps']['time_seconds'].iloc[0] for c in common_configs]
    k8s_tps = [results['k8s'][c][results['k8s'][c]['operation'] == 'tps']['time_seconds'].iloc[0] for c in common_configs]

    # Plot 1: TPS comparison by config
    ax1 = axes[0, 0]
    x = range(len(common_configs))
    ax1.bar([i - 0.2 for i in x], docker_tps, 0.4, label='Docker', alpha=0.8)
    ax1.bar([i + 0.2 for i in x], k8s_tps, 0.4, label='Kubernetes', alpha=0.8)
    ax1.set_xlabel('Configuration')
    ax1.set_ylabel('Transactions per Second (TPS)')
    ax1.set_title('TPS by Configuration: Docker vs K8s')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'Config {c}' for c in common_configs], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: TPS vs CPU for both modes
    ax2 = axes[0, 1]
    ax2.plot(cpu_vals, docker_tps, 'o-', label='Docker', color='blue')
    ax2.plot(cpu_vals, k8s_tps, 's-', label='Kubernetes', color='red')
    ax2.set_xlabel('CPU Cores')
    ax2.set_ylabel('Transactions per Second (TPS)')
    ax2.set_title('TPS vs CPU: Docker vs K8s')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Performance difference
    ax3 = axes[1, 0]
    diff_tps = [k - d for k, d in zip(k8s_tps, docker_tps)]
    colors = ['red' if x < 0 else 'green' for x in diff_tps]
    ax3.bar(range(len(common_configs)), diff_tps, color=colors, alpha=0.7)
    ax3.set_xlabel('Configuration')
    ax3.set_ylabel('TPS Difference (K8s - Docker)')
    ax3.set_title('Performance Difference: K8s vs Docker')
    ax3.set_xticks(range(len(common_configs)))
    ax3.set_xticklabels([f'Config {c}' for c in common_configs], rotation=45)
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    # Plot 4: Percentage difference
    ax4 = axes[1, 1]
    pct_diff = [(k - d) / d * 100 if d > 0 else 0 for k, d in zip(k8s_tps, docker_tps)]
    colors = ['red' if x < 0 else 'green' for x in pct_diff]
    ax4.bar(range(len(common_configs)), pct_diff, color=colors, alpha=0.7)
    ax4.set_xlabel('Configuration')
    ax4.set_ylabel('Percentage Difference (%)')
    ax4.set_title('Relative Performance: K8s vs Docker')
    ax4.set_xticks(range(len(common_configs)))
    ax4.set_xticklabels([f'Config {c}' for c in common_configs], rotation=45)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/performance_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Comparison plot saved to {output_dir}/performance_comparison.png")

def generate_markdown(results, output_dir="plots"):
    """Generate Markdown report with analysis"""
    docker_configs = sorted(results['docker'].keys())
    k8s_configs = sorted(results['k8s'].keys())
    common_configs = sorted(set(docker_configs) & set(k8s_configs))

    md_content = f"""# PostgreSQL 18 Performance Analysis Report: Docker vs Kubernetes

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This report compares PostgreSQL 18 performance between Docker containers and Kubernetes pods across different resource configurations.

## Configurations Tested

| Config | Docker CPU | Docker RAM | K8s CPU | K8s RAM |
|--------|------------|------------|---------|---------|
"""

    for config in common_configs:
        md_content += f"| {config} | {CONFIGS[config]['cpu']} | {CONFIGS[config]['ram']} | {CONFIGS[config]['cpu']} | {CONFIGS[config]['ram']} |\n"

    md_content += "\n## Performance Analysis\n\n"

    if common_configs:
        md_content += "### Key Findings\n\n"
        
        # Calculate performance differences
        for config in common_configs:
            docker_tps = results['docker'][config][results['docker'][config]['operation'] == 'tps']['time_seconds'].iloc[0]
            k8s_tps = results['k8s'][config][results['k8s'][config]['operation'] == 'tps']['time_seconds'].iloc[0]
            diff = k8s_tps - docker_tps
            pct_diff = (diff / docker_tps) * 100 if docker_tps > 0 else 0
            
            md_content += f"- **Config {config}**: Docker TPS: {docker_tps:.2f}, K8s TPS: {k8s_tps:.2f}, "
            md_content += f"Difference: {diff:+.2f} TPS ({pct_diff:+.1f}%)\n"

    md_content += "\n## Performance Charts\n\n"
    md_content += "![Performance Comparison](plots/performance_comparison.png)\n\n"

    md_content += "\n## Raw Data\n\n"

    for config in common_configs:
        md_content += f"### Config {config} ({CONFIGS[config]['cpu']}, {CONFIGS[config]['ram']})\n\n"
        
        # Docker results
        md_content += "#### Docker\n\n"
        md_content += "```\n"
        md_content += results['docker'][config].to_string(index=False)
        md_content += "\n```\n\n"
        
        # Kubernetes results
        md_content += "#### Kubernetes\n\n"
        md_content += "```\n"
        md_content += results['k8s'][config].to_string(index=False)
        md_content += "\n```\n\n"

    # Write to file
    with open('PERFORMANCE_REPORT.md', 'w') as f:
        f.write(md_content)

    print("Markdown report generated: PERFORMANCE_REPORT.md")

def main():
    print("Loading test results...")
    results = load_results()

    docker_configs = len(results['docker'])
    k8s_configs = len(results['k8s'])
    
    if docker_configs == 0 and k8s_configs == 0:
        print("No result files found in results/ directory")
        return

    print(f"Found Docker results for {docker_configs} configurations")
    print(f"Found Kubernetes results for {k8s_configs} configurations")
    print("Generating plots...")
    create_plots(results)

    print("Generating Markdown report...")
    generate_markdown(results)

    print("Analysis complete!")

if __name__ == "__main__":
    main()