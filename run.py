import argparse
import pandas as pd
import numpy as np
import yaml
import logging
import json
import time
import sys
import os

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def write_metrics(output_path, data):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    setup_logging(args.log_file)
    start_time = time.time()

    try:
        logging.info("Job started")

        # ---- Load config ----
        if not os.path.exists(args.config):
            raise Exception("Config file not found")

        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise Exception(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: {config}")

        # ---- Load dataset ----
        if not os.path.exists(args.input):
            raise Exception("Input file not found")

        df = pd.read_csv(args.input, delimiter=",", engine="python")
        

        if df.empty:
            raise Exception("CSV is empty")

        df.columns = df.columns.str.strip().str.lower()

        if "close" not in df.columns:
            raise Exception("Missing 'close' column")

        logging.info(f"Rows loaded: {len(df)}")

        # ---- Rolling mean ----
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # ---- Signal ----
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        # Drop NaN rows from rolling
        df = df.dropna()

        rows_processed = len(df)
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        write_metrics(args.output, metrics)

        print(json.dumps(metrics, indent=2))
        sys.exit(0)

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, metrics)
        print(json.dumps(metrics, indent=2))

        sys.exit(1)


if __name__ == "__main__":
    main()