import pickle
import os
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def generate_synthetic_data(num_samples=1000):
    data = []
    labels = []
    
    classes = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "O(2^n)"]
    
    for _ in range(num_samples):
        cls = random.choice(classes)
        
        # Base random features
        features = {
            "loop_count": 0,
            "for_loop_count": 0,
            "while_loop_count": 0,
            "max_loop_depth": 0,
            "nested_loop_count": 0,
            "if_count": random.randint(0, 5),
            "function_count": random.randint(0, 2),
            "method_count": random.randint(0, 2),
            "function_call_count": random.randint(0, 5),
            "recursive": 0,
            "recursive_call_count": 0,
            "ast_depth": random.randint(5, 20),
            "statement_count": random.randint(1, 20),
            "condition_count": random.randint(0, 5),
            "linear_loop_count": 0,
            "logarithmic_loop_count": 0,
        }
        
        if cls == "O(1)":
            pass # No loops or recursion
            
        elif cls == "O(log n)":
            features["loop_count"] = 1
            features["while_loop_count"] = 1
            features["max_loop_depth"] = 1
            features["logarithmic_loop_count"] = 1
            features["ast_depth"] += 5
            features["statement_count"] += 3
            
        elif cls == "O(n)":
            features["loop_count"] = 1
            features["for_loop_count"] = random.choice([0, 1])
            features["while_loop_count"] = 1 - features["for_loop_count"]
            features["max_loop_depth"] = 1
            features["linear_loop_count"] = 1
            features["ast_depth"] += 5
            features["statement_count"] += 3
            
        elif cls == "O(n log n)":
            features["loop_count"] = 2
            features["for_loop_count"] = 1
            features["while_loop_count"] = 1
            features["max_loop_depth"] = 2
            features["nested_loop_count"] = 1
            features["linear_loop_count"] = 1
            features["logarithmic_loop_count"] = 1
            features["ast_depth"] += 10
            features["statement_count"] += 5
            
        elif cls == "O(n²)":
            features["loop_count"] = 2
            features["for_loop_count"] = 2
            features["max_loop_depth"] = 2
            features["nested_loop_count"] = 1
            features["linear_loop_count"] = 2
            features["ast_depth"] += 10
            features["statement_count"] += 5
            
        elif cls == "O(n³)":
            features["loop_count"] = 3
            features["for_loop_count"] = 3
            features["max_loop_depth"] = 3
            features["nested_loop_count"] = 2
            features["linear_loop_count"] = 3
            features["ast_depth"] += 15
            features["statement_count"] += 7
            
        elif cls == "O(2^n)":
            features["recursive"] = 1
            features["recursive_call_count"] = random.randint(2, 4)
            features["function_call_count"] += features["recursive_call_count"]
            features["ast_depth"] += 10
            
        data.append(features)
        labels.append(cls)
        
    return pd.DataFrame(data), labels

def train_and_save():
    print("Generating synthetic data...")
    X, y = generate_synthetic_data(2000)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the model
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "complexity_model.pkl")
    
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"Model saved successfully to {model_path}")
    print("Model classes:", model.classes_)

if __name__ == "__main__":
    train_and_save()
