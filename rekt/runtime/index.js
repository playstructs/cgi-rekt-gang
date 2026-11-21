// The Rekt Gang overlay's runtime, loaded ahead of structs-webapp's entry.
//
// __rekt.guild is the guild this page plays through, Rekt Gang (guild.js),
// __rekt.recovery moves a recovered player of another guild into it
// (recovery.js), __rekt.pfp shows players' own pictures (pfp.js) and
// __rekt.gallery lets a player pick a Rekt Gang NFT as theirs, at sign-up and
// on their profile (gallery.js). rekt/patches.cjs points webapp's code at them.
// __rekt.account creates the account at sign-up without showing its recovery
// key, and offers Download Player in place of Log Out (account.js).
import {guild} from './guild.js';
import {recovery} from './recovery.js';
import * as pfp from './pfp.js';
import {gallery} from './gallery.js';
import {account} from './account.js';

globalThis.__rekt = Object.freeze({guild, recovery, pfp: Object.freeze({...pfp}), gallery, account});
