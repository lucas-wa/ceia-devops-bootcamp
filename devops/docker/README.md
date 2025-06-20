# Fundamentos de Docker

Este repositório contém os fundamentos sobre Docker, abordando desde a motivação para seu uso até a execução de containers.

## 💡 Motivação para usar Docker

Tradicionalmente, ao implantar várias aplicações em um único servidor, surgem problemas de dependências e conflitos entre elas, pois todas compartilham o mesmo ambiente e sistema operacional (SO).

A virtualização resolve parte desse problema ao permitir que cada aplicação seja executada em sua própria Máquina Virtual (VM) com seu próprio SO virtualizado (como no VMware), isolando as dependências. No entanto, um SO completo, mesmo virtualizado, consome muitos recursos (sistema de arquivos, interface gráfica, gerenciador de processos, controlador de I/O, controle de rede, segurança, etc.). Em muitos casos, as aplicações não necessitam de todos esses recursos.

## 📦 Containers

Containers oferecem uma alternativa mais leve à virtualização. Ao invés de virtualizar um SO completo para cada aplicação, os containers compartilham o kernel do SO do host. Isso significa que cada aplicação é empacotada em seu próprio container, isolada das outras, mas sem a sobrecarga de um SO completo por trás de cada uma.

## 🐳 O que é Docker?

Docker é uma plataforma que facilita a implementação e gerenciamento de containers. É uma tecnologia popular, com uma comunidade ativa e um "Hub" (Docker Hub) para compartilhamento de imagens. Sua adoção é ampla em ambientes de cloud, sendo open source. Exemplos de serviços em nuvem que utilizam a tecnologia de containers incluem Google Cloud Run (GCP) e AWS Fargate.

## 🖼️ Imagens Docker

Containers são instâncias executáveis criadas a partir de imagens. Uma imagem define os recursos e comandos que um container precisa para rodar uma aplicação. É importante notar que imagens não são containers; elas são os "modelos" a partir dos quais os containers são gerados.

Para listar as imagens Docker disponíveis localmente, utilize o comando:

```bash
docker images
```

## 📝 Dockerfile

Um Dockerfile é um arquivo de texto que descreve como uma imagem Docker será construída. Ele é geralmente montado com referência a uma pasta local que contém os arquivos da aplicação.

Exemplo de um Dockerfile (o conteúdo exato dependerá da sua aplicação):

```dockerfile
# Exemplo de Dockerfile (pode variar)
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```


## ⚙️ Construindo uma Imagem (Build)

Após criar seu Dockerfile, você pode construir a imagem Docker usando o comando `docker build`:

```bash
docker build -f <DOCKERFILE_PATH> -t <CONTAINER_NAME> .
```


  * `<DOCKERFILE_PATH>`: Caminho para o seu Dockerfile (ex: `Dockerfile`).
  * `<CONTAINER_NAME>`: Um nome para a sua imagem (ex: `minha-app-docker`). Opcionalmente, pode-se adicionar uma tag, como `minha-app-docker:v1.0`.
  * `.`: Indica o contexto de build, geralmente o diretório atual onde o Dockerfile está localizado.

## 🚀 Executando um Container (Run)

Uma vez que a imagem é construída, o container pode ser executado com base nela. O comando `docker run` permite iniciar um container e pode incluir parâmetros específicos que diferenciam containers criados a partir da mesma imagem.

Para executar um container e mapear portas, utilize:

```bash
docker run -p <OUT_PORT>:<IN_PORT> -it <CONTAINER_NAME>
```


  * `<OUT_PORT>`: A porta no seu host (máquina local) que você deseja expor.
  * `<IN_PORT>`: A porta interna no container onde sua aplicação está rodando.
  * `-it`: Combinação de `-i` (modo interativo) e `-t` (aloca um pseudo-TTY), que permite interagir com o container.
  * `<CONTAINER_NAME>`: O nome da imagem que você construiu.

**Exemplo de execução:*
Se sua aplicação no container roda na porta 8501, e você quer acessá-la pela porta 8501 do seu host:

```bash
docker run -p 8501:8501 -it streamlit-app
```



## 🔄 Fluxo de Trabalho do Docker

O fluxo básico do Docker é:
**Dockerfile (descreve a imagem) ➡️ build (cria a imagem) ➡️ Imagem (modelo do container) ➡️ run (executa o container) ➡️ Container (instância em execução)**.

## 🌐 Rede em Containers

Ao executar um container com o comando `-p <OUT_PORT>:<IN_PORT>`, o Docker configura a rede para que o tráfego da `<OUT_PORT>` no host seja encaminhado para a `<IN_PORT>` dentro do container. Isso permite que aplicações externas se comuniquem com a aplicação em execução no container.

## 💾 Volumes em Containers

Volumes Docker permitem persistir dados gerados por e usados por containers, mesmo após o container ser removido. Eles também são usados para compartilhar dados entre o host e o container.

Para montar um volume, utilize:

```bash
docker run -v <OUT_PATH>:<IN_PATH> -it <CONTAINER_NAME>
```

  * `<OUT_PATH>`: O caminho no seu host (máquina local).
  * `<IN_PATH>`: O caminho dentro do container onde o volume será montado.

## ✨ Exercício Prático: Hello World com Docker

Vamos criar uma aplicação "Hello World" simples e Dockerizá-la.

### Requisitos:

1.  **Docker Desktop** (ou Docker Engine) instalado em seu sistema operacional (Windows, macOS, Linux).
      * [Instalação do Docker Desktop](https://www.google.com/search?q=https://docs.docker.com/desktop/install/)
2.  Um editor de texto.

### Etapas:

1.  **Crie um diretório para o seu projeto:**

    ```bash
    mkdir docker-hello-world
    cd docker-hello-world
    ```

2.  **Crie um arquivo Python simples (`app.py`):**

    ```python
    # app.py
    print("Hello, Docker World!")
    ```

3.  **Crie um Dockerfile no mesmo diretório:**

    ```dockerfile
    # Dockerfile
    FROM python:3.9-slim-buster
    WORKDIR /app
    COPY app.py .
    CMD ["python", "app.py"]
    ```

      * `FROM python:3.9-slim-buster`: Define a imagem base. Estamos usando uma imagem Python leve.
      * `WORKDIR /app`: Define o diretório de trabalho dentro do container.
      * `COPY app.py .`: Copia o arquivo `app.py` do seu host para o diretório `/app` no container.
      * `CMD ["python", "app.py"]`: Define o comando que será executado quando o container iniciar.

4.  **Construa a imagem Docker:**
    No terminal, dentro do diretório `docker-hello-world`:

    ```bash
    docker build -t hello-world-app .
    ```

    Este comando construirá uma imagem chamada `hello-world-app`.

5.  **Execute o container:**

    ```bash
    docker run hello-world-app
    ```

    Você deverá ver a saída: `Hello, Docker World!`

**Parabéns\!** Você acabou de executar sua primeira aplicação Dockerizada\!

-----

## 📚 Referências

  * [Docker Guides](https://docs.docker.com/guides/)
  * [Developer Roadmap (Docker)](https://roadmap.sh/docker)
  * [Um breve histórico sobre virtualização](https://www2.decom.ufop.br/terralab/um-breve-historico-sobre-virtualizacao/)
  * [Dive into the decades-long history of container technology](https://www.techtarget.com/searchitoperations/feature/Dive-into-the-decades-long-history-of-container-technology)
  * [Análise de desempenho entre máquinas virtuais e containers utilizando o Docker](https://www.grupounibra.com/repositorio/REDES/2022/analise-de-desempenho-entre-maquinas-virtuais-e-containers-utilizando-o-docker3.pdf?)
  * [Containers e virtualização](https://www.targetso.com/artigos/containers-e-virtualizacao/)

-----
