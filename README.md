![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white) ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

# Amazon Wishlist Tracker (WIP)
Este projeto é um **scraper + pipeline de mensageria com Kafka** que monitora uma **wishlist pública da Amazon** e envia os dados periodicamente para um **tópico Kafka**, permitindo gerar alertas baseados em **flutuação de preços**.

<img width="601" height="610" alt="python alert drawio" src="https://github.com/user-attachments/assets/e2e366ce-d031-4338-8d15-053583d62a21" />

## Notas de Segurança

### ⚠️ Para Ambientes de Produção
- **Altere a senha do PostgreSQL**: A senha padrão `apppassword` no `docker-compose.yml` deve ser alterada para uma senha forte
- **Proteja as credenciais**: Use variáveis de ambiente ou gerenciadores de segredos para armazenar tokens e senhas
- **Configure SSL/TLS**: Habilite conexões seguras para Kafka e PostgreSQL
- **Valide URLs**: O scraper só deve acessar domínios confiáveis da Amazon
- **Configure o DATABASE_URL**: Defina a variável de ambiente `DATABASE_URL` com as credenciais corretas do banco de dados

### Melhorias de Segurança Implementadas
- ✅ Validação de URLs para prevenir acesso a sites maliciosos
- ✅ Tratamento de erros para evitar vazamento de informações sensíveis
- ✅ Validação de entrada de dados e prevenção de divisão por zero
- ✅ Uso de consultas parametrizadas para prevenir SQL injection
- ✅ Validação de variáveis de ambiente obrigatórias
