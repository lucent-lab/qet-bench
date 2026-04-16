# Noise-Survival Diagnostics

The noise-survival study is a fixed-protocol simulation diagnostic for the
minimal two-qubit benchmark. It scans a small predeclared set of `(h, k)` anchor
Hamiltonians and named one-parameter channel families. It does not claim a
universal noise threshold, phase boundary, hardware noise model, or closed
environment ledger.

The release anchor set is `(1, 0.25)`, `(1, 0.5)`, `(1, 1)`, and `(0.5, 1)`.

For a scan coordinate `lambda`, define

```math
R(\lambda)=\frac{E_B(\lambda)}{E_B(0)}.
```

A sampled point is marked as positive survival only when

```math
E_B(\lambda)>0
```

and the reported model ledger still satisfies

```math
E_A(\lambda)-E_B(\lambda)\ge 0
```

within numerical tolerance.

The summary artifacts report:

- `lambda_ratio_cutoff`: first linearly interpolated scan coordinate where
  `R(lambda) <= 0.5`,
- `lambda_zero_crossing`: first linearly interpolated scan coordinate where
  `E_B(lambda) <= 0`,
- `first_sampled_nonpositive_x`: first sampled point with nonpositive `E_B`,
- `min_survival_ratio`: minimum sampled `R(lambda)`,
- `interval_mean_survival_ratio`: the scan-interval average of `R(lambda)` over
  the finite sampled coordinate range.

These are robustness diagnostics for named one-parameter channel families under
the fixed protocol and the listed anchors. They are not theorem-level
thresholds and should not be interpreted as universal robustness scores.
