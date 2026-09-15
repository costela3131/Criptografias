import hashlib
import json
from pathlib import Path

def calcular_sha256(caminho):
    caminho = Path(caminho)
    sha = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            sha.update(bloco)
    return sha.hexdigest()

def gerar_hash(caminho):
    arquivo = Path(caminho)
    digest = calcular_sha256(arquivo)
    saida = arquivo.with_name(arquivo.name + ".has")
    saida.write_text(json.dumps({
        "algoritmo": "SHA-256",
        "arquivo": arquivo.name,
        "hash": digest
    }, indent=2), encoding="utf-8")
    return saida, digest

def verificar_hash(caminho, caminho_has):
    esperado = json.loads(Path(caminho_has).read_text(encoding="utf-8"))["hash"]
    atual = calcular_sha256(caminho)
    return esperado == atual, esperado, atual
