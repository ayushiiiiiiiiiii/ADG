import pytest
from app.analyzers.python_analyzer import PythonAnalyzer

def test_constant_time():
    code = "x = 5\ny = x * 2\nprint(y)"
    analyzer = PythonAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 0
    assert features.recursive == False

def test_linear_time():
    code = "for i in range(n):\n    print(i)"
    analyzer = PythonAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.max_loop_depth == 1
    
def test_quadratic_time():
    code = "for i in range(n):\n    for j in range(n):\n        print(i, j)"
    analyzer = PythonAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 2
    assert features.max_loop_depth == 2
    assert features.nested_loop_count == 1
    
def test_logarithmic_time():
    code = "i = 1\nwhile i < n:\n    i *= 2"
    analyzer = PythonAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.logarithmic_loop_count == 1
    
def test_exponential_time():
    code = "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)"
    analyzer = PythonAnalyzer()
    features = analyzer.analyze(code)
    assert features.recursive == True
    assert features.recursive_call_count == 2
