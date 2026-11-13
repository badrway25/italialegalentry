# W1-A shipped — 9 October 2026

- Merge: design-v5 `8c3caad` (no-ff), steward files `8d45acd`, tag `v54/w1-a`; v5-live at the tag; 8780 restarted and verified (V5 faces preloaded and served: Host Grotesk 19 208 B, ILE Wordmark 1 748 B; no reference to the removed V4 fonts sheet; 0 idle connections).
- Review once: REVIEW.md SHIP_AFTER_FIXES (1 major — the preview frames linking css/fonts.css — closed by W1-P's dynamic stylesheet loading, verified on the merged branch: every preview page's CSS links resolve); A11Y_PERF.md SHIP AFTER FIXES, 0 blocking, 0 major, 3 minor; LCP −558…−886 ms on every cell; CLS 0 by probe.
- Tests before the merge (branch with design-v5 merged in): 1 171 passed, 1 deliberate xfail, 0 failed (tokens, design docs, preview, bundles, static assets, layout, RTL static, shim, security).
- Not done: the three minor a11y/perf items (skip-link ring, forum eyebrow contrast, Arabic mono budget on two page types) go to their owning families; specimen boards and deletion-map paperwork skipped by decision (V5.5).
