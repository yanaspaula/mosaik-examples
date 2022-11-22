# Tutorial Mosaik 3.0

Para execução deste tutorial, é importante ter o pacote `virutalenv` ou `conda` instalados em seu computador para criação de um ambiente virtual isolado. Este tutorial baseará suas etapas na utilização do pacote `conda`.

Para instalar o pacote `conda`, siga o passo-a-passo identificado [nesse link](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

Abaixo, seguem as etapas para executar adequadamente esse tutorial em sua máquina.

## Execução
Com o pacote `conda` corretamente instalado em sua máquina, siga os passos a seguir para criação do ambiente virtual:

1. Crie um novo ambiente, com Python 3.7. Siga as instruções e confirme a criação do ambiente.
```
conda create --name mosaik3 python=3.7
```

2. Acesse o ambiente recém-criado.
```
conda activate mosaik3
```

3. Clone este repositório em uma pasta da sua máquina.
```
git clone https://github.com/yanaspaula/mosaik-examples.git
```

4. Instale o pacote do Mosaik 3.0 no ambiente.
```
pip install mosaik
```

5. Acesse a pasta do tutorial e execute o exemplo.
```
python3 demo_3.py
```
