from decimal import Decimal, InvalidOperation
import json

import pytest
from src.adapters.input.json_parser import JsonParser
from src.domain.exceptions.parse_error import ParseError
from src.domain.models.operacao import Operacao, TipoOperacao


class TestJsonParser:
    def test_parse_operations_com_json_valido(self):
        """Testa o parse de um JSON válido com uma operação."""
        json_data = '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}]'
        operacoes = JsonParser.parse_operations(json_data)

        assert len(operacoes) == 1
        assert isinstance(operacoes[0], Operacao)
        assert operacoes[0].tipo_operacao == TipoOperacao.BUY
        assert operacoes[0].preco_unitario == Decimal("10.00")
        assert operacoes[0].quantidade == 100

    def test_parse_operations_com_multiplas_operacoes(self):
        """Testa o parse de um JSON válido com múltiplas operações."""
        json_data = """[
            {"operation":"buy", "unit-cost":10.00, "quantity": 100},
            {"operation":"sell", "unit-cost":15.00, "quantity": 50},
            {"operation":"buy", "unit-cost":20.00, "quantity": 200}
        ]"""

        operacoes = JsonParser.parse_operations(json_data)

        assert len(operacoes) == 3

        # Verifica primeira operação
        assert operacoes[0].tipo_operacao == TipoOperacao.BUY
        assert operacoes[0].preco_unitario == Decimal("10.00")
        assert operacoes[0].quantidade == 100

        # Verifica segunda operação
        assert operacoes[1].tipo_operacao == TipoOperacao.SELL
        assert operacoes[1].preco_unitario == Decimal("15.00")
        assert operacoes[1].quantidade == 50

        # Verifica terceira operação
        assert operacoes[2].tipo_operacao == TipoOperacao.BUY
        assert operacoes[2].preco_unitario == Decimal("20.00")
        assert operacoes[2].quantidade == 200

    def test_parse_operations_com_formatos_diferentes_de_numeros(self):
        """Testa o parse de um JSON com diferentes formatos de números."""
        json_data = """[
            {"operation":"buy", "unit-cost":10, "quantity": 100},
            {"operation":"buy", "unit-cost":10.5, "quantity": 100},
            {"operation":"buy", "unit-cost":10.00, "quantity": 100}
        ]"""

        operacoes = JsonParser.parse_operations(json_data)

        assert len(operacoes) == 3
        assert operacoes[0].preco_unitario == Decimal("10")
        assert operacoes[1].preco_unitario == Decimal("10.5")
        assert operacoes[2].preco_unitario == Decimal("10.00")

    def test_parse_operations_com_json_mal_formatado(self):
        """Testa o parse de um JSON mal formatado."""
        json_data = '[{"operation":"buy", "unit-cost":10.00, "quantity": 100'

        with pytest.raises(ParseError) as excinfo:
            JsonParser.parse_operations(json_data)

        assert "Erro ao processar JSON" in str(excinfo.value)

    def test_parse_operations_com_campos_faltando(self):
        """Testa o parse de um JSON com campos obrigatórios faltando."""
        json_data = '[{"operation":"buy", "quantity": 100}]'

        with pytest.raises(ParseError) as excinfo:
            JsonParser.parse_operations(json_data)

        assert "Erro ao processar JSON" in str(excinfo.value)

    def test_parse_operations_com_tipo_operacao_invalido(self):
        """Testa o parse de um JSON com tipo de operação inválido."""
        json_data = '[{"operation":"invalid", "unit-cost":10.00, "quantity": 100}]'

        with pytest.raises(ParseError) as excinfo:
            JsonParser.parse_operations(json_data)

        assert "Erro ao processar JSON" in str(excinfo.value)

    def test_parse_operations_com_tipo_de_dados_invalido(self):
        """Testa o parse de um JSON com tipo de dados inválido."""
        # Teste com preço unitário inválido
        json_data = '[{"operation":"buy", "unit-cost":"invalid", "quantity": 100}]'

        with pytest.raises(ParseError) as excinfo:
            JsonParser.parse_operations(json_data)

        assert "Erro ao processar JSON" in str(excinfo.value)

        # Teste com quantidade inválida
        json_data = '[{"operation":"buy", "unit-cost":10.00, "quantity": "invalid"}]'

        with pytest.raises(ParseError) as excinfo:
            JsonParser.parse_operations(json_data)

        assert "Erro ao processar JSON" in str(excinfo.value)

    def test_parse_operations_com_json_vazio(self):
        """Testa o parse de um JSON vazio."""
        json_data = "[]"

        operacoes = JsonParser.parse_operations(json_data)

        assert len(operacoes) == 0
        assert isinstance(operacoes, list)

    def test_parse_operations_com_espacos_e_quebras_de_linha(self):
        """Testa o parse de um JSON com espaços extras e quebras de linha."""
        json_data = """
        [
          {
            "operation": "buy",
            "unit-cost": 10.00,
            "quantity": 100
          }
        ]
        """

        operacoes = JsonParser.parse_operations(json_data)

        assert len(operacoes) == 1
        assert operacoes[0].tipo_operacao == TipoOperacao.BUY
        assert operacoes[0].preco_unitario == Decimal("10.00")
        assert operacoes[0].quantidade == 100
