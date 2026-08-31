import pytest
from app.analyzers.java_analyzer import JavaAnalyzer

analyzer = JavaAnalyzer()

def test_no_loop():
    code = "int a = 1; int b = 2; int c = a + b;"
    features = analyzer.analyze(code)
    assert features.loop_count == 0
    assert features.if_count == 0

def test_single_loop():
    code = "for(int i=0; i<n; i++) { System.out.println(i); }"
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.for_loop_count == 1
    assert features.max_loop_depth == 1
    assert features.nested_loop_count == 0

def test_nested_loops():
    code = "for(int i=0; i<n; i++) { for(int j=0; j<m; j++) { System.out.println(i + j); } }"
    features = analyzer.analyze(code)
    assert features.loop_count == 2
    assert features.max_loop_depth == 2
    assert features.nested_loop_count == 1
    
def test_recursion():
    code = "public class A { int fact(int n) { if (n <= 1) return 1; return n * fact(n-1); } }"
    features = analyzer.analyze(code)
    assert features.function_count == 1
    assert features.recursive == True
    assert features.recursive_call_count == 1
