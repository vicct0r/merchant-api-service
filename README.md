# Merchant API Service

API REST para gerenciamento de lojas (merchants), pedidos, clientes e produtos em uma arquitetura multi-tenant.

## 🚀 Visão Geral

O **Merchant API Service** é uma aplicação backend robusta construída com Django Rest Framework para gerenciar operações de e-commerce e lojas online. A plataforma suporta:

- **Multi-tenant**: Cada usuário pode possuir um ou mais workspaces (lojas)
- **Gerenciamento de Pedidos**: Criar, rastrear e modificar pedidos com múltiplos status
- **Catálogo de Produtos**: Gerenciar produtos com SKU, preço e quantidade
- **Gestão de Clientes**: Manter registro de clientes e seus pedidos
- **Autenticação JWT**: Segurança via tokens JWT com Django Rest Framework
- **Documentação Automática**: Schema OpenAPI 3.0 integrado via drf-spectacular
- **Auditoria**: Rastreamento de eventos importantes do sistema
- **Logging Avançado**: Sistema de logs estruturado para produção

## 📦 Dependências Principais

| Pacote | Versão | Propósito |
|--------|--------|----------|
| Django | 6.0.2 | Framework web |
| djangorestframework | 3.16.1 | API REST |
| djangorestframework_simplejwt | 5.5.1 | Autenticação JWT |
| drf-spectacular | 0.29.0 | Documentação OpenAPI |
| psycopg | 3.3.2 | Driver PostgreSQL |
| gunicorn | 25.0.3 | WSGI server produção |

## 🏗️ Arquitetura e Apps

### Apps Principais

#### `accounts`
Gerenciamento de usuários e autenticação.
- **CustomUser**: Modelo de usuário customizado com autenticação por email
- Suporte a verificação de email
- Integração com Workplace para multi-tenancy

#### `merchants`
Gerenciamento de workspaces (lojas).
- **Workplace**: Representa uma loja/merchant
  - Proprietário único (OneToOne com CustomUser)
  - CNPJ e nome da loja
  - Whitelist de usuários permitidos
  - Todos os registros são isolados por workplace

#### `orders`
Gerenciamento completo de pedidos.
- **Order**: Pedido principal com status
  - Status: pending, on_route, delivered, issue, in_preparation, returned, scheduled
  - Validação: Pedidos entregues/retornados não podem ser modificados
  - ManyToMany com produtos através de OrderItem
- **OrderItem**: Item individual no pedido
  - Quantidade e preço unitário
  - Relação com produtos
- **Reversal**: Sistema de reversão/devolução de pedidos

#### `clients`
Gerenciamento de clientes.
- **Client**: Informações de clientes
  - Nome, telefone e observações
  - Status ativo/inativo
  - Relacionado a um workplace específico

#### `products`
Catálogo de produtos.
- **Product**: Produtos disponíveis
  - SKU único por workplace
  - Preço e quantidade em estoque
  - Status ativo/inativo
  - Validação: Preço deve ser maior que 0

#### `audit`
Sistema de auditoria e rastreamento.
- Registro de eventos importantes do sistema
- Rastreamento de modificações

## 🛡️ Segurança

- Autenticação JWT obrigatória em todos os endpoints
- Validação CSRF ativa
- Senha validada com múltiplas regras (tamanho, caracteres, histórico)
- CORS configurado para domínios específicos
- Isolamento de dados por workspace (multi-tenancy)

## 📋 Validações Importantes

- **Pedidos**: Não podem ser modificados após entrega/devolução
- **Produtos**: Preço deve ser positivo, SKU único por workspace
- **Workplaces**: Um usuário pode ter apenas um workspace de proprietário
- **OrderItems**: Quantidade deve ser positiva
- **Usuários**: Email obrigatório e único

## 🤝 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m 'feat: descrição'`
3. Push para a branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

## 📄 Licença

Este projeto é privado e não está disponível sob licença pública.

## 👥 Suporte

Para dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.

---

## ⚠️ Status do Projeto

Este repositório é o ponto de partida original do **Merchant API Service**. Atualmente, está havendo uma refatoração completa do projeto em um fork/repositório separado, onde estão sendo implementadas melhorias arquiteturais, otimizações e novas funcionalidades. Para informações sobre o desenvolvimento mais recente, consulte o repositório de refatoração.
