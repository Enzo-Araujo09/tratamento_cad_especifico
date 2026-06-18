from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_azul(imagem, tolerancia=15): 
    """
    Encontra posições onde há o padrão de linhas do ENEM no centro da imagem.
    Padrão vertical (13 pixels de altura total):
    - 2 pixels escuros (35, 31, 32)
    - 3 pixels brancos (255, 255, 255)
    - 3 pixels escuros (35, 31, 32)
    - 3 pixels brancos (255, 255, 255)
    - 2 pixels escuros (35, 31, 32)
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Definição das cores do padrão (RGB 0-255)
    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)
    
    # Altura total do padrão é 2 + 3 + 3 + 3 + 2 = 13 pixels
    altura_faixa = 13 
    x_centro = largura // 2  # Analisa exatamente o pixel do meio da imagem
    
    def cor_combina(pixel_rgb, cor_alvo):
        r, g, b = pixel_rgb[:3]
        return (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia)

    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - altura_faixa:
        faixa_encontrada = True
        
        # Sequência esperada de offsets verticais para os 13 pixels
        # 0 e 1: escuros | 2, 3 e 4: brancos | 5, 6 e 7: escuros | 8, 9 e 10: brancos | 11 e 12: escuros
        for dy in range(altura_faixa):
            pixel = pixels[x_centro, y + dy]
            
            if dy in [0, 1, 5, 6, 7, 11, 12]:
                cor_esperada = cor_escura
            else:
                cor_esperada = cor_branca
                
            if not cor_combina(pixel, cor_esperada):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Corta exatamente 5 pixels ACIMA de começar o padrão
            posicao_corte = y - 50
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão ENEM encontrado em y={y}, cortando em y={posicao_corte}")
            
            # Pula a faixa inteira detectada para evitar múltiplas detecções do mesmo padrão
            y += altura_faixa
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando ANTES das faixas
    """
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    # Encontra as posições com base no padrão do centro
    posicoes_corte = encontrar_faixa_azul(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão de divisão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas padrão para corte")
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Corta as seções da imagem
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta do início anterior até a posição de corte calculada (5px acima do padrão)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        # Salva a imagem cortada
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa exatamente de onde a atual parou + os 5px de recuo + os 13px da faixa
        posicao_anterior = posicao_corte + 5 + 13
    
    # Corta a seção final (após a última faixa)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Substitua pelo caminho da sua imagem
    pasta_saida = "questoes_colunas" # Substitua pelo nome da pasta de saída desejada
    
    # Executa a divisão
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")