# Cypherx

** Cypherx ** é uma ferramenta simples e descomplicada para criptografar e descriptografar textos

## Requerimentos
python 3.5 ou superior
argparse
rich

## Instalação

```
git clone https://github.com/yuritorresf/cypherx.git
pip install argparse rich
```

## Uso

### Comandos disponíveis via linha de comando
```
python cypherx.py -h

argumentos opcionais:
  -h, --help                        Mostrar ajuda e sair
  -c, --caesar                      Criptografar com cifra de César
  -a, --atbash                      Criptografar com cifra de Atbash
  -e, --encrypt                     Encriptar mensagem
  -d, --decrypt                     Descriptografar mensagem

  -m MESSAGE, --message MESSAGE     Mensagem a ser criptografada ou descriptografada
  -k KEY, --key KEY                 Chave para criptografar ou descriptografar [Requerido para: César]
  -v, --version                     Mostre a versão do programa e sair
```

### Importando como módulo
```
Exemplo:
from cypherx import Caesar
```

### Para utilizar a interface gráfica via terminal
```
python cypherx.py
```

### Exemplos
```
python cypherx.py -c -e -m "mensagem" -k 3
python cypherx.py -a -e -m "mensagem"
python cypherx.py -c -d -m "mensagem" -k 3
python cypherx.py -a -d -m "mensagem"
```

## Contribuição
Pull requests são bem-vindos. Para mudanças importantes, abra um problema primeiro para discutir o que você gostaria de mudar.