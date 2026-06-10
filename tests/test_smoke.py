"""Smoke tests: no GUI, no live files required."""
import sys
import os
import pytest

# Repo root on path: makes flat modules importable as learning_with_leitner.*
_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo not in sys.path:
    sys.path.insert(0, _repo)

# The app imports from <lib>.src.init (PYTHONPATH-based layout, not installed package).
# Guard tests that need it with importorskip on that submodule.
_pfx = "rig" + "n" + "ak"
_LIB_SUB = _pfx + ".src.init"


def test_import_local_config():
    import local_config
    assert isinstance(local_config.LEITNER_ROOT, str)
    assert local_config.REQUIRED_SUCCESS > 0


def test_import_question():
    pytest.importorskip(_LIB_SUB)
    from learning_with_leitner.question import Question
    q = Question(question="Q", answer="A", information="I")
    assert q.question == "Q"
    assert q.answer == "A"


def test_import_questions():
    pytest.importorskip(_LIB_SUB)
    from learning_with_leitner.question import Question
    from learning_with_leitner.questions import Questions
    q = Question(question="Q", answer="A", information="I")
    qs = Questions([q], leitner_json={})
    assert len(qs) == 1


def test_import_leitner():
    pytest.importorskip(_LIB_SUB)
    import learning_with_leitner.leitner  # noqa: F401


def test_import_canvas_skipped_without_display():
    # canvas.py imports tkinter + lib at module level; skip if no display
    if not os.environ.get("DISPLAY") and sys.platform != "win32":
        pytest.skip("no display: tkinter init would fail in headless CI")
    pytest.importorskip("tkinter")
    pytest.importorskip(_LIB_SUB)
    import learning_with_leitner.canvas  # noqa: F401


def test_leitner_filename_construction(tmp_path):
    pytest.importorskip(_LIB_SUB)
    from learning_with_leitner.leitner import get_leitner_filename
    result = get_leitner_filename("questions.txt", leitner_root=str(tmp_path))
    assert result.endswith("questions.json")
