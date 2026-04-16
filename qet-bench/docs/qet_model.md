# Two-Qubit QET Model

Qubit `0` is Alice and qubit `1` is Bob. Computational basis vectors are ordered
as `|00>`, `|01>`, `|10>`, `|11>`.

Define

```math
s=\sqrt{h^2+k^2},
```

```math
H_n=hZ_n+\frac{h^2}{s}I,\quad n=0,1,
```

and

```math
V=2kX_0X_1+\frac{2k^2}{s}I.
```

The total Hamiltonian is

```math
H_\mathrm{tot}=H_0+H_1+V.
```

The analytic ground state is

```math
|g\rangle=
\sqrt{\frac{1-h/s}{2}}|00\rangle
-
\sqrt{\frac{1+h/s}{2}}|11\rangle.
```

Alice's projectors are

```math
P_\mu=\frac12(I+\mu X_0),\quad \mu\in\{-1,+1\}.
```

Bob's angle is

```math
\phi=\frac12\operatorname{atan2}(hk,h^2+2k^2).
```

The implementation keeps the post-measurement branch states unnormalized and
sums them directly, which makes the unconditional branch average explicit.

