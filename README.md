# 🌍 SIDES - Sistema Inteligente de Deslizamentos (IoT-PI)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)

> Um sistema completo de monitoramento IoT para prevenção de desastres naturais, integrando simulação de hardware, back-end em Python e dashboard responsivo em tempo real.

---

## 🖥️ Preview do Dashboard

![Dashboard do Projeto](Painel.png)

---

## 🎮 Gamificação Interativa (Quiz)

Para engajar os visitantes durante a Mostra de Projetos, o sistema conta com um **Quiz Interativo**. 

Através de um QR Code, o público acessa uma página de perguntas e respostas sobre o funcionamento do SIDES. O sistema calcula a pontuação automaticamente e exibe uma animação de comemoração para quem atingir a meta de acertos, liberando brindes.

![Preview do Quiz](quiz.png)

> **Acesse o Quiz:** https://cauabrenno.github.io/pi-game/
---

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para iniciar o ecossistema completo (Hardware, Servidor e Cliente).

### 1. Hardware (Simulação)
Acesse o circuito simulado no Tinkercad para visualizar os sensores e o monitor serial.

[![Tinkercad](https://img.shields.io/badge/Acessar-Tinkercad-2481f2?style=for-the-badge&logo=tinkercad&logoColor=white)](https://www.tinkercad.com/things/78XLOJyYiUB-sensor-de-deslizamento/editel?returnTo=https%3A%2F%2Fwww.tinkercad.com%2Fdashboard&sharecode=EIngOTVKE-p3g-p7n3jG1XPNodWXAjTmE4EoqgQrg8w)

---

### 2. Back-end (Servidor)
Abra o terminal na pasta do projeto e inicie o servidor Flask.

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Inicie o servidor
python servidor.py