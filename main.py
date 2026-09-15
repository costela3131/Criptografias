from pathlib import Path
from simetrica import criptografar_simetrico, descriptografar_simetrico
from assimetrica import gerar_chaves, criptografar_assimetrico, descriptografar_assimetrico
from hash_arquivo import gerar_hash, verificar_hash
from esteganografia import ocultar_mensagem, extrair_mensagem

def escolher_arquivo(msg="Caminho do arquivo: "):
    return Path(input(msg).strip().strip('"')).expanduser()

def menu():
    while True:
        print("\n" + "=" * 48)
        print(" SISTEMA DE CRIPTOGRAFIA E ESTEGANOGRAFIA")
        print("=" * 48)
        print("1 - Criptografia simétrica")
        print("2 - Decriptografia simétrica")
        print("3 - Criptografia assimétrica")
        print("4 - Decriptografia assimétrica")
        print("5 - Gerar hash SHA-256")
        print("6 - Verificar hash")
        print("7 - Gerar chaves RSA")
        print("8 - Ocultar mensagem em PNG")
        print("9 - Extrair mensagem de PNG")
        print("0 - Sair")

        op = input("\nEscolha uma opção: ").strip()
        try:
            if op == "1":
                arquivo = escolher_arquivo()
                chave = input("Chave Fernet (ENTER para gerar automaticamente): ").strip()
                key = chave.encode() if chave else None
                saida, key = criptografar_simetrico(arquivo, key)
                print(f"\nArquivo gerado: {saida}")
                print(f"Chave: {key.decode()}")
                print("Guarde a chave. Sem ela, não será possível decriptografar o arquivo.")

            elif op == "2":
                arquivo = escolher_arquivo("Arquivo .sim: ")
                key = input("Chave Fernet: ").strip().encode()
                saida = descriptografar_simetrico(arquivo, key)
                print(f"Arquivo recuperado: {saida}")

            elif op == "3":
                arquivo = escolher_arquivo()
                pub = Path(input("Chave pública [chaves/publica.pem]: ").strip() or "chaves/publica.pem")
                saida = criptografar_assimetrico(arquivo, pub)
                print(f"Arquivo gerado: {saida}")

            elif op == "4":
                arquivo = escolher_arquivo("Arquivo .asi: ")
                priv = Path(input("Chave privada [chaves/privada.pem]: ").strip() or "chaves/privada.pem")
                saida = descriptografar_assimetrico(arquivo, priv)
                print(f"Arquivo recuperado: {saida}")

            elif op == "5":
                arquivo = escolher_arquivo()
                saida, digest = gerar_hash(arquivo)
                print(f"Arquivo .has: {saida}")
                print(f"SHA-256: {digest}")

            elif op == "6":
                arquivo = escolher_arquivo("Arquivo original: ")
                hash_file = escolher_arquivo("Arquivo .has: ")
                ok, esperado, atual = verificar_hash(arquivo, hash_file)
                print("HASH VÁLIDO." if ok else "HASH NÃO CONFERE.")
                print(f"Esperado: {esperado}")
                print(f"Atual:    {atual}")

            elif op == "7":
                pasta = Path(input("Pasta das chaves [chaves]: ").strip() or "chaves")
                pub, priv = gerar_chaves(pasta)
                print(f"Chave pública: {pub}")
                print(f"Chave privada: {priv}")

            elif op == "8":
                imagem = escolher_arquivo("Imagem PNG: ")
                mensagem = input("Mensagem: ")
                saida = escolher_arquivo("Imagem de saída [imagem_esteganografada.png]: ") if False else Path(
                    input("Imagem de saída [imagem_esteganografada.png]: ").strip() or "imagem_esteganografada.png"
                )
                ocultar_mensagem(imagem, mensagem, saida)
                print(f"Imagem gerada: {saida}")

            elif op == "9":
                imagem = escolher_arquivo("Imagem PNG: ")
                print("Mensagem:", extrair_mensagem(imagem))

            elif op == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida.")
        except Exception as exc:
            print(f"\nERRO: {exc}")

if __name__ == "__main__":
    menu()
