#  MLOps Batch Pipeline

A minimal MLOps-style batch job that processes OHLCV data, generates trading signals, and outputs structured metrics with full logging and reproducibility.

---

## Features

- Config-driven execution using YAML  
- Deterministic runs using seed  
- Rolling mean-based signal generation  
- Structured metrics output (JSON)  
- Detailed logging for observability  
- Robust error handling  
- Dockerized for reproducibility  

---

## How It Works

1. Load configuration (seed, window, version)  
2. Read OHLCV dataset (`data.csv`)  
3. Compute rolling mean on `close` prices  
4. Generate signal:
   - `1` → close > rolling mean  
   - `0` → otherwise  
5. Output metrics and logs  

---

##  Run Locally

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log