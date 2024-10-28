# Documentação do Projeto

Este é um servidor simples desenvolvido com o Flask para realizar upload de arquivos `.fbx`, listar o arquivo mais recente e deletar arquivos após um período.

## Funcionalidades

- **Upload de Arquivos**: Permite o upload de arquivos `.fbx`.
- **Obter Último Arquivo**: Retorna o nome do arquivo `.fbx` mais recente no diretório de uploads.
- **Servir Arquivos**: Acessa arquivos diretamente pela URL.
- **Exclusão Automática**: Remove arquivos da pasta `uploads/` após um tempo de delay.

## Estrutura do Código

### Variáveis e Configurações

- `UPLOAD_FOLDER`: Define o diretório de armazenamento dos arquivos enviados.
- `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`: Garante que o diretório `uploads/` seja criado se não existir.

### Rotas

- **`/` [GET]**: Retorna uma mensagem confirmando que o servidor está rodando.
  
- **`/upload` [POST]**:
  - Realiza o upload de um arquivo `.fbx`.
  - Retorna erro se o arquivo não for enviado ou se não for do tipo `.fbx`.
  - Resposta de sucesso inclui o nome do arquivo salvo.

- **`/get-latest-file` [GET]**:
  - Retorna o nome do arquivo `.fbx` mais recente na pasta de uploads.
  - Retorna erro se nenhum arquivo for encontrado.

- **`/uploads/<filename>` [GET]**:
  - Acessa e baixa um arquivo enviado pelo nome.
  - Inicia uma thread para deletar arquivos após 10 segundos.

### Funções

- **`delete_files_after_delay(delay)`**:
  - Aguarda um tempo definido (delay) e, em seguida, exclui todos os arquivos da pasta `uploads/`.

## Execução

Para rodar o servidor, execute:

```bash
python main.py
