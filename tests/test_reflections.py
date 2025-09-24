from sensors.adapter import self_reflect
from explainability.tracer import Trace

def test_self_reflect_runs():
    result = self_reflect("P?", "I feel changes across iterations.", trace=Trace("x"))
    assert 0.0 <= result["self_confidence"] <= 1.0
    assert "drift" in result
