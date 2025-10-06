# lab-fia-engdados
https://github.com/Labdata-FIA/Lab-Engenharia-Dados-v2


# Subir o container do NIFI
docker compose up -d nifi minio

## Conexão com o NIFI
https://localhost:9443/nifi/#/login

Usuário	Senha
admin	fia@2024@ladata@laboratorio


## Configurando GetFile
Property	Value
Input Directory:	/files
File Filter:	.*.csv$
