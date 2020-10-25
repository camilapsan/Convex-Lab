---------------------------------- README ------------------------------------------

--------------------------- Desafio UniSoma 2020 ------------------------------------
------------------------------- Convex-Lab ------------------------------------------
A solução apresentada é constituída de duas parte principais: modelo e relatório web.

O modelo apresentado funciona em três fases:

Na fase 0,  verifica-se a possibilidade de juntar turmas de alunos de continuidade e fechar turmas existentes desnecessárias para alocar os alunos de continuidade. Além disso, o orçamento também é ajustado, se for insuficiente para alocar os alunos de continuidade.

Na fase 1, utilizando-se um modelo otimização linear, os alunos de continuidade são alocados às turmas pré-existentes e, caso seja necessário, novas turmas são criadas para alocar esses alunos de continuidade. Ainda na primeira fase, o modelo aloca alunos de formulário às vagas remanescentes apenas, de turmas existentes ou criadas para alocar os alunos de formulário.

Na fase 2, utilizando-se um processo interativo, os demais alunos de formulário são alocados a novas turmas criadas, respeitando-se restrições orçamentárias e a ordem dos alunos no formulário.

Já o relatório web é um item opcional. Trata-se de uma interface criada para facilitar na visualização das entradas e saídas do modelo.

Sendo assim, tem-se os seguintes arquivos:
 	
- Arquivo convex-lab_final_modelo.py: código do modelo em python para ser executado.
- Arquivo convex-lab_final_modelo_interface.py: código do modelo com interface web em python para ser executado.
- Pastas cenários: contém os arquivos de banco de dados SQL, preenchidos com as soluções.
- Arquivo Convex-Lab_Relatorio_Final.pdf: relatório.

Caso deseje-se rodar apenas o modelo localmente, são necessários os seguintes requisitos:
- Python, versão 3.6.9
- Pandas, versão 1.0.5
- Numpy, versão 1.18
- sqlite3, versão 2.6.0
- Scipy, versão 1.4.1
- PuLP, versão 2.3

Normalmente pandas, numpy, sqlite3 e/ou scipy são pacotes já existentes em alguns compiladores, verifique antes de instalá-los novamente. 

Para rodar o modelo com a interface localmente são necessários os seguintes requisitos adicionais:
- setuptools, versão 50.3.2
- dash, versão 1.16.0
- dash-table, versão 4.10.1
- dash-daq, versão 0.5.0
- dash-bootstrap-components, versão 0.10
- plotly, versão 4.10.0

Para executar (arquivos convex-lab_final_modelo.py e convex-lab_final_modelo_interface.py):
- Uma vez que tenha as bibliotecas instaladas, para executar o código, chame a função main passando como parâmetro o nome do arquivo do cenário de sua escolha. Você ainda tem a opção de armazenar o arquivo em pastas, porém o diretório deverá ser modificado na função main. 

Para visualizar a interface (apenas arquivo convex-lab_final_modelo_interface.py):
- Após a execução do arquivo convex-lab_final_modelo_interface.py, o relatorio web é gerado no navegador em 127.0.0.1:4050.

Com os arquivos devidamente armazenados, procede-se à execução do código. O código com apenas o modelo é estruturado em 7 seções: 

(i) Instalação das bibliotecas: caso não tenha instalado as bibliotecas, retire os comentários para instalar as bibliotecas apenas na primeira vez que rodar o código. Recomente-as novamente após o primeiro uso.

(ii) Banco de dados - SQL: conjunto de funções de auxílio, para importação das tabelas.

(iii) Pré-processamento - Tabelas: conjunto de funções de auxílio, para ajuste das tabelas antes de serem utilizadas pelo modelo.

(iv) Fase 0: procedimentos da fase 0.

(v) Fase 1: conjunto de funções de auxílio, incluindo variáveis de decisão, função objetivo e restrições, que serão utilizadas no modelo.

(vi) Fase 2: conjunto de funções de auxílio utilizadas, com processo iterativos, utilizadas na segunda fase do modelo.

(vii) Main: Função que incorpora todas as outras anteriores e retorna como resposta o banco de dados com as soluções propostas.

(viii) Testes: Executa os vários cenários. Para isso, descomente as últimas linhas do arquivo .py e adicione os cenários ao mesmo diretório do arquivo .py.

Após a execução do código, proceda aos arquivos .db no seu diretório e os analise em algum software de banco de dados de sua preferência. Alguns "prints" foram adicionados à execução do modelo, a fim de facilitar a visualização do funcionamento do mesmo.

No caso do código com modelo e interface, uma seção é adicionada ao início, contendo a função que gerará a interface.
