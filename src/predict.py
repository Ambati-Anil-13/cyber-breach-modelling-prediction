"""Run predictions for new network-traffic records using a trained model."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "breach_prediction_model.joblib"
REQUIRED_FEATURES = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "failed_logins",
    "connection_count",
    "unusual_port",
    "same_src_dst",
    "protocol_type",
    "service",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify rows in a CSV as normal or potentially suspicious."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a CSV containing the network-traffic feature columns.",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "reports" / "predictions.csv"),
        help="Where to save predictions (default: reports/predictions.csv).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run 'python src/train_model.py' first."
        )
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    records = pd.read_csv(input_path)
    missing = sorted(set(REQUIRED_FEATURES) - set(records.columns))
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {', '.join(missing)}")
    if records.empty:
        raise ValueError("Input CSV contains no records.")

    model = joblib.load(MODEL_PATH)
    features = records[REQUIRED_FEATURES]
    predicted_labels = model.predict(features).astype(int)
    probabilities = model.predict_proba(features)[:, 1]

    results = records.copy()
    results["predicted_label"] = predicted_labels
    results["prediction"] = [
        "Potentially suspicious" if value == 1 else "Normal" for value in predicted_labels
    ]
    results["suspicious_probability"] = probabilities.round(4)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)
    print(f"Processed {len(results)} record(s).")
    print(f"Predictions saved to: {output_path}")
    print("Note: a model prediction is a screening result, not proof of a breach.")


if __name__ == "__main__":
    main()
