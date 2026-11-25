# Writing a brief

A brief is what the person wants of the ads, in the fields `request_ads` takes. Iris reads the product, its pictures, its page and its Product Note on her own. The brief adds only what those do not say: what this batch of ads is for.

## Where each thing goes

| The person says | Field |
|---|---|
| Who the ad is for | `persona` |
| The reason to buy that the ad leads with | `angle` |
| The kind of ad: a comparison, a list of benefits, a testimonial look | `format` |
| A sale, a bundle, free shipping, a deadline | `offer` |
| Words that must appear in the picture exactly as written | `exact_lines` |
| Where it runs: feed, stories, reels | `placement` (`square`, `portrait`, `vertical`, `landscape`) |
| Anything else: the occasion, the mood, what to avoid this time | `brief` |

Leave a field out when the person did not speak to it. An empty field lets Iris choose; a guessed one constrains her to your guess.

## What belongs on the product instead

If it is true of the product every time, it belongs in the **Product Note**, not the brief. "Mostly bought as a gift" is a note. "This batch is for Mother's Day" is a brief.

If it is true of the brand every time, it belongs in the **Design Kit**: colours, typography, mood, what to avoid.

## Asking for variety

One request draws its ads together, so they differ from one another by design. To compare two directions cleanly, send two requests with different `angle` or `persona`, each with its own `idempotency_key`, and keep in mind the limit of two requests in progress.

## Exact lines

Use `exact_lines` only for text the person dictated: a headline they wrote, a legal line, a price. Up to four short lines. Everything else Iris writes, and writes better when free to.

## After a rejection or a request for changes

Read the Verdict's `reasons` and `note` with `adadvisor:get_ad_concept` and fold them into the next brief in plain words: what to keep, what to change. A new request makes new ads; it does not edit the old one.
