---
title: "How to Make a Website to Sell Your AI Art: Prints and 1/1s"
h1: "How to make a website to sell your AI Art: prints, 1/1s and one home for both"
slug: make-a-website-to-sell-your-ai-art
description: "How to make a website to sell your art when it lives on marketplaces and as prints: the shop, editions and live marks from a real vibe coded AI Art site."
target_keyword: "how to make a website to sell my art"
secondary_keywords:
  - "how to make a website to sell your art"
  - "how to sell prints of your digital art"
  - "how to sell ai art online"
canonical: "{{HUB_URL}}/make-a-website-to-sell-your-ai-art/"
og_image: "visuals/s3-shop-page.png"
status: draft
published: "2026-11-09T10:11:11-06:00"
updated: "2026-11-09T10:11:11-06:00"
---

Ask how to make a website to sell your art and the usual answer is a store builder: pick a template, add products, connect payments. That works if every piece you sell sits in one stock room. It does not fit an AI artist whose one-of-ones are listed on several marketplaces and whose prints are made and shipped by a print partner.

[circularsurrealism.com](https://circularsurrealism.com) has exactly that problem. Slowfreeze, an AI artist, vibe coded it in Grok Build as one home for both: one-of-ones and editions that sell on marketplaces, and fine art prints through **INPRNT**. The site doesn't take payments itself. It shows what is for sale right now and sends each buyer to the right place.

The prints shop alone took **47 prompts, 11 fix rounds and 5 active days (12 to 23 October)**, the most prompts of any feature in the build. Here is what came out of it.

## Do you need your own checkout to sell art online?

Not necessarily. On the case-study site, every buy button goes to someone else's checkout:

- **One-of-ones and editions** go to the marketplace where the piece is listed.
- **Prints** go to INPRNT, the print partner, which makes and ships them.

The website's job is to be the place people come back to: the whole body of work, what is available today, and a clear way to buy it. That splits the work into three rooms.

| Room | Its one job |
|---|---|
| Available | "The shop floor": only what is listed right now, with the buy button on the card |
| Prints | Fine art prints, through the print partner |
| Collect | Where to buy, by market |

![Collection rooms and the prints room on circularsurrealism.com](visuals/s3-rooms.png)

## How do you keep the "for sale" page true without updating it by hand?

The author did not want to log in every Sunday to type that something sold. So the site listens to the marketplaces instead.

In the final case-study code, live listings are read from **Transient Labs, Manifold, Objkt and Networked.art**, and the builder set them to refresh about every 90 seconds. Other marketplaces, such as OpenSea and Zora, are used as links, not live data. Everything reads from one merged list: the homepage sales row, the Available page, the marks on every card and the sales ledger.

The Available page is not a second inventory. It is that live list, filtered to what is for sale, with filters for category, shop and type. When something sells, it leaves the page on its own.

```prompt
My work is listed on [marketplaces], from these wallets/contracts: [public addresses or collection links]. Check which marketplaces have a public API you can poll for live listings and sales. Poll those, merge them into one list, and use the others only as links. Give me a list of which are live and which are not.
```

## What should a card say: Live, Listed or Sold?

The first version showed "Live" on some cards and "Listed" on others. Visitors were confused, because they were all simply for sale. The fix: one **Listed** mark (or **Sold**) on every card, a countdown only on auctions that are actually running, and plain cards for anything not for sale.

![Cards with a Listed mark, a Sold mark and a plain card](visuals/s1-status-marks.png)

## Why is a transfer to an auction not a sale?

This one catches anyone who reads sales from the chain. Many transfers from the artist's wallet were "just me listing the piece for auction so it goes to the platform auction contracts and it shows like if it was a sale". The first build counted those transfers as sales.

The fix was to exclude transfers into marketplace auction (escrow) contracts and count only settled sales. If your site shows a sales total, compare it with sales you know before you trust it.

## How do you sell prints of your digital art from your own site?

When the prints started, they got their own door, not a link hidden in the footer:

- a homepage rail, **"Fine art prints from the studio"**, newest first and swipeable;
- a **Prints** page next to Available in the navigation;
- an **"All prints"** page with the same small filter button as the collection pages.

A new print enters the same rail.

![A collection page with the small filter button open](visuals/s3-category-page.png)

```prompt
Create a new section dedicated to [prints / products / services]: a row on the homepage, newest first, that people can swipe; a [Shop] page next to [Available] in the navigation; and an "All [items]" page with the same filter button as the category pages.
```

## How do you show editions and stock honestly?

Limited print editions on the case-study site are numbered per size, and the page shows how many are left in each size instead of one total. One edition is 111 in each of five sizes, 555 in all. Another is 50 per size with one held back, so the page says 49 of 50.

One pile for all sizes misleads buyers. Show the count per size.

## What goes on a print page?

Two lessons came out of the 11 fix rounds:

1. **Use the partner's own words** for how each format is made. Screenshot the partner's descriptions and ask for the text word for word.
2. **Show buyer prices, not your cost.** The first version used the seller's cost prices. Later, the frame price line was confusing ("the price is the frame, not the print") until it was rewritten to say the price is the print already in that frame, at that size.

Then one template for every print page, in this order: the buy button (to the partner), a link to the original work when it exists, "From the artist" (a short story), a separator line, the paper and specs, the sizes beside the image, the zoom viewer, and more prints at the bottom. Once it worked, the author asked the builder to "remember this structure" for every future print.

![A print page: buttons, story, sizes and more prints](visuals/s3-shop-page.png)

```prompt
Use the partner's product descriptions exactly as in these screenshots, and show buyer prices, not my cost. For frames, say clearly that the price is the [print] already in that frame, at that size.
```

## Does this only work for AI Art?

No. The pattern is a catalog, a live "available" page, and a shop that hands buyers to a partner. It fits a painter with an online gallery, a photographer with a print lab, or a maker with a shop elsewhere. For the full set of rooms, see [how to build an artist portfolio website]({{HUB_URL}}/build-an-artist-portfolio-website-with-ai/), and for the method behind the whole build, [how to build a website with AI, step by step]({{HUB_URL}}/how-to-build-a-website-with-ai/).

## FAQ

### Can I sell my art on my own website without a store builder?

Yes, if someone else handles the checkout. The case-study site sends buyers to marketplaces for one-of-ones and editions, and to INPRNT for prints. The site itself shows what is for sale and where.

### Do I need to know how to code to build this?

No coding experience necessary. The whole site was vibe coded in Grok Build: the artist described each room, checked the preview, and said what was wrong until it was right.

### How long did the prints shop take?

47 prompts and 11 fix rounds over 5 active days, from 12 to 23 October. It was the feature with the most prompts in the build.

### How do I stop sold work from showing as available?

Read listings from the marketplaces instead of typing them in. On the case-study site, listings refresh about every 90 seconds, and sold work leaves the Available page on its own.

## Go further

The catalog, collection pages and shop, the live marks and the optional Web3 rooms are all in **The House Guide**, lesson by lesson with the prompts. **Quick Start** covers planning, performance and publishing.

- [Free performance checklist]({{CHECKLIST_URL}})
- [Quick Start, $19]({{QUICKSTART_URL}}): foundation, performance and publishing, 39 lessons
- [The House Guide, $39]({{GUIDE_URL}}): the whole build, 102 lessons

{{FOUNDING_PRICE_LINE}}

*Built with Grok. The case-study site was built with Grok Build by xAI. This article and the guides are independent and are not made, endorsed or sponsored by xAI.*
