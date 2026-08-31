import joblib
import os

class ModelService:
    def __init__(self):
        self.models = {}
        # Ensure path is correct relative to backend
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        model_dir = os.path.join(base_dir, "Models")

        self.models["flood"] = joblib.load(os.path.join(model_dir, "flood_xgboost.pkl"))
        self.models["drought"] = joblib.load(os.path.join(model_dir, "drought_xgboost.pkl"))
        self.models["heatwave"] = joblib.load(os.path.join(model_dir, "heatwave_xgboost.pkl"))

    def predict(self, hazard: str, features: list):
        model = self.models.get(hazard)
        if not model:
            raise ValueError(f"Model {hazard} not found")
        # Ensure features are in correct shape
        return model.predict_proba([features])
