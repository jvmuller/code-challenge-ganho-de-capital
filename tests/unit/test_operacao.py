from decimal import Decimal

import pytest
from src.domain.models.operacao import Operacao, TipoOperacao


class TestOperacao:
    def test_criacao_operacao_compra(self):
        """Testa a criação de uma operação de compra."""
        operacao = Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10.5"), quantidade=100)

        assert operacao.tipo_operacao == TipoOperacao.BUY
        assert operacao.preco_unitario == Decimal("10.5")
        assert operacao.quantidade == 100
        assert operacao.valor_total == Decimal("1050")

    def test_criacao_operacao_venda(self):
        """Testa a criação de uma operação de venda."""
        operacao = Operacao(tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("25.75"), quantidade=50)

        assert operacao.tipo_operacao == TipoOperacao.SELL
        assert operacao.preco_unitario == Decimal("25.75")
        assert operacao.quantidade == 50
        assert operacao.valor_total == Decimal("1287.5")

    def test_frozen_dataclass(self):
        """Testa se a dataclass é frozen (imutável)."""
        operacao = Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("15.0"), quantidade=200)

        with pytest.raises(Exception):
            operacao.quantidade = 300

    def test_valores_extremos(self):
        """Testa a criação com valores extremos."""
        # Teste com valor muito grande
        operacao_grande = Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("9999.99"), quantidade=10000)
        assert operacao_grande.valor_total == Decimal("99999900")

        # Teste com valor muito pequeno
        operacao_pequena = Operacao(tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("0.01"), quantidade=1)
        assert operacao_pequena.valor_total == Decimal("0.01")

    def test_enum_tipo_operacao(self):
        """Testa o enum TipoOperacao."""
        assert TipoOperacao.BUY.value == "buy"
        assert TipoOperacao.SELL.value == "sell"

        # Verificar se podemos criar a partir da string
        assert TipoOperacao("buy") == TipoOperacao.BUY
        assert TipoOperacao("sell") == TipoOperacao.SELL
