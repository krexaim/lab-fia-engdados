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

## Configurando GetFile
Property	Value
Input Directory:	/files
File Filter:	.*.csv$

## Configurando conexão do NIFI + MINIO
1. Entrar em parameter context
2. Criar uma variável de ambiente
3. Criar uma tabela com as seguintes variáveis:

Name	Value
DirectoryCSV	/files
RecordReader	CSVReader
RecordWriter	JsonRecordSetWriter
EndPoint-Minio	http://minio:9000

* **Observação**: Após criar a variáveis de contexto, é necessário alterar o input file para os parametros que foram criados:
Property	Value
Input Directory	#{DirectoryCSV}


# Subir o minio
docker compose up -d minio

## Configurando conexão com o MINIO
http://localhost:9001/login

Senha : admin
password: minioadmin

## Obtendo credenciais do MINIO

1. Criar bucket RAW
2. Obter as credenciais

## configurar Controller Services
