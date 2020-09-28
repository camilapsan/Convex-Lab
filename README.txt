---------------------------------- README ------------------------------------------

--------------------------- Desafio Unisoma 2020 ------------------------------------
------------------------------- Convex-Lab ------------------------------------------

O modelo apresentado funciona em duas fases. Em um primeira fase, utilizando-se um modelo otimização linear, os alunos de continuidade são alocados às turmas pré-existentes e, caso seja necessário, novas turmas são criadas para alocar esses alunos de continuidade. Ainda na primeira fase, o modelo aloca alunos de formulário às vagas remanescentes apenas, de turmas existentes ou criadas para alocar os alunos de formulário. Em uma segunda fase, utilizando-se um processo interativo, os demais alunos de formulário são alocados a novas turmas criadas, respeitando-se restrições orçamentárias e a ordem dos alunos no formulário.

Arquivos: 	
	- Arquivo convex_lab_desafio_unisoma_2020.py: código em python para ser executado.
	- Arquivo Modelo de Dados - MatMov.db: arquivo do banco de dados SQL fornecido no Desafio, populado com a solução encontrada.
	-Pasta cenários: contém os arquivos de banco de dados SQL, preenchidos com as soluções.
	- Arquivo Convex-Lab_Relatorio_Desafio_Unisoma_2020.pdf: relatório.

Para rodar o modelo localmente são necessários os seguintes requisitos:
- Python, versão 3.6.9;
- Pandas, versão 1.0.5;
- Numpy, versão 1.18;
- sqlite3, versão 2.6.0;
- Scipy, versão 1.4.1;
- PuLP, versão 2.3.

Normalmente pandas, numpy, sqlite3 e/ou scipy são pacotes já existentes em alguns compiladores, verifique antes de instalá-los novamente. Uma vez que tenha as versões instaladas, renomeio o arquivo .db com as entradas do modelo para "Modelo de Dados - MatMov.db" e armazene ele no mesmo diretório que o arquivo .py.

Você ainda tem a opção de armazenar o arquivo em pastas, porém o diretório deverá ser modificado na função main. 

Com os arquivos devidamente armazenados, procede-se à execução do código. O código é estruturado em 7 seções: 

(i) Instalação das bibliotecas: caso não tenha instalado as bibliotecas, retire os comentários para instalar as bibliotecas apenas na primeira vez que rodar o código. Recomente-as novamente após o primeiro uso.

(ii) Banco de dados - SQL: conjunto de funções de auxílio, para importação das tabelas.

(iii) Pré-processamento - Tabelas: conjunto de funções de auxílio, para ajuste das tabelas antes de serem utilizadas pelo modelo.

(i) Fase 1: conjunto de funções de auxílio, incluindo variáveis de decisão, função objetivo e restrições, que serão utilizadas no modelo.

(v) Fase 2: conjunto de funções de auxílio utilizadas, com processo iterativos, utilizadas na segunda fase do modelo.

(vi) Main: Função que incorpora todas as outras anteriores e retorna como resposta o banco de dados com as soluções propostas.

(vii) Testes: Executa os vários cenários. Para isso, descomente as últimas linhas do arquivo .py e adicione os cenários de v1 a v6 ao mesmo diretório do arquivo .py.

Após a execução do código, proceda aos arquivos .db no seu diretório e os analise em algum software de banco de dados de sua preferência. Alguns "prints" foram adicionados à execução do modelo, a fim de facilitar a visualização do funcionamento do mesmo.