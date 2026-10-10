# Scoring and routing

Explainable signal weights are summed and clipped to [0,1]. This is a rule-based severity index, **not** a calibrated posterior fraud probability. Thresholds: 0.25 review, 0.4 high priority, 0.65 suspicious label, 0.75 critical. Confidence is illustrative and should not be shown as empirical accuracy. Routable categories are separate from company relevance and reply urgency. Security-alert emails with low risk still require contextual scrutiny.
