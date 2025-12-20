# PostgreSQL 18 Performance Research: Docker vs Kubernetes

This project benchmarks PostgreSQL 18 performance across different resource configurations in both Docker containers and Kubernetes pods.

## Setup

### Docker Mode
1. Ensure Docker is running.
2. Install PostgreSQL client tools (for pgbench): `brew install postgresql` (on macOS)
3. Create a Docker volume for persistent data: `docker volume create pg-data`

## Kubernetes Setup

The `k8s/` directory contains static resources (PVC, ConfigMap, Service). Deployment YAML files are **generated dynamically** at runtime with filenames like `pg-deployment-{cpu}-{memory}.yaml` based on the resource configurations defined in the script.

## Configurations

Resource values are centrally managed in the `run_tests.sh` script. The deployment YAML files use placeholders that are dynamically replaced at runtime.

| Config | Docker CPU | Docker RAM | K8s CPU | K8s RAM |
|--------|------------|------------|---------|---------|
| 1 | 1.0 | 1g | 1000m | 1Gi |
| 2 | 1.0 | 2g | 1000m | 2Gi |
| 3 | 1.0 | 4g | 1000m | 4Gi |
| 4 | 1.0 | 8g | 1000m | 8Gi |
| 5 | 2.0 | 1g | 2000m | 1Gi |
| 6 | 2.0 | 2g | 2000m | 2Gi |
| 7 | 2.0 | 4g | 2000m | 4Gi |
| 8 | 2.0 | 8g | 2000m | 8Gi |
| 9 | 3.0 | 1g | 3000m | 1Gi |
| 10 | 3.0 | 2g | 3000m | 2Gi |
| 11 | 3.0 | 4g | 3000m | 4Gi |
| 12 | 3.0 | 8g | 3000m | 8Gi |
| 13 | 4.0 | 1g | 4000m | 1Gi |
| 14 | 4.0 | 2g | 4000m | 2Gi |
| 15 | 4.0 | 4g | 4000m | 4Gi |
| 16 | 4.0 | 8g | 4000m | 8Gi |

## Fair Performance Comparison

**Important**: This benchmark runs pgbench **inside** the containers/pods to eliminate network variables and measure pure PostgreSQL performance differences between Docker and Kubernetes environments.

- **Docker**: pgbench runs inside the PostgreSQL container
- **Kubernetes**: pgbench runs inside the PostgreSQL pod
- **Result**: Direct comparison of runtime performance without network overhead differences

## Running Tests

### Automated Script

Use the provided script to run tests in either Docker or Kubernetes mode:

```bash
# Run all configurations in Docker mode
./run_tests.sh docker

# Run all configurations in Kubernetes mode
./run_tests.sh k8s

# Run specific configuration in Docker mode
./run_tests.sh docker 4

# Run specific configuration in Kubernetes mode
./run_tests.sh k8s 4

# Run both modes for a specific configuration
./run_tests.sh 4

# Run all configurations in both modes (comprehensive test)
./run_tests.sh
```

Where `<config_number>` is 1-16 corresponding to the configurations listed above.

It will also run the visualization script to generate performance charts and analysis:

```bash
python visualize_results.py
```

This will create:
- Performance plots in the `plots/` directory
- A comprehensive analysis report in `PERFORMANCE_REPORT.md`

The analysis includes charts showing how PostgreSQL TPS (transactions per second) scales with CPU and memory resources across different configurations using pgbench's TPC-B workload.