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
- Copiar mensagens enviadas ao bot no privado para um chat de destino com `/xend` usando `copy_message`, com opção de fixar usando `/xend pin`.
- Aceitar aliases opcionais de `chat_id` via variável `CHAT_ALIASES`.

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

Todos os comandos abaixo devem ser usados no privado do bot e são restritos ao `OWNER_ID`.

Quando configurado, `<chat_id>` aceita tanto ID numérico quanto alias definido em `CHAT_ALIASES`.

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

/xend pin <chat_id>
Usar respondendo, no privado do bot, a mensagem que deve ser copiada e fixada no destino.

/ximg
<chat_id>

/hidden

/vvv
<chat_id>
<user_id>
```

## Aliases de chat_id

A variável `CHAT_ALIASES` permite configurar apelidos para grupos no Railway sem alterar o código.

Exemplo:

```text
CHAT_ALIASES={"geeks":-1001234567890,"royal":-1009876543210}
```

Com essa configuração, comandos como estes passam a ser equivalentes:

```text
/ximg
geeks
```

```text
/ximg
-1001234567890
```

A resolução de alias é aplicada apenas em mensagens privadas do `OWNER_ID` e apenas para comandos administrativos que já recebem `<chat_id>`. Se a variável estiver ausente, vazia ou inválida, o comportamento antigo com IDs numéricos permanece inalterado.

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

Para copiar e fixar a mensagem no chat de destino, use:

```text
/xend pin <chat_id>
```

O bot usa `copy_message` para reenviar ao destino a mensagem respondida, preservando mídia, legenda e entidades de formatação quando o Telegram permitir. Na variação `pin`, depois da cópia, o bot tenta fixar a mensagem enviada.

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
CHAT_ALIASES
```

`DATABASE_URL` é opcional. Se ausente, o projeto usa SQLite em `/data/app.db`.

`CHAT_ALIASES` é opcional. Se ausente, o bot mantém o comportamento antigo e usa apenas IDs numéricos.