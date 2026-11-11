import pandas as pd
import pytest

from task_Jan_Zdyb import add_virtual_column

def test_sum_of_two_columns():
    df = pd.DataFrame(
        [[1, 1]] * 2,
        columns=["label_one", "label_two"]
    )

    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2,
        columns=["label_one", "label_two", "label_three"]
    )

    df_result = add_virtual_column(
        df,
        "label_one+label_two",
        "label_three"
    )

    assert df_result.equals(df_expected)


def test_multiplication_of_two_columns():
    df = pd.DataFrame(
        [[1, 1]] * 2,
        columns=["label_one", "label_two"]
    )

    df_expected = pd.DataFrame(
        [[1, 1, 1]] * 2,
        columns=["label_one", "label_two", "label_three"]
    )

    df_result = add_virtual_column(
        df,
        "label_one * label_two",
        "label_three"
    )

    assert df_result.equals(df_expected)


def test_subtraction_of_two_columns():
    df = pd.DataFrame(
        [[1, 1]] * 2,
        columns=["label_one", "label_two"]
    )

    df_expected = pd.DataFrame(
        [[1, 1, 0]] * 2,
        columns=["label_one", "label_two", "label_three"]
    )

    df_result = add_virtual_column(
        df,
        "label_one - label_two",
        "label_three"
    )

    assert df_result.equals(df_expected)


def test_empty_result_when_invalid_labels():
    df = pd.DataFrame(
        [[1, 2]] * 3,
        columns=["label_one", "label_two"]
    )

    # Invalid new column name
    result = add_virtual_column(
        df,
        "label_one + label_two",
        "label3"
    )

    assert result.empty

    # Invalid existing column name
    df_invalid = pd.DataFrame(
        [[1, 2]] * 3,
        columns=["label-one", "label_two"]
    )

    result = add_virtual_column(
        df_invalid,
        "label-one + label_two",
        "label"
    )

    assert result.empty

    # Invalid DataFrame column name, even if role uses another name
    result = add_virtual_column(
        df_invalid,
        "label_one + label_two",
        "label"
    )

    assert result.empty


def test_empty_result_when_invalid_rules():
    df = pd.DataFrame(
        [[1, 1]] * 2,
        columns=["label_one", "label_two"]
    )

    # Invalid backslash character
    result = add_virtual_column(
        df,
        r"label_one \ label_two",
        "label_three"
    )

    assert result.empty

    # Invalid ampersand character
    result = add_virtual_column(
        df,
        "label&one + label_two",
        "label_three"
    )

    assert result.empty

    # Column does not exist
    result = add_virtual_column(
        df,
        "label_five + label_two",
        "label_three"
    )

    assert result.empty


def test_when_extra_spaces_in_rules():
    df = pd.DataFrame(
        [[1, 1]] * 2,
        columns=["label_one", "label_two"]
    )

    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2,
        columns=["label_one", "label_two", "label_three"]
    )

    expressions = [
        "label_one+label_two",
        "label_one + label_two ",
        " label_one + label_two ",
    ]

    for expression in expressions:
        df_result = add_virtual_column(
            df,
            expression,
            "label_three"
        )

        assert df_result.equals(df_expected)


def test_input_dataframe_is_not_modified():
    df = pd.DataFrame(
        {
            "label_one": [1, 2],
            "label_two": [3, 4],
        }
    )

    original = df.copy(deep=True)

    add_virtual_column(
        df,
        "label_one + label_two",
        "label_three"
    )

    pd.testing.assert_frame_equal(df, original)


def test_multiple_operations_are_rejected():
    df = pd.DataFrame(
        {
            "label_one": [1],
            "label_two": [2],
        }
    )

    result = add_virtual_column(
        df,
        "label_one + label_two * label_one",
        "label_three"
    )

    assert result.empty


def test_parentheses_are_rejected():
    df = pd.DataFrame(
        {
            "label_one": [1],
            "label_two": [2],
        }
    )

    result = add_virtual_column(
        df,
        "(label_one + label_two)",
        "label_three"
    )

    assert result.empty


def test_duplicate_column_names_are_rejected():
    df = pd.DataFrame(
        [[1, 2]],
        columns=["label_one", "label_one"]
    )

    result = add_virtual_column(
        df,
        "label_one + label_one",
        "label_three"
    )

    assert result.empty


def test_non_string_role_is_rejected():
    df = pd.DataFrame(
        {
            "label_one": [1],
            "label_two": [2],
        }
    )

    result = add_virtual_column(
        df,
        None,
        "label_three"
    )

    assert result.empty


def test_empty_dataframe_is_supported():
    df = pd.DataFrame(
        columns=["label_one", "label_two"]
    )

    expected = pd.DataFrame(
        columns=["label_one", "label_two", "label_three"]
    )

    result = add_virtual_column(
        df,
        "label_one + label_two",
        "label_three"
    )

    pd.testing.assert_frame_equal(result, expected)


def test_existing_new_column_is_overwritten():
    df = pd.DataFrame(
        {
            "label_one": [2],
            "label_two": [3],
            "label_three": [999],
        }
    )

    result = add_virtual_column(
        df,
        "label_one + label_two",
        "label_three"
    )

    assert result["label_three"].tolist() == [5]
    assert df["label_three"].tolist() == [999]


def test_non_dataframe_input_is_rejected():
    result = add_virtual_column(
        [],
        "label_one + label_two",
        "label_three"
    )

    assert result.empty


def test_unicode_letters_are_valid_labels():
    df = pd.DataFrame(
        {
            "cena": [2],
            "ilość": [3],
        }
    )

    result = add_virtual_column(
        df,
        "cena * ilość",
        "łączna"
    )

    assert result["łączna"].tolist() == [6]