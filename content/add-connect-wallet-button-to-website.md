---
title: "How to Add a Connect Wallet Button to Your Website (Read-Only)"
h1: "How to add a Connect Wallet button to your artist website: read-only, four chains, never signs"
slug: add-connect-wallet-button-to-website
description: "How to add wallet connect to your website without writing code: a read-only button for Ethereum, Base, Tezos and Solana, from a vibe coded AI Art site."
target_keyword: "how to add wallet connect to my website"
secondary_keywords:
  - "add connect wallet button to website"
  - "thirdweb connect wallet button"
canonical: "{{HUB_URL}}/add-connect-wallet-button-to-website/"
og_image: "visuals/w2-connectors.png"
status: draft
published: "2026-11-06T10:09:49-06:00"
updated: "2026-11-06T10:09:49-06:00"
---

Search for how to add wallet connect to a website and most answers are developer code: install a library, paste a component, wire up a provider. That is fine if you write code. Most artists don't. And the real question collectors ask is not "how" but "is it safe?"

This article is how the Connect Wallet button on [circularsurrealism.com](https://circularsurrealism.com) was built. Slowfreeze, an AI artist, vibe coded the whole site in Grok Build, and the wallet room was one feature of it: **25 prompts, 14 fix rounds and 914 builder steps over 3 active days (19 to 23 September)**. It connects on Ethereum, Base, Tezos and Solana, it is read-only, and it never asks a collector to sign anything.

## What does a Connect Wallet button actually do on an artist site?

On the case-study site, the wallet room is called **You hold**. A collector connects a wallet, and the page shows which works from this site that wallet holds, named by their ENS or Tezos alias where one exists.

That is the whole job. It is not a mint button, it is not a checkout, and it does not move anything. It answers one question for a collector: "what do I own from this artist?"

## Is it safe to connect a wallet to a website?

Before shipping it, the author asked the builder directly: "Is it completely safe to connect your wallet in the three chains?"

The builder checked what the connect flow requests from each wallet and confirmed it: the wallet only shares its **public address**, the same one anyone can already see on a marketplace. It never asks to send, transfer, approve or sign. The connect sheet says this out loud and never lists "send".

![The wallet connect sheet, stating it is read-only](visuals/w2-read-only.png)

That gives you the rule for your own button:

1. Ask the builder exactly what the connect flow requests from each wallet.
2. Make sure it only asks for the public address.
3. Write the promise on the connect sheet in plain words: "read-only: never asks to send, approve or sign".
4. Ask the same question again after every change to the flow.

Unclear wording scares people. A plain promise on the sheet does more for trust than any logo.

## Which wallet connectors work for Ethereum, Base, Tezos and Solana?

The goal was a button that connects "when you are on a normal browser", not only inside a wallet's own browser. The case study uses one connector per chain:

| Chain | Connector |
|---|---|
| Ethereum and Base | WalletConnect |
| Tezos | Beacon |
| Solana | A Phantom app link |

![One connector per chain: WalletConnect, Beacon and Phantom](visuals/w2-connectors.png)

If you are wondering about the thirdweb connect wallet button that shows up in so many tutorials: the case-study site does not use thirdweb. Grok Build wired the connectors above directly. Any of these routes can work; what matters is that the button stays read-only and works on a phone.

One practical recommendation: get your own WalletConnect project ID from Reown's dashboard, and keep it in the project's settings, not pasted into the code.

The prompt that starts it:

```prompt
Add a connect button for [chains] that works from a normal browser, is read-only, never asks to send or sign, and shows the items from my site that wallet holds. On the connect sheet, say plainly that it only shares the public address.
```

## What broke on the way, and how was it fixed?

Fourteen fix rounds is a lot for one button. Here is what actually went wrong, so you can recognise it on your own site:

- **Phantom opened a web page instead of the app.** The fix was to ask for the wallet's app link.
- **Tezos crashed with an error**, and later broke again while other chains were being fixed.
- **Phantom lost the session** when the collector came back from the app.
- **Fixing one chain broke another.** The rule that came out of it: fix one chain at a time, and retest all the others after every fix.

```prompt
[Chain] is not connecting: [what happens]. Fix only [chain]. Do not change the other chains. After the fix, tell me how to test each chain on a phone.
```

## Why does the wallet extension say "unexpected error" on desktop?

Phones worked first. On a computer, the MetaMask and Phantom extensions said "unexpected error", even when they were installed.

The author's instruction was to fix desktop "and do not touch anything of how it's on mobile". The final fix: on desktop, Ethereum and Phantom open the connect step in a small window of their own, where Chrome can show the extension's approval. The phone path was left alone.

The lesson is bigger than wallets: when one platform works, name it as the thing that must not change.

```prompt
This works on the phone but not on desktop. On desktop, [wallet] extensions show [error]. Fix desktop only (for example by opening the connect step in its own small window) and do not touch the mobile version.
```

## How does the site know which works a wallet holds?

The case-study code reads holdings from public chain explorers: **Blockscout** for Ethereum and Base, **TzKT** for Tezos, and Solana's public RPC. Then it matches what it finds against the site's own catalog, so a collector sees "this museum, not the whole chain".

At first, the lookup found nothing, even for wallets that held works. It was reading the wrong field on each token. The only way to catch that is to test with a wallet you know holds your work.

```prompt
When a wallet connects (or an address is pasted), read which of my catalog's items it holds on [chains], using public data. Show only items from this site. Test with [a public address you know holds items] and tell me what you find.
```

## Should the page show the collector's name?

"Not a raw string of characters pretending to be a person." When a wallet connects, the case study titles the page with the collector's ENS or Tezos alias when one exists, then shows how many works they hold and in which collections.

What it does not do is publish a public list of collectors. The result stays on the visitor's own screen.

## Before you ship: a short checklist

- [ ] Only the public address is requested, and the sheet says so
- [ ] One connector per chain, each tested on a phone with the real wallet app
- [ ] Desktop extensions tested, with the phone flow unchanged
- [ ] Holdings tested with a wallet you know holds your work
- [ ] Your own WalletConnect project ID, kept out of the code
- [ ] No public list of collectors

The wallet room is one room in a bigger house. For the rest of the structure (the catalog, collections, Available and Collect), see [how to build an artist portfolio website]({{HUB_URL}}/build-an-artist-portfolio-website-with-ai/).

## FAQ

### Do I need to know how to code to add a Connect Wallet button?

No coding experience necessary. On the case-study site, the button was built by describing it to Grok Build, testing it on a phone and on a computer, and saying what was wrong until it worked.

### Can a read-only Connect Wallet button take funds?

The case-study flow only requests the public address. It never asks to send, transfer, approve or sign, and the connect sheet says so. Ask your builder to confirm this for every wallet, and again after every change.

### Does it work on a phone?

Yes. On the case-study site, phones worked first and desktop extensions needed their own fix. Test both.

### How long did it take?

25 prompts and 14 fix rounds over 3 active days, from 19 to 23 September.

## Go further

The whole wallet room, lesson by lesson with the prompts, is in **The House Guide**, in its optional Web3 track. **Quick Start** covers planning, performance and publishing.

- [Free performance checklist]({{CHECKLIST_URL}})
- [Quick Start, $19]({{QUICKSTART_URL}}): foundation, performance and publishing, 39 lessons
- [The House Guide, $39]({{GUIDE_URL}}): the whole build, 107 lessons

{{FOUNDING_PRICE_LINE}}

*Built with Grok. The case-study site was built with Grok Build by xAI. This article and the guides are independent and are not made, endorsed or sponsored by xAI.*
