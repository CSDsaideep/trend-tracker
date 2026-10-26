# Trend Tracker - Real-Time Product Popularity Analysis Pipeline

## Pipeline Core Architecture
This repository implements an end-to-end data analytics streaming pipeline engineered to identify and predict real-time trending products across e-commerce ecosystems. 

The analytical engine monitors sliding transactional time windows, computes spatial-temporal transaction density updates, and applies a **Z-Score anomaly detection metric** over the current volume distributions to isolate viral consumption spikes instantly.

## Core Capabilities Developed
- **Data Engineering Layer:** Includes a pipeline script to impute missing transactional values and clean input streams.
- **Statistical Trend Indexing:** Utilizes rolling standard deviations rather than fixed counts to isolate true product demand volatility.
- **Enterprise Scalability:** Built using vectorized operational states, laying structural framework paths for future Kafka or Spark expansions.

## Execution Sequence
1. Clone the repository: `git clone https://github.com`
2. Install standard framework components: `pip install pandas numpy`
3. Generate data logs: `python generate_data.py`
4. Run analytical validation: `python trend_tracker.py`
