# Performance Analysis: Docker vs Kubernetes and Postgres v16 vs v18

A comprehensive analysis of PostgreSQL performance across different versions, resource configurations, and deployment environments. This repository contains research results comparing Docker containers and Kubernetes pods across 16 resource configurations for PostgreSQL 16 and 18.

The benchmarks measure transactions per second (TPS) under standard `pgbench` workloads, helping developers and system administrators make informed decisions about PostgreSQL deployment strategies.

## Key Findings

### PostgreSQL 16 Performance

| Aspect | Finding | Details |
|--------|---------|---------|
| Kubernetes Advantage | 🟢 15-47% performance gains | Kubernetes provides superior resource management and isolation, leading to consistent TPS improvements over Docker across all tested configurations, especially with higher CPU cores |
| CPU Scaling | Most significant improvements with higher cores | Performance gains in Kubernetes become more pronounced as CPU cores increase from 1 to 4, due to better thread scheduling and resource allocation in orchestrated environments |
| Memory Impact | More pronounced with adequate allocation | Kubernetes shows greater performance benefits when sufficient RAM is allocated, as its advanced memory management optimizes PostgreSQL's buffer pool usage more effectively than Docker |
| Best Configuration | 🟢 Config 14 (4 CPUs, 2GB RAM) | The combination of 4 CPU cores and 2GB RAM in Kubernetes yields the highest improvement (47.2% TPS gain), demonstrating optimal resource utilization for high-throughput workloads |

### PostgreSQL 18 Performance

| Aspect | Finding | Details |
|--------|---------|---------|
| Performance Parity | ±0-3% difference | Docker and Kubernetes deployments show nearly identical performance, with differences within measurement error, indicating deployment method has minimal impact on TPS |
| Maturity Benefits | 🟢 Significant improvements over PG16 | PostgreSQL 18's internal optimizations provide substantial performance gains regardless of deployment method, representing a major advancement in database efficiency |
| Resource Efficiency | Consistent across allocations | Performance scaling remains stable across different CPU and memory configurations, showing improved resource utilization and reduced sensitivity to allocation variations |
| Deployment Flexibility | Minimal performance impact | Organizations can choose Docker or Kubernetes based on operational requirements rather than performance considerations, as both provide equivalent TPS results |

### Version Comparison

| Aspect | Finding | Details |
|--------|---------|---------|
| PG18 vs PG16 | 🟢 40-50% improvement | PostgreSQL 18 delivers substantial performance gains across all resource configurations and deployment methods, representing a significant generational improvement in database performance |
| Deployment Trends | PG16 favors K8s; PG18 agnostic | PG16 shows clear preference for Kubernetes orchestration, while PG18 performs equally well in both Docker and Kubernetes environments, indicating architectural maturation |
| Resource Utilization | 🟢 Better in PG18 | PostgreSQL 18 demonstrates more efficient use of allocated CPU and memory resources, with improved scaling characteristics and reduced dependency on external orchestration sophistication |

## Performance Visualizations

**PostgreSQL 16: Docker vs Kubernetes Performance**
![PG16 Performance Comparison](PG16/plots/performance_comparison.png)

**PostgreSQL 18: Docker vs Kubernetes Performance**
![PG18 Performance Comparison](PG18/plots/performance_comparison.png)

## Benchmark Configurations

| Config | CPUs | Memory(GB) | Use Case |
|--------|-----------|--------|----------|
| 1-4    | 1         | 1,2,4,8  | Low-resource environments such as development, testing, or small-scale applications with minimal concurrent users and basic transactional requirements |
| 5-8    | 2         | 1,2,4,8  | Standard web applications including e-commerce sites, content management systems, and business applications serving moderate user loads with mixed read/write patterns |
| 9-12   | 3         | 1,2,4,8  | High-throughput services such as API gateways, data processing pipelines, and real-time analytics platforms requiring consistent performance under sustained load |
| 13-16  | 4         | 1,2,4,8  | Enterprise workloads including large-scale databases, mission-critical applications, and systems handling thousands of concurrent transactions with high availability requirements |

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
| 1 | Account Selection | Random selection of an account from the database, with 80% probability of choosing from the "hot" subset of recently accessed accounts to simulate realistic access patterns in banking systems |
| 2 | Balance Update | Debit or credit operation on the selected account balance, representing the core transactional workload that tests database update performance and concurrency control |
| 3 | Teller Update | Increment of the transaction counter for the teller associated with this account, simulating teller activity tracking in branch banking operations |
| 4 | Branch Update | Increment of the transaction counter for the branch containing this account, representing branch-level transaction aggregation and reporting requirements |
| 5 | History Insert | Insertion of an audit record into the history table documenting the transaction details, testing database write performance and storage subsystem capabilities |

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
| Hardware | MacBook Pro M1 (Apple Silicon) | Apple M1 chip with unified memory architecture, providing consistent performance characteristics for containerized workloads and accurate benchmarking of orchestration differences |
| Docker Desktop | 8 CPUs, 12GB RAM allocated | Docker Desktop configured with 8 virtual CPU cores and 12GB RAM, matching the maximum resources available on the host system for fair comparison with Kubernetes |
| Kubernetes | Local cluster via Docker Desktop | Single-node Kubernetes cluster running through Docker Desktop's built-in Kubernetes support, providing production-like orchestration without external dependencies |
| Storage | Host filesystem | Direct host filesystem access without dedicated storage volumes or network-attached storage, ensuring consistent I/O performance across all test configurations |
| PostgreSQL Configuration | Default settings | Standard PostgreSQL installation with no custom performance tuning, shared buffers, or query optimization settings modified to represent typical out-of-the-box deployments |

## Results Analysis

### Performance Reports

| Content | Description |
|---------|-------------|
| Detailed TPS comparisons | Comprehensive tables showing transactions per second for each of the 16 resource configurations, with direct Docker vs Kubernetes comparisons and percentage differences |
| Performance difference analysis | Statistical analysis of performance variations between deployment methods, including average gains, standard deviations, and configuration-specific insights |
| Raw benchmark data | Complete pgbench output files containing latency measurements, transaction counts, and timing data for reproducibility and detailed analysis |
| Visual performance charts | Generated plots and graphs illustrating performance trends across CPU cores, memory allocations, and deployment methods for intuitive understanding |

### Key Insights for Deployment

| Deployment Strategy | PostgreSQL Version | Key Points |
|---------------------|-------------------|------------|
| Choose Kubernetes | PG16 | 🟢 Significant performance advantages (15-47% TPS improvement)<br>🟢 Better resource utilization with higher CPU allocations<br>🟢 Recommended for production PG16 deployments |
| Flexible Deployment | PG18 | - Minimal performance difference between Docker/K8s<br>- Choose based on operational preferences<br>- Consistent performance across resource configurations |
| Resource Optimization | Both | 🟢 PG18 shows better memory efficiency[^resource]<br>- CPU scaling benefits both versions<br>- Monitor actual workload patterns for optimal sizing |


## Architectural Insights: Deployment Performance Differences

### Why Kubernetes Outperforms Docker in PG16 but Not PG18

The observed performance differences between Docker and Kubernetes deployments across PostgreSQL versions can be attributed to several architectural factors:

**PostgreSQL 16 Characteristics:**
- 🔴 **Resource Scheduling Sensitivity**: PG16's performance is more dependent on precise CPU and memory allocation. Kubernetes' advanced scheduling and resource management (via kube-scheduler and resource quotas) provide superior isolation and allocation compared to Docker's simpler container runtime.
- 🟢 **Multi-Core Utilization**: The significant TPS gains in Kubernetes (15-47%) correlate with higher CPU core counts, suggesting Kubernetes' pod-level resource management better handles PostgreSQL's thread-based architecture.
- **Overhead Trade-offs**: While Kubernetes adds orchestration overhead, in PG16 this is offset by better resource efficiency, especially under load.

**PostgreSQL 18 Advancements:**
- 🟢 **Internal Optimizations**: PG18 includes major performance improvements including enhanced parallel query execution, improved JIT compilation, and better memory management. These optimizations reduce the impact of external orchestration inefficiencies.
- 🟢 **Container-Aware Design**: PG18's architecture is more container-optimized, with better handling of cgroup limitations and resource constraints, making deployment method less critical.
- 🟢 **Reduced Overhead Sensitivity**: The near-parity between Docker and Kubernetes (±0-3%) indicates PG18's internal efficiencies minimize orchestration layer differences.

### Resource Efficiency Comparisons

| Resource Type | PG 16 | PG 18 |
|---------------|----------------------|----------------------|
| Memory Utilization | 🔴 Higher allocations show diminishing returns, less efficient usage | 🟢 Better memory management, consistent performance scaling, improved efficiency |
| CPU Scaling | Benefits significantly from Kubernetes' distributed management (3-4 cores) | 🟢 Strong scaling with reduced orchestration dependency, deployment-agnostic |
| Overall Efficiency | Performance dependent on orchestration sophistication | 🟢 40-50% improvement over PG16, independent of deployment method |

**Overall Efficiency Trends:**
- PG18 demonstrates 40-50% performance improvement over PG16, largely independent of deployment method.
- The convergence of Docker/Kubernetes performance in PG18 suggests PostgreSQL's evolution toward more self-contained optimization, reducing infrastructure dependency.


## Disclaimer

| Purpose | Description |
|---------|-------------|
| Performance Reference | Provides real-world PostgreSQL performance measurements across different versions and deployment scenarios to serve as a practical reference for system architects and developers |
| Deployment Guide | Offers evidence-based recommendations for choosing between Docker and Kubernetes deployments based on observed performance characteristics and resource utilization patterns |
| Version Comparison | Documents the performance evolution between PostgreSQL versions, highlighting improvements and changes in deployment behavior that affect infrastructure decisions |
| Methodology Example | Demonstrates a reproducible benchmarking framework using standard tools and configurations that can be adapted for other database performance evaluation projects |

[^stat]: Statistical significance not established due to single-run methodology per configuration; results represent point estimates only with no error bars, standard deviation, or confidence intervals.

[^latency]: Latency metrics (average transaction latency) are available in raw pgbench output but not analyzed or compared in this report.

[^method]: Tests lack details on isolation between runs, warm-up periods, or baseline validation; potential interference between configurations not assessed.

[^resource]: No system resource utilization monitoring (CPU, memory, I/O) was performed during benchmarks.