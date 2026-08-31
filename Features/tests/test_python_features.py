import pytest
from app.analyzers.python_analyzer import PythonAnalyzer

analyzer = PythonAnalyzer()

def test_no_loop():
    code = "a = 1\nb = 2\nc = a + b"
    features = analyzer.analyze(code)
    assert features.loop_count == 0
    assert features.if_count == 0

def test_single_loop():
    code = "for i in range(n):\n    print(i)"
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.for_loop_count == 1
    assert features.max_loop_depth == 1
    assert features.nested_loop_count == 0

def test_nested_loops():
    code = "for i in range(n):\n    for j in range(m):\n        print(i, j)"
    features = analyzer.analyze(code)
    assert features.loop_count == 2
    assert features.max_loop_depth == 2
    assert features.nested_loop_count == 1
    
def test_recursion():
    code = "def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n-1)"
    features = analyzer.analyze(code)
    assert features.function_count == 1
    assert features.recursive == True
    assert features.recursive_call_count == 1
