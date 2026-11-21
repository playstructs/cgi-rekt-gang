# rekt.structs.zone — Structs for Rekt Gang

The [structs-webapp](https://github.com/playstructs/structs-webapp) game client
for [Rekt Gang](https://www.rektgang.com/)'s Structs guild (`REKT`, guild
`0-8`). structs-webapp is a git submodule (`structs-webapp/`, following its
`main`) and its client is built as it is: its own JavaScript, page, styles and
art, in English, with its webpack configuration as the starting point. What
this repository adds is the overlay in [`rekt/`](rekt/README.md), applied while
webpack reads webapp's sources. Nothing in the submodule is edited, so a newer
structs-webapp builds with the same overlay.

Only the client side is used. This site hosts no guild API of its own: the page
talks straight to the guild's API, its GRASS feed and its chain node, which
`beta.playstructs.com` runs for Rekt Gang.

Onboarding and tutorial telemetry is reported with the interface name
`rekt.structs.zone`, so these runs can be told apart from other clients' in the
guild's reports (`?interface_name=rekt.structs.zone`).

## Setup

```bash
git clone --recurse-submodules <this repository>
npm install          # also installs structs-webapp/src's own dependencies
npm run dev          # http://localhost:5191
```

## Updating structs-webapp

```bash
npm run update:webapp
```

This moves the submodule to the latest `main`, installs its dependencies and
runs the check, which lists what the update touched:

| Report | Meaning | What to do |
|---|---|---|
| `stale` | upstream changed the text a patch replaces | fix the patch in `rekt/patches.cjs` |
| `orphan` | a patched upstream file is gone | move or delete its patches |
| `branding` | SN Corp is named somewhere a player sees | add a patch naming Rekt Gang |
| `guild` | `rekt/public/guild.json` and `GUILD_ID` disagree | fix whichever is wrong |

`npm test` fails while any remain. The build shows stale patches as warnings.
Commit the submodule pointer together with the overlay.

## Which guild

The site is Rekt Gang's: its guild is `0-8`, fixed in `webpack.config.js`
(`GUILD_ID`), and never looked up. Webapp normally asks its guild API which
guild it is (`/guild/this`), but Rekt Gang shares SN Corp's API, so the page
asks for `/guild/0-8` instead.

Before webapp's code starts, the page reads `0-8`'s `guild.json` (the endpoint
the guild set on chain, `https://rekt.structs.zone/guild.json`, which this site
serves from [`rekt/public/guild.json`](rekt/public/guild.json)) for its
`guild_api`, `grass_nats_websocket` and `client_websocket`
(`rekt/runtime/guild.js`). If it can't be read, it uses what it last read, then
the fallback in `webpack.config.js`. Requests carry a bearer token from the
guild's `/api/auth/token` (the same signed login as `/api/auth/login`), since a
guild's session cookie would be third-party here.

Account recovery asks the chain which guild the key's player is in before it
calls the guild API, since a shared API may log in another guild's player. A
player of another guild is moved here first: the key signs
`MsgGuildMembershipJoin` for this guild (allowed when its join minimum is 0),
and recovery goes on once the chain shows the move and the guild API knows the
player. Recovery stops instead when the player owns their guild, the guild asks
a join minimum, or the chain can't be read (`rekt/runtime/recovery.js`).

| Variable (build time) | Default | |
|---|---|---|
| `REKT_LCD_URL` | `https://public.testnet.structs.network` | the chain node the guild is read from |
| `REKT_GUILD_API` | — | a fixed guild API (a local guild in development), skipping guild.json |
| `REKT_GRASS_URL`, `REKT_CHAIN_WS` | — | override what the guild publishes |

### On chain

| | |
|---|---|
| Guild | `0-8` Rekt Gang, tag `REKT`, owned by founder player `1-508` |
| Primary reactor | `3-2` ChainTools (`structsvaloper1ch8p2mje28yevt5hrwxscxcvmrjak7jluekfvx`) |
| Entry substation | `4-19`, fed by allocation `6-69` from the guild's own stake |
| Joining | open: join minimum 0, invite bypass permissioned |
| Endpoint | `https://rekt.structs.zone/guild.json` |
| Bank denom | `rug` / `urug` (in guild.json) |

## Building and serving

```bash
npm run build        # dist/
```

`dist/` is a static site: `index.html` (webapp's game page), the bundles in
`js/` and webapp's `css/`, `img/`, `lottie/` and fonts, plus `guild.json` and
Rekt Gang's art in `rekt/`. It uses absolute paths, so serve it from the root
of `rekt.structs.zone`; it needs nothing else on that domain, but `guild.json`
must be readable cross-origin (`Access-Control-Allow-Origin: *`), since other
clients read it. `.github/workflows/pages.yml` publishes it to GitHub Pages.

## Licences

structs-webapp is Apache-2.0 (Slow Ninja Inc). Rekt Gang's logo and icons in
`rekt/public/` are Rekt Gang's own, used for its guild.
