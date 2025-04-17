import io
import json
import os
import sys
from unittest.mock import patch

import pytest
from src.main import main


def load_input_file(filename):
    with open(os.path.join("input_examples", filename), "r") as f:
        return json.loads(f.read())


def test_main_with_input_01():
    """Testa o Caso #1 do exemplo de ganho de capital."""
    input_data = load_input_file("input_01.txt")
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(json.dumps(input_data))), patch("sys.stdout", output_data):
        main()

    expected_output = '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]'
    assert output_data.getvalue() == expected_output
