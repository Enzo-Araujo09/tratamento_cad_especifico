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
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Definição das cores do padrão (RGB 0-255)
    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)
    
    x_centro = largura // 2  # Analisa exatamente o pixel do meio da imagem
    
    def cor_combina(pixel_rgb, cor_alvo):
        r, g, b = pixel_rgb[:3]
        return (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia)

    # --- Funções internas para verificar cada um dos padrões ---
    def verifica_padrao_13px(y_atual):
        # Padrão original: 2 escuros, 3 brancos, 3 escuros, 3 brancos, 2 escuros
        for dy in range(13):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 1, 5, 6, 7, 11, 12] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    def verifica_padrao_12px(y_atual):
        # Padrão novo: 1 escuro, 3 brancos, 4 escuros, 2 brancos, 2 escuros
        for dy in range(12):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 4, 5, 6, 7, 10, 11] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - 12:
        altura_faixa_detectada = 0
        
        # Tenta o padrão 1 (13px) se houver espaço na imagem
        if y < altura - 13 and verifica_padrao_13px(y):
            altura_faixa_detectada = 13
            print(f"Padrão ENEM Antigo (13px) encontrado em y={y}")
            
        # Se não achou o primeiro, tenta o padrão 2 (12px)
        elif verifica_padrao_12px(y):
            altura_faixa_detectada = 12
            print(f"Padrão ENEM Novo (12px) encontrado em y={y}")
        
        # Se algum dos dois padrões foi mapeado
        if altura_faixa_detectada > 0:
            # ALTERADO: Removeu-se o "- 75". O corte agora é exatamente onde o padrão inicia (y).
            posicao_corte = y
                
            # Guardamos uma tupla com a posição do corte e o tamanho da faixa
            posicoes_corte.append((posicao_corte, altura_faixa_detectada))
            print(f"-> Cortando em y={posicao_corte}")
            
            # Pula o tamanho exato da faixa detectada
            y += altura_faixa_detectada
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando APENAS nas faixas detectadas
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_azul(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão de divisão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas padrão para corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, (posicao_corte, altura_faixa) in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Recorta da posição anterior até o início da faixa encontrada
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # ALTERADO: A próxima seção começará exatamente após a faixa (sem somar os 50px extras)
        posicao_anterior = posicao_corte + altura_faixa
    
    # Salva o último bloco restante da imagem
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_colunas" 
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")