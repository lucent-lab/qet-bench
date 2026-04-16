# Noise-Survival Diagnostics

The noise-survival study is a fixed-protocol simulation diagnostic for the
minimal two-qubit benchmark. It does not claim a universal noise threshold,
phase boundary, hardware noise model, or closed environment ledger.

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
- `min_survival_ratio`: minimum sampled `R(lambda)`.

These are robustness diagnostics for named one-parameter channel families under
the fixed protocol. They are not theorem-level thresholds.

