# Studio tools

One line per tool. Parameter details are in each tool's own schema. Every tool takes `business_id`.

## Products

| Tool | What it does | Cost |
|---|---|---|
| `adadvisor:list_products` | The business's products, each with a short readiness summary | Free |
| `adadvisor:get_product` | One product in full: fields, Product Note, pictures with their addresses, readiness | Free |
| `adadvisor:add_product_from_link` | Adds a product from its page. Answers a `task_id` to poll | Free |
| `adadvisor:create_product` | Adds a product by hand, for one with no page | Free |
| `adadvisor:update_product` | Changes fields, writes the Product Note, archives or restores | Free |
| `adadvisor:update_product_pictures` | Adds, describes, removes and reorders pictures in one call | Free |

## Design Kits

| Tool | What it does | Cost |
|---|---|---|
| `adadvisor:list_design_kits` | Every kit in full, the default first | Free |
| `adadvisor:create_design_kit` | A new kit. Never the default | Free |
| `adadvisor:update_design_kit` | Renames, replaces content, changes assets, or makes it the default | Free |
| `adadvisor:delete_design_kit` | Deletes a kit. Cannot be undone | Free |

`update_design_kit` replaces a kit's whole content. Read the kit first and send back every part you want kept.

## Ad Requests

| Tool | What it does | Cost |
|---|---|---|
| `adadvisor:get_credit_balance` | The balance, the price of a static ad, and whether the business is an AI Business | Free |
| `adadvisor:request_ads` | Asks Iris for 1 to 4 static ads. Answers a `task_id` | Credits: held for every ad asked for, charged for each ad drawn |
| `adadvisor:get_task_status` | How a request or a product import is going | Free, and outside the daily call allowance |

## Ad Concepts

| Tool | What it does | Cost |
|---|---|---|
| `adadvisor:list_ad_concepts` | The business's ads by where each stands, with counts | Free |
| `adadvisor:get_ad_concept` | One ad in full: every Revision, Verdict and Meta ad made from it | Free |
| `adadvisor:show_ad_concepts` | Opens the review deck for the person. The deck keeps their Verdicts | Free |
| `adadvisor:give_ad_verdict` | Keeps a Verdict the person stated in words | Free. Rejecting a running ad pauses it on Meta, after `confirm_pause` |

## Where an ad stands

| Group | Meaning |
|---|---|
| `to_review` | No Verdict yet on its latest Revision |
| `ready` | Approved and not running |
| `running` | Live on Meta now |
| `changes_requested` | A change was asked for, with a note |
| `rejected` | Not this idea |

## Limits

- 4 ads per request.
- 2 requests in progress per business.
- A request draws the product. It does not make people.
- Picture addresses (`display_url`) expire after 15 minutes. Read the ad again for a fresh one.
