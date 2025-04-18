FROM python:3.13.2-slim

WORKDIR /app

# Instala o Poetry
RUN pip install poetry==2.1.1

# Copia o código-fonte primeiro
COPY . ./

# Configura o Poetry para não criar um ambiente virtual
RUN poetry config virtualenvs.create false

# Instala as dependências
RUN poetry install

# Define o comando padrão para executar a aplicação
ENTRYPOINT ["python", "-m", "src.main"] 