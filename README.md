# 🌍 SIDES - Sistema inteligente de Deslizamentos (IoT-PI)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)

> Um sistema completo de monitoramento IoT para prevenção de desastres naturais, integrando simulação de hardware, back-end em Python e dashboard responsivo em tempo real.

---

## 🖥️ Preview do Dashboard

![Dashboard do Projeto](Painel.png)

---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para iniciar o ecossistema completo (Hardware, Servidor e Cliente).

### 1. Hardware (Simulação)
Acesse o circuito simulado no Tinkercad para visualizar os sensores e o monitor serial.

[![Tinkercad](https://img.shields.io/badge/Acessar-Tinkercad-2481f2?style=for-the-badge&logo=tinkercad&logoColor=white)](https://www.tinkercad.com/things/78XLOJyYiUB-sensor-de-deslizamento/editel?returnTo=https%3A%2F%2Fwww.tinkercad.com%2Fdashboard&sharecode=EIngOTVKE-p3g-p7n3jG1XPNodWXAjTmE4EoqgQrg8w)

---

### 2. Back-end (Servidor)
Abra o terminal na pasta do projeto e inicie o servidor Flask. Ele será responsável por receber os dados, salvar no banco e servir o dashboard.

```bash
# Instale as dependências (caso ainda não tenha feito)
pip install -r requirements.txt

# Inicie o servidor
python servidor.py

Desenvolvedor: Cauã Brenno