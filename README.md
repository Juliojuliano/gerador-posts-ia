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

1. *Abra a pasta do projeto no seu terminal ou VS Code:*
   ```bash
   cd caminhos/para/projetos_IA