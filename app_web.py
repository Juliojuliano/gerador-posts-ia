import streamlit as st
import pandas as pd
from google import genai
import time

# Configuração da página web
st.set_page_config(page_title="Gerador de Posts IA", page_icon="📊", layout="centered")

# Função interna para garantir que o cliente esteja sempre aberto e ativo
def obter_cliente_ativo():
    if "client" not in st.session_state:
        st.session_state.client = genai.Client()
    return st.session_state.client

# Título principal da página
st.title("🚀 Gerador Estratégico de Posts com IA")
st.markdown("Transforme suas ideias de planilhas em posts prontos ou converse com a inteligência artificial.")

# Criando abas para organizar o sistema de forma elegante
aba_planilha, aba_chat = st.tabs(["📊 Processar Planilha", "💬 Chat em Tempo Real"])

# =====================================================================
# ABA 1: PROCESSAMENTO DE PLANILHA
# =====================================================================
with aba_planilha:
    st.subheader("Automação via CSV")
    st.write("Gere posts em lote a partir do seu arquivo ideias_posts.csv.")
    
    if st.button("Executar Geração em Lote", type="primary"):
        nome_planilha = "ideias_posts.csv"
        arquivo_saida = "cronograma_da_planilha.txt"
        
        try:
            dados = pd.read_csv(nome_planilha, encoding="utf-8")
            progresso = st.progress(0)
            status_texto = st.empty()
            
            total_linhas = len(dados)
            conteudo_gerado = "=== CONTEÚDO GERADO AUTOMATICAMENTE VIA WEB ===\n\n"
            
            client = obter_cliente_ativo()
            
            for indice, linha in dados.iterrows():
                tema_atual = linha['Tema']
                publico_atual = linha['Publico']
                
                prompt = f"""
                Crie um post estratégico para o Instagram direcionado para o público: {publico_atual}.
                O tema principal é: {tema_atual}.
                Adicione um gancho forte e uma chamada para ação no final.
                """
                
                sucesso = False
                tentativas_maximas = 3
                
                for tentativa in range(tentativas_maximas):
                    try:
                        status_texto.write(f"⏳ Processando {indice + 1} de {total_linhas}: {tema_atual} (Tentativa {tentativa + 1}/{tentativas_maximas})...")
                        
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        
                        texto_resposta = response.text
                        sucesso = True
                        break
                        
                    except Exception as e:
                        if "503" in str(e) or "UNAVAILABLE" in str(e).upper() or "CLOSED" in str(e).upper():
                            status_texto.warning(f"⚠️ Instabilidade temporária. Reiniciando conexão e aguardando 5 segundos...")
                            if "st.session_state.client" in st.session_state:
                                del st.session_state.client
                            client = obter_cliente_ativo()
                            time.sleep(5)
                        else:
                            raise e
                
                if not sucesso:
                    texto_resposta = "[Erro: Não foi possível gerar este post devido à instabilidade temporária do Google.]"
                
                conteudo_gerado += f"📌 LINHA {indice + 1} | TEMA: {tema_atual}\n"
                conteudo_gerado += f"👥 PÚBLICO: {publico_atual}\n"
                conteudo_gerado += "-" * 40 + "\n"
                conteudo_gerado += texto_resposta
                conteudo_gerado += "\n\n" + "="*50 + "\n\n"
                
                progresso.progress((indice + 1) / total_linhas)
                time.sleep(1)
            
            with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo_gerado)
                
            status_texto.empty()
            st.success(f"🎉 Pronto! Arquivo '{arquivo_saida}' atualizado com sucesso.")
            
            with st.expander("👀 Ver prévia do cronograma gerado"):
                st.code(conteudo_gerado, language="text")
                
        except FileNotFoundError:
            st.error(f"❌ Não encontrei o arquivo '{nome_planilha}' na pasta do projeto.")
        except Exception as e:
            st.error(f"❌ Ocorreu um erro crítico: {e}")

# =====================================================================
# ABA 2: CHATBOT INTERATIVO
# =====================================================================
with aba_chat:
    st.subheader("Conversa com o Gemini")
    
    # Inicializa o histórico se não existir
    if "historico_mensagens" not in st.session_state:
        st.session_state.historico_mensagens = []
        
    # Garante que o cliente e o objeto do chat existam e estejam sincronizados
    client = obter_cliente_ativo()
    if "objeto_chat" not in st.session_state:
        st.session_state.objeto_chat = client.chats.create(model="gemini-2.5-flash")

    # Exibe o histórico existente na tela de forma correta
    for msg in st.session_state.historico_mensagens:
        with st.chat_message(msg["autor"]):
            st.write(msg["texto"])

    # Recebe a nova entrada do usuário
    if prompt_usuario := st.chat_input("Digite sua dúvida ou peça ajustes aqui..."):
        # 1. Mostra e guarda a mensagem do usuário imediatamente
        with st.chat_message("user"):
            st.write(prompt_usuario)
        st.session_state.historico_mensagens.append({"autor": "user", "texto": prompt_usuario})
        
        # 2. Processa a resposta do assistente com proteção de conexão
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Tenta enviar usando o chat atual
                    resposta = st.session_state.objeto_chat.send_message(prompt_usuario)
                    st.write(resposta.text)
                    st.session_state.historico_mensagens.append({"autor": "assistant", "texto": resposta.text})
                except Exception as e:
                    # Se der erro de cliente fechado, reconecta de forma transparente e tenta mais uma vez
                    if "closed" in str(e).lower() or "client" in str(e).lower():
                        try:
                            # Força a criação de um novo cliente e sessão de chat fresca
                            st.session_state.client = genai.Client()
                            st.session_state.objeto_chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
                            
                            # Tenta retransmitir a mensagem
                            resposta = st.session_state.objeto_chat.send_message(prompt_usuario)
                            st.write(resposta.text)
                            st.session_state.historico_mensagens.append({"autor": "assistant", "texto": resposta.text})
                        except Exception as erro_fatal:
                            st.error(f"⚠️ Falha de comunicação com o servidor. Detalhe: {erro_fatal}")
                    else:
                        st.error(f"⚠️ Ocorreu um desvio no processamento: {e}")