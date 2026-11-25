---
title: "Auto-Display New NFT Mints on Your Website"
h1: "How to auto-display new NFT mints on your website: one sync, five places, real bugs"
slug: auto-display-new-nft-mints-on-website
description: "How one AI Art site auto-displays new Ethereum and Tezos NFT mints: contract map, dedupe, 10-minute cache, and the bugs that taught the rules."
target_keyword: "auto display new NFT mints on website"
secondary_keywords:
  - "auto display nft mints on website"
  - "sync new nft mints to website"
  - "nft mint feed on artist website"
  - "ethereum tezos mint sync website"
canonical: "{{HUB_URL}}/auto-display-new-nft-mints-on-website/"
og_image: "visuals/cover-auto-mints.jpg"
status: draft
suggested_publish: "2026-11-16"
sources_checked: "2026-11-09"
published: "2026-11-16T10:21:39-06:00"
updated: "2026-11-16T10:21:39-06:00"
---

Every new mint used to mean opening the catalog by hand. Add the piece, wire its collection, check five places, publish. On [circularsurrealism.com](https://circularsurrealism.com), that stopped. One mint-sync now picks up new Ethereum and Tezos mints and puts them where a hand-added piece already goes.

This is the real build story from 6 November 2026: what was reused, what broke, and the checks that proved it. The case-study site holds **440+ works in 27 collections**, vibe coded over **400+ prompts**.

![I Stopped Adding New Mints by Hand. The Site Catches Them Now.](visuals/cover-auto-mints.jpg)

## What does "auto-display" mean here?

Not a second inventory. The site already had a path for a hand-added piece. Sync extends that path.

When a new mint is picked up, it reaches the same destinations a hand-added piece reaches:

1. Its collection card
2. Latest from the studio (animated card when the media is animated)
3. The Activity ledger, with the real on-chain mint time when the explorer has it
4. Recent mints
5. Its own piece page, with full media

On top of that, for Based Knights, Based Knights • Short Films, Mystic Orbs and Mystic Orbs • Short Films, the mint is also added to the home hero. The hero stays curated: nothing is pushed out, and the first slide stays a still image.

If the explorer has not indexed the mint yet, the piece can still appear, and the mint time fills in on a later check.

## Start from the hand-added path, do not build a second system

The first sync, around 4:15 PM CT on 6 November, covered Based Knights Ethereum contracts only. It checked about every 10 minutes and on visit. Tokens already in the catalog were skipped, so a repeat run was safe.

Files that path already touched included the catalog, the knights and listings APIs, knight-sync, the site shell, collection pages, piece pages, Collect and the atlas. The lesson was written into the next prompt: generalize that sync. Do not invent a parallel catalog.

## All-chains sync: Ethereum map plus Tezos

Around 5:28 PM CT the all-chains prompt landed. Mint-sync now covers:

- every Ethereum contract in the map
- new contracts minted from the artist's Ethereum wallet (slowfreeze.eth)
- Tezos via TzKT (slowfreeze.tez plus the gallery contract)

A live pass that day added zero pieces. That was expected: nothing new had minted yet. The dry run still mattered. It skipped three things on purpose: the slowfreeze.tez domain token; Mystic Knights Genesis #17 (no metadata, burned); and extra Harmonious Symphony token numbers for the same edition.

## Dedupe key: chain + contract + tokenId

The unique key is chain + contract + tokenId. Hand-added entries win.

A dedupe test checked pieces that already existed: Ethereal (Tezos #31) and Mystic Orb #57 • Short Film (Ethereum #15). Each still appeared once and stayed unchanged.

Shared contracts only accept tokens whose creator or first minter is the artist's wallet. Other artists' tokens on the same contract never enter the catalog.

## Unknown contract: show the piece, do not invent a collection

If a new token's contract is not in the map, the piece still appears in Latest, the Activity ledger, Recent mints and its own page. It does not enter a collection. The sync logs needsRoom so a collection can be assigned later. Adding the contract to the map later moves those pieces in automatically.

## The hero stays curated (and still picks up the right new mints)

Around 6:40 PM CT the artist asked whether new mints should also enter the hero. Answer: the hero stays curated. New mints from Based Knights, Based Knights • Short Films, Mystic Orbs and Mystic Orbs • Short Films are added on top. Nothing is pushed out. The first slide stays a still image. Tezos pieces and older collections stay out of that auto-hero rule.

Live check on 9 November 2026: the home hero carousel included **Vortyx • Glitched Knight #4** (Based Knights) among its slides (seen as slide 8 of 73 in a desktop pass).

## Cache and the rescan bug

A live check around 7:04 PM CT called `/api/mints` twice, 17 seconds apart, and got different refreshedAt values. Each server was keeping its own memory, so every request could rescan.

A two-fix prompt around 7:17 PM CT fixed that: one result kept for 10 minutes, in memory and on disk, with `s-maxage=600` for the CDN. The live site uses that 10-minute sync only.

By about 7:39 PM CT a live check matched: the same refreshedAt across calls, cache-control `public, max-age=0, s-maxage=600`, and known edition labels such as Celestial and Cosmic Pie stayed "edition of 5".

If a chain fails, the last good result stays up. `/api/mints` returns per-chain ok/added.

## Edition labels and the ENS pitfall

ERC-1155 reads totalSupply(tokenId): 1 becomes "1/1", more than 1 becomes "edition of N", and 0 is treated as burned and skipped. ERC-721 is always 1/1.

The first try swept every ERC-1155 in the wallet and pulled in ENS names and other non-AI-Art tokens. That sweep was taken back out. Lesson: filter to AI Art contracts and the creator wallet, not "everything this wallet ever touched".

## What still stays manual

- Base (no new mints there)
- Solana (Mallow)
- Light 720p card loops built at publish time (the card can play the full file until a loop is added)
- The sitemap (a new piece gets in after it is saved to the catalog and published)

## First real proof: Vortyx

Verified on 9 November 2026 (America/Chicago) against the live site, `/api/mints`, phone screenshots from the user, and a headless browser pass:

- **Vortyx • Glitched Knight #4** is on Ethereum contract `0x93f21bb8462a3485f05fae28c46064d64dd9623b`, tokenId **1**, edition **1/1**, clan Glitched
- On-chain mint time **2026-11-08T00:46:47.000000Z** (7 November 2026, 6:46 PM CT), tx `0x6c16d226341d1c168695edc351bcdcd1149e375c054d0f8ce8f239296a1aaf21`
- Piece page live: https://circularsurrealism.com/works/bk-still-eth-1
- **Vortyx • Glitched Knight #4 • Short Film** is on Ethereum contract `0x12b0ebae8e7ae334bb53d6c4c349e71464e28543`, tokenId **1**, piece page https://circularsurrealism.com/works/bk-film-eth-1
- Short Film on-chain mint time 7 November 2026, 7:51:35 PM CT, tx `0x3327f0abccd9f421a8bbabf350aadf08c5313623b557bbac054bf66686c5b245`
- Transient listings exist for both tokens
- `/api/mints` reported ethereum ok with added 2, tezos ok with added 0, `every: 10m`, empty needsRoom, stable refreshedAt across two calls, cache-control `public, max-age=0, s-maxage=600`

Where it showed up on the site:

- **Home hero:** Vortyx still in the curated carousel (added on top)
- **Latest / From the studio:** Vortyx Short Film first; Vortyx still second, listed at 0.0411 ETH
- **Activity ledger:** Vortyx in Listed lots at 0.0411 ETH; Recent mints shows Vortyx first
- **Based Knights collection:** Vortyx first of **17** works (Ethereum card beside the Base Glitched Knights)
- **Piece pages:** both still and Short Film URLs above return 200

![Home hero carousel on desktop with Vortyx • Glitched Knight #4 as the current slide.](visuals/hero-vortyx.png)

![Home page, Latest / From the studio: Vortyx Short Film first, Vortyx still second at 0.0411 ETH.](visuals/home-from-the-studio-vortyx.jpg)

![Activity ledger, Recent mints, with Vortyx first.](visuals/activity-vortyx-filled.png)

![Activity ledger, Listed lots: Vortyx at 0.0411 ETH on Transient Labs.](visuals/ledger-listed-vortyx.png)

![Based Knights collection, 17 works, Vortyx first on Ethereum.](visuals/based-knights-vortyx-filled.png)

## Key steps if you vibe code the same idea

1. Read how a hand-added piece reaches the site today
2. Extend that path; do not build a second system
3. Write a contract map plus creator-wallet discovery
4. Dedupe on chain + contract + tokenId; let hand-added entries win
5. Dry run, then a dedupe test on pieces you already know
6. Cache the result for about 10 minutes
7. Check live with two calls a few seconds apart

## FAQ

### Can new NFT mints show on a website without editing the catalog each time?

Yes, if you extend the same path a hand-added piece already uses. On the case-study site, mint-sync covers mapped Ethereum contracts, new contracts from the creator wallet, and Tezos via TzKT.

### How often does the sync run?

About every 10 minutes, and on visit, with a 10-minute cached result (`s-maxage=600`).

### What if the marketplace has not indexed the mint yet?

The piece can still appear. The mint time fills in on a later check when the explorer has it.

### Does this replace hand-added pieces?

No. Hand-added entries win on the same chain + contract + tokenId key.

### Do I need to know how to code?

No coding experience necessary. The case-study site was vibe coded in Grok Build.

## Go further

The multi-chain collection pattern that sits next to this sync is written up in the guides, and the whole vibe coding build is in **The House Guide**. **Quick Start** covers planning, performance and publishing.

- [Free performance checklist]({{CHECKLIST_URL}})
- [Quick Start, $19]({{QUICKSTART_URL}}): foundation, performance and publishing, 39 lessons
- [The House Guide, $39]({{GUIDE_URL}}): the whole build, 115 lessons

{{FOUNDING_PRICE_LINE}}

*Built with Grok. The case-study site was built with Grok Build by SpaceXSI. This article and the guides are independent and are not made, endorsed or sponsored by SpaceXSI.*
