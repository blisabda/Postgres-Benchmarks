#!/bin/bash
set -e

# run_tests.sh - Run PostgreSQL performance tests
# Usage: ./run_tests.sh [mode] [config_number]
# Modes: docker, k8s (optional - if omitted, runs both modes)
# Config: 1-16 (optional - if omitted, runs all configurations)
# Configurations:
# 1-4: 1 CPU with 1GB, 2GB, 4GB, 8GB memory
# 5-8: 2 CPU with 1GB, 2GB, 4GB, 8GB memory
# 9-12: 3 CPU with 1GB, 2GB, 4GB, 8GB memory
# 13-16: 4 CPU with 1GB, 2GB, 4GB, 8GB memory

MODE=""
CONFIGS=""
CONFIG=""

# Parse arguments
if [ $# -eq 0 ]; then
    # Run both modes with all configurations
    MODES="docker k8s"
    CONFIGS="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"
    echo "Running all configurations in both docker and k8s modes: $CONFIGS"
elif [ $# -eq 1 ]; then
    if [[ "$1" == "docker" || "$1" == "k8s" ]]; then
        # Run specific mode with all configurations
        MODES="$1"
        CONFIGS="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16"
        echo "Running all configurations in $1 mode: $CONFIGS"
    elif [[ "$1" =~ ^[1-9]$|^1[0-6]$ ]]; then
        # Run both modes with specific configuration
        MODES="docker k8s"
        CONFIGS="$1"
        echo "Running configuration $1 in both docker and k8s modes"
    else
        echo "Error: Invalid argument '$1'. Must be 'docker', 'k8s', or a config number (1-16)"
        echo "Usage: $0 [mode] [config_number]"
        exit 1
    fi
elif [ $# -eq 2 ]; then
    if [[ "$1" == "docker" || "$1" == "k8s" ]]; then
        MODE="$1"
        MODES="$1"
        if [[ "$2" =~ ^[1-9]$|^1[0-6]$ ]]; then
            CONFIGS="$2"
            echo "Running configuration $2 in $1 mode"
        else
            echo "Error: Config number must be between 1 and 16"
            exit 1
        fi
    else
        echo "Error: Invalid mode '$1'. Must be 'docker' or 'k8s'"
        echo "Usage: $0 [mode] [config_number]"
        exit 1
    fi
else
    echo "Usage: $0 [mode] [config_number]"
    echo "Modes: docker, k8s (optional)"
    echo "Config: 1-4 (optional)"
    exit 1
fi

# Function to get CPU and memory for config (Docker format)
get_resources() {
    case $1 in
        1) echo "1.0 1g" ;;
        2) echo "1.0 2g" ;;
        3) echo "1.0 4g" ;;
        4) echo "1.0 8g" ;;
        5) echo "2.0 1g" ;;
        6) echo "2.0 2g" ;;
        7) echo "2.0 4g" ;;
        8) echo "2.0 8g" ;;
        9) echo "3.0 1g" ;;
        10) echo "3.0 2g" ;;
        11) echo "3.0 4g" ;;
        12) echo "3.0 8g" ;;
        13) echo "4.0 1g" ;;
        14) echo "4.0 2g" ;;
        15) echo "4.0 4g" ;;
        16) echo "4.0 8g" ;;
    esac
}

# Function to get CPU and memory for config (Kubernetes format)
get_k8s_resources() {
    case $1 in
        1) echo "1000m 1Gi" ;;
        2) echo "1000m 2Gi" ;;
        3) echo "1000m 4Gi" ;;
        4) echo "1000m 8Gi" ;;
        5) echo "2000m 1Gi" ;;
        6) echo "2000m 2Gi" ;;
        7) echo "2000m 4Gi" ;;
        8) echo "2000m 8Gi" ;;
        9) echo "3000m 1Gi" ;;
        10) echo "3000m 2Gi" ;;
        11) echo "3000m 4Gi" ;;
        12) echo "3000m 8Gi" ;;
        13) echo "4000m 1Gi" ;;
        14) echo "4000m 2Gi" ;;
        15) echo "4000m 4Gi" ;;
        16) echo "4000m 8Gi" ;;
    esac
}

# Function to generate Kubernetes deployment YAML
generate_deployment_yaml() {
    local config=$1
    local cpu=$2
    local memory=$3
    
    cat << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pg-deployment-$config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:18
        env:
        - name: POSTGRES_PASSWORD
          value: "password"
        - name: POSTGRES_DB
          value: "testdb"
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: pg-data
          mountPath: /var/lib/postgresql18
        - name: init-scripts
          mountPath: /docker-entrypoint-initdb.d
        resources:
          requests:
            cpu: "$cpu"
            memory: "$memory"
          limits:
            cpu: "$cpu"
            memory: "$memory"
      volumes:
      - name: pg-data
        persistentVolumeClaim:
          claimName: pg-data-pvc
      - name: init-scripts
        configMap:
          name: pg-init-config
EOF
}

# Docker mode functions
setup_docker() {
    # Create Docker volume if it doesn't exist
    docker volume create pg-data 2>/dev/null || true
}

run_docker_test() {
    local config=$1
    local cpus=$2
    local memory=$3

    # 1. Clean up existing container
    echo "Cleaning up existing container..."
    docker stop postgres 2>/dev/null || true
    docker rm postgres 2>/dev/null || true
    sleep 2

    # 2. Run PostgreSQL container
    echo "Starting PostgreSQL container with $cpus CPUs and $memory memory..."
    docker run -d --name postgres --cpus $cpus --memory $memory \
        -e POSTGRES_PASSWORD=password \
        -e POSTGRES_DB=testdb \
        -v pg-data:/var/lib/postgresql18 \
        -v $(pwd)/docker/init.sql:/docker-entrypoint-initdb.d/init.sql \
        -p 5432:5432 \
        postgres:18

    # 3. Wait for container to be ready
    echo "Waiting for PostgreSQL to be ready..."
    for i in {1..30}; do
        if docker exec postgres pg_isready -U postgres -d testdb >/dev/null 2>&1; then
            break
        fi
        sleep 2
    done

    if ! docker exec postgres pg_isready -U postgres -d testdb >/dev/null 2>&1; then
        echo "PostgreSQL failed to start"
        exit 1
    fi

    # 4. Initialize pgbench
    echo "Initializing pgbench database..."
    docker exec -e PGPASSWORD=password postgres pgbench -h localhost -p 5432 -U postgres -d testdb -i -s 10

    # 5. Run benchmark
    echo "Running pgbench benchmark..."
    docker exec -e PGPASSWORD=password postgres pgbench -h localhost -p 5432 -U postgres -d testdb -c 10 -t 1000 > results/${MODE}_config_$config.txt 2>/dev/null

    # 6. Clean up
    echo "Cleaning up container..."
    docker stop postgres
    docker rm postgres
}

# Kubernetes mode functions
setup_k8s() {
    # Apply common resources once at the beginning
    echo "Applying common Kubernetes resources..."
    kubectl apply -f k8s/pg-pvc.yaml -f k8s/pg-configmap.yaml -f k8s/pg-service.yaml
}

run_k8s_test() {
    local config=$1

    # Get the resource values for this config
    local k8s_resources=$(get_k8s_resources $config)
    local k8s_cpu=$(echo $k8s_resources | cut -d' ' -f1)
    local k8s_memory=$(echo $k8s_resources | cut -d' ' -f2)

    # Generate deployment YAML with CPU-memory suffix
    local deployment_name="pg-deployment-${k8s_cpu}-${k8s_memory}"
    local temp_deployment="/tmp/${deployment_name}.yaml"
    
    generate_deployment_yaml $config $k8s_cpu $k8s_memory > "$temp_deployment"

    # 1. Kill all running deployments
    echo "Cleaning up existing resources..."
    kubectl delete deployments --all 2>/dev/null || true
    sleep 5

    # 2. Deploy
    echo "Deploying configuration $config with $k8s_cpu CPU and $k8s_memory memory..."
    kubectl apply -f "$temp_deployment"

    # 3. Wait for pod ready
    echo "Waiting for pod to be ready..."
    kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

    # 4. Restart pod
    echo "Restarting pod for clean state..."
    kubectl delete pod -l app=postgres
    sleep 5

    # 6. Wait again
    echo "Waiting for pod to be ready again..."
    kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

    # 7. Initialize pgbench (run inside pod)
    echo "Initializing pgbench database..."
    kubectl exec $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- env PGPASSWORD=password pgbench -h localhost -p 5432 -U postgres -d testdb -i -s 10

    # 8. Run benchmark (run inside pod)
    echo "Running pgbench benchmark..."
    kubectl exec $(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- env PGPASSWORD=password pgbench -h localhost -p 5432 -U postgres -d testdb -c 10 -t 1000 > results/${MODE}_config_$config.txt 2>/dev/null

    # 9. Clean up deployment
    echo "Cleaning up deployment..."
    kubectl delete -f "$temp_deployment"
    rm "$temp_deployment"
}

# Setup for all modes (idempotent operations)
setup_docker
setup_k8s

# Run tests for each mode and configuration
for MODE in $MODES; do
    echo "========================================"
    echo "Starting $MODE mode tests"
    echo "========================================"

    for CONFIG in $CONFIGS; do
        echo "=========================================="
        echo "Running $MODE test for configuration $CONFIG"
        echo "=========================================="

        if [ "$MODE" = "docker" ]; then
            # Get resources for this config
            RESOURCES=$(get_resources $CONFIG)
            CPUS=$(echo $RESOURCES | cut -d' ' -f1)
            MEMORY=$(echo $RESOURCES | cut -d' ' -f2)
            run_docker_test $CONFIG $CPUS $MEMORY
        else
            run_k8s_test $CONFIG
        fi

        echo "Configuration $CONFIG completed. Results saved to results/${MODE}_config_$CONFIG.txt"
        echo ""
    done

    echo "$MODE mode tests completed!"
    echo ""
done

# 7. Generate final visualization report
echo "=========================================="
echo "Generating final performance report..."
python visualize_results.py

echo "=========================================="
echo "All tests completed! Check PERFORMANCE_REPORT.md for analysis."
echo "Modes tested: $MODES"
echo "Configurations tested: $CONFIGS"