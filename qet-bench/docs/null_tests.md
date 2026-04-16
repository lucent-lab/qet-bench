# Null Tests

The first deliverable includes diagnostics that protect against overinterpreting
the exact benchmark.

## Zero Coupling

At `k=0`, Alice and Bob are not coupled by `V`. Bob extraction should vanish
even though Alice's local measurement can still inject energy.

## Scrambled Feedforward

Bob's operation depends on Alice's classical sign. A sign-flip probability
`q=0.5` removes the useful correlation between Alice's result and Bob's
rotation. The benchmark checks that this reduces or reverses `E_B`.

## Product-State Reference

The `product_00` diagnostic is intentionally not a ground-state QET setup:
`|00>` is an excited product reference for the benchmark Hamiltonian. It is
included to keep the distinction between prepared local excitation and
ground-state-correlation-assisted extraction explicit.

## Wrong Angle

The wrong-angle scan evaluates Bob extraction away from the analytic angle. It
is a numerical sanity check on the sign convention and the rotation formula.

## Bob-Only Random Unitaries

The Bob-only scan samples random local unitaries without Alice measurement or
feedforward. It is a finite implementation diagnostic, not a theorem over all
possible controls.

