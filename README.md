# Weather Bot

## Visão geral

Weather Bot é um bot para ver a previsão do tempo no Discord.

## Recursos

- Previsão do tempo atual.
- Previsão do tempo para os proximos 3 dias.
- Alertas meteorológicos.
- Possui suporte para os seguintes idiomas.
  - pt-BR
  - en-US
  - es-ES

## Instalação

1 . Clone o repositorio:

```bash
git clone https://github.com/Joab0/WeatherBot
```

2 . Entre na pasta do projeto clonado usando o comando:

```bash
cd WeatherBot
```

3 . Instale as dependências do projeto usando:

```bash
pip install -r requirements.txt
```

4 . Edite o arquivo `.env.example` e troque o nome para `.env`:

```env
# Token do bot
DISCORD_BOT_TOKEN = ""

# Weather API key
# Você pode conseguir em: https://www.weatherapi.com/
WEATHER_API_KEY = ""

# Se você quiser testar o bot em um servidor específico, coloque seu ID abaixo
TEST_GUILD_ID =
```

5 . Rode o bot usando:

```bash
python run.py
```
