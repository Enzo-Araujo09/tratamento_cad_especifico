import os

# Defina o caminho da pasta onde estão as imagens
# Exemplo: 'C:/Usuarios/Nome/Imagens' ou apenas 'imagens_prova' se estiver na mesma pasta do script
caminho_pasta = '96-180' 

# Configurações do intervalo
numero_inicial = 6
numero_final = 90

# Extensões de imagem permitidas (você pode adicionar mais se necessário)
extensoes_permitidas = ('.png', '.jpg', '.jpeg', '.webp')

try:
    # Lista todos os arquivos da pasta e os ordena
    arquivos = sorted(os.listdir(caminho_pasta))
    
    # Filtra apenas os arquivos que são imagens
    imagens = [f for f in arquivos if f.lower().endswith(extensoes_permitidas)]
    
    numero_atual = numero_inicial

    for nome_arquivo in imagens:
        # Se ultrapassar o número final, interrompe o processo
        if numero_atual > numero_final:
            print(f"Aviso: O limite de questão_{numero_final} foi atingido, mas ainda restam imagens na pasta.")
            break
            
        # Pega a extensão original do arquivo (.png, .jpg, etc)
        extensao = os.path.splitext(nome_arquivo)[1]
        
        # Cria o novo nome no padrão solicitado
        novo_nome = f"questao_{numero_atual}{extensao}"
        
        # Caminhos completos
        caminho_antigo = os.path.join(caminho_pasta, nome_arquivo)
        caminho_novo = os.path.join(caminho_pasta, novo_nome)
        
        # Renomeia o arquivo
        os.rename(caminho_antigo, caminho_novo)
        print(f"Renomeado: {nome_arquivo} -> {novo_nome}")
        
        numero_atual += 1

    print("\nProcesso concluído com sucesso!")

except FileNotFoundError:
    print("Erro: A pasta especificada não foi encontrada. Verifique o caminho.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")