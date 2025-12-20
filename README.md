# Performance Analysis: Docker vs Kubernetes and Postgres v16 vs v18

A comprehensive analysis of PostgreSQL performance across different versions, resource configurations, and deployment environments. This repository contains research results comparing Docker containers and Kubernetes pods across 16 resource configurations for PostgreSQL 16 and 18.

The benchmarks measure transactions per second (TPS) under standard `pgbench` workloads, helping developers and system administrators make informed decisions about PostgreSQL deployment strategies.

## Key Findings

### PostgreSQL 16 Performance
- **🚀 Kubernetes Advantage**: K8s consistently outperforms Docker, with performance gains of 15-47%[^stat]
- **⚡ CPU Scaling**: Higher CPU cores show the most significant improvements in Kubernetes
- **🧠 Memory Impact**: Performance benefits are more pronounced with adequate memory allocation
- **🏆 Best Configuration**: Config 14 (4 CPUs, 2GB RAM) shows 47.2% improvement in K8s vs Docker

### PostgreSQL 18 Performance
- **⚖️ Performance Parity**: Docker and Kubernetes show nearly identical performance (±0-3% difference)[^stat]
- **🎯 Maturity Benefits**: PG18 demonstrates significant overall performance improvements over PG16
- **🔄 Resource Efficiency**: More consistent performance across different resource allocations
- **🎛️ Deployment Flexibility**: Choice between Docker/K8s has minimal performance impact

### Version Comparison
- **📊 PG18 vs PG16**: 40-50% performance improvement across all configurations[^stat]
- **📈 Deployment Trends**: PG16 favors Kubernetes; PG18 shows deployment-agnostic performance
- **💪 Resource Utilization**: PG18 better utilizes allocated resources regardless of orchestration

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

Each transaction consists of the following operations:
1. **Account Selection**: Random account lookup (80% from "hot" accounts)
2. **Balance Update**: Debit/credit the selected account
3. **Teller Update**: Update teller's transaction counter
4. **Branch Update**: Update branch's transaction counter  
5. **History Insert**: Insert audit record into history table

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

**Hardware**: MacBook Pro M1 (Apple Silicon)
- **Docker Desktop**: 8 CPUs, 12GB RAM allocated
- **Kubernetes**: Local cluster via Docker Desktop
- **Storage**: Host filesystem (no dedicated storage optimization)

**PostgreSQL Configuration**: Default settings (no custom tuning applied)[^method]

## Results Analysis

### Performance Reports
Each version directory contains a `PERFORMANCE_REPORT.md` with:
- Detailed TPS comparisons for all configurations
- Performance difference analysis
- Raw benchmark data
- Visual performance charts

### Key Insights for Deployment

**Choose Kubernetes for PG16:**
- Significant performance advantages (15-47% TPS improvement)
- Better resource utilization with higher CPU allocations
- Recommended for production PG16 deployments

**Flexible Deployment for PG18:**
- Minimal performance difference between Docker/K8s
- Choose based on operational preferences
- Consistent performance across resource configurations

**Resource Optimization:**
- PG18 shows better memory efficiency[^resource]
- CPU scaling benefits both versions
- Monitor actual workload patterns for optimal sizing

### Performance Reports
Each version directory contains a `PERFORMANCE_REPORT.md` with:
- Detailed TPS comparisons for all configurations
- Performance difference analysis
- Raw benchmark data
- Visual performance charts

### Key Insights for Deployment

**Choose Kubernetes for PG16:**
- Significant performance advantages (15-47% TPS improvement)[^version]
- Better resource utilization with higher CPU allocations
- Recommended for production PG16 deployments

**Flexible Deployment for PG18:**
- Minimal performance difference between Docker/K8s
- Choose based on operational preferences
- Consistent performance across resource configurations

**Resource Optimization:**
- PG18 shows better memory efficiency
- CPU scaling benefits both versions
- Monitor actual workload patterns for optimal sizing

## Limitations and Notes

[^stat]: Statistical significance not established due to single-run methodology per configuration; results represent point estimates only with no error bars, standard deviation, or confidence intervals.

[^latency]: Latency metrics (average transaction latency) are available in raw pgbench output but not analyzed or compared in this report.

[^method]: Tests lack details on isolation between runs, warm-up periods, or baseline validation; potential interference between configurations not assessed.

[^resource]: No system resource utilization monitoring (CPU, memory, I/O) was performed during benchmarks.

[^version]: No architectural analysis provided explaining why Kubernetes outperforms Docker in PG16 but not PG18, or deeper resource efficiency comparisons.

## Educational Value

This repository serves as:
- **Performance Reference**: Real-world PostgreSQL performance data
- **Deployment Guide**: Evidence-based recommendations for Docker vs K8s
- **Version Comparison**: Performance evolution across PostgreSQL versions
- **Methodology Example**: Reproducible benchmarking framework
