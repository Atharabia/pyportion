from __future__ import annotations

import re

_MEMORY_VARIABLE_PATTERN = re.compile(r"^\$(\w+)$")


def _resolve_operand(operand: str, memory: dict[str, str]) -> str:
    operand = operand.strip()
    match = _MEMORY_VARIABLE_PATTERN.match(operand)
    if match:
        return memory.get(match.group(1), "")
    return operand


def _evaluate_comparison(comparison_text: str, memory: dict[str, str]) -> bool:
    comparison_text = comparison_text.strip()
    if not comparison_text:
        raise ValueError("empty comparison in when")

    has_equals = "==" in comparison_text
    has_not_equals = "!=" in comparison_text
    if has_equals and has_not_equals:
        raise ValueError("each comparison must use only == or !=")

    if has_equals:
        left_operand, right_operand = comparison_text.split("==", 1)
        return _resolve_operand(left_operand, memory) == _resolve_operand(
            right_operand, memory
        )
    if has_not_equals:
        left_operand, right_operand = comparison_text.split("!=", 1)
        return _resolve_operand(left_operand, memory) != _resolve_operand(
            right_operand, memory
        )
    raise ValueError("each when clause must contain == or !=")


def evaluate_when(when: str | None, memory: dict[str, str]) -> bool:
    if when is None or not when.strip():
        return True

    when_expression = when.strip()
    or_branches = [branch.strip() for branch in when_expression.split(" or ")]
    if any(branch == "" for branch in or_branches):
        raise ValueError("invalid use of or in when")

    for or_branch in or_branches:
        and_terms = [term.strip() for term in or_branch.split(" and ")]
        if any(term == "" for term in and_terms):
            raise ValueError("invalid use of and in when")
        if all(_evaluate_comparison(term, memory) for term in and_terms):
            return True
    return False
