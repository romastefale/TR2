# tigraoRADIO

Bot de Telegram integrado ao Spotify para mostrar a música atual ou a última música ouvida, registrar reproduções, curtidas e rankings.

## Funcionalidades principais

- Mostrar a música atual ou a última música ouvida via Spotify.
- Registrar reproduções por faixa e por usuário.
- Curtir e descurtir músicas pelos botões inline.
- Exibir perfil musical do usuário.
- Exibir ranking de músicas, artistas e curtidas.
- Executar comandos administrativos privados restritos ao `OWNER_ID`.
- Apagar mensagens por link com `/dx`.
- Gerenciar links, permissões e solicitações de entrada com comandos privados.
- Copiar mensagens enviadas ao bot no privado para um chat de destino com `/xend` usando `copy_message`.

## Comandos públicos

```text
/start
/help
/login
/playing
/kingplay
/mood
/myself
/songcharts
/logout
```

Observação: `/kingplay` é registrado junto aos comandos principais, mas fica restrito ao `OWNER_ID`.

## Comandos administrativos privados

Todos os comandos abaixo devem ser usados no privado do bot e são restritos ao `OWNER_ID`:

```text
/dx
<links_de_mensagem>

/ddx
<chat_id>
<add|remove|list|off|test>
<palavras ou texto>

/mx1
<chat_id>

/mx2
<chat_id>

/joinx
<chat_id>
<user_id>

/vx
<chat_id>
<user_id>

/uv
<chat_id>
<user_id>

/mx
<chat_id>
<user_id>
<duração>

/xend <chat_id>
Usar respondendo, no privado do bot, a mensagem que deve ser copiada para o destino.

/ximg
<chat_id>

/hidden

/vvv
<chat_id>
<user_id>
```

## Gatilhos textuais

Os textos abaixo podem acionar a mesma lógica de `/playing`:

```text
tocando
kur
xxt
ts
cebrutius
tigraofm
djpi
royalfm
geeksfm
radinho
qap
```

## Como funciona

### /playing

Busca a música atual no Spotify. Se não houver música em execução, tenta a última música ouvida. Registra a reprodução, calcula plays e likes da faixa, mostra capa do álbum e adiciona botões inline para plays e likes.

### /mood

Usa a faixa atual ou a última faixa ouvida para montar uma resposta de mood com base na nota informada no comando. O fluxo atual não usa mais `audio features` do Spotify.

### /myself

Mostra estatísticas pessoais:

- top músicas;
- top artistas;
- total de curtidas.

### /songcharts

Mostra estatísticas do grupo:

- top músicas;
- top artistas;
- músicas mais curtidas.

### /xend

O comando `/xend` deve ser usado respondendo uma mensagem no privado do bot:

```text
/xend <chat_id>
```

O bot usa `copy_message` para reenviar ao destino a mensagem respondida, preservando mídia, legenda e entidades de formatação quando o Telegram permitir.

## Banco de dados

Tabelas usadas pelo fluxo atual:

- `spotify_tokens`;
- `track_plays`;
- `track_likes`;
- `join_requests`;
- `known_groups`;
- `ddx_rules`.

## Deploy

O projeto está configurado para Railway.

- Start command: `python -m app.bootstrap`
- Healthcheck: `/healthz`

## Variáveis de ambiente

```text
TELEGRAM_BOT_TOKEN
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
BASE_URL
OWNER_ID
DATABASE_URL
```

`DATABASE_URL` é opcional. Se ausente, o projeto usa SQLite em `/data/app.db`.
