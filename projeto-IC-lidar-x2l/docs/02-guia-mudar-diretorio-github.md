Como Mudar o Diretório de Clone do GitHub e Vincular ao VS Code

Este guia mostra como alterar o repositório remoto de um projeto Git local e vinculá-lo a um novo repositório no GitHub, utilizando o Visual Studio Code.

# 🧭 Etapas

## 1\. Verifique o Diretório Atual do Projeto

Certifique-se de que os arquivos do projeto já estão salvos localmente em uma pasta, por exemplo:  
  
C:\\MeusProjetos\\meu-projeto

## 2\. Abra o Projeto no VS Code

\- No VS Code, vá em File > Open Folder.  
\- Selecione a pasta onde os arquivos do projeto estão localizados.

## 3\. Inicialize o Repositório Git (se necessário)

Abra o terminal no VS Code (Ctrl + \`) e execute:

git init

Isso inicializa um repositório Git local, caso ainda não exista.

## 4\. Adicione ou Altere o Repositório Remoto

Se ainda não houver um repositório remoto:

git remote add origin https://github.com/usuario/novo-repositorio.git

Se quiser substituir o repositório remoto existente:

git remote set-url origin https://github.com/usuario/novo-repositorio.git

## 5\. Verifique o Repositório Remoto

Confirme se o repositório remoto foi configurado corretamente:

git remote -v

Você deve ver algo como:  
  
origin https://github.com/usuario/novo-repositorio.git (fetch)  
origin https://github.com/usuario/novo-repositorio.git (push)

## 6\. Configuração global (todos os repositórios)

`git config --global user.name "Seu Nome"`

`git config --global user.email "seu.email@exemplo.com"`

## 7\. Faça o Primeiro Push (se necessário)

Se for um novo repositório e você quiser enviar os arquivos:

git add .

git commit -m "Primeiro commit"

git push -u origin main

Nota: Se o branch principal do seu repositório for 'master', substitua 'main' por 'master'.

Com isso, seu projeto local estará vinculado ao novo repositório no GitHub e pronto para ser versionado diretamente pelo VS Code.