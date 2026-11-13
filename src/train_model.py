"""Train and evaluate an educational cyber-traffic classification model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT: Final[Path] = Path(__file__).resolve().parents[1]
DATA_PATH: Final[Path] = ROOT / "data" / "sample_network_traffic.csv"
MODEL_PATH: Final[Path] = ROOT / "models" / "breach_prediction_model.joblib"
METRICS_PATH: Final[Path] = ROOT / "reports" / "evaluation_metrics.json"
IMPORTANCE_PATH: Final[Path] = ROOT / "reports" / "feature_importance.csv"

NUMERIC_FEATURES: Final[list[str]] = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "failed_logins",
    "connection_count",
    "unusual_port",
    "same_src_dst",
]
CATEGORICAL_FEATURES: Final[list[str]] = ["protocol_type", "service"]
TARGET: Final[str] = "label"
REQUIRED_COLUMNS: Final[list[str]] = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET]


def main() -> None:
    """Load sample data, train a pipeline, evaluate it and save artefacts."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. Make sure the repository's data folder is present."
        )

    data = pd.read_csv(DATA_PATH)
    missing = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
    if data[TARGET].nunique() < 2:
        raise ValueError("The target column must contain both classes 0 and 1.")

    X = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = data[TARGET].astype(int)

    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("classifier", classifier)]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    report = classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["normal (0)", "potentially_suspicious (1)"],
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_test, predictions, labels=[0, 1]).tolist()

    ROOT.joinpath("models").mkdir(exist_ok=True)
    ROOT.joinpath("reports").mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        "dataset": "synthetic educational sample data",
        "random_state": 42,
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
        "confusion_matrix_labels": ["normal (0)", "potentially_suspicious (1)"],
        "confusion_matrix": matrix,
        "classification_report": report,
        "disclaimer": "Results apply only to this synthetic demonstration dataset; they are not real-world detection performance.",
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    fitted_preprocessor = model.named_steps["preprocessor"]
    feature_names = fitted_preprocessor.get_feature_names_out()
    importances = model.named_steps["classifier"].feature_importances_
    importance_frame = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    ).sort_values("importance", ascending=False)
    importance_frame.to_csv(IMPORTANCE_PATH, index=False)

    print("Model training completed.")
    print(f"Saved model: {MODEL_PATH.relative_to(ROOT)}")
    print(f"Saved evaluation: {METRICS_PATH.relative_to(ROOT)}")
    print(f"Saved feature importance: {IMPORTANCE_PATH.relative_to(ROOT)}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, labels=[0, 1], zero_division=0))
    print("Confusion matrix (rows = actual, columns = predicted; order [0, 1]):")
    print(matrix)
    print("\nReminder: these are demonstration results from synthetic data.")


if __name__ == "__main__":
    main()
