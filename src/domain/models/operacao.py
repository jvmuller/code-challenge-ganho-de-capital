from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class TipoOperacao(Enum):
    """Enum para representar o tipo de operação."""

    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class Operacao:
    """Classe para representar uma operação.

    Args:
        tipo_operacao: Se a operação é uma operação de compra (buy) ou venda (sell)
        preco_unitario: Preço unitário da ação em uma moeda com duas casas decimais
        quantidade: Quantidade de ações negociadas
    """

    tipo_operacao: TipoOperacao
    preco_unitario: Decimal
    quantidade: int

    @property
    def valor_total(self) -> Decimal:
        """Calcula o valor total da operação."""
        return self.preco_unitario * self.quantidade
