# Aplicação Preditiva de Obesidade — Streamlit

## 🔗 Aplicação em produção
Acesse o app preditivo aqui: https://app-obesidade-tech-challenge-eyetpkyhewtznjyjyf6wgk.streamlit.app/

## O que tem aqui
- `app.py` — a tela preditiva (formulário + integração com o modelo).
- `requirements.txt` — bibliotecas que o Streamlit Cloud precisa instalar.
- `modelo_obesidade.pkl` — **você precisa adicionar este arquivo** (é o que o seu notebook gera na última célula, seção "23. SALVAMENTO DOS RESULTADOS", a partir da planilha `Obesity_Ana_lise_Preliminar.xlsx`, aba `Base_Data`).

O app espera exatamente as colunas e os valores (em português) que aparecem
nessa planilha: `Gênero, Idade, Altura (m), Peso (Kg), Histórico Familiar,
FAVC, FCVC, NCP, CAEC, SMOKE, CH2O, SCC, FAF, TUE, CALC, MTRANS` + a coluna
`IMC` (calculada como `Peso / Altura²`, igual ao notebook faz). Por isso não
precisa mexer em nada — é só colocar o `.pkl` do seu modelo treinado na mesma
pasta.

## Passo 1 — Testar localmente (recomendado antes do deploy)
1. Rode o notebook até o fim para gerar o `modelo_obesidade.pkl` e baixe o arquivo.
2. Coloque `app.py`, `requirements.txt` e `modelo_obesidade.pkl` na mesma pasta no seu computador.
3. No terminal, dentro dessa pasta:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Vai abrir automaticamente no navegador em `http://localhost:8501`. Preencha o formulário e confira se a predição aparece.

## Passo 2 — Subir para o GitHub
1. Crie um repositório novo no GitHub (pode ser público, é o que o Streamlit Cloud pede na versão gratuita).
2. Suba estes 3 arquivos para a raiz do repositório:
   - `app.py`
   - `requirements.txt`
   - `modelo_obesidade.pkl`
3. Confirme que os 3 arquivos aparecem juntos na página principal do repositório no GitHub.

> Dica: se o `.pkl` for grande (alguns modelos como Random Forest podem passar de 25MB),
> o GitHub aceita normalmente até 100MB por arquivo — sem problema para esse projeto.

## Passo 3 — Deploy no Streamlit Community Cloud
1. Acesse **https://share.streamlit.io** e faça login com sua conta do GitHub.
2. Clique em **"New app"** (ou "Create app").
3. Selecione:
   - **Repository**: o repositório que você acabou de criar.
   - **Branch**: `main` (ou a branch onde estão os arquivos).
   - **Main file path**: `app.py`
4. Clique em **"Deploy"**.
5. Aguarde alguns minutos — o Streamlit Cloud vai instalar as dependências do `requirements.txt` e subir o app automaticamente.
6. Quando terminar, você recebe uma URL pública do tipo:
   `https://seu-usuario-nome-do-repo.streamlit.app`

Esse link é o que você vai colocar no arquivo `.doc`/`.txt` de entrega, junto com o link do painel analítico e do repositório do GitHub.

## Erros comuns
- **"ModuleNotFoundError"**: alguma biblioteca usada no `app.py` não está no `requirements.txt`. Adicione o nome da lib e faça um novo commit (o Streamlit Cloud reimplanta sozinho a cada push).
- **"FileNotFoundError: modelo_obesidade.pkl"**: o arquivo do modelo não foi enviado para o repositório, ou está em uma subpasta diferente da raiz.
- **Versão do scikit-learn diferente entre o Colab e o deploy**: se aparecer aviso/erro de versão incompatível ao carregar o `.pkl`, adicione a versão exata usada no Colab no `requirements.txt` (neste projeto: `scikit-learn==1.6.1`, com Python 3.12 selecionado nas "Advanced settings" do deploy).
- **App "dorme" após um tempo sem uso**: é normal no plano gratuito do Streamlit Cloud — ele volta ao acessar o link novamente, só demora alguns segundos para "acordar".
