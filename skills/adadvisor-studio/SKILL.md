---
name: adadvisor-studio
description: |
  Have AdAdvisor's ad maker, Iris, draw static ads of a business's own products, then review them with the person. Covers the Product Store, Design Kits, Ad Requests (which spend Credits) and Verdicts on the finished ads. Use when: "make ads for my product", "create static ads", "generate ad creatives", "draw me an ad", "new ad images", "ask Iris", "add my product", "product note", "design kit", "brand look for my ads", "review my ads", "approve this ad", "how many credits do I have". Chain with: adadvisor (always, for the account and its business_id); adadvisor-creative to decide what to test before asking for ads; adadvisor-launch to put an approved ad live. NOT for: uploading images or videos the person already has (use adadvisor-creative); video ads (made in the AdAdvisor app); launching, budgets or targeting (use adadvisor-launch, adadvisor-scale, adadvisor-targeting).
license: Apache-2.0
version: 0.1.0
---

# AdAdvisor: Studio

Iris is AdAdvisor's ad maker. You hand her a **brief**: which products, how many ads, and what the person wants of them. She draws the ads and each one comes back as an **Ad Concept** waiting for the person's **Verdict**. You are the conversation; Iris is the specialist. The better the brief and the more AdAdvisor knows about the product, the better the ads.

Everything here is named by `business_id`, which `adadvisor:list_ad_accounts` answers beside each ad account. It is a UUID, never an ad account id.

## When to use

- The person wants new static ads of a product they sell.
- A product, its pictures or what AdAdvisor knows about it needs adding or fixing.
- The person wants a different look for their ads (a Design Kit).
- Finished ads are waiting for a Verdict.

## Workflow

Run the steps in order. Each ends on a check; do not start the next one before it holds.

### 1. Find the business and what it can spend

Call `adadvisor:list_ad_accounts` for the `business_id`, then `adadvisor:get_credit_balance`.

- `ai_business: false` ends the flow: Ad Requests are for AI Businesses. Tell the person what the answer's `reason` says and where to turn it on. Products, Design Kits and reviewing existing ads still work.
- Note the balance and the price of one static ad. You quote both before spending.

**Done when** you can say: this business, this many Credits, this price per ad.

### 2. Get the product ready

Call `adadvisor:list_products`. If the product is missing, add it: `adadvisor:add_product_from_link` when it has a page (then poll `adadvisor:get_task_status` until `done`), `adadvisor:create_product` when it has none.

Read its `readiness` with `adadvisor:get_product`:

- `can_be_drawn: false` means no picture, and no ad can be made. Add one with `adadvisor:update_product_pictures`.
- `to_improve` lists what would make the ads better. Act on it with the person, in this order of effect:
  1. **The Product Note** (`update_product`, `changes.note`): what the owner knows that the storefront does not say. Who really buys it, what to stress, what objection to answer, what never to claim. Ask the person; write it in their words. It outranks everything else when the ad is written.
  2. **Picture descriptions** (`update_product_pictures`, `describe`): what cannot be told from the picture. Which size or variant, which side, "old packaging, do not use".
  3. **The page link and description**, when the product was added by hand.

A product a connected Shopify store keeps (`store_kept: true`) takes only its note and added pictures here. Its other fields are changed in Shopify.

**Done when** `can_be_drawn` is true and the person has either improved the product or said to go ahead as it is.

### 3. Choose the look

`adadvisor:list_design_kits` shows the kits; the default one is used unless the request names another.

- To try a theme without touching the default: `adadvisor:create_design_kit`, then name it in the request with `design_kit_id`. A new kit is never the default.
- `design_kit: "none"` draws with no kit.
- Making a kit the default (`update_design_kit`, `make_default`) changes every later ad of the business, in the AdAdvisor app too. Do it only when the person asks for exactly that.

**Done when** you know which of the three the request runs under: the default kit, a named kit, or none.

### 4. Agree the brief, then ask

Say back to the person, in one message: the products, the number of ads (1 to 4), the Credits it holds, the balance after, and the look. **Wait for their yes.** This is the only step that spends.

Then call `adadvisor:request_ads` once, with:

- a fresh random `idempotency_key`. Keep it. Sending the same key again returns the same request and never draws or charges twice, so reuse it on any retry of this request and never for a new one.
- what the person asked for, in their words: `brief`, and any of `persona`, `angle`, `format`, `offer`.
- `exact_lines` only for words the person wants set in the picture word for word.
- `placement` when they named where the ad runs.

The Credits for every ad asked for are held at once. Ads that are drawn are charged; the rest come back.

**Done when** the answer carries a `task_id`. A refusal holds nothing and names the fix: follow it, then ask again with the same key.

### 5. Wait for the ads

Call `adadvisor:get_task_status` about every 20 seconds until `status` is `done` or `failed`. Four ads take about five minutes. Tell the person it is running; relay `done` of `requested` as it moves.

When it ends, report: how many ads were drawn, each failure's reason, and the Credits taken and returned.

**Done when** the status is `done` or `failed` and the person has those numbers.

### 6. Review with the person

Call `adadvisor:show_ad_concepts` with `group: "to_review"`. It opens a deck the person swipes: approve, reject with reasons, or ask for a change with a note. **The deck keeps each Verdict itself.** Do not also call `give_ad_verdict` for what they decide there.

Where no deck appears, or the person tells you their decision in words:

1. Read the ads with `adadvisor:list_ad_concepts`, and one in full with `adadvisor:get_ad_concept` when they want to see it.
2. Keep exactly the Verdict they stated with `adadvisor:give_ad_verdict`, sending the `revision_id` they looked at.

A Verdict is the person's judgment, never yours. An approval launches nothing.

**Done when** every ad the person judged has their Verdict, and you have said what is still waiting.

### 7. What happens next

- **Approved** ads are ready and not running. Putting one live is `adadvisor-launch`: register its picture to the ad account with `adadvisor:register_media_assets` (the ad's `media_asset_id`), then build the creative and the ad from the Ad Concept's copy.
- **Changes requested** is kept with the person's note. It is not redrawn on its own yet: for a new take, send a new `request_ads` with the note folded into the brief.
- **Rejected** ads stay as a record of what the person does not want. Carry the reasons into the next brief.

## Decision rules

| Situation | Do |
|---|---|
| Person says "make me some ads" with no product | Ask which product. Never pick one for them. |
| No count given | Propose 2. Four is the most per request. |
| `request_ads` refused for a product little is known about | Offer the fixes in `to_improve`. Send `proceed_anyway: true` only when the person chooses to go ahead as it is. |
| Not enough Credits | Give the numbers from the refusal. Offer fewer ads. |
| Two requests already in progress | Wait for one to finish. Do not queue around the limit. |
| Status stays `working` past ten minutes | Keep polling with the same `task_id`. A request that cannot finish is ended and its Credits returned. |
| A call to `request_ads` timed out or errored | Call it again with the same `idempotency_key`. |
| The person rejects an ad that is running | The tool refuses first. Ask them plainly whether to stop that ad on Meta, and send `confirm_pause: true` only on their yes. |
| Person wants ads with a model or a person in them | Those are made in the AdAdvisor app. A request draws the product. |
| Person wants a specific image generator, a prompt, or to copy another brand's ad | Not available. Put what they want into the brief in plain words. |

## References

- [`references/tools.md`](references/tools.md): one line per tool this skill uses, and what each costs.
- [`references/briefs.md`](references/briefs.md): how to turn what a person says into a brief Iris can draw from, with the fields each part belongs in.

## Anti-patterns

- ❌ Calling `request_ads` because the person sounded keen. ✅ State the count and the Credits, then wait for a yes.
- ❌ A new `idempotency_key` on a retry. That is a second request and a second charge. ✅ One key per request, reused until it answers.
- ❌ Sending `proceed_anyway: true` on the first call to skip the refusal. ✅ Let the refusal list what would help, and let the person choose.
- ❌ Writing a Product Note yourself from the product page. It repeats what Iris already reads. ✅ Ask the owner what the page does not say.
- ❌ Giving a Verdict the person did not state, or approving "to move things along". ✅ Keep the Verdict they gave, on the Revision they saw.
- ❌ Calling `give_ad_verdict` after the person swiped in the deck. The deck already kept it. ✅ Read `list_ad_concepts` to see where each ad stands.
- ❌ Making a new Design Kit the default to "apply" it. ✅ Name it in the request with `design_kit_id`.
- ❌ Telling the person an approved ad is live. ✅ "Approved and ready. Nothing is running until we launch it."
- ❌ Passing an ad account id as `business_id`. ✅ The UUID beside the account in `list_ad_accounts`.
