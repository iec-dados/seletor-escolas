# Seletor de escolas – Instituto Escolas Criativas

Página leve que substitui o app em Apps Script. A pessoa escolhe UF → município → escola,
e a página abre o Typeform já com os hidden fields preenchidos:
`escola`, `inep`, `uf`, `municipio`, `dependencia`.

## Arquivos
- `index.html` – a página.
- `uf-XX.json` – lista de escolas de cada UF (Censo Escolar 2025).
- `gerar_dados.py` – regera os `uf-XX.json` a partir de um CSV novo.

## Como usar o link
`https://SEU-USUARIO.github.io/seletor-escolas/?form=EWT2cR3n`

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
