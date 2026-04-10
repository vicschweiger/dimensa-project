# Desafio para vaga Python - Dimensa

Este projeto é uma API desenvolvida em Python (Flask) para consulta e armazenamento de informações geográficas de endereços IP. O sistema utiliza Celery com Redis para processamento assíncrono e MongoDB Atlas como banco de dados persistente, tudo orquestrado via Docker.

<br>

## 🛠️ Tecnologias Utilizadas

* Linguagem: Python 3.12

* Framework: Flask

* Banco de Dados: MongoDB Atlas

* Mensageiro: Redis

* Processamento de Tarefas: Celery

* Containerização: Docker e Docker Compose

* Versionamento de código: GitHub

<br>

## 📂 Controle de Versão

**Repositório:** [GitHub](https://github.com/vicschweiger/dimensa-project)

**Status do Projeto:** Finalizado / Estável

<br>

## 🏗️ Arquitetura do Sistema

A aplicação foi desenhada para ser escalável e segura:

>API Flask: Recebe as requisições, valida o token de segurança e interage com o banco de dados.

>Celery Worker: Executa tarefas em segundo plano (como a atualização periódica de dados via ipwhois) para não travar a resposta da API.

>Redis: Atua como o mensageiro entre a API e o Worker.

<br>

## ⚙️ Como Executar o Projeto

1. **Pré-requisitos**

Ter o Docker e o Docker Compose instalados em sua máquina.

Extensão REST Client no VS Code (recomendada para executar os arquivos de teste .http incluídos no corpo do projeto).

<br>

2. **Configuração de Variáveis de Ambiente**

Por questões de segurança, o arquivo .env não foi versionado.

>Na raiz do projeto, haverá um arquivo chamado .env.example. Crie um arquivo chamado .env e siga o arquivo modelo .env.example inserindo a string de conexão do MongoDB (MONGO_URI) que foi enviada no corpo do e-mail de entrega deste teste.

<br>

3. **Subindo os Containers**

No terminal, dentro da pasta do projeto, execute:

    docker-compose up --build

Aguarde a inicialização. A API estará disponível em: http://localhost:8000

<br>

## 🧪 Como Testar

Na pasta raiz, existem arquivos com a extensão .http que podem ser usados com a extensão REST Client do VS Code:

>test_post.http: Envia um IP para cadastro, processamento ou consulta.

>test_get.http: Lista todos os IPs cadastrados (com paginação).

>test_filter.http: Busca e filtra IPs específicos por número.

`O SECRET_TOKEN padrão para este teste é "dimensa_aprovou", já preenchido no arquivo de exemplo (.env.example).`

`Nota: Todas as requisições requerem o header Authorization: Bearer dimensa_aprovou.`

<br>

## 📌 Decisões Técnicas

Porta 8000: Escolhida para evitar conflitos comuns com serviços de sistema na porta 5000.

Mapeamento de Portas: Escolhida a porta 8000 para evitar conflitos comuns com serviços de sistema na porta 5000. Foi utilizado o mapeamento 8000:5000 no Docker Compose para garantir portabilidade entre diferentes sistemas operacionais.

Isolamento de Ambiente: O uso de Docker garante que a aplicação rode exatamente da mesma forma em qualquer máquina, eliminando erros.

Segurança: Implementação de autenticação via Token (Bearer) e isolamento de variáveis sensíveis.

Escalabilidade: A separação entre API e Worker permite que o processamento de IPs seja feito de forma assíncrona, aumentando a performance da resposta ao usuário.

<br>

## Notas de Desenvolvimento

O projeto foi desenvolvido utilizando GitHub Codespaces para garantir agilidade e um ambiente de desenvolvimento padronizado durante o processo. Para assegurar a portabilidade total, o sistema foi validado e testado localmente em ambiente Windows/Linux via Docker, garantindo que o mapeamento de portas e a orquestração dos containers funcionem perfeitamente em qualquer host ou sistema.