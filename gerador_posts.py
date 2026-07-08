import os
import pandas as pd
from google import genai

# =====================================================================
# CONFIGURAÇÕES E INICIALIZAÇÃO
# =====================================================================
client = genai.Client()
NOME_PLANILHA = "ideias_posts.csv"
ARQUIVO_SAIDA = "cronograma_da_planilha.txt"

# =====================================================================
# FUNÇÕES DO SISTEMA
# =====================================================================

def processar_cronograma_csv(nome_arquivo, arquivo_destino):
    """
    Função responsável por ler o arquivo CSV e gerar os posts em lote.
    """
    print("📊 [PARTE 1] Lendo o arquivo de ideias e gerando cronograma...")
    
    try:
        dados = pd.read_csv(nome_arquivo, encoding="utf-8")
        
        with open(arquivo_destino, "w", encoding="utf-8") as arquivo:
            arquivo.write("=== CONTEÚDO GENERADO AUTOMATICAMENTE VIA PLANILHA ===\n\n")
            
            for indice, linha in dados.iterrows():
                tema_atual = linha['Tema']
                publico_atual = linha['Publico']
                
                print(f"⏳ Processando linha {indice + 1}: '{tema_atual}'...")
                
                prompt = f"""
                Crie um post estratégico para o Instagram direcionado para o público: {publico_atual}.
                O tema principal é: {tema_atual}.
                Adicione um gancho forte e uma chamada para ação no final.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                arquivo.write(f"📌 LINHA {indice + 1} | TEMA: {tema_atual}\n")
                arquivo.write(f"👥 PÚBLICO: {publico_atual}\n")
                arquivo.write("-" * 40 + "\n")
                arquivo.write(response.text)
                arquivo.write("\n\n" + "="*50 + "\n\n")
                
        print(f"🎉 Cronograma saved com sucesso em '{arquivo_destino}'!\n")

    except FileNotFoundError:
        print(f"❌ Não encontrei o arquivo '{nome_arquivo}'. Pulando para o chat...\n")
    except Exception as e:
        print(f"❌ Aviso na leitura do arquivo: {e}\n")


def iniciar_chatbot():
    """
    Função responsável por gerenciar a conversa interativa no terminal 
    com proteção contra encerramento manual (Ctrl+C).
    """
    print("=" * 50)
    print("💬 [PARTE 2] CHATBOT INTERATIVO ATIVADO!")
    print("Digite suas perguntas abaixo. Para encerrar o chat, digite: sair")
    print("=" * 50 + "\n")

    chat = client.chats.create(model="gemini-2.5-flash")

    # Esse bloco captura se você interromper o programa e evita as letras vermelhas de erro
    try:
        while True:
            mensagem_usuario = input("Você: ")
            
            if mensagem_usuario.lower() == "sair":
                print("\n👋 Chat encerrado. Até a próxima!")
                break
                
            if not mensagem_usuario.strip():
                continue
                
            print("🤖 Pensando...")
            
            try:
                resposta_ia = chat.send_message(mensagem_usuario)
                print(f"\nGemini: {resposta_ia.text}\n" + "-"*40)
            except Exception as e:
                print(f"\n❌ Erro ao enviar mensagem: {e}\n")
                
    except KeyboardInterrupt:
        print("\n\n👋 Chat encerrado pelo usuário de forma limpa. Até logo!")


# =====================================================================
# FLUXO PRINCIPAL DE EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    processar_cronograma_csv(NOME_PLANILHA, ARQUIVO_SAIDA)
    iniciar_chatbot()