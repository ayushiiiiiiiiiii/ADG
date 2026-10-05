# ⚡ Time Complexity Analyzer (ADG)

A full-stack, machine-learning-powered static code analysis tool that combines **Compiler Design (AST parsing)** and **Machine Learning (Random Forest Classification)** to analyze Python and Java source code, extract structural features, predict asymptotic time complexity, and output human-readable explanations.

---

## 🚀 Overview

Static analysis of algorithm complexity is traditionally challenging due to the dynamic nature of runtime execution. This project bridges **compiler design** and **machine learning**:
1. **Lexical & Syntactic Analysis**: Parses source code into Abstract Syntax Trees (ASTs) using Python's `ast` module and Java's `javalang` library.
2. **Compiler Feature Extraction**: Traverses AST nodes to compute structural heuristics (loop depth, recursion count, condition branches, logarithmic progression, etc.).
3. **ML Prediction**: Feeds the extracted feature vectors into a trained **Random Forest Classifier** to predict Big-O time complexity.
4. **Explanation Engine**: Generates human-understandable reasoning based on the extracted AST metadata.
5. **Interactive UI**: Offers a web interface for pasting code snippets and viewing predictions, confidence scores, and AST metrics.

---

## 🛠 Project Architecture

```text
ADG Project Root
 ├── backend/       # FastAPI REST API, AST Analyzers, ML Model & Explainer
 ├── frontend/      # Interactive Web Dashboard (HTML5 / Vanilla CSS / JS)
 └── Features/      # Standalone AST Feature Extraction Service (Pure Parser)
```

### Complete End-to-End Pipeline

```text
       Source Code (Python / Java)
                   │
                   ▼
       Lexical Analysis & AST Parsing (ast / javalang)
                   │
                   ▼
       Static Feature Extraction
       (Loop Depths, Branching, Recursion, Statement Counts)
                   │
                   ▼
       Random Forest ML Classifier
                   │
                   ▼
    Time Complexity Prediction + Confidence Score
                   │
                   ▼
       Explanation Engine & Visual Dashboard
```

---

## 🌟 Key Features

- **Multi-Language AST Parsing**: Supports Python and Java syntax trees out of the box.
- **Rich Feature Vector Extraction**:
  - `loop_count`, `for_loop_count`, `while_loop_count`
  - `max_loop_depth`, `nested_loop_count`
  - `linear_loop_count`, `logarithmic_loop_count`
  - `if_count`, `condition_count`
  - `function_count`, `method_count`, `function_call_count`
  - `recursive` (Boolean), `recursive_call_count`
  - `ast_depth`, `statement_count`
- **Supported Complexity Classes**:
  - $O(1)$ — Constant Time
  - $O(\log n)$ — Logarithmic Time
  - $O(n)$ — Linear Time
  - $O(n \log n)$ — Linearithmic Time
  - $O(n^2)$ — Quadratic Time
  - $O(n^3)$ — Cubic Time
  - $O(2^n)$ — Exponential Time
- **Web Interface**: Clean, modern dark-themed dashboard built with vanilla web technologies for zero build step friction.

---

## 📁 Repository Structure

```text
ADG/
│
├── backend/                  # Machine Learning & API Backend
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── api/              # API router & endpoints (/api/analyze, /api/health)
│   │   ├── analyzers/        # AST Visitors (PythonAnalyzer, JavaAnalyzer)
│   │   ├── ml/               # Model inference (ComplexityPredictor)
│   │   ├── explanation/      # Rule-based natural language explainer
│   │   └── schemas/          # Pydantic request/response models
│   ├── ml_pipeline/          # Synthetic dataset generator & model training scripts
│   ├── complexity_model.pkl  # Trained Random Forest classifier binary
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # Interactive Frontend Dashboard
│   ├── index.html            # UI layout & snippet form
│   ├── styles.css            # Dark mode glassmorphic styling
│   └── app.js                # Frontend API client & dynamic DOM rendering
│
└── Features/                 # Standalone Compiler Feature Extraction API
    ├── app/                  # AST parsing routes without ML overhead
    ├── tests/                # Pytest suite for parser verification
    └── requirements.txt      # Microservice dependencies
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.9+**
- **pip**
- Modern Web Browser (Chrome, Firefox, Edge, Safari)

---

### Step 1: Set Up Backend

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Train / verify the Machine Learning Model:
   ```bash
   python ml_pipeline/train_model.py
   ```

5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend API will run on `http://127.0.0.1:8000`.

---

### Step 2: Launch Frontend

Simply open `frontend/index.html` in your web browser, or serve it using any HTTP server:

Using Python's built-in HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000` in your browser.

---

### Step 3 (Optional): Standalone Feature Extractor

If you wish to run the compiler feature extraction microservice independently without ML inference:

```bash
cd Features
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

---

## 📡 API Reference

### Health Check
`GET /api/health`

**Response:**
```json
{
  "status": "ok"
}
```

---

### Analyze Code
`POST /api/analyze`

**Request Body:**
```json
{
  "language": "python",
  "code": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1"
}
```

**Response Body:**
```json
{
  "language": "python",
  "time_complexity": "O(log n)",
  "confidence": 0.95,
  "reason": "The program contains logarithmic loop progression (variable modified by division/halving).",
  "features": {
    "loop_count": 1,
    "for_loop_count": 0,
    "while_loop_count": 1,
    "max_loop_depth": 1,
    "nested_loop_count": 0,
    "if_count": 2,
    "function_count": 1,
    "method_count": 0,
    "function_call_count": 1,
    "recursive": false,
    "recursive_call_count": 0,
    "ast_depth": 9,
    "statement_count": 10,
    "condition_count": 2,
    "linear_loop_count": 0,
    "logarithmic_loop_count": 1
  }
}
```

---

## 🧪 Testing

To run the automated test suite for the feature extractor and parser modules:

```bash
cd Features
pytest
```

---

## 📌 Limitations & Scope

- **Static Analysis Halting Constraints**: Time complexity calculation in the general case is undecidable (related to the Halting Problem). Predictions rely on static syntactic structures.
- **Dynamic Semantics**: Code relying on dynamic execution (e.g., Python `eval()`, Java reflection, or runtime array sizes passed via external APIs) cannot be fully analyzed statically.
- **Heuristic Boundaries**: Unconventional iteration patterns or custom iterator objects may be classified based on AST structural approximations.

---

## 📜 License

This project is licensed under the MIT License — feel free to use and extend for academic and research purposes.
