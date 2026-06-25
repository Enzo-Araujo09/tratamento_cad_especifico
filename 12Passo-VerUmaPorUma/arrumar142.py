import os

# 1. COLE O CAMINHO DA SUA PASTA AQUI (use barras normais / )
caminho_pasta = 'finalizada'

# Garante que o Python está olhando para a pasta certa
if not os.path.exists(caminho_pasta):
    print(f"Erro: A pasta {caminho_pasta} não foi encontrada. Verifique o caminho.")
    exit()

print("Iniciando a renomeação na pasta 'finalizadas'...")

# Loop de trás para frente (do 58 até o 52) para não sobrescrever arquivos
for num_atual in range(58, 51, -1):
    
    # Define o nome antigo e o novo
    if num_atual == 58:
        nome_antigo = "questao_58.png"
        nome_novo = "questao_52.png"
    else:
        nome_antigo = f"questao_{num_atual}.png"
        nome_novo = f"questao_{num_atual + 1}.png"
    
    # Cria o caminho completo para o Python achar os arquivos
    caminho_antigo = os.path.join(caminho_pasta, nome_antigo)
    caminho_novo = os.path.join(caminho_pasta, nome_novo)
    
    # Executa a renomeação se o arquivo existir
    if os.path.exists(caminho_antigo):
        os.rename(caminho_antigo, caminho_novo)
        print(f"Sucesso: {nome_antigo} -> {nome_novo}")
    else:
        print(f"Aviso: {nome_antigo} não foi encontrado na pasta.")

print("Processo concluído!")