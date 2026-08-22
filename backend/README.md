# Machine Learning Based Time Complexity Analyzer

This is the backend for the Machine Learning Based Time Complexity Analyzer, built as a college project combining **Compiler Design** and **Machine Learning**.

## What the project does
The backend accepts source code written in Python or Java, analyzes its structure using compiler-design techniques (AST parsing), extracts meaningful static features, passes those features to a machine-learning model, and returns the predicted **time complexity** along with a clear human-readable explanation.

## Architecture

The system follows a strict pipeline:
```
Source Code
    ↓
Language Parser (ast / javalang)
    ↓
AST / Parse Tree
    ↓
Static Feature Extraction (loops, depth, recursion, ifs, etc.)
    ↓
Machine Learning Model (Random Forest Classifier)
    ↓
Time Complexity Prediction (e.g., O(n²))
    ↓
Explanation Engine
    ↓
JSON Response
```

## Requirements
- Python 3.9+
- pip

## Installation

1. Clone the repository and navigate to the backend directory:
```bash
git clone https://github.com/gauravpurohit685/ADG.git
cd backend
```

2. Create a virtual environment and activate it:
**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```
**Linux/macOS**:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Generate the ML Model (Required before running the API):
```bash
python ml_pipeline/train_model.py
```

## Running the API

Start the backend using uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Usage

### Health Check
```bash
curl -X GET http://127.0.0.1:8000/api/health
```

### Analyze Python Code
```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "code": "for i in range(n):\n    print(i)"}'
```

### Analyze Java Code
```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"language": "java", "code": "for(int i=0; i<n; i++) { for(int j=0; j<n; j++) { System.out.println(i+j); } }"}'
```

## Example Response
```json
{
  "language": "python",
  "time_complexity": "O(n)",
  "confidence": 0.94,
  "reason": "The program contains 1 non-nested linear loop(s) that iterate through the input.",
  "features": {
    "loop_count": 1,
    "for_loop_count": 1,
    "while_loop_count": 0,
    "max_loop_depth": 1,
    "nested_loop_count": 0,
    "if_count": 0,
    "function_count": 0,
    "method_count": 0,
    "function_call_count": 1,
    "recursive": 0,
    "recursive_call_count": 0,
    "ast_depth": 5,
    "statement_count": 2,
    "condition_count": 0,
    "linear_loop_count": 1,
    "logarithmic_loop_count": 0
  }
}
```

## ML Model Details

- **Algorithm**: Random Forest Classifier
- **Features Used**: Structural features extracted from the AST such as `loop_count`, `max_loop_depth`, `recursive_call_count`, `linear_loop_count`, etc.
- **Dataset**: Since we are using custom engineered compiler-level features, the dataset is synthetically generated via `ml_pipeline/train_model.py`. The generation script creates a mapping of structural patterns to expected time complexities (O(1), O(log n), O(n), O(n log n), O(n²), O(n³), O(2^n)).
- **Origin**: Trained locally and saved as `complexity_model.pkl`. It runs entirely locally.

## Project Limitations

Time complexity prediction from arbitrary source code is inherently difficult (related to the Halting Problem), and exact analysis is not possible in the general case. The predictions provided by this API are **estimates** based on static structural patterns (like loop depth and recursion). It does not execute the code, and complex algorithmic behaviors hidden behind arbitrary mathematics or external function calls may be misclassified.
