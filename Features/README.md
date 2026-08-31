# Features

This project is the compiler-based feature extraction component of a machine-learning-based time-complexity analyzer.

This service intentionally stops before ML prediction. Its single responsibility is parsing source code, traversing its Abstract Syntax Tree (AST), extracting numerical/boolean features, and returning them in JSON format for consumption by the downstream ML component.

## Architecture

```text
Source Code
     ↓
Lexical Analysis (AST Parsing)
     ↓
AST / Parse Tree
     ↓
Feature Extraction
     ↓
JSON
```

- **Lexical Analysis & Parsing**: The code is tokenized and parsed into an Abstract Syntax Tree (AST) using `ast` for Python and `javalang` for Java.
- **AST / Parse Tree**: A hierarchical representation of the syntactic structure of the code.
- **Feature Extraction**: An AST visitor traverses the tree and collects structural metadata (loops, branches, function calls).
- **JSON**: The extracted features are serialized as a JSON response.

## Supported Languages

- **Python**: Parsed using Python's built-in `ast` module.
- **Java**: Parsed using the `javalang` library. 

## Features

The APIs return the following extracted features for the source code:

- `loop_count`: Total number of loops.
- `for_loop_count`: Number of `for` loops.
- `while_loop_count`: Number of `while` loops.
- `max_loop_depth`: Maximum depth of nested loops. High depths suggest higher polynomial complexities.
- `nested_loop_count`: Count of loops that are nested inside other loops.
- `if_count`: Total number of `if` statements.
- `function_count`: Total number of functions/methods defined.
- `method_count`: Total number of methods defined (primarily for Java).
- `function_call_count`: Number of times a function is called.
- `recursive`: Boolean indicating if recursion is present.
- `recursive_call_count`: Number of recursive calls.
- `ast_depth`: Maximum depth of the abstract syntax tree.
- `statement_count`: Total number of statements in the program.
- `condition_count`: Total number of conditional checks.
- `linear_loop_count`: Loops iterating linearly (e.g., standard `for` loops).
- `logarithmic_loop_count`: Loops that update variables multiplicatively/divisionally, typical in logarithmic complexities.

## Installation

```bash
cd Features

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

Start the API server locally:

```bash
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## API Documentation

### Python
`POST /api/analyze/python`

**Request:**
```json
{
    "code": "for i in range(n):\n    print(i)"
}
```

**Response:**
```json
{
    "language": "python",
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
        "recursive": false,
        "recursive_call_count": 0,
        "ast_depth": 12,
        "statement_count": 2,
        "condition_count": 0,
        "linear_loop_count": 1,
        "logarithmic_loop_count": 0
    }
}
```

### Java
`POST /api/analyze/java`

**Request:**
```json
{
    "code": "for(int i=0; i<n; i++) { System.out.println(i); }"
}
```

**Response:**
```json
{
    "language": "java",
    "features": {
        "loop_count": 1,
        "for_loop_count": 1,
        "while_loop_count": 0,
        "max_loop_depth": 1,
        "nested_loop_count": 0,
        "if_count": 0,
        "function_count": 1,
        "method_count": 1,
        "function_call_count": 1,
        "recursive": false,
        "recursive_call_count": 0,
        "ast_depth": 27,
        "statement_count": 3,
        "condition_count": 0,
        "linear_loop_count": 1,
        "logarithmic_loop_count": 0
    }
}
```

## cURL Examples

**Python:**
```bash
curl -X POST "http://127.0.0.1:8000/api/analyze/python" \
     -H "Content-Type: application/json" \
     -d '{"code":"def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"}'
```

**Java:**
```bash
curl -X POST "http://127.0.0.1:8000/api/analyze/java" \
     -H "Content-Type: application/json" \
     -d '{"code":"void test() { int i = 1; while(i < 10) { i *= 2; } }"}'
```

## Example Programs

### Example 1 — O(1)-like structure
```python
x = 10
y = 20
print(x + y)
```
*Extracted:* `loop_count`: 0, `ast_depth`: 17, `statement_count`: 3

### Example 2 — Single loop
```python
for i in range(10):
    pass
```
*Extracted:* `loop_count`: 1, `max_loop_depth`: 1

### Example 3 — Nested loops
```python
for i in range(n):
    for j in range(n):
        print(i, j)
```
*Extracted:* `loop_count`: 2, `max_loop_depth`: 2, `nested_loop_count`: 1

### Example 4 — Logarithmic loop
```java
int i = 1;
while(i < n) {
    i *= 2;
}
```
*Extracted:* `while_loop_count`: 1, `logarithmic_loop_count`: 1

### Example 5 — Conditional branching
```python
if a > b:
    print(a)
else:
    print(b)
```
*Extracted:* `if_count`: 1, `condition_count`: 1

### Example 6 — Recursion
```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```
*Extracted:* `function_count`: 1, `recursive`: true, `recursive_call_count`: 2

## Relationship With Backend

`backend/` and `Features/` are entirely separate projects. 

```text
Features
    ↓
feature vector (JSON)
    ↓
ML model (in Backend)
    ↓
time complexity
```

This `Features` project *only* generates the input feature vector. It **does not** perform ML prediction or predict time complexity itself.

## Testing

Run the test suite with `pytest`:

```bash
pytest
```

The tests verify:
- API endpoint availability.
- Correct parsing and feature extraction counts for various code topologies (single loops, nested loops, conditional logic, recursion).
- Both Python and Java language endpoints.

## Limitations

- Arbitrary source-code semantics can be difficult to analyze purely statically.
- Dynamic behavior cannot always be inferred statically (e.g., Python `eval()` or reflection in Java).
- Advanced language constructs (like Java 8 streams or Python comprehensions) might not be fully covered by the heuristic counters.
- The extracted features are heuristics intended as inputs to a Machine Learning model rather than rigorous mathematical proofs of complexity.
