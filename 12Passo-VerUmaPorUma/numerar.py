from pathlib import Path

# Caminho da pasta com as imagens
pasta = Path(r"finalizada")  # Altere aqui

# Extensões aceitas
extensoes = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

# Lista de imagens ordenadas pelo nome
imagens = sorted([f for f in pasta.iterdir() if f.suffix.lower() in extensoes])

# A 11ª imagem (índice 10) será a questão 96
indice_inicial = 10
questao_inicial = 96
questao_final = 180

# Quantidade de questões
total_questoes = questao_final - questao_inicial + 1

if len(imagens) < indice_inicial + total_questoes:
    print("Não há imagens suficientes para renomear todas as questões.")
else:
    # Primeiro renomeia para nomes temporários para evitar conflitos
    temporarios = []
    for i in range(total_questoes):
        arquivo = imagens[indice_inicial + i]
        temp = arquivo.with_name(f"__temp_{i}{arquivo.suffix}")
        arquivo.rename(temp)
        temporarios.append(temp)

    # Depois renomeia para os nomes finais
    for i, arquivo in enumerate(temporarios):
        numero = questao_inicial + i
        novo_nome = pasta / f"questao_{numero}.png"
        arquivo.rename(novo_nome)

    print("Renomeação concluída!")