# Energy Accounting

The Hamiltonian constants set the two-qubit ground-state energy to zero. Alice's
measurement changes the state by

```math
\rho_A=\sum_{\mu=\pm1}P_\mu |g\rangle\langle g|P_\mu,
```

so the injected energy is

```math
E_A=\mathrm{Tr}(\rho_A H_\mathrm{tot}).
```

Bob receives Alice's classical outcome and applies

```math
U_\mu=\cos(\phi)I-i\mu\sin(\phi)Y_1.
```

The final unconditional state is

```math
\rho_\mathrm{QET}=\sum_{\mu=\pm1}U_\mu P_\mu |g\rangle\langle g|P_\mu U_\mu^\dagger.
```

Bob's local/semi-local energy is

```math
E_1=\mathrm{Tr}[\rho_\mathrm{QET}(H_1+V)],
```

and the extracted energy is reported as

```math
E_B=-E_1.
```

The benchmark always reports

```math
E_A-E_B\ge0.
```

This inequality is the central accounting check. It states that the local
Bob-side extraction is bounded by the Alice-side measurement/control resource in
the exact ground-state protocol.

## Open-System Noise Sweeps

Noise sweeps apply simple channels after Alice's measurement and before Bob's
conditional rotation. Those runs report `post_noise_energy` and
`noise_energy_delta` as system-energy diagnostics for the abstract channel.
Without a concrete dilation or bath model, they are not direct environment
ledgers or closed-system thermodynamic ledgers.
