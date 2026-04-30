# Diagnóstico Técnico Atual — Private Tools e Segurança

## Status

Documento atualizado para refletir a versão atual do bot e seus comandos administrativos ativos.

## Fluxo atual

O bot usa FastAPI com webhook e um único dispatcher principal. No startup, o app inclui os routers administrativos e registra os handlers principais.

Routers ativos:

- `private_tools`;
- `lili_rodou`;
- `plus`;
- handlers registrados por `_register_handlers`.

## Segurança administrativa

Os comandos administrativos privados devem ficar restritos ao `OWNER_ID`, definido por variável de ambiente e centralizado em `app/config/settings.py`.

Comandos administrativos atuais:

```text
/dx
/ddx
/mx1
/mx2
/joinx
/vx
/uv
/mx
/ovbx
/lgx
/fdx
/clx
/xend
/ximg
/hidden
/vvv
/plus
```

## Join request

O fluxo atual possui handler de `chat_join_request`, registra pedidos em `join_requests` e permite aprovação manual com `/joinx`. O comando também tenta fallback direto pelo Telegram quando o registro local não existe.

Para maior confiabilidade, o webhook é registrado com `allowed_updates=dispatcher.resolve_used_update_types()`.

## Moderação

O comando `/dx` apaga uma ou mais mensagens por link. O bot precisa ter permissão administrativa para apagar mensagens no chat de destino.

## Observações de produção

- Validar `python -m compileall .` antes do deploy.
- Validar `python -c "import app.main; print('import ok')"` no ambiente com dependências instaladas.
- Testar `/hidden`, `/dx`, `/mx2`, `/joinx`, `/vvv`, `/plus`, `/playing` e callbacks de like/play no Telegram real.
