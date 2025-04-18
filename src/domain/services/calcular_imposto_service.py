from decimal import Decimal
from typing import List

from src.domain.models.investimento import Investimento
from src.domain.models.operacao import Operacao, TipoOperacao


class CalcularImpostoService:
    """Serviço para calcular o imposto a ser pago sobre lucros ou prejuízos de operações no mercado financeiro."""

    ALIQUOTA_IMPOSTO = Decimal("0.20")
    LIMITE_ISENCAO_IMPOSTO = Decimal("20000.00")

    def calcular_impostos(self, operacoes: List[Operacao]) -> List[Decimal]:
        """Calcula o imposto para uma lista de operações."""
        impostos = []
        investimento = Investimento()
        prejuizo_acumulado = Decimal("0")

        for operacao in operacoes:
            if operacao.tipo_operacao == TipoOperacao.BUY:
                investimento.adicionar_acao(operacao.quantidade, operacao.preco_unitario)
                impostos.append(Decimal("0"))
            else:
                lucro_ou_prejuizo = self._calcular_lucro_ou_prejuizo(investimento, operacao)
                imposto = self._calcular_imposto(lucro_ou_prejuizo, prejuizo_acumulado, operacao.valor_total)

                if lucro_ou_prejuizo < 0:
                    prejuizo_acumulado += abs(lucro_ou_prejuizo)
                elif operacao.valor_total > self.LIMITE_ISENCAO_IMPOSTO and lucro_ou_prejuizo > 0:
                    prejuizo_acumulado = max(Decimal("0"), prejuizo_acumulado - lucro_ou_prejuizo)

                investimento.remover_acao(operacao.quantidade)
                impostos.append(imposto)

        return impostos

    def _calcular_lucro_ou_prejuizo(self, investimento: Investimento, operacao: Operacao) -> Decimal:
        """Calcula o lucro ou prejuizo de uma operação de venda."""
        preco_medio = investimento.preco_medio
        return (operacao.preco_unitario - preco_medio) * operacao.quantidade

    def _calcular_imposto(self, lucro_bruto: Decimal, prejuizo_acumulado: Decimal, valor_operacao: Decimal) -> Decimal:
        """Calcula o imposto considerando prejuízos acumulados e o limite de isenção."""
        if lucro_bruto <= 0:
            return Decimal("0")

        lucro_liquido = max(Decimal("0"), lucro_bruto - prejuizo_acumulado)

        if valor_operacao <= self.LIMITE_ISENCAO_IMPOSTO:
            return Decimal("0")

        return (lucro_liquido * self.ALIQUOTA_IMPOSTO).quantize(Decimal("0.01"))
