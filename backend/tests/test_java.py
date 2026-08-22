import pytest
from app.analyzers.java_analyzer import JavaAnalyzer

def test_constant_time():
    code = "int x = 5;\nint y = x * 2;\nSystem.out.println(y);"
    analyzer = JavaAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 0
    assert features.recursive == False

def test_linear_time():
    code = "for(int i=0; i<n; i++) {\n System.out.println(i);\n }"
    analyzer = JavaAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.max_loop_depth == 1
    
def test_quadratic_time():
    code = "for(int i=0; i<n; i++) {\n for(int j=0; j<n; j++) {\n System.out.println(i);\n }\n }"
    analyzer = JavaAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 2
    assert features.max_loop_depth == 2
    assert features.nested_loop_count == 1
    
def test_logarithmic_time():
    code = "int i = 1;\n while(i < n) {\n i *= 2;\n }"
    analyzer = JavaAnalyzer()
    features = analyzer.analyze(code)
    assert features.loop_count == 1
    assert features.logarithmic_loop_count == 1
