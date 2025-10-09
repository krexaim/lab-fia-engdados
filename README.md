# Informação do Laboratório
https://github.com/Labdata-FIA/Lab-Engenharia-Dados-v2


# Subindo o ambiente com Docker
`docker compose up -d`



## Logins
| Serviço | Usuário | Senha | 
|---|---|---|
| [NIFI](https://localhost:9443/nifi/#/login) | admin | fia@2024@ladata@laboratorio |
| [Airflow](http://localhost:8080/) | airflow | airflow |
| [MinIO](http://localhost:9001/login) | admin | minioadmin |

# Importando o template do NIFI
1. Criar process group e fazer upload do template em formato json
2. Entrar no process group - Ingest File
3. Configurar o ```controller settings``` para conectar com o MinIO com as credenciais:
    | Property | Value |
    |---|---|
    | Access key ID | admin |
    | Secret Access key | minioadmin |
4. Habilitar o controller -> enable

## Configurando GetFile
| Property | Value |
|---|---|
| Input Directory | /files |
| File Filter | .*.csv$ |

## Configurando conexão do NIFI + MINIO
1. Entrar em parameter context
2. Criar uma variável de ambiente
3. Criar uma tabela com as seguintes variáveis:

| Name | Value |
| --- | --- |
| DirectoryCSV | /files |
| RecordReader	| CSVReader |
| RecordWriter	| JsonRecordSetWriter |
| EndPoint-Minio | http://minio:9000 |

* **Observação**: Após criar a variáveis de contexto, é necessário alterar o input file para os parametros que foram criados:
  
| Property | Value |
|---|---|
| Input Directory | #{DirectoryCSV} |


## Rodando as DAGs no Airflow

## Inserindo os dados transformados no postgres

## Conectando o postgres com o metabase para visualizar os dados
![Dash](Imagens/Dash%20Metabase.png)