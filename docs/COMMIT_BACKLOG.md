# Daily Commit Backlog

A queue of real work for this repo, highest priority first. A scheduled Claude Code agent takes the
**top unchecked item**, does it properly, verifies it, and commits.

## The rules the daily agent follows

1. **One item per run.** Finish it or leave it uncommitted - never commit a half-done item.
2. **Verify before committing.** `pip install -r requirements.txt pytest && python -m pytest -q`
   must pass once tests exist. Until then, run the code the item touches (e.g. start `app.py` and
   exercise the route with Flask's test client) and put the real result in the commit body.
3. **No filler commits.** No whitespace churn, comment padding, reformatting, or version bumps
   without a reason. If no item can be done honestly, make no commit and say so.
4. **Never retrain silently.** `fraud_model.pkl` and `scaler.pkl` are tracked binaries. Only
   regenerate them in an item that says so, and state the sklearn version used in the commit body.
   Never report a metric you did not compute.
5. **Stage named paths only** (never `git add -A` / `git add .`). No secrets, no new large data files.
6. **Conventional commit messages**; tick the item below and append to the Log.

---

## Audit findings (verified 2026-10-23 by reading `app.py`, `fraud_detection.py`, README, data)

- No tests, no CI, no `docs/`. Repo was a single "Initial commit".
- README claims "Precision, Recall, F1-score evaluation" and "Combined fraud decision logic", but
  `fraud_detection.py` computes no metrics (the test split is never scored) and `IsolationForest`
  is fitted and then discarded - it is neither saved nor used by `app.py`.
- `app.py` decides fraud via a RandomForest vote plus two hardcoded rules (`amount > 180`,
  `time > 45`). `Time` in `transactions.csv` is a row index 0-59, so the `time > 45` rule is an
  artefact of this small dataset, not a real signal.
- `app.py` does `float(request.form[...])` with no handling: non-numeric input raises ValueError
  (HTTP 500); `nan`/`inf`/negative values are accepted.
- Dataset: 60 rows, 8 frauds (13%); the split is not stratified, so the test set can hold 1-2 frauds.
- The alerts table randomises payment mode and user per request, and uses a hardcoded txn number
  base (1041); only `Amount`/`Class` come from the data. Fine for a demo but undocumented.
- `app.run(debug=True)` is hardcoded. `requirements.txt` is unpinned while the `.pkl` files are
  sklearn-version-coupled. README "Run" section omits the web app and the model-training step.

## Queue

- [ ] **A1 - Validate the predictor form input** (`app.py`). Reject non-numeric, non-finite and
      negative `time`/`amount` with a friendly message instead of a 500. Extract the decision logic
      into a function so it is testable.
- [ ] **A2 - Add `tests/test_app.py`**: GET `/` renders the totals from the CSV (60/8/52), POST with
      a high amount flags fraud, POST with a low one is legitimate, bad input returns 200 + message.
- [ ] **A3 - Evaluate the model for real** in `fraud_detection.py`: stratified split, print
      precision/recall/F1 and confusion matrix on the held-out set (do not retrain pickles in this
      item). Then make the README claim true, with the numbers you actually got.
- [ ] **A4 - Decide IsolationForest's role**: either use its anomaly score in the combined decision
      or remove it and correct the README. Record the choice in `docs/DECISIONS.md`.
- [ ] **A5 - Fix the README**: how to train, how to run the web app (`python app.py`, port 5050),
      what is real vs. simulated in the dashboard, dataset provenance (synthetic, 60 rows).
- [ ] **A6 - Pin `requirements.txt`** to versions the pickles load under, add a load-time check
      that gives a clear error if the pickle cannot be loaded.
- [ ] **A7 - Make `debug` configurable** via env var (default off) and add `.gitignore` entries
      (`.venv/`, `.pytest_cache/`).
- [ ] **A8 - Add a GitHub Actions workflow** running pytest once A2 exists.

## Log

2026-10-23 - audit - docs: add COMMIT_BACKLOG.md with verified audit and work queue
