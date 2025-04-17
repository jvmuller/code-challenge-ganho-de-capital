import pytest
from src.domain.exceptions.parse_error import ParseError


class TestParseError:
    def test_criar_excecao_parse_error(self):
        """Testa a criação de uma exceção ParseError."""
        # Criação simples da exceção
        erro = ParseError()
        assert isinstance(erro, Exception)
        assert isinstance(erro, ParseError)

    def test_criar_excecao_com_mensagem(self):
        """Testa a criação de uma exceção ParseError com mensagem."""
        mensagem = "Erro ao fazer parse do JSON"
        erro = ParseError(mensagem)
        assert str(erro) == mensagem

    def test_lancar_excecao(self):
        """Testa se a exceção pode ser lançada e capturada corretamente."""
        with pytest.raises(ParseError) as excinfo:
            raise ParseError("Formato de entrada inválido")

        assert "Formato de entrada inválido" in str(excinfo.value)

    def test_heranca_exception(self):
        """Testa se a exceção pode ser capturada por um bloco que captura Exception."""
        try:
            raise ParseError("Erro de parsing")
            assert False  # Não deve chegar aqui
        except Exception as e:
            assert isinstance(e, ParseError)
            assert "Erro de parsing" in str(e)
