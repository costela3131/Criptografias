from pathlib import Path
from stegano import lsb

def ocultar_mensagem(imagem_entrada, mensagem, imagem_saida):
    entrada = Path(imagem_entrada)
    saida = Path(imagem_saida)
    if entrada.suffix.lower() != ".png":
        raise ValueError("Para este projeto, a esteganografia utiliza imagens PNG.")
    lsb.hide(str(entrada), mensagem).save(str(saida))
    return saida

def extrair_mensagem(imagem):
    entrada = Path(imagem)
    if entrada.suffix.lower() != ".png":
        raise ValueError("Para este projeto, a extração utiliza imagens PNG.")
    mensagem = lsb.reveal(str(entrada))
    if mensagem is None:
        raise ValueError("Nenhuma mensagem foi encontrada na imagem.")
    return mensagem
