# 🚀 Gerador Estratégico de Posts com IA

Uma aplicação web moderna e resiliente desenvolvida em Python com *Streamlit, integrada à API oficial do **Google GenAI* (utilizando o modelo gemini-2.5-flash). O sistema foi projetado para automatizar a criação de conteúdos estratégicos para redes sociais de duas formas: em lote (via planilhas) ou de forma interativa (via chat).

---

## 🛠️ Funcionalidades Principais

* *📊 Processamento de Planilhas em Lote:* Lê automaticamente um arquivo local ideias_posts.csv contendo colunas de "Tema" e "Público", processa cada linha usando inteligência artificial e gera um cronograma completo de publicações estruturadas.
* *💬 Chatbot Interativo em Tempo Real:* Uma aba dedicada para conversar diretamente com o Gemini, ideal para solicitar ajustes em posts gerados, fazer brainstorming de novos títulos ou tirar dúvidas sobre estratégias digitais.
* *🛡️ Engenharia de Resiliência (Anti-Falhas):* Implementação de políticas avançadas de tentativas automáticas (retries) com controle de tempo (time.sleep). Caso os servidores do Google apresentem instabilidade temporária (como o Erro 503 Overloaded/Unavailable) ou o ciclo de vida do Streamlit encerre a conexão, o próprio sistema reinicia o cliente e tenta novamente de forma transparente.
* *💾 Gerenciamento de Estado Inteligente:* Utilização do st.session_state para garantir que o histórico de mensagens e as sessões de chat permaneçam vivos durante as recargas nativas da interface web.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Ter o Python instalado em sua máquina e a sua chave de API do Google configurada no sistema.

### Passo a Passo

1. *Clone o repositório e acesse a pasta do projeto:*
   ```bash
   git clone https://github.com/Juliojuliano/gerador-posts-ia.git
   cd gerador-posts-ia
   ```

2. *Instale as dependências:*
   ```bash
   pip install -r requirements.txt
   ```

3. *Configure a chave de API do Gemini:*
   O projeto usa a biblioteca `google-genai`, que lê a chave automaticamente da variável de ambiente `GEMINI_API_KEY`. Crie uma chave gratuita em [Google AI Studio](https://aistudio.google.com/app/apikey) e defina a variável antes de rodar:
   ```bash
   # Linux/macOS
   export GEMINI_API_KEY="sua-chave-aqui"

   # Windows (PowerShell)
   $env:GEMINI_API_KEY="sua-chave-aqui"
   ```

4. *Execute o projeto.* Existem duas formas de uso:

   - *Interface web (recomendada)*, com as abas de planilha em lote e chat:
     ```bash
     streamlit run app_web.py
     ```
     O app abrirá automaticamente no navegador em `http://localhost:8501`.

   - *Versão de terminal*, que processa o `ideias_posts.csv` e depois abre um chat via linha de comando:
     ```bash
     python gerador_posts.py
     ```

### Formato do arquivo `ideias_posts.csv`
O arquivo precisa ter as colunas `Tema` e `Publico`, uma linha por post desejado. Exemplo:
```csv
Tema,Publico
Como a Inteligência Artificial está mudando o mercado de trabalho em 2026,Jovens profissionais e estudantes
```