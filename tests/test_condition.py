import pytest

from portion.utils.condition import _evaluate_comparison
from portion.utils.condition import evaluate_when


def test_evaluate_comparison_whitespace_only_raises() -> None:
    with pytest.raises(ValueError, match="empty comparison"):
        _evaluate_comparison("   ", {})


def test_when_none_or_blank_is_true() -> None:
    assert evaluate_when(None, {}) is True
    assert evaluate_when("", {}) is True
    assert evaluate_when("   ", {}) is True


def test_equals_with_memory_and_literal() -> None:
    memory = {"flag": "yes"}
    assert evaluate_when("$flag == yes", memory) is True
    assert evaluate_when("$flag == no", memory) is False


def test_equals_both_literals() -> None:
    assert evaluate_when("a == a", {}) is True
    assert evaluate_when("a == b", {}) is False


def test_not_equals() -> None:
    memory = {"x": "1"}
    assert evaluate_when("$x != 2", memory) is True
    assert evaluate_when("$x != 1", memory) is False


def test_missing_memory_key_is_empty_string() -> None:
    assert evaluate_when("$missing == ", {}) is True
    assert evaluate_when("$missing != ", {}) is False


def test_and_all_must_hold() -> None:
    memory = {"a": "1", "b": "2"}
    assert evaluate_when("$a == 1 and $b == 2", memory) is True
    assert evaluate_when("$a == 1 and $b == 3", memory) is False


def test_or_any_branch_suffices() -> None:
    memory = {"a": "1", "b": "2"}
    assert evaluate_when("$a == 1 or $b == 2", memory) is True
    assert evaluate_when("$a == 0 or $b == 0", memory) is False


def test_and_binds_tighter_than_or() -> None:
    memory = {"a": "yes", "b": "no", "c": "maybe"}
    assert evaluate_when(
        "$a == yes or $b == no and $c == maybe",
        memory,
    ) is True
    assert evaluate_when(
        "$a == no or $b == no and $c == maybe",
        {"a": "yes", "b": "no", "c": "no"},
    ) is False


def test_compound_with_not_equals() -> None:
    memory = {"a": "ok", "b": "bad"}
    assert evaluate_when("$a != bad and $b == bad", memory) is True
    assert evaluate_when("$a != ok or $b != bad", memory) is False


def test_raises_when_single_comparison_mixes_operators() -> None:
    with pytest.raises(ValueError, match="only =="):
        evaluate_when("$a == 1 != 2", {})


def test_raises_when_comparison_has_no_operator() -> None:
    with pytest.raises(ValueError, match="== or !="):
        evaluate_when("$a", {})


def test_raises_on_empty_or_branch() -> None:
    with pytest.raises(ValueError, match="or"):
        evaluate_when("$a == 1 or  or $b == 2", {})


def test_raises_on_empty_and_term() -> None:
    with pytest.raises(ValueError, match="and"):
        evaluate_when("$a == 1 and  and $b == 2", {})
