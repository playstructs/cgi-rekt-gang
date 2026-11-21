# The Rekt Gang overlay

Everything in this directory is applied to the `structs-webapp` submodule as it
is built. Nothing in the submodule is edited. The client stays in English;
there is no translation layer.

| Path | What it is |
|---|---|
| `patches.cjs` | `[exact upstream text, replacement]` pairs per upstream file: the guild connection, recovery, the telemetry name, players' own pictures, the Rekt gallery, and Rekt Gang in place of SN Corp in sign-up and the tutorial |
| `runtime/` | Loaded before webapp's entry as `__rekt`: `guild` (`guild.js`, the services of the guild the page plays through, Rekt Gang `0-8`), `recovery` (`recovery.js`, moving a recovered player of another guild into it), `pfp` (`pfp.js`, every portrait showing the player's `pfp` URL over the generated one, and setting a sign-up picture as `pfp` on chain), `gallery` (`gallery.js`, the Rekt NFT gallery, at sign-up and on a member's own profile) and `account` (`account.js`, creating the account at sign-up without a recovery key section, and Download Player in place of Log Out) |
| `pfp/` | The Rekt Gang NFTs players choose from, `<collection>/<id>.webp`, and `collections.json`; made by `make_pfps.py` from `../RektGang`, served at `/rekt/pfp/` |
| `public/` | Static files served over webapp's: `guild.json` (guild `0-8`'s on-chain endpoint), `favicon.ico`, and `rekt/` with `rekt.css`, the sign-up badge, the guild logo and icons |
| `page.cjs` | Renders webapp's Twig page (`templates/`) to `index.html`, adding Google Tag Manager (`GTM-58HZKHDD`), the icons and `rekt.css` |
| `overlay.cjs`, `loader.cjs` | Apply `patches.cjs` to each source file webpack reads |
| `check.cjs` | `npm run check` / `npm test`: stale or orphaned patches, SN Corp left on screen, guild.json against `GUILD_ID`, pictures missing from `pfp/` |

## Writing a patch

```js
'js/view_models/signup/Orientation7ViewModel.js': [
  ['on behalf of SN.CORPORATION.`', 'on behalf of REKT GANG.`'],
],
```

- The first string is copied exactly from the upstream file; every occurrence
  is replaced, in one pass, longest first.
- Include enough around it (quotes, tags) that it only matches what you mean,
  never an id, class, storage key or anything sent to the guild or the chain.
  CSS classes such as `snc-logo` keep webapp's names.
- One key per upstream file: a second entry for the same file replaces the
  first.

## The art

`public/rekt/img/rekt-gang-badge.png` is Rekt Gang's wordmark
(`../RektGang/logos/community/rekt-gang-logo.png`, trimmed) in the top of a
384px square, the shape of webapp's 192px sign-up logo slot, with the motto set
under it by `rekt.css`. `rekt-gang-logo.png` is the same wordmark, 512px
square, for `guild.json`. The icons are Rekt Gang's own (`logos/icons/`).

`pfp/` holds every Rekt Gang NFT as a 256px WebP: Rekt Wolves, Trippy Wolves,
Rekt Bulls, Rekt Chickens (Stargaze, Solana and Polygon, numbered 1 to 16420)
and Based Rekt Chickens. See the main README's *Profile pictures*.
