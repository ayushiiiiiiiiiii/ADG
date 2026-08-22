import os
import pickle
import numpy as pd
import pandas as pd
from app.features.feature_schema import ExtractedFeatures

class ComplexityPredictor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "complexity_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Please run train_model.py first.")
            
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, features: ExtractedFeatures) -> (str, float):
        if self.model is None:
            self.load_model()
            
        # Convert features to DataFrame as the model was trained on a DataFrame
        # to ensure feature names and order match
        feature_dict = features.to_dict()
        # Ensure we only use the features the model was trained on
        # This matches the dictionary keys in train_model.py
        feature_names = [
            "loop_count", "for_loop_count", "while_loop_count", "max_loop_depth",
            "nested_loop_count", "if_count", "function_count", "method_count",
            "function_call_count", "recursive", "recursive_call_count",
            "ast_depth", "statement_count", "condition_count", 
            "linear_loop_count", "logarithmic_loop_count"
        ]
        
        # We need to ensure bool 'recursive' is converted to int like training data
        feature_dict["recursive"] = int(feature_dict["recursive"])
        
        # Create a single-row DataFrame
        df = pd.DataFrame([{k: feature_dict[k] for k in feature_names}])
        
        prediction = self.model.predict(df)[0]
        
        # Get probability/confidence
        probabilities = self.model.predict_proba(df)[0]
        confidence = float(max(probabilities))
        
        return prediction, confidence
