# **WaterFlow - Backend**

Este repositório contém o servidor backend para o sistema de monitoramento e gestão de fluxo de água. O objetivo é fornecer uma API para armazenar e gerenciar dados de vazão capturados por sensores conectados a dispositivos embarcados.

## **Sumário**

- [Introdução](#introdução)
- [Primeiros Passos](#primeiros-passos)
  - [Configuração do Ambiente](#configuração-do-ambiente)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
- [Uso](#uso)
  - [Iniciar o Servidor](#iniciar-o-servidor)
- [Rotas da API](#rotas-da-api)
- [Considerações Finais](#considerações-finais)

---

## **Introdução**

Este projeto visa fornecer uma API REST para monitoramento e registro da vazão de água utilizando sensores de fluxo conectados a dispositivos embarcados.  
Os dispositivos enviam leituras periódicas ao backend, que armazena os dados em um banco PostgreSQL, possibilitando consultas e análises posteriores.

O backend foi desenvolvido com **Django e Django REST Framework (DRF)**, garantindo escalabilidade e segurança no armazenamento das informações.

---

## **Primeiros Passos**

### **Configuração do Ambiente**

#### **Pré-requisitos**

Antes de iniciar, certifique-se de que o ambiente atende aos seguintes requisitos:

| Requisitos | Versão recomendada |
|------------|--------------------|
| **Sistema Operacional** | Ubuntu 20.04+ ou WSL2 com Debian |
| **Python** | 3.11 ou superior |
| **PostgreSQL** | 16 ou superior |
| **Git** | 2.30+ |
| **Editor de Código** | [Visual Studio Code](https://code.visualstudio.com/download) (opcional) |

---

#### **Instalação**

1. **Atualize o sistema e instale os pacotes necessários:**
   ```bash
   sudo apt update &&
   sudo apt upgrade -y &&
   sudo apt install -y git python3-pip python3.11-venv postgresql postgresql-client
