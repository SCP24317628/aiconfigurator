# MiniMax-M2.5 on S5000 HYBRID Simulation Summary

> This result is a HYBRID simulation based on `src/aiconfigurator/systems/s5000.yaml` and estimate-only fallback. It is not a measured S5000 SILICON result because no real S5000 operator performance database exists under `src/aiconfigurator/systems/data/s5000/` yet.

## Input

| Item | Value |
|---|---:|
| Model | MiniMaxAI/MiniMax-M2.5 |
| System | s5000 |
| Total GPUs | 16 |
| ISL | 4000 |
| OSL | 1000 |
| Database mode | HYBRID |
| Backend selection | auto |
| TTFT limit | < 2000 ms |
| TPOT limit | < 35 ms |

## SGLang and vLLM Results

| Backend | Deployment scenario | Machine count | GPU layout | Parallel strategy | Batch size | Concurrency | TTFT limit | TPOT limit | Simulated TTFT | Simulated TPOT | Request latency | Request rate | Total throughput | Per-GPU throughput | Per-user throughput | SLA status |
|---|---|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| sglang | agg | 2 | 16 GPUs = 2 replicas x 8 GPUs | tp8 pp1 dp1 etp1 ep8 | 20 | 40 (=20x2) | 2000 ms | 35 ms | 281.10 ms | 30.18 ms | 30436.20 ms | 1.31 req/s | 1312.16 tokens/s | 82.01 tokens/s/gpu | 33.13 tokens/s/user | PASS |
| vllm | agg | 2 | 16 GPUs = 2 replicas x 8 GPUs | tp8 pp1 dp1 etp1 ep8 | 20 | 40 (=20x2) | 2000 ms | 35 ms | 294.45 ms | 30.22 ms | 30489.40 ms | 1.31 req/s | 1309.76 tokens/s | 81.86 tokens/s/gpu | 33.09 tokens/s/user | PASS |
| sglang | disagg | 2 | 16 GPUs = 1 replica x 16 GPUs | prefill: 1 worker x 4 GPUs; decode: 3 workers x 4 GPUs | prefill bs=1; decode bs=10 | 30 (=30x1) | 2000 ms | 35 ms | 259.37 ms | 32.24 ms | 32472.12 ms | 0.86 req/s | 855.68 tokens/s | 53.48 tokens/s/gpu | 31.01 tokens/s/user | PASS |
| vllm | disagg | 2 | 16 GPUs = 1 replica x 16 GPUs | prefill: tp1 pp1 dp4 etp1 ep4; decode: tp4 pp1 dp1 etp1 ep4 | prefill bs=1; decode bs=10 | 30 (=30x1) | 2000 ms | 35 ms | 494.77 ms | 32.25 ms | 32707.52 ms | 0.86 req/s | 855.68 tokens/s | 53.48 tokens/s/gpu | 31.01 tokens/s/user | PASS |

## Notes

- Machine count assumes `s5000.yaml` uses 8 GPUs per node, so 16 total GPUs means 2 machines/nodes.
- `Total throughput` is calculated as `Per-GPU throughput x 16 GPUs` from the AIC output.
- For vLLM agg, TPOT is derived from `(request_latency - TTFT) / (OSL - 1)`: `(30489.40 - 294.45) / 999 ~= 30.22 ms`.
- For disagg rows, the table uses the best row per backend by `tokens/s/gpu` from the AIC top-20 output.
- The current best among SGLang/vLLM is SGLang agg at about `1312.16 tokens/s`, very close to vLLM agg at about `1309.76 tokens/s`.
