# PostgreSQL 18 Performance Analysis Report: Docker vs Kubernetes

**Generated on:** 2025-12-21 11:33:19

## System Environment

### Hardware & OS
- **Operating System**: Darwin 24.6.0
- **Architecture**: arm64

### Container Runtimes
- **Docker Version**: Docker version 29.1.3, build f52814d
- **Docker CPUs**: 8
- **Docker Memory**: 11.67GiB
- **Docker Runtime**: runc
- **Kubernetes Client**: Not available

### Kubernetes Cluster
```
docker-desktop   Ready    control-plane   18h   v1.34.1   192.168.65.3   <none>        Docker Desktop   6.12.54-linuxkit   docker://29.1.3

## Overview

This report compares PostgreSQL 18 performance between Docker containers and Kubernetes pods across different resource configurations.

## Configurations Tested

| Config | Docker CPU | Docker RAM | K8s CPU | K8s RAM |
|--------|------------|------------|---------|---------|
| 1 | 1.0 | 1g | 1.0 | 1g |
| 2 | 1.0 | 2g | 1.0 | 2g |
| 3 | 1.0 | 4g | 1.0 | 4g |
| 4 | 1.0 | 8g | 1.0 | 8g |
| 5 | 2.0 | 1g | 2.0 | 1g |
| 6 | 2.0 | 2g | 2.0 | 2g |
| 7 | 2.0 | 4g | 2.0 | 4g |
| 8 | 2.0 | 8g | 2.0 | 8g |
| 9 | 3.0 | 1g | 3.0 | 1g |
| 10 | 3.0 | 2g | 3.0 | 2g |
| 11 | 3.0 | 4g | 3.0 | 4g |
| 12 | 3.0 | 8g | 3.0 | 8g |
| 13 | 4.0 | 1g | 4.0 | 1g |
| 14 | 4.0 | 2g | 4.0 | 2g |
| 15 | 4.0 | 4g | 4.0 | 4g |
| 16 | 4.0 | 8g | 4.0 | 8g |

## Performance Analysis

### Key Findings

- **Config 1**: Docker TPS: 1753.65, K8s TPS: 1725.63, Difference: -28.02 TPS (-1.6%)
- **Config 2**: Docker TPS: 1801.82, K8s TPS: 1774.55, Difference: -27.27 TPS (-1.5%)
- **Config 3**: Docker TPS: 1743.57, K8s TPS: 1737.98, Difference: -5.59 TPS (-0.3%)
- **Config 4**: Docker TPS: 1782.88, K8s TPS: 1766.46, Difference: -16.42 TPS (-0.9%)
- **Config 5**: Docker TPS: 4161.81, K8s TPS: 4188.51, Difference: +26.70 TPS (+0.6%)
- **Config 6**: Docker TPS: 4102.12, K8s TPS: 4128.07, Difference: +25.94 TPS (+0.6%)
- **Config 7**: Docker TPS: 4111.70, K8s TPS: 4159.88, Difference: +48.18 TPS (+1.2%)
- **Config 8**: Docker TPS: 4201.19, K8s TPS: 4232.16, Difference: +30.97 TPS (+0.7%)
- **Config 9**: Docker TPS: 6144.20, K8s TPS: 6268.18, Difference: +123.98 TPS (+2.0%)
- **Config 10**: Docker TPS: 6246.98, K8s TPS: 6310.83, Difference: +63.85 TPS (+1.0%)
- **Config 11**: Docker TPS: 6349.90, K8s TPS: 6298.42, Difference: -51.49 TPS (-0.8%)
- **Config 12**: Docker TPS: 6126.60, K8s TPS: 6332.34, Difference: +205.74 TPS (+3.4%)
- **Config 13**: Docker TPS: 7243.82, K8s TPS: 7460.25, Difference: +216.43 TPS (+3.0%)
- **Config 14**: Docker TPS: 7843.04, K8s TPS: 7855.05, Difference: +12.01 TPS (+0.2%)
- **Config 15**: Docker TPS: 7349.74, K8s TPS: 7845.41, Difference: +495.67 TPS (+6.7%)
- **Config 16**: Docker TPS: 7827.31, K8s TPS: 7825.52, Difference: -1.79 TPS (-0.0%)

## Performance Charts

![Performance Comparison](plots/performance_comparison.png)


## Raw Data

### Config 1 (1.0, 1g)

#### Docker

```
operation  time_seconds
      tps   1753.650355
```

#### Kubernetes

```
operation  time_seconds
      tps   1725.632686
```

### Config 2 (1.0, 2g)

#### Docker

```
operation  time_seconds
      tps   1801.820956
```

#### Kubernetes

```
operation  time_seconds
      tps   1774.546053
```

### Config 3 (1.0, 4g)

#### Docker

```
operation  time_seconds
      tps   1743.573667
```

#### Kubernetes

```
operation  time_seconds
      tps   1737.984574
```

### Config 4 (1.0, 8g)

#### Docker

```
operation  time_seconds
      tps    1782.88364
```

#### Kubernetes

```
operation  time_seconds
      tps   1766.462057
```

### Config 5 (2.0, 1g)

#### Docker

```
operation  time_seconds
      tps   4161.809488
```

#### Kubernetes

```
operation  time_seconds
      tps   4188.509745
```

### Config 6 (2.0, 2g)

#### Docker

```
operation  time_seconds
      tps    4102.12486
```

#### Kubernetes

```
operation  time_seconds
      tps   4128.069219
```

### Config 7 (2.0, 4g)

#### Docker

```
operation  time_seconds
      tps   4111.698399
```

#### Kubernetes

```
operation  time_seconds
      tps    4159.87567
```

### Config 8 (2.0, 8g)

#### Docker

```
operation  time_seconds
      tps    4201.18818
```

#### Kubernetes

```
operation  time_seconds
      tps   4232.162915
```

### Config 9 (3.0, 1g)

#### Docker

```
operation  time_seconds
      tps   6144.200704
```

#### Kubernetes

```
operation  time_seconds
      tps   6268.177715
```

### Config 10 (3.0, 2g)

#### Docker

```
operation  time_seconds
      tps   6246.978024
```

#### Kubernetes

```
operation  time_seconds
      tps   6310.832481
```

### Config 11 (3.0, 4g)

#### Docker

```
operation  time_seconds
      tps   6349.903831
```

#### Kubernetes

```
operation  time_seconds
      tps    6298.41513
```

### Config 12 (3.0, 8g)

#### Docker

```
operation  time_seconds
      tps   6126.602566
```

#### Kubernetes

```
operation  time_seconds
      tps   6332.344221
```

### Config 13 (4.0, 1g)

#### Docker

```
operation  time_seconds
      tps   7243.820478
```

#### Kubernetes

```
operation  time_seconds
      tps   7460.253634
```

### Config 14 (4.0, 2g)

#### Docker

```
operation  time_seconds
      tps   7843.038832
```

#### Kubernetes

```
operation  time_seconds
      tps   7855.046121
```

### Config 15 (4.0, 4g)

#### Docker

```
operation  time_seconds
      tps   7349.741877
```

#### Kubernetes

```
operation  time_seconds
      tps   7845.413963
```

### Config 16 (4.0, 8g)

#### Docker

```
operation  time_seconds
      tps    7827.31074
```

#### Kubernetes

```
operation  time_seconds
      tps   7825.516034
```

