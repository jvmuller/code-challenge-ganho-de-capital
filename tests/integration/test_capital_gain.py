import io
import json
import os
import sys
from unittest.mock import patch

import pytest
from src.main import main


def load_input_file(filename):
    with open(os.path.join("input_examples", filename), "r") as f:
        return f.read()


@pytest.mark.parametrize(
    "input_file,expected_output",
    [
        ("input_01.txt", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n'),
        ("input_02.txt", '[{"tax": 0.0},{"tax": 10000.0},{"tax": 0.0}]\n'),
        (
            "input_01_with_02.txt",
            '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n[{"tax": 0.0},{"tax": 10000.0},{"tax": 0.0}]\n',
        ),
        ("input_03.txt", '[{"tax": 0.0},{"tax": 0.0},{"tax": 1000.0}]\n'),
        ("input_04.txt", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n'),
        ("input_05.txt", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 10000.0}]\n'),
        ("input_06.txt", '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 3000.0}]\n'),
        (
            "input_07.txt",
            '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 3000.0},{"tax": 0.0},{"tax": 0.0},{"tax": 3700.0},{"tax": 0.0}]\n',
        ),
        ("input_08.txt", '[{"tax": 0.0},{"tax": 80000.0},{"tax": 0.0},{"tax": 60000.0}]\n'),
        (
            "input_09.txt",
            '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 1000.0},{"tax": 2400.0}]\n',
        ),
    ],
)
def test_main_with_input(input_file, expected_output):
    """Testa o Caso #1 do exemplo de ganho de capital."""
    input_data = load_input_file(input_file)
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == expected_output
