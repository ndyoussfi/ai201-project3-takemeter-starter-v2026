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

**Moment 3 (unit 6)**

- *What I asked for:* After the baseline did worse with my definitions (0.348 accuracy) than with bare label names (0.565), I asked Claude why.
- *What came back:* My `announcement` definition is written as a negation ("without the poster making their own argument backed by checkable facts") and reuses the same words as `results`, so a model judging which definition a post matches couldn't tell the two apart; `announcement` F1 fell from 0.471 to 0.000.
- *What I changed:* Nothing in the taxonomy, since unit 6 doesn't allow it, but I wrote it up in Baseline vs. Trained as a finding: my decision rule makes the line clear to a person, but the definition alone doesn't.

**Unit 6 AI help, for completeness:** Claude wrote `staff_label.py`. After I'd labelled the 30 staff posts and before I had the staff labels, it told me how often my labels matched its own reading (16 of 30) and what kinds of disagreements we had; my labels in `my_staff_labels.csv` are my own first pass, unchanged. For each disagreement with staff it laid out the case for both labels from the staff rules; the pile for each was my call. It also recommended the epochs change from my diagnosis and drafted most of the unit 6 README text from my results and decisions.

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
| 1. Overall accuracy | ≥ 0.80 | 0.522 | 0.522 | 0.522 | MISSED |
| 2. Recall for `results` | ≥ 0.75 | 0.000 | 0.000 | 0.000 | MISSED |
| 3. Confidence gap (most-confident third minus least-confident third) | ≥ 0.30 | 0.286 | 0.286 | 0.429 | MISSED |
| 4. Balance in `labels.csv` (no label > 65% or < 15%) | max ≤ 65%, min ≥ 15% | 51.3% / 18.0% | 51.3% / 18.0% | 51.3% / 18.0% | MET |
| 5. Precision for `results` | ≥ 0.83 | 0.000 | 0.000 | 0.000 | MISSED |

Device: `mps` (Intel Mac, AMD GPU), torch 2.2.2. The test split is 23 posts on every seed (12 `announcement`, 7 `results`, 4 `help`). Criterion 4 is measured on `labels.csv` itself, so it's the same on every seed. Criterion 5's 0.000 is scikit-learn's value when the model predicts `results` zero times; precision is really undefined there.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | announcement | results | help |
|---|---|---|---|
| **announcement** | 12 | 0 | 0 |
| **results** | 7 | 0 | 0 |
| **help** | 4 | 0 | 0 |

**My biggest off-diagonal number, and what it means:** 7 real `results` posts were called `announcement`, and 0 went the other way; all 4 `help` posts were called `announcement` too. That looks like the lopsided pattern the slides describe, but it isn't one fuzzy boundary: the model never predicts `results` or `help` at all, on any seed. It collapsed to the majority label, so the matrix can't tell me yet whether it also failed my hardest boundary (`announcement` vs `results`). That's a training problem first (104 posts, 21 steps, validation accuracy flat at 0.522 from epoch 1), and the agreement check is what will show whether my labels added to it.
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.80 | MISSED | 0.522 on all three seeds, which is exactly the `announcement` share of the test split (12/23) |
| 2 | Recall for `results` | ≥ 0.75 | MISSED | 0.000 on all three seeds; none of the 7 `results` test posts was labelled `results` |
| 3 | Confidence gap | ≥ 0.30 | MISSED | 0.286, 0.286, 0.429. It has to hold on every seed, and two of three fall short |
| 4 | Balance in `labels.csv` | no label > 65% or < 15% | MET | 51.3% / 30.7% / 18.0%, checked on the file itself, so the same on every seed |
| 5 | Precision for `results` | ≥ 0.83 | MISSED | the model never predicted `results` on any seed, so precision is undefined (scored 0.000). A target that can't be reached at all is a miss |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criteria 1, 2 and 5: one cause, a model that collapsed to the majority label.** On all three seeds the model predicted `announcement` for every test post (the confusion matrix is a single column), so accuracy equals the `announcement` share and `results` gets zero recall and no predictions at all. This is mainly a **model / data-size problem**, and I can tell it apart from a labelling problem with three pieces of evidence:

- **Training never moved.** Validation accuracy was 0.522 and macro F1 0.229 after epoch 1, 2 and 3 alike, and training loss only fell from 1.03 to 0.96. With 104 training posts at batch 16 for 3 epochs, the model got 21 small updates. The cheapest answer it found was "always the 51% label", and it never got past it.
- **The task is reachable without my training.** The bare-names baseline, with no training at all, scored 0.565 accuracy and 0.667 F1 on `results` on the same 23 posts. So the texts do carry the distinction; my fine-tune just didn't learn it from this much data.
- **The collapse is the same on every split.** If one boundary were fuzzy, I'd expect a mix of right and wrong answers that changed between seeds. Instead all three seeds give the identical one-column matrix, which points at training, not at particular posts.

**My labels probably made it worse, and the agreement report is the evidence.** On the staff set I labelled only 3 of 30 posts `analysis` against staff's 10, and 7 of my 8 misses there were `analysis` called `hot_take` or `reaction`: I under-call the fact-backed label when a post states a confident conclusion. My `results` vs `announcement` boundary is the same judgement (does the fact carry the poster's conclusion?), so I likely labelled some fact-backed posts `announcement`. That would add to the `announcement` majority and blur the `results` examples the model did see. I can't confirm it from the matrix, because a model that never predicts `results` can't show which `results` posts it confused, but it's the most likely labelling contribution.

Two smaller factors: `help` and `results` have only 4 and 7 test posts, so even a working model's scores would jump by 0.14–0.25 per post; and the model reads only the first 128 tokens (about 500 characters) of posts with a median of about 1,000, so in long posts the measurements that make something `results` can sit past the cutoff.

**Criterion 3: a near miss on a tiny sample.** With 23 test posts, each third holds 7 posts, so one post moves the gap by about 0.14. The gaps of 0.286, 0.286 and 0.429 are 2, 2 and 3 posts. My reason for the target assumed about 10 posts per third; the real number is 7, which makes 0.30 a 2-to-3-post target. Even so, there is a real signal here: the model's most-confident third was 5 of 7 `announcement` posts against 2–3 of 7 in its least-confident third, so its confidence leans toward real announcements even though its answers never change. The cause of the miss is the same collapse plus a test set too small for thirds to be stable.

**Criterion 4 (MET):** met because I stopped labelling at a balance I'd planned for, not because of anything the model did.

**No criteria revised.** All five could be measured; criterion 5 is undefined only because of the collapse, not because it was badly written. Lowering any target after missing it isn't a revision.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 16 / 30 = 53%

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

**1. sp_003**
> *The post:* "The club championship scoring changed in 2019 from top-6 to top-10. Since then our B team has finished above the A team twice. That's not depth improving, it's the scoring rewarding turnout."
>
> *Staff said / I said:* `analysis` / `reaction`
>
> *My call, and why:* Staff is right. The conclusion ("the scoring rewarding turnout") is drawn from the 2019 rule change and the B team finishing above the A team twice. Rule 1: the fact carries the argument. Nothing happened to the writer, so `reaction` doesn't fit either.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**2. sp_004**
> *The post:* "Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The poster split the field by first-half time and found the same slowdown after 18 in both groups; "if the hill were the problem the fast starters would fall apart harder" follows from that data. It opens by disputing a common belief, which made it feel like a hot take, but rule 1 is about whether the fact is load-bearing, and here it is the whole argument.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**3. sp_005**
> *The post:* "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* I think my reading holds. The second 2%, in the same shoes after mileage went from 35 to 50 a week, is real evidence, but it's one runner over two years, offered after the conclusion ("Carbon plates aren't the whole story") is already stated. Rule 1 says that if the number is decoration on a conclusion the writer had already reached, it's `hot_take` with a statistic in it. A single personal anecdote can't carry a claim about carbon plates in general, so the fact is closer to decoration than to the argument.
>
> *Which pile:* (c) the rule is ambiguous here and my reading is defensible

**4. sp_006**
> *The post:* "Checked the entry lists. 41% of this year's field have never run the distance before, against 26% five years ago. That's why the finish-line photos look different, not because standards dropped."
>
> *Staff said / I said:* `analysis` / `reaction`
>
> *My call, and why:* Staff is right. 41% first-timers against 26% five years ago is the reason given for "that's why the finish-line photos look different". Rule 1: the number is the argument. There's no event or feeling of the writer's, so `reaction` was a misread.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**5. sp_007**
> *The post:* "Ran the same loop in 4C and in 24C within a fortnight, same effort by heart rate. 90 seconds slower in the heat over six miles. People keep saying heat costs you 'a bit' and it's more than that."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The same loop at 4C and 24C, same heart-rate effort, 90 seconds slower: that measurement is what supports "it's more than a bit". The punchy last line made it read as a hot take, but rule 1 asks whether the fact does the work, and it does.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**6. sp_008**
> *The post:* "Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. "Between 18 and 23 percent every year since 2012" is exactly what makes "it's the base rate" true. Rule 1: load-bearing fact.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**7. sp_009**
> *The post:* "The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The remeasurement (60 metres long, about 12 seconds at club pace) is the whole argument that before-and-after PBs aren't comparable. Rule 1.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**8. sp_010**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. Three runners within 10 seconds over 5 miles in different shoes supports a carefully hedged conclusion ("smaller than the noise between three people"). Three people is thin, but the post argues from it rather than decorating a view, which is what rule 1 asks.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**9. sp_013**
> *The post:* "The club needs to stop pretending the Tuesday session is for everyone. It isn't and it never has been."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* Staff is right. "The club needs to stop pretending the Tuesday session is for everyone" is a general claim about the club, with no support offered. Rule 2: `reaction` reports what just happened to the writer; this asserts something about the world. I read the frustration as a reaction, but the taxonomy says a post can be heated and still be `hot_take`.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**10. sp_014**
> *The post:* "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* Staff is right, and this one is almost word for word rule 1's own `hot_take` example: the 3% is a flourish on "the shoes are the whole story". Nothing happened to the writer, so it can't be `reaction`.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**11. sp_019**
> *The post:* "Nobody actually enjoys the long run. They enjoy having done it, which is a completely different thing, and the sport would be more honest if it said so."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* Staff is right. "Nobody actually enjoys the long run" is a sweeping claim about all runners, not about the writer's own experience. Rule 2.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**12. sp_025**
> *The post:* "Blew up at 20 with the pace band still in my hand like it was going to help. Rough one."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff is right. Blowing up at 20 with the pace band in hand is what just happened to the writer, and "Rough one" is how it felt. Rule 2: it makes no general claim.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**13. sp_027**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff is right. The wind and "coming back felt like cheating" describe the writer's own run. "About 20 degrees" is a number, but it describes the experience rather than supporting a general claim, so it's not a `hot_take` and not `analysis`. Rule 2.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**14. sp_029**
> *The post:* "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is closest, but the rules don't quite say. "Every PB this year" is a checkable fact, yet nothing is argued from it, so it isn't `analysis`. `reaction` is defined as "feeling rather than argument", and this is a factual realisation about the writer with very little feeling. The rule that would have settled it: *a personal observation with no argument is `reaction`, even when it contains a checkable fact.*
>
> *Which pile:* (b) the rule genuinely doesn't say

**What the pattern in my disagreements tells me:** 12 of my 14 disagreements are pile (a): the rule covered the post and I didn't apply it. They fall into two habits. The bigger one: 8 posts staff called `analysis`, and I called 7 of them `hot_take` or `reaction`. I labelled only 3 posts `analysis` out of 30, against staff's 10. When a post states a confident conclusion, I read it as a hot take even when the conclusion comes after the data and depends on it. The second habit: I read strong feeling as `reaction` (sp_013, 014, 019) when rule 2 says it's who the post is about that decides. Only sp_005 is a defensible disagreement (c), and sp_029 points at a real gap in the rules (b).

This is direct evidence about my own 150 labels. My `announcement` vs `results` boundary is the same kind of judgement as staff's `hot_take` vs `analysis`: does the fact carry the poster's conclusion? If I under-called `analysis` here by about two thirds, I probably under-called `results` in my own data too, labelling some fact-backed posts as `announcement`. That fits my model collapsing toward `announcement`.

---

## The Improvement

**What I changed:** One training setting: `EPOCHS` from 3 to 10, which takes the model from 21 to 70 weight updates. Everything else stayed the same: the same 150 labels, the same seeds (42, 7, 2024) and so the same splits, learning rate 2e-5, batch size 16, 128 tokens, device `mps`. `RUN_LABEL` was set to `"after"`, so the before file wasn't overwritten.

**Which diagnosis pointed at it:** Criteria 1, 2 and 5 all missed because the model collapsed to `announcement`. Validation accuracy didn't move between epochs 1 and 3, training loss barely fell, and the bare-names baseline showed the task is reachable without training. That points at too little training, not at a single boundary, and it's the one case where the brief says to change a training setting. The agreement report suggests my labels add to the problem too, but relabelling first would have meant changing two things at once.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.80 | 0.696 | 0.696 | 0.739 | MISSED |
| 2. Recall for `results` | ≥ 0.75 | 0.571 | 0.429 | 0.714 | MISSED |
| 3. Confidence gap (most-confident third minus least-confident third) | ≥ 0.30 | 0.000 | 0.571 | 0.429 | MISSED |
| 4. Balance in `labels.csv` (no label > 65% or < 15%) | max ≤ 65%, min ≥ 15% | 51.3% / 18.0% | 51.3% / 18.0% | 51.3% / 18.0% | MET |
| 5. Precision for `results` | ≥ 0.83 | 0.800 | 0.600 | 0.625 | MISSED |

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.696 | 0.696 | 0.739 | 0.043 |
| Macro F1 | 0.608 | 0.576 | 0.638 | 0.062 |
| F1 — `announcement` | 0.759 | 0.828 | 0.846 | 0.087 |
| F1 — `results` | 0.667 | 0.500 | 0.667 | 0.167 |
| F1 — `help` | 0.400 | 0.400 | 0.400 | 0.000 |

Confusion matrix after, seed 42 (seeds 7 and 2024 in `results_three_seeds_after.json`):

| true \ predicted | announcement | results | help |
|---|---|---|---|
| **announcement** | 11 | 1 | 0 |
| **results** | 3 | 4 | 0 |
| **help** | 3 | 0 | 1 |

Summed over all three seeds: 9 real `results` posts were called `announcement` and only 2 went the other way; `help` was right 3 times out of 12, with its misses split 5 to `announcement` and 4 to `results`.

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

Yes, a lot, though it still misses four of five criteria. On every seed accuracy rose by 0.17 to 0.22 (0.522 → 0.696–0.739) and macro F1 more than doubled (0.229 → 0.576–0.638). More important, the model now predicts all three labels: `results` went from zero recall to 0.43–0.71, and `help` from 0.00 F1 to 0.40. It now beats the bare-names baseline on accuracy (0.696–0.739 vs 0.565) and macro F1 (0.576–0.638 vs 0.561). It matches it on `results` F1 (up to 0.667) and still trails it on `help` (0.400 vs 0.545). Accuracy only moved 0.043 across seeds, so those numbers are fairly stable; the confidence gap is not (0.000 to 0.571), because each third is only 7 posts.

Now that the model makes real choices, the matrix shows a direction the collapse hid: `results` is confused with `announcement` far more in one direction (9 vs 2). That's my hardest boundary, and it leans the same way as my staff-set habit of under-calling the fact-backed label.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

- **1. Accuracy (0.696–0.739 vs 0.80).** Most remaining errors are `results` → `announcement` and `help` → anything. I'd re-check every `announcement` row in `labels.csv` that contains measurements, applying my decision rule strictly, since the staff set showed I under-call the fact-backed label. I stopped because the brief allows one change this unit, and I was out of time.
- **2. `results` recall (0.43–0.71 vs 0.75).** Same boundary. Besides relabelling, I'd raise `MAX_LENGTH` from 128 to 256 tokens, because many of my posts are about 1,000 characters and the measurements often come after the first 500. That's a second change, so I didn't make it.
- **3. Confidence gap (0.000, 0.571, 0.429 vs 0.30).** With 23 test posts each third is 7, so one post moves the gap by about 0.14. The fix is more data: reviewing the 133 pre-labelled posts in `data/unreviewed.csv` would take me past 250 rows and roughly 40 test posts. I stopped at 150 for time in unit 5.
- **5. `results` precision (0.60–0.80 vs 0.83).** The false `results` calls are mostly `help` posts (4 across seeds), which contain specs and measured numbers too. `help` is my thinnest label (27 rows), so I'd add 30 more `help` posts, including ones with numbers. I stopped for time.



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `results` to capture posts where checkable facts carry the poster's own conclusion, but the model seems to have learned something closer to "posts with measurements in them", which is why `help` posts full of specs and tok/s numbers get called `results` (4 across seeds). It also misses `results` posts that open like a release (9 called `announcement`), which suggests it reads the opening tone of a post more than what its facts are doing, and with only the first 128 tokens it often can't see those facts at all.



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
