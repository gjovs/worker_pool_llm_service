# Worker pool LLM service - Análise de Documentos

![Python](https://img.shields.io/badge/Python-3.15-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-4284f4.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-008cc1.svg)
![Redis](https://img.shields.io/badge/Redis-dc382d.svg)

## Descrição do Projeto

Este serviço é um worker assíncrono e isolado, responsável por toda a carga de processamento de Inteligência Artificial para o Módulo de Gestão de Documentos. Seu design foi focado em eficiência, escalabilidade e otimização de custos.

### Principais Funcionalidades

- **Consumo de Tarefas:** O serviço escuta uma fila no **Redis** (`tasks_queue`) para receber novas solicitações de análise de documentos.
- **Processamento de PDF:** Baixa arquivos PDF a partir de URLs e extrai seu conteúdo textual para análise.
- **Cache de Similaridade com Neo4j:** Para reduzir custos e latência de APIs de LLM, o serviço implementa uma camada de cache vetorial. Documentos com alto grau de similaridade semântica têm seus insights reutilizados.
- [cite_start]**Análise de Conteúdo com LLM:** Integra-se com a API da **OpenAI** para gerar análises detalhadas, resumos e identificar cláusulas faltantes em documentos[cite: 26, 34].
- **Streaming de Resultados:** Publica os resultados da análise token por token em um canal **Redis Pub/Sub**, permitindo que a API principal retransmita esses dados em tempo real para o cliente via SSE.
- **Persistência:** Salva o resultado final e completo da análise no banco de dados principal **PostgreSQL**.

## Como Executar o Projeto

### Pré-requisitos

- Docker & Docker Compose
- Um arquivo `.env` configurado na raiz do monorepo com as chaves para `OPENAI`, `NEO4J`, `POSTGRES` e `REDIS`.

### Executando com Docker (Recomendado)

O `docker-compose.yml` na raiz do projeto já orquestra este serviço. Para executá-lo:

```bash
# Para iniciar um único worker
docker-compose up ai_service

# Para iniciar um "pool" de 3 workers em paralelo
docker-compose up --scale ai_service=3
```

### Executando Localmente (Para Desenvolvimento)

O projeto inclui um `Makefile` para facilitar o setup.

```bash
# Navegue até a pasta do serviço
cd ai_service/

# Crie o ambiente virtual e instale as dependências
make setup

# Inicie o worker
make run
```
