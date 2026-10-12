# W1-P shipped — 8 October 2026

- Merge: design-v5 `e124b56` (no-ff), steward files `5fda43e`, tag `v54/w1-p`; v5-live checked out at the tag; 8780 restarted from it.
- What the owner sees on http://127.0.0.1:8780/__design-v5/ : the real home in one frame under a 40 px strip (language, desktop/phone, personas, index, news); /__design-v5/index/ every public page in fr/ar with desktop and phone frames and the V4 twin; /__design-v5/research/ the former hub as the archive; the persona switch for the four QA personas (read-only sessions, no password).
- Tests before the merge (branch with design-v5 merged in): 481 passed, 0 failed, 0 skipped (test_design_preview under the dev chain, tests/security, test_design_docs, the dev-settings test).
- Not done: the pages themselves are still V4 (the foundation v54/w1-a is next); live_status.json marks no product surface as v5 yet; WebKit/Firefox not run.
