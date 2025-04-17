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
    """Testa todos os dez casos de testes presentes nas especificações do code challenge."""
    input_data = load_input_file(input_file)
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == expected_output


def test_main_with_alternative_case_10():
    """Caso #10: Múltiplas compras e vendas com variações significativas de preço."""
    input_data = """[{"operation":"buy", "unit-cost":50.00, "quantity": 1000},{"operation":"buy", "unit-cost":25.00, "quantity": 2000},{"operation":"buy", "unit-cost":10.00, "quantity": 3000},{"operation":"sell", "unit-cost":40.00, "quantity": 1500},{"operation":"sell", "unit-cost":5.00, "quantity": 2000},{"operation":"buy", "unit-cost":30.00, "quantity": 5000},{"operation":"sell", "unit-cost":35.00, "quantity": 7500}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == (
        '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 5500.0},{"tax": 0.0},{"tax": 0.0},{"tax": 5000.0}]\n'
    )


def test_main_with_alternative_case_11():
    """Caso #11: Venda precisamente no limite de isenção (R$20.000)."""
    input_data = """[{"operation":"buy", "unit-cost":10.00, "quantity": 5000},{"operation":"sell", "unit-cost":14.00, "quantity": 1429},{"operation":"sell", "unit-cost":15.00, "quantity": 3571}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 1143.2},{"tax": 3571.0}]\n')


def test_main_with_alternative_case_12():
    """Caso #12: Muitas pequenas operações alternadas (abaixo do limite de isenção)."""
    input_data = """[{"operation":"buy", "unit-cost":100.00, "quantity": 100},{"operation":"sell", "unit-cost":110.00, "quantity": 50},{"operation":"buy", "unit-cost":90.00, "quantity": 100},{"operation":"sell", "unit-cost":95.00, "quantity": 50},{"operation":"buy", "unit-cost":85.00, "quantity": 100},{"operation":"sell", "unit-cost":100.00, "quantity": 50},{"operation":"buy", "unit-cost":80.00, "quantity": 100},{"operation":"sell", "unit-cost":90.00, "quantity": 50},{"operation":"buy", "unit-cost":75.00, "quantity": 100},{"operation":"sell", "unit-cost":85.00, "quantity": 150}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == (
        '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n'
    )


def test_main_with_alternative_case_13():
    """Caso #13: Acumulação e uso de prejuízos em múltiplas etapas."""
    input_data = """[{"operation":"buy", "unit-cost":20.00, "quantity": 10000},{"operation":"sell", "unit-cost":10.00, "quantity": 5000},{"operation":"sell", "unit-cost":30.00, "quantity": 1000},{"operation":"sell", "unit-cost":30.00, "quantity": 1000},{"operation":"sell", "unit-cost":30.00, "quantity": 1000},{"operation":"sell", "unit-cost":30.00, "quantity": 1000},{"operation":"sell", "unit-cost":30.00, "quantity": 1000}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == (
        '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n'
    )


def test_main_with_alternative_case_14():
    """Caso #14: Preço médio exato (teste de arredondamento)."""
    input_data = """[{"operation":"buy", "unit-cost":10.00, "quantity": 3},{"operation":"buy", "unit-cost":20.00, "quantity": 3},{"operation":"buy", "unit-cost":30.00, "quantity": 3},{"operation":"sell", "unit-cost":25.00, "quantity": 6},{"operation":"sell", "unit-cost":15.00, "quantity": 3}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n')


def test_main_with_alternative_case_15():
    """Caso #15: Muitas operações grandes seguidas de pequenas (teste de limite de isenção)."""
    input_data = """[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":15.00, "quantity": 5000},{"operation":"sell", "unit-cost":15.00, "quantity": 2500},{"operation":"sell", "unit-cost":15.00, "quantity": 1250},{"operation":"sell", "unit-cost":15.00, "quantity": 625},{"operation":"sell", "unit-cost":15.00, "quantity": 313},{"operation":"sell", "unit-cost":15.00, "quantity": 156},{"operation":"sell", "unit-cost":15.00, "quantity": 78},{"operation":"sell", "unit-cost":15.00, "quantity": 39},{"operation":"sell", "unit-cost":15.00, "quantity": 39}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == (
        '[{"tax": 0.0},{"tax": 5000.0},{"tax": 2500.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n'
    )


def test_main_with_alternative_case_16():
    """Caso #16: Compras e vendas fracionadas com números decimais."""
    input_data = """[{"operation":"buy", "unit-cost":100.50, "quantity": 100},{"operation":"buy", "unit-cost":98.75, "quantity": 150},{"operation":"sell", "unit-cost":102.25, "quantity": 120},{"operation":"buy", "unit-cost":95.60, "quantity": 200},{"operation":"sell", "unit-cost":110.30, "quantity": 330}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 870.1}]\n')


def test_main_with_alternative_case_17():
    """Caso #17: Sequência de prejuízos seguidos por grandes lucros."""
    input_data = """[{"operation":"buy", "unit-cost":50.00, "quantity": 1000},{"operation":"sell", "unit-cost":40.00, "quantity": 200},{"operation":"sell", "unit-cost":30.00, "quantity": 200},{"operation":"sell", "unit-cost":20.00, "quantity": 200},{"operation":"buy", "unit-cost":60.00, "quantity": 1000},{"operation":"sell", "unit-cost":100.00, "quantity": 1400}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == (
        '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 9600.0}]\n'
    )


def test_main_with_alternative_case_18():
    """Caso #18: Teste de limite no valor de R$20.000 exato."""
    input_data = """[{"operation":"buy", "unit-cost":10.00, "quantity": 1000},{"operation":"sell", "unit-cost":30.00, "quantity": 667},{"operation":"sell", "unit-cost":30.00, "quantity": 333}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 2668.0},{"tax": 0.0}]\n')


def test_main_with_alternative_case_19():
    """Caso #19: Mistura de preços altos e baixos com grandes quantidades."""
    input_data = """[{"operation":"buy", "unit-cost":0.50, "quantity": 100000},{"operation":"buy", "unit-cost":2000.00, "quantity": 10},{"operation":"sell", "unit-cost":1.00, "quantity": 50000},{"operation":"sell", "unit-cost":3000.00, "quantity": 5}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 0.0},{"tax": 3000.7},{"tax": 0.0}]\n')


def test_main_with_alternative_case_20():
    """Caso #20: Operações intercaladas com preços iguais (teste de estabilidade)."""
    input_data = """[{"operation":"buy", "unit-cost":100.00, "quantity": 100},{"operation":"sell", "unit-cost":100.00, "quantity": 50},{"operation":"buy", "unit-cost":100.00, "quantity": 100},{"operation":"sell", "unit-cost":100.00, "quantity": 150}]"""
    output_data = io.StringIO()

    with patch("sys.stdin", io.StringIO(input_data)), patch("sys.stdout", output_data):
        main()

    assert output_data.getvalue() == ('[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]\n')
