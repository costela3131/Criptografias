import base64
import json
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

def criptografar_simetrico(caminho_entrada, chave=None):
    entrada = Path(caminho_entrada)
    if not entrada.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {entrada}")

    if chave is None:
        chave = Fernet.generate_key()
    try:
        fernet = Fernet(chave)
    except Exception as exc:
        raise ValueError("Chave Fernet inválida.") from exc

    dados = entrada.read_bytes()
    token = fernet.encrypt(dados)

    saida = entrada.with_name(entrada.name + ".sim")
    envelope = {
        "algoritmo": "Fernet (AES-128-CBC + HMAC-SHA256)",
        "arquivo_original": entrada.name,
        "dados": token.decode("ascii")
    }
    saida.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    return saida, chave

def descriptografar_simetrico(caminho_sim, chave):
    arquivo = Path(caminho_sim)
    envelope = json.loads(arquivo.read_text(encoding="utf-8"))
    if envelope.get("algoritmo") != "Fernet (AES-128-CBC + HMAC-SHA256)":
        raise ValueError("Formato .sim incompatível.")
    try:
        dados = Fernet(chave).decrypt(envelope["dados"].encode("ascii"))
    except InvalidToken as exc:
        raise ValueError("Chave incorreta ou arquivo .sim alterado.") from exc

    nome = envelope["arquivo_original"]
    if nome.endswith(".sim"):
        nome = nome[:-4]
    saida = arquivo.with_name(nome + ".decrypted")
    saida.write_bytes(dados)
    return saida
