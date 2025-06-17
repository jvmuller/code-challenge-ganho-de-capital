from decimal import Decimal

import pytest
from src.domain.models.investimento import Investimento


class TestInvestimento:
    def test_investimento_inicializacao(self):
        """Testa se o investimento é inicializado corretamente com zero ações e preço médio zero."""
        investimento = Investimento()
        assert investimento.quantidade == 0
        assert investimento.preco_medio == Decimal("0")
        assert investimento.valor_total == Decimal("0")

    def test_adicionar_acao_em_investimento_vazio(self):
        """Testa a adição de ações em um investimento vazio."""
        investimento = Investimento()
        investimento.adicionar_acao(10, Decimal("25.5"))

        assert investimento.quantidade == 10
        assert investimento.preco_medio == Decimal("25.5")
        assert investimento.valor_total == Decimal("255")

    def test_adicionar_acao_em_investimento_existente(self):
        """Testa a adição de ações em um investimento que já possui ações."""
        investimento = Investimento()
        investimento.adicionar_acao(10, Decimal("20"))
        investimento.adicionar_acao(5, Decimal("30"))

        # Verificação correta: (10*20 + 5*30) / 15 = (200 + 150) / 15 = 350 / 15 = 23.333...
        assert investimento.quantidade == 15
        valor_esperado = (Decimal("10") * Decimal("20") + Decimal("5") * Decimal("30")) / Decimal("15")
        assert investimento.preco_medio == valor_esperado
        assert investimento.valor_total == valor_esperado * Decimal("15")

    def test_adicionar_acao_com_quantidade_invalida(self):
        """Testa a adição de ações com quantidade inválida (menor ou igual a zero)."""
        investimento = Investimento()

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            investimento.adicionar_acao(0, Decimal("20"))

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            investimento.adicionar_acao(-5, Decimal("20"))

    def test_remover_acao_parcial(self):
        """Testa a remoção parcial de ações de um investimento."""
        investimento = Investimento()
        investimento.adicionar_acao(10, Decimal("20"))
        investimento.remover_acao(5)

        assert investimento.quantidade == 5
        assert investimento.preco_medio == Decimal("20")
        assert investimento.valor_total == Decimal("100")

    def test_remover_acao_total(self):
        """Testa a remoção de todas as ações de um investimento."""
        investimento = Investimento()
        investimento.adicionar_acao(10, Decimal("20"))
        investimento.remover_acao(10)

        assert investimento.quantidade == 0
        assert investimento.preco_medio == Decimal("0")
        assert investimento.valor_total == Decimal("0")

    def test_remover_acao_com_quantidade_invalida(self):
        """Testa a remoção de ações com quantidade inválida (menor ou igual a zero)."""
        investimento = Investimento()
        investimento.adicionar_acao(10, Decimal("20"))

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            investimento.remover_acao(0)

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            investimento.remover_acao(-5)

    # def test_remover_acao_maior_que_disponivel(self):
    #     """Testa a remoção de ações em quantidade maior que a disponível."""
    #     investimento = Investimento()
    #     investimento.adicionar_acao(10, Decimal("20"))

    #     with pytest.raises(
    #         ValueError, match="Não é possível remover 15 ações. O investimento possui apenas 10 ações."
    #     ):
    #         investimento.remover_acao(15)
