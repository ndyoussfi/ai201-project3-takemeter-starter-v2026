# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->
Overall accuracy on the held-out test set is at least 0.8 on every one of the three seeds.


**Why this target:** The posts carry important measurable facts and more than 2 out of 10 mistakes makes it untrustworthy. Since about 61% of the 30 posts are announcements, always guessing announcement scores about 0.61, so 0.8 means the model also has to get about 6 of the 12 results and help posts in the test set right.



---

## 2.

<!-- Your criterion. -->
Recall for `results` on the held-out test set is at least 0.75 on every one of the three seeds.


**Why this target:** I'm using TakeMeter to filter results posts, so a `results` post the model misses is one I don't see.
Only about 7–8 `results` posts hit the test split, and each one moves recall by about 0.13, so 0.75 allows about 1–2 misses whether a seed gets 7 or 8. I expect those misses to be posts like the Kokon 0.10 post, because it looks like an `announcement` post for a new version of Kokon and lists new features, but includes real measurements, which make it a `results` post.


---

## 3.

<!-- Your criterion. -->
On every one of the three seeds, the model's accuracy on its most confident third of test posts is at least 0.30 higher than on its least confident third.


**Why this target:** If the model is sure about a post's label, I want to be able to trust that label without checking it myself. Each third is about 10 posts, so 0.30 means the confident third gets 3 more posts right than the unsure third. I didn't pick 0.40 because if the model makes only 3 mistakes, a 0.40 gap is impossible, so a 0.9 model would fail.

---

## 4.

<!-- Your criterion. -->
In labels.csv, no label is above 65% of the rows, and no label is below 15%.


**Why this target:** In the 30 posts I read, `announcement` was about 61% and `help` about 14%. The brief's cap is 70%, so a 65% cap makes me go looking for `results` and `help` posts instead of just collecting what shows up. The 15% floor matters most for `help`, because even at 15% it gets only about 4–5 posts in the 30-post test split.


---

## 5.

<!-- Your criterion. -->
Precision for `results` on the held-out test set is at least 0.83 on every one of the three seeds.


**Why this target:** A post the model wrongly calls `results` ends up in my filtered feed, where I'd trust it as real measurements when it has nothing behind it. The model calls about 6–8 posts `results` per seed, so 0.83 allows 1 wrong. That's stricter than my recall target (0.75) because a fake results post misleads me, while a missed one only means I don't see it. It also matches criterion 1, where more than 2 out of 10 mistakes is untrustworthy.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
