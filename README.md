# Salonsuite

Este é um projeto desenvolvido com [FastAPI](https://fastapi.tiangolo.com/) e [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/), utilizando o gerenciador de dependências [Poetry](https://python-poetry.org/).

## Pré-requisitos

- Python 3.12 ou superior
- Poetry instalado (veja [como instalar o Poetry](https://python-poetry.org/docs/#installation))

## Configuração do ambiente

1. Clone este repositório para sua máquina local:

   ```bash
   git clone https://github.com/seu-usuario/salonsuite.git
   cd salonsuite
   ```

2. Instale as dependências do projeto com o Poetry:

   ```bash
   poetry install
   ```

3. Ative o ambiente virtual gerenciado pelo Poetry:

   ```bash
   poetry shell
   ```

## Como popular o banco de dados

Após configurar o ambiente, você pode popular o banco de dados com os dados iniciais. Para isso, siga os passos abaixo:

1. Certifique-se de que você está no ambiente virtual (se não estiver, execute `poetry shell`).
2. Execute o script de seeds para popular o banco de dados:

   ```bash
   python salonsuite/seeds/main.py
   ```

Este script criará os dados iniciais necessários para o funcionamento da aplicação.

## Executando a aplicação

Para iniciar a aplicação, utilize o seguinte comando:

```bash
task run
```

Acesse a documentação interativa em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).


## Contribuição

Se você quiser contribuir para este projeto, abra uma issue ou envie um pull request. Toda ajuda é bem-vinda!

---

**Nota:** Certifique-se de ter o banco de dados configurado antes de executar a aplicação ou os seeds. Se estiver usando SQLite, o banco será criado automaticamente.
``` 

### Personalizações
- Altere o nome do repositório e os caminhos caso eles sejam diferentes no seu projeto.
- Adicione informações específicas do projeto, se necessário.