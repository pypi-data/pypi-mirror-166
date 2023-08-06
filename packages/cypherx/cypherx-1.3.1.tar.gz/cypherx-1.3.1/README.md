# Cypherx

**Cypherx** é uma ferramenta simples e descomplicada para criptografar e descriptografar textos

## Requerimentos
python 3.6.3 ou superior
argparse
rich
### Para desenvolvimento
setuptools
twine



## Instalação

```python
pip install cypherx
```

Ou se prefirir: 
```bash
git clone https://github.com/yuritorresf/cypherx.git
cd cypherx
python setup.py install
```

## Uso

### Argumentos disponíveis via linha de comando
```bash
cypherx -h

argumentos posicionais:
  start                             Inicia o programa em modo de interface gráfica via terminal.

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
```python
# Exemplo de importação de modúlo
import cypherx
cifra_cesar = cypherx.Caesar("Texto a ser criptografado", chave, modo)
```

### Para utilizar a interface gráfica via terminal
```bash
cypherx start
```

### Exemplos
```bash
cypherx -c -e -m "mensagem" -k 3
cypherx -a -e -m "mensagem"
cypherx -c -d -m "mensagem" -k 3
cypherx -a -d -m "mensagem"
```

## Contribuição
Pull requests são bem-vindos. Para mudanças importantes, abra um problema primeiro para discutir o que você gostaria de mudar.
