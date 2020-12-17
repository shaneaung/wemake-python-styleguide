import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    InconsistentComprehensionVisitor,
)

# Tests that should NOT be flagged

# List comprehension tests

correct_list_empty = """
a = []
"""

correct_one_line_comprehension = """
[some(number) for number in numbers]
"""

correct_list_well_spaced_comprehension = """
[
    some(number)
    for number in matrix
    if number > 0
]
"""

nested_comprehension = """
def get_all_args(call: ast.Call) -> Sequence[ast.AST]:
    return [
              *call.args,
              *[kw.value for kw in call.keywords],
    ]
"""


@pytest.mark.parametrize('code', [
    correct_list_empty,
    correct_one_line_comprehension,
    correct_list_well_spaced_comprehension,
    nested_comprehension,
])
def test_correct_list_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct consistency does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [])


# Dictionary comprehension tests

correct_dict_empty = """
a = {{}}
"""

correct_dict_full = """
a = {'a':1,'b':2,'c':3}
"""

correct_dict_one_line_comprehension = """
{key:val for (key, val) in tuples}
"""

correct_dict_well_spaced_comprehension = """
{
    key:val
    for (key, val) in matrix
    if key > 0
}
"""


@pytest.mark.parametrize('code', [
    correct_dict_empty,
    correct_dict_full,
    correct_dict_one_line_comprehension,
    correct_dict_well_spaced_comprehension,
])
def test_correct_dict_comprehension_consistency(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct consistency does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [])


# Set comprehensions

correct_empty_set = """
{{}}
"""

correct_one_line_comprehension = """
{some(number) for number in numbers}
"""

correct_well_spaced_comprehension = """
{
    some(number)
    for number in matrix
    if number > 0
}
"""

# The below test is inspired by:
# https://python-reference.readthedocs.io/en/
#       latest/docs/comprehensions/set_comprehension.html
nested_comprehension = """
{s for s in [1, 2, 3, 4]}
"""


@pytest.mark.parametrize('code', [
    correct_empty_set,
    correct_one_line_comprehension,
    correct_well_spaced_comprehension,
    nested_comprehension,
])
def test_correct_set_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct consistency does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [])


# Should raise flag

# List comprehension tests

wrong_almost_one_line = """
[
    some(number) for number in numbers
    if number > 0
]
"""


wrong_two_fors = """
[
    some(number)
    for numbers in matrix for number in numbers
]
"""


wrong_for_and_if = """
[
    some(number)
    for number in matrix if number > 0
]
"""


@pytest.mark.parametrize('code', [
    wrong_almost_one_line,
    wrong_two_fors,
    wrong_for_and_if,
])
def test_wrong_list_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong comprehension consistencies raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [InconsistentComprehensionViolation])


# Dictionary comprehension tests

wrong_dict_because_almost_one_line = """
{
    key:val for (key, val) in tuples
    if key > 0
}
"""

wrong_dict_because_two_lines_in_one = """
{
    key:val
    for numbers in matrix
    for (key, val) in numbers if key > 0
}
"""


@pytest.mark.parametrize('code', [
    wrong_dict_because_almost_one_line,
    wrong_dict_because_two_lines_in_one,
])
def test_wrong_dictionary_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong comprehension consistencies raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [InconsistentComprehensionViolation])


# Set comprehensions

wrong_almost_one_line = """
{
    some(number) for number in numbers
    if number > 0
}
"""

wrong_two_fors = """
{
    some(number)
    for numbers in matrix for number in numbers
}
"""

wrong_for_and_if_set = """
{
    some(number)
    for number in matrix if number > 0
}
"""


@pytest.mark.parametrize('code', [
    wrong_almost_one_line,
    wrong_two_fors,
    wrong_for_and_if,
])
def test_wrong_set_comprehension_consistency(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong comprehension consistencies raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [InconsistentComprehensionViolation])
