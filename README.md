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
| `pfp` | a picture `rekt/pfp/collections.json` lists isn't in `rekt/pfp/` | run `rekt/make_pfps.py` |

`npm test` fails while any remain. The build shows stale patches as warnings.
Commit the submodule pointer together with the overlay.

## Profile pictures

Every portrait (the HUD, profile, guild roster, player search, scans, spectator
and device activation) shows the player's own picture, their `pfp` on chain,
when it is a URL a browser can load: `https` (`http` is upgraded), or `ipfs://`,
`ipns://` and `ar://` through the ipfs.io and arweave.net gateways. webapp's
generated portrait stays underneath, and shows when a player has no such
picture or it fails to load (`rekt/runtime/pfp.js`). Sector Blitz's public raid
lists are the exception: the guild API sends them only the generated portrait's
attributes, so they show a player's picture only when it is in those too, as it
is for everyone who signs up here.

### The Rekt gallery

Members choose their picture from every Rekt Gang NFT, which this site hosts
itself, at `https://rekt.structs.zone/rekt/pfp/<collection>/<id>.webp`:

| Collection | `<collection>` | Numbers |
|---|---|---|
| Rekt Wolves | `wolves` | 1 to 2222 |
| Trippy Wolves | `trippy-wolves` | 1 to 2222 |
| Rekt Bulls | `bulls` | 1 to 2269 (no #364: its image is lost from IPFS) |
| Rekt Chickens | `chickens` | 1 to 16420 (Stargaze 1–5000, Solana 5001–10000, Polygon 10001–16420) |
| Based Rekt Chickens | `based-chickens` | 1 to 1000 (Base) |

The gallery has a tab per collection (webapp's own nav tabs), each one endless
scroll of its pictures, edge to edge; images load as they come into view, and
the grid holds only the rows around what's in view, so even the 16,420 Chickens
scroll and jump at once. A player who knows their picture's number finds it:
the gallery scrolls to it and outlines it. Clicking a picture chooses it. No
wallet is involved: the picture is the player's choice. Its controls are
webapp's own SUI components: nav tabs, screen buttons, the text input and its
warning, and the close link (`rekt/runtime/gallery.js`).

It opens from two places:

- **Sign-up**: **Choose Rekt**, beside the generated picture. That URL can't go
  into the sign-up request's `pfp`: the guild API requires it to be JSON, which
  the chain then refuses as a pfp. So it goes in `pfp_client_render_attributes`
  as `url` (beside the generated layers, which other clients keep showing), the
  player joins with it, and when they first play, their own key sets their
  `pfp` on chain to the same URL (`MsgPlayerUpdatePfp`).
- **Profile**: the edit button on a member's own portrait. Their key sets the
  new picture as their `pfp` on chain at once (`MsgPlayerUpdatePfp`), and the
  profile and HUD show it.

Rekt pictures are shown from whichever host serves the page (`/rekt/pfp/…`),
so they show in development too; other clients load them from
rekt.structs.zone.

The pictures are made from the Rekt Gang NFT archive (`../RektGang`, with its
`README.txt`) by [`rekt/make_pfps.py`](rekt/make_pfps.py): 256px square WebP,
the illustrated collections resized (quality 80), the pixel-art Chickens kept
pixel for pixel (4×, lossless, and drawn sharp at any size). They come to about
93 MB in 24,132 files, which the dev server serves from disk and the build
copies into `dist/rekt/pfp/` as they are. `rekt/pfp/collections.json` lists
the collections for the gallery.

```bash
../RektGang/.venv/bin/python -I rekt/make_pfps.py ../RektGang   # keeps existing pictures
```

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
| Sign-up (TSA) | player `1-14654` (`structs1h7qgjwzwtyywuwmg4r2dm2gek9ne4gvlq8psad`), the host's proxy-join signer: 512 (GuildMembership) on `0-8`, 1024 (SubstationConnection) on `4-19` |
| Bank denom | `rug` / `urug` (in guild.json) |

## Building and serving

```bash
npm run build        # dist/
```

`dist/` is a static site: `index.html` (webapp's game page), the bundles in
`js/` and webapp's `css/`, `img/`, `lottie/` and fonts, plus `guild.json` and
Rekt Gang's art in `rekt/`, its NFT pictures in `rekt/pfp/`. It uses absolute paths, so serve it from the root
of `rekt.structs.zone`; it needs nothing else on that domain, but `guild.json`
must be readable cross-origin (`Access-Control-Allow-Origin: *`), since other
clients read it. `.github/workflows/pages.yml` publishes it to GitHub Pages.

## Licences

structs-webapp is Apache-2.0 (Slow Ninja Inc). Rekt Gang's logo and icons in
`rekt/public/`, and the NFT art in `rekt/pfp/`, are Rekt Gang's own, used for
its guild.
