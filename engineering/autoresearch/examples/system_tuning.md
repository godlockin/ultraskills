# Example: System Configuration Optimization

Optimize nginx configuration for web server throughput.

## Task Configuration

```yaml
task:
  name: "nginx_performance_tuning"
  description: "Optimize nginx throughput while maintaining low latency"
  created_at: "2026-04-07T00:00:00Z"

inner:
  type: "config_tuning"
  files:
    - "/etc/nginx/nginx.conf"
    - "/etc/nginx/sites-available/myapp.conf"
  execution:
    command: "sudo systemctl reload nginx && ./benchmark.sh > run.log 2>&1"
    timeout: 120  # 2 minutes for benchmark
    working_dir: "/home/user/nginx-bench"

  evaluation:
    primary_metric:
      name: "throughput"
      pattern: "^Requests/sec:\\s+([0-9.]+)"
      objective: "maximize"

    auxiliary_metrics:
      - name: "latency_p99"
        pattern: "^99th percentile:\\s+([0-9.]+)ms"
        objective: "minimize"
      - name: "error_rate"
        pattern: "^Error rate:\\s+([0-9.]+)%"
        objective: "minimize"

    constraints:
      hard:
        - metric: "error_rate"
          condition: "< 0.1"  # Must be under 0.1%
        - metric: "latency_p99"
          condition: "< 100"  # p99 latency < 100ms

    success_criteria:
      type: "threshold"
      primary_metric: "> 10000"  # 10k req/sec
      max_iterations: 50

outer:
  strategy: "config_snapshot"  # No git needed

  decision:
    keep_threshold: 0.05  # 5% improvement
    auxiliary_importance: 0.3

  limits:
    max_iterations: 50
    max_consecutive_failures: 3

  hypothesis_generation:
    mode: "guided"
    search_space:
      nginx_params:
        worker_processes: [4, 8, 16, "auto"]
        worker_connections: [1024, 2048, 4096]
        keepalive_timeout: [30, 60, 120]
        keepalive_requests: [100, 500, 1000]
        sendfile: ["on", "off"]
        tcp_nopush: ["on", "off"]
        tcp_nodelay: ["on", "off"]
```

## Usage

```bash
cd /home/user/nginx-bench

# Make sure benchmark.sh exists and outputs metrics
./benchmark.sh  # Test it first

# Start Claude Code
claude

# Then say:
"Optimize nginx configuration for maximum throughput while keeping p99 latency under 100ms"
```

## Config Snapshot Strategy

Unlike git_based, this uses snapshots:

```
1. Save current nginx.conf → .autoresearch/snapshots/config_001.tar.gz
2. Modify nginx.conf (e.g., "worker_processes: 8 → 16")
3. Reload nginx
4. Run benchmark
5. If throughput improves → delete snapshot, keep new config
6. If throughput worse → restore from snapshot
```

No git commits, just file copies. Perfect for system configs!

## Expected Hypotheses

```
A) Increase worker_processes from auto to 16
   Expected gain: +15% throughput (based on CPU cores)
   Risk: Low
   Rationale: You have 16 cores, should use them all

B) Increase worker_connections to 4096
   Expected gain: +10% throughput
   Risk: Medium (may hit ulimit)
   Rationale: Current 1024 may be bottleneck under load

C) Enable tcp_nopush and tcp_nodelay
   Expected gain: +5% throughput, -10% latency
   Risk: Low
   Rationale: Common optimization for serving static files

Recommendation: Try A first - clear CPU headroom
```

## Benchmark Script Example

`benchmark.sh`:
```bash
#!/bin/bash
# Simple benchmark using wrk

wrk -t 8 -c 200 -d 30s http://localhost/ | tee /tmp/wrk_output.txt

# Parse and format output
grep "Requests/sec" /tmp/wrk_output.txt
grep "99%" /tmp/wrk_output.txt | awk '{print "99th percentile: " $2}'
grep "Non-2xx" /tmp/wrk_output.txt | awk '{print "Error rate: " ($4/$2)*100 "%"}'
```

## Safety Features

- Hard constraints prevent bad configs (error_rate < 0.1%)
- Snapshots allow instant rollback
- Max consecutive failures = 3 (stops if nginx keeps breaking)

## Tips

- Test your benchmark script first
- Ensure sudo permissions for nginx reload
- Monitor system resources during optimization
- Consider time-of-day effects (run during low traffic)
