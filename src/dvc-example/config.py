from pathlib import Path

class Config:
    DVC_ASSETS_PATH = Path("./assets")
    ORIGINAL_DATASET_FILE_PATH = Path("wine-quality.csv")
    DATASET_PATH = Path(DVC_ASSETS_PATH / "data")
    FEATURES_PATH = Path(DVC_ASSETS_PATH / "features")
    MODELS_PATH = Path(DVC_ASSETS_PATH / "models")
    METRICS_FILE_PATH = Path(DVC_ASSETS_PATH / "metrics.json")
    PLOTS_FILE_PATH = Path(DVC_ASSETS_PATH / "plots.json")