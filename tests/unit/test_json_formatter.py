from decimal import Decimal
import json

import pytest
from src.adapters.output.json_formatter import DecimalEncoder, JsonFormatter


class TestJsonFormatter:
    def test_formatar_impostos_lista_vazia(self):
        """Testa a formatação de uma lista vazia de impostos."""
        impostos = []
        resultado = JsonFormatter.formatar_impostos(impostos)

        assert resultado == "[]"

    def test_formatar_impostos_com_valores_zero(self):
        """Testa a formatação de uma lista de impostos com valores zero."""
        impostos = [Decimal("0"), Decimal("0"), Decimal("0")]
        resultado = JsonFormatter.formatar_impostos(impostos)

        # O formato esperado é: [{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]
        assert resultado == '[{"tax": 0.0},{"tax": 0.0},{"tax": 0.0}]'

    def test_formatar_impostos_com_valores_decimais(self):
        """Testa a formatação de uma lista de impostos com valores decimais."""
        impostos = [Decimal("10.5"), Decimal("15.75"), Decimal("20.25")]
        resultado = JsonFormatter.formatar_impostos(impostos)

        # O formato esperado é: [{"tax": 10.5},{"tax": 15.75},{"tax": 20.25}]
        assert resultado == '[{"tax": 10.5},{"tax": 15.75},{"tax": 20.25}]'

    def test_formatar_impostos_com_valores_grandes(self):
        """Testa a formatação de uma lista de impostos com valores grandes."""
        impostos = [Decimal("1000.00"), Decimal("10000.00"), Decimal("100000.00")]
        resultado = JsonFormatter.formatar_impostos(impostos)

        # O formato esperado é: [{"tax": 1000.0},{"tax": 10000.0},{"tax": 100000.0}]
        assert resultado == '[{"tax": 1000.0},{"tax": 10000.0},{"tax": 100000.0}]'

    def test_formatar_impostos_com_precisao_decimal(self):
        """Testa a formatação de uma lista de impostos com precisão decimal variada."""
        impostos = [Decimal("10.1"), Decimal("10.12"), Decimal("10.123"), Decimal("10.1234")]
        resultado = JsonFormatter.formatar_impostos(impostos)

        # O formato esperado mantém a precisão original (exceto zeros à direita)
        assert resultado == '[{"tax": 10.1},{"tax": 10.12},{"tax": 10.123},{"tax": 10.1234}]'


class TestDecimalEncoder:
    def test_converter_decimal_para_float(self):
        """Testa a conversão de Decimal para float ao codificar para JSON."""
        encoder = DecimalEncoder()
        valor_decimal = Decimal("123.45")

        resultado = encoder.default(valor_decimal)

        assert isinstance(resultado, float)
        assert resultado == 123.45

    def test_converter_outros_tipos(self):
        """Testa o comportamento do encoder com outros tipos de dados."""
        encoder = DecimalEncoder()

        # Com outros tipos, deve delegar para a implementação padrão
        with pytest.raises(TypeError):
            encoder.default("string")

        with pytest.raises(TypeError):
            encoder.default([1, 2, 3])

    def test_json_dumps_com_decimal_encoder(self):
        """Testa o uso do DecimalEncoder com json.dumps."""
        dados = {"valor": Decimal("99.99")}

        resultado = json.dumps(dados, cls=DecimalEncoder)

        assert resultado == '{"valor": 99.99}'

    def test_json_dumps_com_lista_de_decimals(self):
        """Testa o uso do DecimalEncoder com json.dumps para uma lista de Decimals."""
        dados = [Decimal("1.1"), Decimal("2.2"), Decimal("3.3")]

        resultado = json.dumps(dados, cls=DecimalEncoder)

        assert resultado == "[1.1, 2.2, 3.3]"
