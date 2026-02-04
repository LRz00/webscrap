# Security Policy

## Vulnerabilidades Corrigidas

### 1. Divisão por Zero (CVE: N/A)
**Severidade**: Média  
**Arquivo**: `src/kafka/consumer.py`  
**Status**: ✅ Corrigido

**Descrição**: Quando o preço anterior de um produto era 0, o cálculo de variação percentual causava uma divisão por zero, resultando em erro.

**Correção**: Adicionada verificação para evitar divisão por zero. Quando o preço anterior é 0, exibe mensagem "new price" ao invés de percentual.

### 2. Falta de Validação de Variáveis de Ambiente
**Severidade**: Alta  
**Arquivo**: `src/db/db.py`  
**Status**: ✅ Corrigido

**Descrição**: O código acessava `os.environ["DATABASE_URL"]` diretamente sem verificar se a variável existe, causando exceção não tratada.

**Correção**: Implementada validação com `os.environ.get()` e mensagem de erro clara quando a variável não está configurada.

### 3. Vazamento de Recursos
**Severidade**: Baixa  
**Arquivo**: `src/kafka/producer.py`, `src/main.py`  
**Status**: ✅ Corrigido

**Descrição**: O produtor Kafka não era fechado adequadamente, podendo causar vazamento de recursos.

**Correção**: Adicionada função `close_producer()` e bloco `finally` no main.py para garantir o fechamento.

### 4. Falta de Validação de URL
**Severidade**: Alta  
**Arquivo**: `src/scrapper/wishlist_scrapper.py`  
**Status**: ✅ Corrigido

**Descrição**: Não havia validação da URL antes de acessá-la, permitindo potencialmente acesso a sites maliciosos.

**Correção**: Implementada função `validate_url()` que verifica:
- URL não vazia
- Esquema HTTP/HTTPS válido
- Domínio Amazon (com aviso se diferente)

### 5. Incompatibilidade de Campos de Dados
**Severidade**: Média  
**Arquivo**: `src/kafka/consumer.py`  
**Status**: ✅ Corrigido

**Descrição**: O consumidor esperava campo `product_name`, mas o scraper retornava `name`, causando erros.

**Correção**: Adicionado suporte para ambos os campos usando `item.get("name", item.get("product_name", "Unknown"))`.

### 6. Falta de Tratamento de Erros
**Severidade**: Média  
**Arquivos**: Múltiplos  
**Status**: ✅ Corrigido

**Descrição**: Diversas operações não tinham tratamento adequado de exceções.

**Correção**: Adicionados blocos try-except em:
- Producer Kafka
- Consumer Kafka
- Scraper
- Discord Notifier
- Main.py

### 7. Validação de Tipos de Dados
**Severidade**: Média  
**Arquivo**: `src/kafka/consumer.py`  
**Status**: ✅ Corrigido

**Descrição**: Não havia validação se os dados recebidos eram do tipo esperado.

**Correção**: Adicionadas verificações com `isinstance()` para garantir tipos corretos antes do processamento.

## Vulnerabilidades SQL Injection
**Status**: ✅ Não Encontrado

O código já utiliza consultas parametrizadas com SQLAlchemy (`text()` com bind parameters), prevenindo SQL injection:
```python
GET_LAST_PRICE_QUERY = text("""
    SELECT price 
    FROM price_history                            
    WHERE product_name = :product_name
    ORDER BY recorded_at DESC
    LIMIT 1
""")
```

## Recomendações de Segurança para Produção

### Configuração de Senhas
- ❌ **Não usar** a senha `apppassword` do PostgreSQL em produção
- ✅ Definir senhas fortes via variáveis de ambiente
- ✅ Usar gerenciadores de segredos (AWS Secrets Manager, HashiCorp Vault, etc.)

### Configuração de Rede
- ✅ Não expor portas do PostgreSQL (5432) publicamente
- ✅ Não expor portas do Kafka (9092) publicamente
- ✅ Usar VPN ou rede privada para comunicação entre serviços

### Credenciais
- ✅ Armazenar `discord_token` em variáveis de ambiente, nunca no código
- ✅ Usar `.env` local apenas para desenvolvimento
- ✅ Adicionar `.env` no `.gitignore` (já configurado)

### Monitoramento
- ✅ Implementar logging adequado de erros
- ✅ Configurar alertas para falhas de segurança
- ✅ Monitorar acessos não autorizados

## Ferramentas de Segurança Utilizadas

### Bandit
Ferramenta de análise de segurança para Python.
```bash
bandit -r src/
```
**Resultado**: 1 alerta de baixa severidade em arquivo de exemplo (esperado)

### CodeQL
Análise estática de código para detectar vulnerabilidades.
**Resultado**: 0 alertas encontrados

## Reportando Vulnerabilidades

Se você encontrar uma vulnerabilidade de segurança, por favor:
1. **NÃO** abra uma issue pública
2. Entre em contato com os mantenedores diretamente
3. Forneça detalhes suficientes para reproduzir o problema
4. Aguarde resposta antes de divulgar publicamente
