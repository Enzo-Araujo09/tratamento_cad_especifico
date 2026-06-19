from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_azul(imagem, tolerancia=15): 
    largura, altura = imagem.size
    pixels = imagem.load()
    posicoes_corte = []
    
    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)
    x_centro = largura // 2  
    
    def cor_combina(pixel_rgb, cor_alvo):
        r, g, b = pixel_rgb[:3]
        return (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia)

    # --- Padrões de Verificação ---
    
    def verifica_padrao_13px(y_atual):
        # Padrão original: 2 escuros, 3 brancos, 3 escuros, 3 brancos, 2 escuros
        for dy in range(13):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 1, 5, 6, 7, 11, 12] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    def verifica_padrao_12px_a(y_atual):
        # Padrão original 2: 1 escuro, 3 brancos, 4 escuros, 2 brancos, 2 escuros
        for dy in range(12):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 4, 5, 6, 7, 10, 11] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    def verifica_padrao_12px_b(y_atual):
        # Padrão anterior: 2 pretos, 2 brancos, 4 pretos, 3 brancos, 1 preto
        for dy in range(12):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 1, 4, 5, 6, 7, 11] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    def verifica_padrao_12px_c(y_atual):
        # NOVO PADRÃO: 2 pretos (0,1), 2 brancos (2,3), 4 pretos (4,5,6,7), 2 brancos (8,9), 2 pretos (10,11)
        for dy in range(12):
            pixel = pixels[x_centro, y_atual + dy]
            cor_esperada = cor_escura if dy in [0, 1, 4, 5, 6, 7, 10, 11] else cor_branca
            if not cor_combina(pixel, cor_esperada):
                return False
        return True

    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - 12:
        altura_faixa_detectada = 0
        
        if y < altura - 13 and verifica_padrao_13px(y):
            altura_faixa_detectada = 13
            print(f"Padrão 13px encontrado em y={y}")
        elif verifica_padrao_12px_a(y):
            altura_faixa_detectada = 12
            print(f"Padrão 12px (A) encontrado em y={y}")
        elif verifica_padrao_12px_b(y):
            altura_faixa_detectada = 12
            print(f"Padrão 12px (B) encontrado em y={y}")
        elif verifica_padrao_12px_c(y):
            # Ativação do novo padrão solicitado
            altura_faixa_detectada = 12
            print(f"Padrão 12px (C - Novo) encontrado em y={y}")
        
        if altura_faixa_detectada > 0:
            posicoes_corte.append((y, altura_faixa_detectada))
            y += altura_faixa_detectada
        else:
            y += 1
            
    return posicoes_corte

def isolar_todas_as_questoes(caminho_imagem, pasta_saida, margem_superior=45):
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    posicoes_corte = encontrar_faixa_azul(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão de divisão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas divisórias. Isolando questões...")
    os.makedirs(pasta_saida, exist_ok=True)
    
    for i in range(len(posicoes_corte)):
        y_faixa_atual, _ = posicoes_corte[i]
        
        ponto_inicial = y_faixa_atual - margem_superior
        if ponto_inicial < 0:
            ponto_inicial = 0
            
        if i + 1 < len(posicoes_corte):
            y_proxima_faixa, _ = posicoes_corte[i + 1]
            ponto_final = y_proxima_faixa - margem_superior
        else:
            ponto_final = altura
            
        if ponto_final <= ponto_inicial:
            continue
            
        area_questao = (0, ponto_inicial, largura, ponto_final)
        questao_recortada = imagem.crop(area_questao)
        
        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        questao_recortada.save(caminho_completo)
        print(f"Salvo: {caminho_completo} (y: {ponto_inicial} até {ponto_final})")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_colunas" 
    
    isolar_todas_as_questoes(caminho_imagem, pasta_saida, margem_superior=45)
    
    print("Processo concluído! Todas as questões foram isoladas.")