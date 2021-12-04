import pytest

from paithon.model.runner import ModelStats


def test_run_stats(clean_model):
    # Given
    stats = ModelStats()
    # When
    stats.update(duration=1.2)
    # Asserts
    assert stats.runs == 1
    assert stats.duration_total == 1.2
    assert stats.duration_avg == 1.2
    # When
    stats.update(duration=2.4)
    # Asserts
    assert stats.runs == 2
    assert stats.duration_total == pytest.approx(3.6)
    assert stats.duration_avg == pytest.approx(1.8)
