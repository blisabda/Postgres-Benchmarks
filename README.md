# Performance Analysis: Docker vs Kubernetes and Postgres v16 vs v18

A comprehensive analysis of PostgreSQL performance across different versions, resource configurations, and deployment environments. This repository contains research results comparing Docker containers and Kubernetes pods across 16 resource configurations for PostgreSQL 16 and 18.

The benchmarks measure transactions per second (TPS) under standard `pgbench` workloads, helping developers and system administrators make informed decisions about PostgreSQL deployment strategies.

## Key Findings

### PostgreSQL 16 Performance

| Aspect | Finding | Details |
|--------|---------|---------|
| Kubernetes Advantage | 15-47% performance gains | K8s consistently outperforms Docker |
| CPU Scaling | Most significant improvements with higher cores | Benefits from distributed resource management |
| Memory Impact | More pronounced with adequate allocation | Performance benefits scale with RAM |
| Best Configuration | Config 14 (4 CPUs, 2GB RAM) | 47.2% improvement in K8s vs Docker |

### PostgreSQL 18 Performance

| Aspect | Finding | Details |
|--------|---------|---------|
| Performance Parity | ±0-3% difference | Docker and Kubernetes nearly identical |
| Maturity Benefits | Significant improvements over PG16 | Overall performance enhancements |
| Resource Efficiency | Consistent across allocations | More stable performance scaling |
| Deployment Flexibility | Minimal performance impact | Choice based on operational needs |

### Version Comparison

| Aspect | Finding | Details |
|--------|---------|---------|
| PG18 vs PG16 | 40-50% improvement | Across all configurations |
| Deployment Trends | PG16 favors K8s; PG18 agnostic | Performance evolution patterns |
| Resource Utilization | Better in PG18 | Regardless of orchestration |

## Performance Visualizations

**PostgreSQL 16: Docker vs Kubernetes Performance**
![PG16 Performance Comparison](PG16/plots/performance_comparison.png)

**PostgreSQL 18: Docker vs Kubernetes Performance**
![PG18 Performance Comparison](PG18/plots/performance_comparison.png)

## Benchmark Configurations

| Config | CPU Cores | Memory | Use Case |
|--------|-----------|--------|----------|
| 1-4    | 1         | 1-8GB  | Low-resource environments |
| 5-8    | 2         | 1-8GB  | Standard web applications |
| 9-12   | 3         | 1-8GB  | High-throughput services |
| 13-16  | 4         | 1-8GB  | Enterprise workloads |

## Test Workload Details

### pgbench Benchmark Overview

This analysis uses PostgreSQL's built-in `pgbench` benchmarking tool, which simulates a simplified banking system workload based on the TPC-B benchmark specification. pgbench is the standard tool for measuring PostgreSQL performance and is included with every PostgreSQL installation.

**📚 [pgbench Documentation](https://www.postgresql.org/docs/current/pgbench.html)**

### Benchmark Configuration

**Database Schema** (Scale Factor: 10):
- **accounts table**: ~1,000,000 rows (10,000 accounts × 100 branches)
- **tellers table**: ~10,000 rows (10 tellers × 100 branches)  
- **branches table**: ~100 rows
- **history table**: Grows during benchmark execution (audit trail)

**Test Parameters**:
- **Clients**: 10 concurrent connections per test
- **Transactions per client**: 1,000 transactions each
- **Total transactions**: 10,000 per configuration
- **Transaction isolation**: Default (READ COMMITTED)
- **Connection pooling**: Direct connections (no connection pooling middleware)

### Transaction Mix (TPC-B Standard)

| Step | Operation | Description |
|------|-----------|-------------|
| 1 | Account Selection | Random account lookup (80% from "hot" accounts) |
| 2 | Balance Update | Debit/credit the selected account |
| 3 | Teller Update | Update teller's transaction counter |
| 4 | Branch Update | Update branch's transaction counter |
| 5 | History Insert | Insert audit record into history table |

**Read/Write Ratio**: Approximately 15% writes, 85% reads (realistic OLTP workload)

### Test Execution

**Initialization**:
```bash
pgbench -i -s 10 postgres  # Create schema with scale factor 10
```

**Benchmark Run**:
```bash
pgbench -c 10 -t 1000 -P 10 postgres  # 10 clients, 1000 transactions each, progress every 10 seconds
```

**Measurement**: Transactions Per Second (TPS) excluding connection time[^latency]

### Test Environment

| Component | Specification | Details |
|-----------|---------------|---------|
| Hardware | MacBook Pro M1 (Apple Silicon) | - |
| Docker Desktop | 8 CPUs, 12GB RAM allocated | - |
| Kubernetes | Local cluster via Docker Desktop | - |
| Storage | Host filesystem | No dedicated storage optimization |
| PostgreSQL Configuration | Default settings | No custom tuning applied[^method] |

## Results Analysis

### Performance Reports

| Content | Description |
|---------|-------------|
| Detailed TPS comparisons | For all configurations |
| Performance difference analysis | Between Docker and Kubernetes |
| Raw benchmark data | Original pgbench output files |
| Visual performance charts | Plots and graphs of results |

### Key Insights for Deployment

| Deployment Strategy | PostgreSQL Version | Key Points |
|---------------------|-------------------|------------|
| Choose Kubernetes | PG16 | - Significant performance advantages (15-47% TPS improvement)<br>- Better resource utilization with higher CPU allocations<br>- Recommended for production PG16 deployments |
| Flexible Deployment | PG18 | - Minimal performance difference between Docker/K8s<br>- Choose based on operational preferences<br>- Consistent performance across resource configurations |
| Resource Optimization | Both | - PG18 shows better memory efficiency[^resource]<br>- CPU scaling benefits both versions<br>- Monitor actual workload patterns for optimal sizing |


## Architectural Insights: Deployment Performance Differences

### Why Kubernetes Outperforms Docker in PG16 but Not PG18

The observed performance differences between Docker and Kubernetes deployments across PostgreSQL versions can be attributed to several architectural factors:

**PostgreSQL 16 Characteristics:**
- **Resource Scheduling Sensitivity**: PG16's performance is more dependent on precise CPU and memory allocation. Kubernetes' advanced scheduling and resource management (via kube-scheduler and resource quotas) provide superior isolation and allocation compared to Docker's simpler container runtime.
- **Multi-Core Utilization**: The significant TPS gains in Kubernetes (15-47%) correlate with higher CPU core counts, suggesting Kubernetes' pod-level resource management better handles PostgreSQL's thread-based architecture.
- **Overhead Trade-offs**: While Kubernetes adds orchestration overhead, in PG16 this is offset by better resource efficiency, especially under load.

**PostgreSQL 18 Advancements:**
- **Internal Optimizations**: PG18 includes major performance improvements including enhanced parallel query execution, improved JIT compilation, and better memory management. These optimizations reduce the impact of external orchestration inefficiencies.
- **Container-Aware Design**: PG18's architecture is more container-optimized, with better handling of cgroup limitations and resource constraints, making deployment method less critical.
- **Reduced Overhead Sensitivity**: The near-parity between Docker and Kubernetes (±0-3%) indicates PG18's internal efficiencies minimize orchestration layer differences.

### Resource Efficiency Comparisons

| Resource Type | PG 16 | PG 18 |
|---------------|----------------------|----------------------|
| Memory Utilization | Higher allocations show diminishing returns, less efficient usage | Better memory management, consistent performance scaling, improved efficiency |
| CPU Scaling | Benefits significantly from Kubernetes' distributed management (3-4 cores) | Strong scaling with reduced orchestration dependency, deployment-agnostic |
| Overall Efficiency | Performance dependent on orchestration sophistication | 40-50% improvement over PG16, independent of deployment method |

**Overall Efficiency Trends:**
- PG18 demonstrates 40-50% performance improvement over PG16, largely independent of deployment method.
- The convergence of Docker/Kubernetes performance in PG18 suggests PostgreSQL's evolution toward more self-contained optimization, reducing infrastructure dependency.


## Disclaimer

| Purpose | Description |
|---------|-------------|
| Performance Reference | Real-world PostgreSQL performance data |
| Deployment Guide | Evidence-based recommendations for Docker vs K8s |
| Version Comparison | Performance evolution across PostgreSQL versions |
| Methodology Example | Reproducible benchmarking framework |

[^stat]: Statistical significance not established due to single-run methodology per configuration; results represent point estimates only with no error bars, standard deviation, or confidence intervals.

[^latency]: Latency metrics (average transaction latency) are available in raw pgbench output but not analyzed or compared in this report.

[^method]: Tests lack details on isolation between runs, warm-up periods, or baseline validation; potential interference between configurations not assessed.

[^resource]: No system resource utilization monitoring (CPU, memory, I/O) was performed during benchmarks.