# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts posts from r/LocalLLaMA, a public subreddit about running AI models on your own hardware. Each post gets one of three labels: `announcement` (it presents a new model, tool, paper or project), `results` (the poster backs their own conclusion with specific, checkable measurements or figures), or `help` (it asks readers to solve a problem or recommend something). I want it as a filter: show me the posts with real measurements and hide the flood of release announcements, which made up about half of what I read. It's `distilbert-base-uncased` fine-tuned on 150 posts I labelled.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `announcement`

**Definition:** Presents a new model, tool, paper or project, the poster's own or someone else's, without the poster making their own argument backed by checkable facts.

**Example 1:**
> **Phonon is now open-source, 31M and 40M TTS models designed to run on the edge**
> At Gradium we just made our first open-source model release with Phonon, a collection of small Text-to-Speech models designed to run on device. The inference stack is fully open-source and targets 10+ different backends (CPUs, GPUs, NPUs), most of them in Rust. We hope that the community will build lots of different things on tops of our models and code, any feedback is very welcome and we're looking forward to many more open-source releases!

**Example 2:**
> **ornith-ai/Ornith-1.5-122B (Qwen finetune)**
> from Ornith: Chirp Chirp! 🐦 We are introducing Ornith-1.5, a major step toward building foundation models through end-to-end self-improvement. [...] Rather than relying on a fixed set of human-curated tasks and manually designed harnesses, Ornith-1.5 continuously generates new training tasks, discovers effective strategies for solving them, and improves the policy through reinforcement learning.

### `results`

**Definition:** The poster uses specific, checkable facts (their own measurements or figures they collected) to support their own conclusion or comparison.

**Example 1:**
> **3M token pool for Nemotron 3.5 Super on a single RTX PRO 6000**
> While benchmark figures are lagging behind Qwen3.8-Flash-Next, Nemotron 3.5 Super does not use any system memory (no 50GB lookup table), is slightly faster (150 to 250 tps tg vs 130 to 230 tps for 3.8 FN) and, most importantly, the tokens, as Qwen3.8 FN only allows for a ~450k token pool.

**Example 2:**
> **Qwen3.8-Flash-Next vs Opus 5.5: Six-way benchmark on a real Rust feature with Claude Code and Pi**
> Opus wrote better code, 82% on average against 68% for Claude Code + Flash-Next and 66% for Pi + Flash-Next. [...] Flash-Next took 1.1x to 2.1x as long as Opus at the same effort. [...] Opus is still ahead, but Flash-Next was right behind, on my laptop, for the cost of electricity.

### `help`

**Definition:** Asks readers to solve the poster's problem or recommend something, even when the post includes specs, numbers or frustration.

**Example 1:**
> **Pi.dev harness bugs**
> Anyone know a fix for some issues? [...] when running context % isn't always accurate it'll change from a big % to somewhat lower later (example it'll go from 78% to randomly 56%). [...] Any help with this would be amazing!

**Example 2:**
> **Meaningful to add another 16 gig GPU or go hybrid (single GPU) + cloud**
> I have a 5070 ti and a 5060 ti 16 gigs, and 48 gigs of DDR5 ram. [...] I'm just curious if it would be worth it to keep the 5060 ti instead of selling it, and use this dual GPU setup and rely on the cloud rarely, if at all. [...] would greatly appreciate some general advice as to what would be a reasonable way forward.

### The hardest boundary

**Which two labels:** `announcement` and `results`

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If the post announces something new but the poster uses specific, checkable facts to support a conclusion of their own, label it `results`, even when it's their own project. Kokon 0.10 is `results`: "about 2 s per image on an RTX 5070 Ti" and "I tested the popular 2.1 LoRAs... they don't beat what Turbo does" support the poster's own conclusions. If the numbers are only specs (parameter counts, context size), are copied without an argument from the poster (paper abstracts), or don't support the headline claim, label it `announcement`. Muse Spark Open is `announcement`: its kernel speedups don't back "the most capable US open-weight model."

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/LocalLLaMA, public, in October 2026. Reddit blocks scripts from its JSON feed, so I saved four listing pages from my browser (New, two pages; Top of the week; Top of the month) and `collect.py` turned them into rows of title + blank line + body. It skipped posts with no body text (link-only and image-only), cross-posts from other subreddits, stickied mod posts, removed posts and duplicates. That gave 295 posts. Flair and Reddit's page text aren't in the listing's title or body, so none of it is in the CSV.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

1. **Cold, 20 posts.** I labelled 20 random posts first with `label.py cold`, using only my definitions. They're marked `cold` in the note column.
2. **A skip rule.** Claude then labelled the same 20 blind and told me only how often we matched: 18 of 24 decisions (75%), or 15 of 17 where neither of us skipped. Half the disagreements were `announcement` vs skip, because I'd never written down what makes a post a skip. So before going further I wrote one: *skip a post if it presents nothing new (no model, tool, paper or project), makes no point backed by checkable facts, and asks readers for nothing*. That covers jokes, rants, opinions, reactions, guides, setup show-offs with no conclusion, and general news (GPU prices, company news, policy).
3. **AI pre-labelling, then my review.** Claude pre-labelled the other 271 posts from my three definitions, my decision rule and the skip rule. I reviewed them one at a time in `label.py review`, deciding each label before looking at the suggestion. Reviewed rows are marked `pre-labelled; checked`. I reviewed 138, 130 became training rows and 8 were confirmed skips.
4. **I stopped at 150, under the brief's stop rule.** I ran short on time, so I reviewed posts in random order until I had 150 usable rows instead of reviewing all 271. The 133 pre-labelled posts I never read are in `data/unreviewed.csv` and are not trained on. The 12 reviewed skips (4 cold, 8 from review) are in `data/skipped.csv`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `announcement` | 77 | 51.3% |
| `results` | 46 | 30.7% |
| `help` | 27 | 18.0% |
| **Total** | 150 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "72 hours, four big open weights drops. The only one that fits in 24GB came from NVIDIA, of all companies." A recap of four model releases, "all numbers from the official repos and model cards", ending with the poster's takeaways: "'Runs locally' now officially means 'runs on a computer that costs more than a car.'"
>
> *Could have been:* `announcement` or `results`
>
> *I chose, because:* `results`. The poster measured nothing, but they collected checkable facts (prices, sizes, licences, benchmark scores) and built their own argument on them. This post changed my rule: `results` used to mean the poster's own measurements, and now it means checkable facts supporting the poster's own conclusion, whether measured or collected.

**2.**
> *The post:* "Qwen 3.8-27B-pi on 3080+3060." The poster lists their setup and real measurements ("30-40 tok/s generation, avg mtp acceptance ~0.75", "started at 10 tokens per second"), then asks "Where should I go for further improvements (if any are possible)?"
>
> *Could have been:* `help` or `results`
>
> *I chose, because:* `help`. The numbers are real, but they describe a starting point for the question rather than supporting a conclusion. What the numbers are doing decides it, not whether they're there.

**3.**
> *The post:* "[Paper] The COUNT: Counting N-grams Unlocks Scaling on Host Memory and Training-Free Adaptation." The paper's abstract, including a real result: COUNT improves validation loss "as much as an LM with 57% more compute."
>
> *Could have been:* `announcement` or `results`
>
> *I chose, because:* `announcement`. The result is the authors', copied from the abstract, and the poster adds no argument of their own. Passing along someone else's results is sharing, not `results`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed --> 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42.

**Device:** `mps` on an **Intel** MacBook Pro (Core i9-8950HK) with an AMD GPU, torch 2.2.2. The notebook prints "Apple Silicon GPU (MPS)", but that's a generic label; this machine isn't Apple Silicon.

**Anything I changed from the defaults, and why:** No hyperparameters changed. One environment fix: torch 2.2.2 is the last PyTorch build for Intel Macs and is compiled against NumPy 1.x, but `requirements.txt` installed NumPy 2 and pyarrow 26 (which needs NumPy 2). I pinned `numpy<2` and `pyarrow<20` so torch and `datasets` both import.

One thing to watch: posts are long (median about 1,000 characters), and 128 tokens is roughly the first 500. In longer posts, the measurements that make something `results` can sit past the cutoff, so the model may never see them.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

| Split | Total | announcement | results | help |
|---|---|---|---|---|
| Train | 104 | 53 | 32 | 19 |
| Validation | 23 | 12 | 7 | 4 |
| Test | 23 | 12 | 7 | 4 |

Two labels have fewer than about 8 in the test split: `results` has 7 and `help` has only 4. One post moves `help`'s recall by 0.25, so expect those numbers to jump between seeds next unit.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I gave Claude my three definitions and decision rule and asked for eight made-up posts that sit on my boundaries, then labelled them myself without seeing its answers.
- *What came back:* Seven were clean. Post #5 benchmarked five embedding models on the poster's own notes (recall@5: 0.81, 0.78, 0.74) but never stated a conclusion, and my `results` definition required "their own conclusion."
- *What I changed:* I decided a ranking is a conclusion and added "or comparison" to the `results` definition. Post #8 ("3x faster indexing" with no setup) also taught me that a number only counts as checkable if the post says what was measured, on what, and how.

**Moment 2**

- *What I asked for:* After labelling my 20 cold posts, I asked Claude to label the same 20 blind and tell me only the agreement percentage and the kinds of disagreements, not which posts.
- *What came back:* 75% (18 of 24 decisions), with half the disagreements being `announcement` vs skip.
- *What I changed:* I hadn't defined what a skip is, so I wrote the skip rule in The Dataset before any pre-labelling. My cold labels stayed as they were.

**Pre-labelling disclosure:** Claude pre-labelled 271 posts from my definitions, decision rule and skip rule. I read and reviewed 138 of them one at a time. The 133 I never reviewed are excluded from `labels.csv` (they're in `data/unreviewed.csv`). The 20 `cold` rows had no AI involvement.

**Other AI help, for completeness:** Claude helped me write `collect.py` and `label.py`, diagnosed the NumPy/pyarrow conflict on my Intel Mac, and drafted some of this README's text from my decisions, which I wrote. The labels, the decision rule, the skip rule and all five criteria targets are mine.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.348 | 0.522 | +0.174 |
| Macro F1 | 0.278 | 0.229 | -0.049 |
| F1 — `announcement` | 0.000 | 0.686 | +0.686 |
| F1 — `help` | 0.333 | 0.000 | -0.333 |
| F1 — `results` | 0.500 | 0.000 | -0.500 |

**Bare-names baseline** (`python baseline.py --definitions no_such_file.txt --out baseline_results_bare.json`, same 23 posts): accuracy 0.565, macro F1 0.561, F1 `announcement` 0.471, `help` 0.545, `results` 0.667. The table above uses my definitions, as the brief asks.

**What I predicted before I looked:**  I'd already seen my seed-42 results in unit 5, so this isn't a blind prediction. I expect the trained model to beat the baseline on overall accuracy and announcement F1, because it guesses `announcement` for nearly everything, and to lose on Macro F1, help and results, because it never predicts the smaller labels.
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:** The trained model beats the baseline only on overall accuracy and `announcement` F1, and only because it predicts `announcement` for almost every post. It scores 0 on `results` and `help`, so fine-tuning on 104 posts for 21 steps added nothing beyond guessing the majority label. My definitions also made the baseline worse: with bare label names it scored 0.565 accuracy and 0.561 macro F1 instead of 0.348 and 0.278, which beats my trained model on everything except `announcement` F1. The likely reason is that my `announcement` definition is written as a negation ("without the poster making their own argument backed by checkable facts") using the same words as `results`, so BART couldn't tell the two apart and `announcement` F1 fell to 0. My decision rule makes the line clear to a person, but the definition alone doesn't.
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
