// The Rekt Gang overlay's runtime, loaded ahead of structs-webapp's entry.
//
// __rekt.guild is the guild this page plays through, Rekt Gang (guild.js), and
// __rekt.recovery moves a recovered player of another guild into it
// (recovery.js). rekt/patches.cjs points webapp's code at both.
import {guild} from './guild.js';
import {recovery} from './recovery.js';

globalThis.__rekt = Object.freeze({guild, recovery});
