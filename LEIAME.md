# Seletor de escolas – Instituto Escolas Criativas

Página leve que substitui o app em Apps Script. A pessoa escolhe UF → município → escola,
e a página abre o Typeform já com os hidden fields preenchidos:
`escola`, `inep`, `uf`, `municipio`, `dependencia`.

## Arquivos
- `index.html` – a página.
- `uf-XX.json` – lista de escolas de cada UF (Censo Escolar 2025).
- `gerar_dados.py` – regera os `uf-XX.json` a partir de um CSV novo.

## Como usar o link
`https://iec-dados.github.io/seletor-escolas/?form=Jore8zKc`

O `?form=` é o ID do Typeform, igual ao link antigo. Sem ele, a página usa o
formulário padrão definido em `CONFIG.formPadrao`, no topo do script do `index.html`.

## Logo
Envie a logo do IEC com o nome `logo.png` junto dos outros arquivos. Sem ela, a página mostra só o texto.

## Quando a pessoa clica em "Não encontrei minha escola"
O Typeform abre com `uf` e `municipio`, mas **sem** `inep` e `escola`.
No Typeform, crie a regra: se `inep` estiver vazio → pergunta de texto "Nome da escola".

## Atualizar a base
    python3 gerar_dados.py base.csv .
O CSV precisa das colunas: estado, municipio, dependencia, nome_escola, inep.
Depois, envie os `uf-XX.json` novos para o GitHub, substituindo os antigos.

## Escolas novas, ainda sem INEP
1. Acrescente uma linha em `escolas_extras.csv` (mesmas colunas da base), com um código provisório
   começando com IEC, ex.: `AL,Arapiraca,Municipal,NOME DA ESCOLA,IEC-AL-0001`.
2. Rode `python3 gerar_dados.py base.csv .` e envie ao GitHub o `uf-XX.json` da UF alterada.
3. Na página, a escola aparece com "Código provisório", e o Typeform recebe `inep=IEC-AL-0001`.
4. Quando a escola ganhar INEP, troque o código no `escolas_extras.csv` (ou remova a linha, se ela já vier
   na base nova do Censo), regere e corrija as respostas antigas trocando IEC-… pelo INEP real.
