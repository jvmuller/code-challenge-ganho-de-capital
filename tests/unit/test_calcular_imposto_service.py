from decimal import Decimal
from unittest.mock import Mock

import pytest
from src.domain.models.investimento import Investimento
from src.domain.models.operacao import Operacao, TipoOperacao
from src.domain.services.calcular_imposto_service import CalcularImpostoService


class TestCalcularImpostoService:
    def setup_method(self):
        """Configuração inicial para cada teste."""
        self.service = CalcularImpostoService()

    def test_calcular_impostos_compra_simples(self):
        """Testa o cálculo de impostos para uma operação de compra."""
        operacoes = [Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10"), quantidade=100)]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 1
        assert impostos[0] == Decimal("0")

    def test_calcular_impostos_compra_e_venda_com_lucro_abaixo_do_limite(self):
        """Testa o cálculo de impostos para compra e venda com lucro abaixo do limite de isenção."""
        operacoes = [
            Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10"), quantidade=100),
            Operacao(tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("15"), quantidade=50),
        ]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 2
        assert impostos[0] == Decimal("0")  # Não há imposto na compra
        assert impostos[1] == Decimal("0")  # Não há imposto na venda (abaixo do limite)

    def test_calcular_impostos_compra_e_venda_com_lucro_acima_do_limite(self):
        """Testa o cálculo de impostos para compra e venda com lucro acima do limite de isenção."""
        operacoes = [
            Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10"), quantidade=2000),  # 20.000
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("20"), quantidade=2000
            ),  # 40.000 (lucro: 20.000)
        ]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 2
        assert impostos[0] == Decimal("0")  # Não há imposto na compra
        assert impostos[1] == Decimal("4000.00")  # 20% de 20.000 = 4.000

    def test_calcular_impostos_compra_e_venda_com_prejuizo(self):
        """Testa o cálculo de impostos para compra e venda com prejuízo."""
        operacoes = [
            Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("30"), quantidade=1000),  # 30.000
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("20"), quantidade=1000
            ),  # 20.000 (prejuízo: 10.000)
        ]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 2
        assert impostos[0] == Decimal("0")  # Não há imposto na compra
        assert impostos[1] == Decimal("0")  # Não há imposto no prejuízo

    def test_calcular_impostos_multiples_operacoes_com_compensacao_prejuizo(self):
        """Testa o cálculo de impostos para múltiplas operações com compensação de prejuízo."""
        operacoes = [
            Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10"), quantidade=1000),  # 10.000
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("5"), quantidade=500
            ),  # 2.500 (prejuízo: 2.500)
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("20"), quantidade=500
            ),  # 10.000 (lucro: 5.000, mas compensado)
        ]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 3
        assert impostos[0] == Decimal("0")  # Não há imposto na compra
        assert impostos[1] == Decimal("0")  # Não há imposto no prejuízo
        # Na terceira operação, temos lucro de 5.000, mas o prejuízo acumulado é 2.500
        # Então o lucro tributável é 2.500, mas ainda está abaixo do limite de isenção
        assert impostos[2] == Decimal("0")

    def test_calcular_impostos_venda_acima_limite_com_prejuizo_anterior(self):
        """Testa o cálculo de impostos para venda acima do limite com prejuízo anterior."""
        operacoes = [
            Operacao(tipo_operacao=TipoOperacao.BUY, preco_unitario=Decimal("10"), quantidade=5000),  # 50.000
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("8"), quantidade=2000
            ),  # 16.000 (prejuízo: 4.000)
            Operacao(
                tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("15"), quantidade=3000
            ),  # 45.000 (lucro: 15.000)
        ]

        impostos = self.service.calcular_impostos(operacoes)

        assert len(impostos) == 3
        assert impostos[0] == Decimal("0")  # Não há imposto na compra
        assert impostos[1] == Decimal("0")  # Não há imposto no prejuízo
        # Lucro: 15.000, prejuízo acumulado: 4.000, lucro tributável: 11.000
        # 11.000 * 0.20 = 2.200
        assert impostos[2] == Decimal("2200.00")

    def test_metodo_calcular_lucro_ou_prejuizo(self):
        """Testa o método _calcular_lucro_ou_prejuizo."""
        investimento = Investimento()
        investimento.adicionar_acao(100, Decimal("10"))

        operacao_lucro = Operacao(tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("15"), quantidade=50)
        operacao_prejuizo = Operacao(tipo_operacao=TipoOperacao.SELL, preco_unitario=Decimal("5"), quantidade=50)

        lucro = self.service._calcular_lucro_ou_prejuizo(investimento, operacao_lucro)
        prejuizo = self.service._calcular_lucro_ou_prejuizo(investimento, operacao_prejuizo)

        assert lucro == Decimal("250")  # (15 - 10) * 50
        assert prejuizo == Decimal("-250")  # (5 - 10) * 50

    def test_metodo_calcular_imposto_sem_lucro(self):
        """Testa o método _calcular_imposto quando não há lucro."""
        imposto = self.service._calcular_imposto(
            lucro_bruto=Decimal("0"), prejuizo_acumulado=Decimal("0"), valor_operacao=Decimal("30000")
        )
        assert imposto == Decimal("0")

        imposto = self.service._calcular_imposto(
            lucro_bruto=Decimal("-1000"), prejuizo_acumulado=Decimal("0"), valor_operacao=Decimal("30000")
        )
        assert imposto == Decimal("0")

    def test_metodo_calcular_imposto_abaixo_limite(self):
        """Testa o método _calcular_imposto quando o valor é abaixo do limite de isenção."""
        imposto = self.service._calcular_imposto(
            lucro_bruto=Decimal("5000"), prejuizo_acumulado=Decimal("0"), valor_operacao=Decimal("19000")
        )
        assert imposto == Decimal("0")

    def test_metodo_calcular_imposto_com_prejuizo_acumulado(self):
        """Testa o método _calcular_imposto quando há prejuízo acumulado."""
        imposto = self.service._calcular_imposto(
            lucro_bruto=Decimal("10000"), prejuizo_acumulado=Decimal("6000"), valor_operacao=Decimal("30000")
        )
        # Lucro líquido: 10.000 - 6.000 = 4.000
        # Imposto: 4.000 * 0.20 = 800
        assert imposto == Decimal("800.00")

    def test_metodo_calcular_imposto_com_prejuizo_maior_que_lucro(self):
        """Testa o método _calcular_imposto quando o prejuízo acumulado é maior que o lucro."""
        imposto = self.service._calcular_imposto(
            lucro_bruto=Decimal("5000"), prejuizo_acumulado=Decimal("10000"), valor_operacao=Decimal("30000")
        )
        assert imposto == Decimal("0")

    def test_constantes_do_service(self):
        """Testa as constantes definidas no serviço."""
        assert self.service.ALIQUOTA_IMPOSTO == Decimal("0.20")
        assert self.service.LIMITE_ISENCAO_IMPOSTO == Decimal("20000.00")
