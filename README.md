# Bootcamp LLMops: Do Colab à Produção

Este repositório contém os scripts e instruções para configurar uma infraestrutura escalável no Google Cloud Platform (GCP), utilizando Compute Engine, Docker e ngrok, para execução de modelos de linguagem com VLLM e exposição de uma aplicação Streamlit.

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter:

* Conta ativa no Google Cloud Platform.
* Acesso ao Google Cloud Shell.
* Permissões adequadas para criar roles, instâncias e configurar metadados no projeto.
* Conta no [ngrok](https://ngrok.com) para expor a aplicação via túnel.

## 🚀 Passo a Passo

### 1. Criar Role para Estudantes

Defina uma role personalizada com permissões restritas ao Compute Engine:

```bash
gcloud iam roles create bootcamp-mlops-student-role \
  --project=PROJECT_ID \
  --title="Bootcamp MLOps Student Role" \
  --description="Permissões restritas para uso do Compute Engine" \
  --permissions="compute.instances.create,compute.instances.get,compute.instances.list,compute.instances.delete"
```

### 2. Habilitar OS Login

Permita que os alunos façam login nas instâncias usando suas contas do IAM:

```bash
gcloud compute project-info add-metadata \
  --metadata enable-oslogin=TRUE
```

### 3. Criar Instância Base

Crie uma instância com 4 vCPUs e 16 GB de RAM (n2d-standard-4):

```bash
gcloud compute instances create base-vllm-vm \
  --zone=us-central1-a \
  --machine-type=n2d-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-balanced \
  --metadata=enable-oslogin=true \
  --tags=bootcamp \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

### 4. Instalar Docker e ngrok na Instância Base

Acesse a instância e execute os seguintes comandos para instalar Docker e ngrok:

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar Docker
sudo apt install -y docker.io
sudo systemctl enable --now docker

# Instalar ngrok
sudo apt install -y unzip
curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o ngrok.zip
unzip ngrok.zip
sudo mv ngrok /usr/local/bin
```

### 5. Clonar Repositórios Necessários

Clone os repositórios do VLLM e do Bootcamp:

```bash
# Clonar repositório do VLLM
git clone https://github.com/vllm-project/vllm

# Clonar repositório do Bootcamp
git clone https://github.com/lucas-wa/ceia-devops-bootcamp
```

### 6. Construir Imagens Docker

Dentro da pasta do VLLM, construa a imagem para o modelo:

```bash
cd ./vllm
docker build -f Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
```

Na pasta do Bootcamp, construa a imagem para a aplicação Streamlit:

```bash
cd ./ceia-devops-bootcamp
docker build -f docker/Dockerfile.app -t streamlit-app .
```

### 7. Executar o Modelo com Docker

Execute o modelo utilizando o Docker:

```bash
docker run -d \
  --rm \
  --network=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm-cpu-env \
  --model Qwen/Qwen2-1.5B-Instruct \
  --trust-remote-code \
  --device cpu \
  --dtype bfloat16 \
  --tokenizer-mode auto
```

O servidor estará disponível na porta 8000.

### 8. Executar a Aplicação Streamlit

Execute a aplicação Streamlit:

```bash
docker run --rm -d --network=host streamlit-app
```

### 9. Expor a Aplicação com ngrok

Inicie um túnel com ngrok para expor a aplicação:

```bash
ngrok http 8501 --authtoken YOUR_NGROK_AUTH_TOKEN
```

Substitua `YOUR_NGROK_AUTH_TOKEN` pelo seu token de autenticação do ngrok.

---

## 📌 Observações

* **Escalabilidade**: Para replicar a instância base, utilize o comando `gcloud compute instances create` com as configurações desejadas. Verifique as cotas do seu projeto para garantir que há recursos suficientes.
* **Acesso dos Estudantes**: Os alunos podem acessar as instâncias via console do GCP utilizando suas contas do IAM, sem necessidade de gerenciar chaves SSH.
* **Segurança**: Certifique-se de que as permissões atribuídas à role personalizada sejam suficientes para as atividades dos alunos, mas restritas para evitar acessos indesejados.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
