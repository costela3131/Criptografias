# Atividade 02 — Criptografia e Esteganografia

Sistema desenvolvido em Python para demonstrar criptografia simétrica, criptografia assimétrica, hash e esteganografia.

## Funcionalidades

- Criptografia simétrica com Fernet (AES-128-CBC + HMAC-SHA256), gerando `.sim`.
- Decriptografia de arquivos `.sim`.
- Geração de par de chaves RSA 2048 em PEM.
- Criptografia assimétrica híbrida RSA-OAEP + Fernet, gerando `.asi`.
- Decriptografia de arquivos `.asi`.
- Hash SHA-256, gerando `.has`.
- Verificação de integridade.
- Esteganografia LSB em imagens PNG.
- Testes automatizados.

## Instalação

Recomenda-se Python 3.11 ou superior.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Extensões

- `.sim`: arquivo protegido por criptografia simétrica.
- `.asi`: arquivo protegido por criptografia assimétrica híbrida.
- `.has`: arquivo contendo o hash SHA-256.

## Segurança

A chave privada RSA deve ser mantida em sigilo. A chave Fernet utilizada na criptografia simétrica também deve ser protegida. Este projeto tem finalidade acadêmica e demonstrativa.
