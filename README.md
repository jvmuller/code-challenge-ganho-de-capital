# Code Challenge: Ganho de Capital

Este projeto é uma solução para o Code Challenge da Nubank sobre cálculo de ganho de capital.

## Requisitos

- Python 3.13.2
- Poetry

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
poetry install
```

## Estrutura do Projeto

```
code-challenge-ganho-de-capital/
│
├── src/                      # Código fonte principal
│   ├── domain/              # Regras de negócio e entidades
│   ├── application/         # Casos de uso da aplicação
│   ├── adapters/            # Adaptadores para I/O
│   └── main.py              # Ponto de entrada da aplicação
│
├── tests/                   # Testes automatizados
│   ├── unit/               # Testes unitários
│   ├── integration/        # Testes de integração
│   └── fixtures/           # Dados de teste
```

## Desenvolvimento

Para executar os testes:

```bash
poetry run pytest
```

Para formatar o código:

```bash
poetry run black .
```

Para verificar tipos:

```bash
poetry run mypy .
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
