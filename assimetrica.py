import base64
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def gerar_chaves(pasta="chaves"):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publica = privada.public_key()

    caminho_privada = pasta / "privada.pem"
    caminho_publica = pasta / "publica.pem"

    caminho_privada.write_bytes(
        privada.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )
    )
    caminho_publica.write_bytes(
        publica.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    return caminho_publica, caminho_privada

def _carregar_publica(caminho):
    return serialization.load_pem_public_key(Path(caminho).read_bytes())

def _carregar_privada(caminho):
    return serialization.load_pem_private_key(Path(caminho).read_bytes(), password=None)

def criptografar_assimetrico(caminho_entrada, chave_publica):
    entrada = Path(caminho_entrada)
    public_key = _carregar_publica(chave_publica)

    # Criptografia híbrida: Fernet protege o arquivo; RSA protege a chave Fernet.
    chave_sessao = Fernet.generate_key()
    token = Fernet(chave_sessao).encrypt(entrada.read_bytes())

    chave_cifrada = public_key.encrypt(
        chave_sessao,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    saida = entrada.with_name(entrada.name + ".asi")
    envelope = {
        "algoritmo": "RSA-2048 OAEP SHA-256 + Fernet",
        "arquivo_original": entrada.name,
        "chave_sessao_rsa": base64.b64encode(chave_cifrada).decode("ascii"),
        "dados": token.decode("ascii")
    }
    saida.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    return saida

def descriptografar_assimetrico(caminho_asi, chave_privada):
    arquivo = Path(caminho_asi)
    envelope = json.loads(arquivo.read_text(encoding="utf-8"))
    private_key = _carregar_privada(chave_privada)

    try:
        chave_sessao = private_key.decrypt(
            base64.b64decode(envelope["chave_sessao_rsa"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        dados = Fernet(chave_sessao).decrypt(envelope["dados"].encode("ascii"))
    except (ValueError, InvalidToken) as exc:
        raise ValueError("Falha na decriptografia: chave incorreta ou arquivo alterado.") from exc

    saida = arquivo.with_name(envelope["arquivo_original"] + ".decrypted")
    saida.write_bytes(dados)
    return saida
