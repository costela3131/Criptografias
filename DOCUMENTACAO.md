# ATIVIDADE 02 — DESENVOLVIMENTO DE SOLUÇÃO PARA CRIPTOGRAFIA E ESTEGANOGRAFIA

## 1. Identificação

**Projeto:** Sistema de Criptografia, Hash e Esteganografia de Arquivos  
**Disciplina:** Segurança / Criptografia  
**Linguagem:** Python  
**Objetivo:** desenvolver uma solução capaz de aplicar mecanismos de criptografia, decriptografia, geração de hash e esteganografia sobre arquivos.

## 2. Introdução

A segurança da informação utiliza diferentes técnicas para proteger dados. A criptografia transforma informações legíveis em dados protegidos por meio de algoritmos e chaves. A criptografia simétrica utiliza a mesma chave para cifrar e decifrar, enquanto a assimétrica utiliza um par de chaves pública e privada. O hash, por sua vez, produz uma impressão digital do conteúdo e é utilizado principalmente para verificar integridade. A esteganografia possui uma finalidade diferente: esconder a existência de uma mensagem dentro de outro arquivo.

Este projeto reúne essas técnicas em uma aplicação desenvolvida em Python, permitindo ao usuário selecionar um arquivo e executar diferentes operações de segurança.

## 3. Objetivos

### 3.1 Objetivo geral

Desenvolver um sistema capaz de realizar operações de criptografia simétrica e assimétrica, geração e verificação de hash e esteganografia.

### 3.2 Objetivos específicos

- Criptografar arquivos usando uma chave simétrica.
- Decriptografar arquivos protegidos pela chave simétrica.
- Gerar chaves pública e privada para criptografia assimétrica.
- Criptografar e decriptografar arquivos utilizando RSA em uma arquitetura híbrida.
- Gerar hash SHA-256 para verificar integridade.
- Detectar alterações no arquivo por meio da comparação de hashes.
- Ocultar e recuperar mensagens em imagens PNG.
- Produzir arquivos de saída com extensões `.sim`, `.asi` e `.has`.
- Realizar testes automatizados das principais funcionalidades.

## 4. Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Desenvolvimento do sistema |
| cryptography | Criptografia simétrica e assimétrica |
| hashlib | SHA-256 |
| stegano | Esteganografia LSB |
| Pillow | Suporte a imagens |
| unittest | Testes automatizados |

## 5. Arquitetura da solução

O sistema foi dividido em módulos para facilitar manutenção e compreensão:

- `main.py`: interface de menu e integração das funcionalidades.
- `simetrica.py`: criptografia e decriptografia simétrica.
- `assimetrica.py`: geração de chaves e criptografia assimétrica híbrida.
- `hash_arquivo.py`: cálculo e verificação do SHA-256.
- `esteganografia.py`: ocultação e extração de mensagens.
- `tests/test_sistema.py`: testes automatizados.

## 6. Criptografia simétrica

A solução utiliza Fernet, mecanismo fornecido pela biblioteca `cryptography`. Uma chave é gerada e utilizada para proteger o conteúdo do arquivo. O resultado é armazenado em um arquivo `.sim`.

O formato `.sim` contém metadados em JSON, incluindo o nome original, o algoritmo utilizado e o conteúdo cifrado.

### Fluxo

Arquivo original → chave Fernet → cifragem → arquivo `.sim`

Para recuperar:

Arquivo `.sim` + chave → decriptografia → arquivo original recuperado.

A chave deve ser armazenada separadamente e não deve ser divulgada.

## 7. Criptografia assimétrica

Foi implementado RSA com chave de 2048 bits. O sistema possui uma função específica para gerar o par de chaves em formato PEM:

- `publica.pem`
- `privada.pem`

A chave pública pode ser distribuída, enquanto a chave privada deve permanecer protegida.

### 7.1 Criptografia híbrida

Como RSA não é apropriado para cifrar diretamente arquivos grandes, o projeto utiliza uma abordagem híbrida. Uma chave de sessão Fernet é criada para cifrar o conteúdo do arquivo. Em seguida, essa chave de sessão é protegida utilizando RSA-OAEP com SHA-256.

Assim:

Arquivo → Fernet → conteúdo cifrado  
Chave Fernet → RSA-OAEP → chave de sessão cifrada  
Resultado → `.asi`

Na decriptografia, a chave privada RSA recupera a chave de sessão e, posteriormente, Fernet recupera o conteúdo original.

## 8. Hash

Foi utilizado SHA-256 para gerar uma impressão digital do arquivo. O hash é armazenado em um arquivo `.has`.

O hash não é utilizado para recuperar o conteúdo original. Sua finalidade no projeto é permitir a verificação de integridade.

Exemplo de fluxo:

Arquivo original → SHA-256 → `.has`

Se o conteúdo do arquivo for modificado, o SHA-256 calculado posteriormente será diferente.

## 9. Esteganografia

A esteganografia implementada utiliza a técnica LSB (Least Significant Bit) por meio da biblioteca `stegano`. Neste projeto, a funcionalidade foi direcionada a imagens PNG.

O usuário fornece uma imagem e uma mensagem. O sistema gera uma nova imagem contendo a mensagem escondida. Posteriormente, a mensagem pode ser extraída da imagem.

A esteganografia não substitui a criptografia: ela procura ocultar a existência da mensagem, enquanto a criptografia procura proteger o conteúdo.

## 10. Extensões dos arquivos

| Extensão | Finalidade |
|---|---|
| `.sim` | Resultado da criptografia simétrica |
| `.asi` | Resultado da criptografia assimétrica |
| `.has` | Registro do hash SHA-256 |
| `.png` | Imagem utilizada na esteganografia |

## 11. Testes realizados

### Teste 1 — Criptografia simétrica

**Entrada:** arquivo TXT.  
**Procedimento:** aplicação da criptografia simétrica.  
**Resultado esperado:** geração de arquivo `.sim`.  
**Validação:** decriptografar o `.sim` e comparar o conteúdo com o arquivo original.

### Teste 2 — Criptografia assimétrica

**Entrada:** arquivo binário.  
**Procedimento:** geração das chaves RSA e criptografia híbrida.  
**Resultado esperado:** geração de `.asi`.  
**Validação:** utilizar a chave privada para recuperar o arquivo e comparar byte a byte com o original.

### Teste 3 — Hash

**Entrada:** arquivo TXT.  
**Procedimento:** geração do SHA-256.  
**Resultado esperado:** arquivo `.has`.  
**Validação:** calcular novamente o SHA-256 e verificar igualdade.

### Teste 4 — Detecção de alteração

**Entrada:** arquivo cujo hash já foi registrado.  
**Procedimento:** modificar o arquivo e verificar o hash novamente.  
**Resultado esperado:** hashes diferentes e indicação de alteração.

### Teste 5 — Esteganografia

**Entrada:** imagem PNG e mensagem.  
**Procedimento:** ocultar a mensagem utilizando LSB.  
**Resultado esperado:** nova imagem PNG.  
**Validação:** extrair a mensagem e comparar com a mensagem original.

## 12. Testes automatizados

O arquivo `tests/test_sistema.py` automatiza três cenários principais:

1. cifragem e decriptografia simétrica;
2. cifragem e decriptografia assimétrica;
3. geração de hash e detecção de alteração.

Para executar:

```bash
python -m unittest discover -s tests -v
```

O resultado esperado é a aprovação de todos os testes.

## 13. Considerações de segurança

A chave privada não deve ser compartilhada. Da mesma forma, a chave utilizada na criptografia simétrica deve ser protegida.

A solução utiliza algoritmos modernos para a finalidade acadêmica proposta. Não foram utilizados MD5 ou SHA-1, pois não são recomendados para aplicações atuais de integridade criptográfica.

A esteganografia deve ser compreendida como uma técnica de ocultação, e não como mecanismo isolado de proteção do conteúdo.

## 14. Conclusão

O projeto atende aos requisitos propostos ao disponibilizar mecanismos de criptografia simétrica e assimétrica, geração de hash, criação de chaves pública e privada e esteganografia. A separação em módulos permite compreender individualmente cada técnica e facilita a realização dos testes.

A combinação de RSA com uma chave de sessão simétrica permite aplicar criptografia assimétrica de forma adequada a arquivos, enquanto o SHA-256 permite verificar sua integridade. A esteganografia complementa o projeto ao demonstrar a possibilidade de ocultar uma mensagem dentro de uma imagem.

## 15. Código-fonte

O código-fonte do projeto deve ser disponibilizado no repositório definido pelo grupo (por exemplo, GitHub ou GitLab), e o link do repositório deve ser inserido na versão final desta documentação.

**Link do repositório:** [INSERIR LINK DO GITHUB/GITLAB AQUI]
