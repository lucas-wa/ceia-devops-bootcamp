# Fundamentos de vLLM: Virtual Large Language Model

Este repositório explora os fundamentos do **vLLM**, uma biblioteca de inferência rápida e eficiente para Large Language Models (LLMs).  
O material baseia-se na apresentação **"Fundamentos de vLLM"**.

---

## 💡 Motivação: Por Que vLLM?

Modelos de Linguagem Grandes (LLMs), como Llama e Gemini, estão cada vez maiores e mais complexos, o que amplia suas capacidades, mas traz desafios:

### Desafios com LLMs Grandes

- **Custo e Recursos de Hardware:** GPUs são essenciais para acelerar inferência e treinamento devido aos cálculos matriciais intensivos. GPUs de alta performance (ex: NVIDIA A100 40GB) são caras.  
- **Geração Autoregressiva:** Cada token é gerado com base nos tokens anteriores, tornando a geração inerentemente serial e criando gargalos.  
- **KV Cache:** Para evitar recálculos na atenção a cada token gerado, utiliza-se um cache das matrizes Key (K) e Value (V). Porém, esse cache pode consumir mais de 30% da memória da GPU e seu tamanho varia dinamicamente, o que dificulta abordagens tradicionais.  

### Processamento de Requisições

- **Enfileiramento (Queuing):** Pode criar gargalos e comprometer o tempo real de resposta, essencial em aplicações como DALL-E.  
- **Batching de Requisições:** Processar várias requisições em lote é eficiente, mas complexo, pois as requisições chegam em momentos e tamanhos diferentes.  
- **Batching por Iteração:** Permite iniciar processamento antes do lote estar completo, substituindo requisições conforme terminam.  

### Fragmentação de Memória (Métodos Tradicionais)

- Alocação contígua do espaço máximo da sentença causa:  
  - **Fragmentação Interna:** Espaço reservado mas não utilizado.  
  - **Fragmentação Externa:** Espaço não reservado e não utilizado entre blocos.  
- Resultado: grande ineficiência no uso da memória GPU.

---

## 🚀 PagedAttention

vLLM soluciona a ineficiência do KV Cache com a técnica **PagedAttention**, inspirada na paginação de memória dos sistemas operacionais:

- **Blocos Não Contíguos:** KV Cache é dividido em blocos, cada um contendo K e V de um número fixo de tokens, não armazenados contiguamente na memória.  
- **Alocação Dinâmica:** Evita espaços ociosos e reduz fragmentação interna e externa.  
- **Compartilhamento de KV Cache:** Permite que diferentes requisições compartilhem KV Cache, especialmente útil com prompts comuns.  
- **Otimizações em Baixo Nível:** Kernels otimizados aceleram transferência de dados e inferência.  

**Analogia:**  
Blocos = Páginas, Tokens = Bytes, Requisições = Processos.

---

## 📦 Arquitetura do vLLM

- Kernels otimizados com PagedAttention para gerenciamento eficiente do KV Cache.  
- API de inferência para interação com o modelo.  
- Schedulers e blocos para gestão eficiente de requisições e alocação de memória.

---

## 💻 Parte Prática: Configurando e Servindo um Modelo com vLLM (CPU)

Este guia mostra como configurar e executar um modelo vLLM localmente via CPU usando Docker.

### Pré-requisitos

- **Git:** Para clonar o repositório oficial.  
- **Docker Desktop ou Docker Engine:** Para construir e executar o container. Certifique-se que o Docker está rodando.

### Passos

1. **Clone o repositório vLLM:**

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
````

2. **Construa a imagem Docker para CPU:**

```bash
docker build -f Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
```

> O parâmetro `--shm-size=4g` aloca memória compartilhada suficiente para o modelo. Esse processo pode levar alguns minutos.

3. **Execute o container para servir o modelo:**

```bash
docker run -it \
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

### Explicação dos parâmetros do `docker run`

* `-it`: modo interativo com pseudo-TTY.
* `--rm`: remove o container automaticamente ao finalizar.
* `--network=host`: conecta o container à rede do host (localhost).
* `-v ~/.cache/huggingface:/root/.cache/huggingface`: monta o cache do Hugging Face para persistência de modelos e acelera downloads futuros.
* `vllm-cpu-env`: nome da imagem Docker construída.
* `--model Qwen/Qwen2-1.5B-Instruct`: modelo a ser carregado (pode substituir por outros disponíveis).
* `--trust-remote-code`: permite executar código remoto necessário em alguns modelos.
* `--device cpu`: usa CPU para inferência.
* `--dtype bfloat16`: define tipo de dado para pesos (comum em CPU).
* `--tokenizer-mode auto`: modo automático para carregar tokenizador.

Ao iniciar, o servidor vLLM estará pronto para receber requisições.

---

## 📨 Fazendo uma Requisição (Exemplo com cURL)

Com o servidor rodando, abra outro terminal e envie uma requisição POST para a API:

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2-1.5B-Instruct",
    "prompt": "Explique a importância da IA.",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

Você receberá uma resposta JSON com o texto gerado pelo modelo.

---

## 📚 Referências

## Referências

* [vLLM Project GitHub](https://github.com/vllm-project/vllm)
* [vLLM Documentation: CPU Installation](https://docs.vllm.ai/en/v0.7.3/getting_started/installation/cpu/index.html)
* [Efficient Memory Management for Large Language
Model Serving with PagedAttention](https://arxiv.org/pdf/2309.06180)
* [SO-CM Slides (UFPR)](https://wiki.inf.ufpr.br/maziero/lib/exe/fetch.php?media=socm%3Asocm-slides-17.pdf)
* [Efficient Generative Large Language Model Serving – Medium](https://medium.com/@javaid.nabi/efficient-generative-large-language-model-serving-1c22b58f3c92)
* [Gemini 1.5 Pro vs GPT-4o: A Head-to-Head Showdown – Medium](https://medium.com/@neltac33/gemini-1-5-pro-vs-gpt-4o-a-head-to-head-showdown-29c4cc837e7b)
* [How ChatGPT Works – Wired](https://www.wired.com/story/how-chatgpt-works-large-language-model/?utm_source=chatgpt.com)
