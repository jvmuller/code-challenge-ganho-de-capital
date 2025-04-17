from decimal import Decimal


class Investimento:
    """Representa um investimento em ações."""

    def __init__(self):
        """Inicializa o investimento com zero ações e preço médio zero."""
        self._quantidade: int = 0
        self._preco_medio: Decimal = Decimal("0")

    @property
    def quantidade(self) -> int:
        """Retorna a quantidade atual de ações investidas."""
        return self._quantidade

    @property
    def preco_medio(self) -> Decimal:
        """Retorna o preço médio das ações investidas."""
        return self._preco_medio

    @property
    def valor_total(self) -> Decimal:
        """Retorna o valor total do investimento."""
        return self._preco_medio * self._quantidade

    def adicionar_acao(self, quantidade: int, preco_unitario: Decimal) -> None:
        """Adiciona uma quantidade de ações ao investimento e recalcula o preço médio ponderado."""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        if self._quantidade == 0:
            self._preco_medio = preco_unitario
            self._quantidade = quantidade
        else:
            valor_atual_total = self._preco_medio * Decimal(self._quantidade)
            valor_novo_total = preco_unitario * Decimal(quantidade)
            quantidade_total = self._quantidade + quantidade

            self._preco_medio = (valor_atual_total + valor_novo_total) / Decimal(quantidade_total)
            self._quantidade = quantidade_total

    def remover_acao(self, quantidade: int) -> None:
        """Remove uma quantidade de ações do investimento e reseta o preço médio se todas as ações forem removidas."""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        if quantidade > self._quantidade:
            raise ValueError(
                f"Não é possível remover {quantidade} ações. O investimento possui apenas {self._quantidade} ações."
            )

        self._quantidade -= quantidade

        if self._quantidade == 0:
            self._preco_medio = Decimal("0")
