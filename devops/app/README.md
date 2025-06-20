# Bootcamp de Integração

Este README é um guia para o Bootcamp de Integração, cobrindo os conceitos teóricos de microsserviços e APIs, e a parte prática focada na execução de uma aplicação Streamlit com Docker.

## 💡 Introdução e Motivação

Em arquiteturas de software, a forma como diferentes componentes se comunicam é crucial. A integração de sistemas conecta sistemas e aplicativos para que trabalhem juntos. Historicamente, sistemas monolíticos centralizavam todas as funcionalidades, mas causavam problemas de escalabilidade e manutenção.

A agilidade, escalabilidade e resiliência impulsionaram a adoção de arquiteturas distribuídas, como os **Microsserviços**.

## 🔄 Microsserviços

Microsserviços são uma abordagem arquitetural onde um aplicativo é construído como uma coleção de pequenos serviços independentes que se comunicam entre si.

### Características dos Microsserviços:

  * **Pequenos e Focados**: Cada microsserviço geralmente se concentra em uma única funcionalidade de negócio.
  * **Independentes**: Podem ser desenvolvidos, implantados e escalados de forma independente.
  * **Comunicam-se via APIs**: A comunicação entre microsserviços ocorre geralmente através de APIs bem definidas.
  * **Tecnologias Híbridas**: Diferentes microsserviços podem ser escritos em diferentes linguagens de programação e usar diferentes bancos de dados.
  * **Resiliência**: A falha em um microsserviço não necessariamente derruba todo o sistema.

### Vantagens:

  * **Escalabilidade**: Componentes específicos podem ser escalados independentemente.
  * **Agilidade**: Equipes pequenas podem desenvolver e implantar mais rapidamente.
  * **Resiliência**: Falhas isoladas não afetam todo o sistema.
  * **Flexibilidade Tecnológica**: Permite o uso de tecnologias diferentes para cada serviço.

### Desvantagens:

  * **Complexidade**: Aumento da complexidade de gerenciamento e monitoramento.
  * **Distribuição**: Desafios na comunicação e consistência de dados.
  * **Deploy**: Exige automação e ferramentas de orquestração.

## 🔌 APIs (Application Programming Interfaces)

APIs são conjuntos de definições e protocolos que permitem que um software se comunique com outro. Em uma arquitetura de microsserviços, as APIs são o principal meio de comunicação entre os serviços.

### Tipos de APIs Comuns:

  * **REST (Representational State Transfer)**: É um estilo arquitetural para sistemas distribuídos. APIs RESTful usam métodos HTTP (GET, POST, PUT, DELETE) para interagir com recursos.
      * **GET**: Recupera dados.
      * **POST**: Cria novos dados.
      * **PUT**: Atualiza dados existentes.
      * **DELETE**: Remove dados.
  * **SOAP (Simple Object Access Protocol)**: Um protocolo baseado em XML para troca de mensagens estruturadas em redes de computador. Geralmente mais robusto e complexo.
  * **GraphQL**: Uma linguagem de consulta para APIs e um tempo de execução para executar essas consultas com seus dados existentes. Permite que os clientes solicitem exatamente os dados de que precisam.

## 🤝 Integração de Sistemas

A integração é o processo de conectar diferentes sistemas de software e aplicativos para permitir que trabalhem juntos como um todo coeso. No contexto de microsserviços, a integração acontece principalmente através do consumo e exposição de APIs.

### Desafios da Integração:

  * **Compatibilidade de Dados**: Diferentes sistemas podem ter formatos de dados distintos.
  * **Performance**: A comunicação entre serviços pode introduzir latência.
  * **Segurança**: Garantir a segurança das comunicações.
  * **Monitoramento**: Dificuldade em rastrear transações através de múltiplos serviços.

### Estratégias de Integração:

  * **Orquestração**: Um serviço central controla o fluxo de trabalho e coordena a comunicação entre outros serviços.
  * **Coreografia**: Serviços se comunicam independentemente através de eventos, sem um coordenador central.
  * **Barramento de Serviço Corporativo (ESB)**: Um middleware que fornece roteamento, transformação e comunicação entre aplicações.

## Parte Prática: Executando uma Aplicação Streamlit com Docker

Esta seção demonstra como construir e executar uma aplicação Streamlit em um container Docker, utilizando o modo de rede `host` para facilitar a comunicação.

### Pré-requisitos:

  * **Docker Desktop** (ou Docker Engine) instalado em seu sistema operacional (Windows, macOS, Linux).
      * Para instalação do Docker Desktop, consulte a [documentação oficial](https://www.google.com/search?q=https://docs.docker.com/desktop/install/).
  * **Repositório com o `Dockerfile` e a aplicação Streamlit**: Assumimos que você possui um diretório `devops/app` contendo seu `Dockerfile` e os arquivos da aplicação Streamlit.

### 1\. Navegar até o Diretório da Aplicação

Primeiro, você precisa navegar até o diretório que contém seu `Dockerfile` e os arquivos da aplicação.

```bash
cd devops/app
```

### 2\. Construir a Imagem Docker

Dentro do diretório `devops/app`, execute o comando `docker build` para criar a imagem Docker da sua aplicação Streamlit.

```bash
docker build -t streamlit-app .
```

  * `-t streamlit-app`: Atribui a tag (nome) `streamlit-app` à sua imagem Docker, facilitando a referência posterior.
  * `.`: Indica que o contexto de construção do Docker é o diretório atual, onde o `Dockerfile` deve estar localizado.

### 3\. Executar o Container Docker

Após a imagem ser construída, você pode executá-la como um container. Utilizaremos a opção `--network=host` para que o container compartilhe a pilha de rede do host, o que simplifica o acesso à aplicação Streamlit, que geralmente roda na porta 8501 por padrão.

```bash
docker run --network=host streamlit-app
```

  * `--network=host`: Esta opção faz com que o container use diretamente a interface de rede do seu host. Isso significa que, se sua aplicação Streamlit estiver rodando na porta 8501 dentro do container, ela estará acessível diretamente em `http://localhost:8501` (ou `http://127.0.0.1:8501`) no seu navegador, sem a necessidade de mapeamento explícito de portas (`-p`).
  * `streamlit-app`: O nome da imagem Docker que você construiu na etapa anterior.

Após executar este comando, o container será iniciado e a aplicação Streamlit deverá estar acessível no seu navegador.

**Para acessar a aplicação Streamlit:**

Abra seu navegador e navegue para:

```
http://localhost:8501
```

Você deverá ver sua aplicação Streamlit em execução.

-----

## 📚 Referências

- [vLLM Project GitHub](https://github.com/vllm-project/vllm): Repositório oficial do vLLM, uma biblioteca rápida e fácil de usar para inferência e serviço de LLMs.
- [vLLM Documentation: CPU Installation](https://docs.vllm.ai/en/v0.7.3/getting_started/installation/cpu/index.html): Guia oficial de instalação do vLLM para plataformas x86 CPU.
- [PagedAttention: Efficient Attention for LLMs (paper)](https://arxiv.org/pdf/2309.06180): Artigo que introduz a técnica PagedAttention para otimizar o uso de memória em LLMs.
- [AWS: O que é Geração Aumentada por Recuperação (RAG)](https://aws.amazon.com/what-is/retrieval-augmented-generation/): Explicação sobre o conceito de RAG e como ele aprimora a geração de texto em LLMs.
- [AWS: Microsserviços](https://aws.amazon.com/pt/microservices/#:~:text=Microsservi%C3%A7os%20s%C3%A3o%20uma%20abordagem%20arquitet%C3%B4nica,comunicam%20usando%20APIs%20bem%20definidas.): Definição e benefícios da arquitetura de microsserviços.
- [AI SDK: Foundations - Streaming](https://ai-sdk.dev/docs/foundations/streaming): Documentação sobre como implementar interfaces de usuário com streaming de dados em tempo real.
- [Developer Roadmap - GitHub](https://github.com/kamranahmedse/developer-roadmap): Mapas interativos e guias educacionais para ajudar desenvolvedores a crescerem em suas carreiras.
- [Qwen2-1.5B-Instruct - Hugging Face](https://huggingface.co/Qwen/Qwen2-1.5B-Instruct): Modelo de linguagem Qwen2-1.5B ajustado para instruções, disponível no Hugging Face.
