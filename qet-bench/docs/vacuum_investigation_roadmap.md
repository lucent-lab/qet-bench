# Vacuum-Investigation Roadmap

This document explains how `qet-bench` can grow from an exact two-qubit QET
benchmark into a broader void/vacuum energy-accounting research program without
turning into a collection of overbroad claims.

The organizing rule is:

```text
Every stage must define the system, controller, environment, memory/reset path,
load or battery, cycle condition, and net energy ledger.
```

The project should not claim autonomous vacuum power unless a closed cyclic
protocol returns every non-load degree of freedom to its initial state while a
load ends with net positive stored energy. Nothing in the current repository
claims that.

## Stage 0: Exact QET Benchmark Foundation

**Status:** done.

**Purpose:** establish a minimal, auditable model where ground-state
correlations enable Bob-side local energy extraction after Alice measurement and
classical feedforward.

**Current deliverables:**

- exact two-qubit Hamiltonian and analytic ground state,
- Alice measurement and Bob conditional rotation,
- unconditional branch averaging with no postselection,
- ledger terms `E_A`, `H1`, `V`, `E1`, `E_B`, and `E_A - E_B`,
- null tests, noise diagnostics, count estimators, reproducible artifacts,
- independent pure-Python reference branch,
- optional Qiskit/Aer interoperability bridge.

**Done criteria:**

- local and CI-style tests pass,
- benchmark CSV values reproduce the documented numbers,
- figure scripts regenerate deterministic artifacts,
- documentation states clearly that QET is not a free-energy source.

**Failure modes to keep blocked:**

- postselection,
- hidden sign or bit-ordering errors,
- presenting `E_B > 0` without `E_A - E_B`,
- describing this as direct vacuum-power extraction.

## Stage 1: Publication and Archive Hardening

**Status:** processing.

**Purpose:** make the foundation citable and reviewable before adding more
physics surface area.

**Deliverables:**

- archived release snapshot with DOI or Software Heritage identifier,
- hosted CI revalidation or documented local substitute,
- JOSS/ReScience/SoftwareX-style manuscript package,
- complete artifact manifest and blocker ledger,
- clear repository description that says this is ground-state energy-accounting
  research, with QET as the first deliverable.

**Done criteria:**

- `CITATION.cff`, manuscript, and roadmap register point at the archive,
- generated artifacts match the release scripts,
- unresolved blockers are either closed or explicitly carried forward.

**Why this comes before more vacuum work:** publication hardening makes the
project's accounting discipline inspectable. Without this baseline, later
vacuum-mechanism modules would inherit uncertainty about conventions,
reproducibility, and overclaiming.

## Stage 2: Controller-Inclusive QET Ledger

**Status:** partially started; current module is conservative bookkeeping, not a
microscopic controller model.

**Purpose:** deepen from protocol-level accounting to apparatus-level
accounting.

**Question:**

```text
After measurement, feedforward, pulse generation, memory, reset, and
controller overheads are counted, what is the net battery/load balance?
```

**Minimum model elements:**

- Alice measurement cost or injected energy,
- classical memory and reset cost,
- communication/feedforward control cost,
- Bob pulse/control cost,
- bath or refrigeration cost if reset/cooling is assumed,
- explicit nonnegative overhead terms,
- diagnostic `net_battery_gain = E_B - E_A - overhead`.

**Done criteria:**

- ledger schema is documented,
- all overhead terms have units and sign conventions,
- null tests show that turning off entanglement or scrambling the bit removes
  the QET-specific signal,
- no result is described as a closed hardware battery unless a physical battery
  model exists.

**What would count as new territory:** a clean controller-inclusive inequality
or reusable accounting framework that can compare QET variants without hiding
measurement, reset, or pulse costs.

## Stage 3: Explicit Battery-Coupled QET

**Status:** not done.

**Purpose:** replace bookkeeping-only `net_battery_gain` diagnostics with an
actual load or battery degree of freedom.

**Question:**

```text
Can Bob's local extraction be deposited into an explicit load while the full
system-controller-battery ledger remains thermodynamically consistent?
```

**Candidate models:**

- two-level battery coupled locally to Bob,
- harmonic-oscillator load,
- explicit time-dependent Bob coupling pulse,
- open-system reset model for Alice and the controller.

**Required outputs:**

- final battery energy,
- controller work,
- reset/bath exchange,
- leakage/cross-talk diagnostics,
- comparison to the original two-qubit exact ledger.

**Done criteria:**

- the battery model is explicit in the Hamiltonian or master equation,
- the cycle condition is stated,
- `net_battery_gain` is computed from modeled terms rather than placeholders,
- entanglement-off and feedforward-scrambled null tests fail as expected.

**What would count as new territory:** a reproducible battery-coupled QET model
that separates local work storage from measurement/controller resources.

## Stage 4: Many-Body, Distance, and Finite-Temperature QET

**Status:** not done.

**Purpose:** test whether the two-qubit effect survives more realistic
ground-state structure, separation, noise, and imperfect initialization.

**Questions:**

- How does `E_B` scale with Alice-Bob distance?
- Which local-energy partition is being measured?
- How do finite temperature and mixed states change the ledger?
- Does controller cost dominate faster than extractable local energy grows?

**Candidate implementations:**

- exact diagonalization for small chains,
- tensor-network methods for larger one-dimensional systems,
- finite-temperature density matrices for small systems,
- equalized-noise comparisons across sizes and distances.

**Done criteria:**

- the two-qubit benchmark remains a regression anchor,
- local Hamiltonian terms and energy partitions are documented,
- distance and temperature sweeps include null tests,
- claims are about scaling diagnostics, not free energy.

**What would count as new territory:** a scaling law, bound, or negative result
that explains when QET-style local extraction is practically suppressed.

## Stage 5: Vacuum-Mechanism Audit Modules

**Status:** not done.

**Purpose:** move beyond QET into other vacuum-adjacent mechanisms while keeping
the same ledger discipline.

Each module should be separate from the exact QET core and should have its own
artifact manifest, null tests, and no-free-energy statement.

### Dynamical Casimir Effect Audit

**Question:** when photons are produced from an initial vacuum by a time-varying
boundary or coupling, does the pump/controller work account for the emitted
energy?

**Required ledger:**

```text
W_controller, E_field, losses, reset cost, final pump/controller state
```

**Done criteria:** photon production tracks the drive work; no output is
described as vacuum-alone energy.

### Casimir or Material-Switching Audit

**Question:** can a material, geometry, or boundary-switching cycle extract net
work after switching and reset costs are included?

**Required ledger:**

```text
mechanical work, material switching/free-energy cost, dissipation, reset work
```

**Done criteria:** the model distinguishes one-shot relaxation from a closed
cycle.

### Ultrastrong-Coupling Discharge Audit

**Question:** can dressed ground-state excitations be released after a coupling
quench, and is the output explained by coupling-switch work?

**Required ledger:**

```text
coupling-switch work, emitted excitation energy, dissipation, re-dressing cost
```

**Done criteria:** output is compared against the full switching protocol, not
against the field vacuum alone.

**What would count as new territory:** a reusable audit showing exactly where
candidate vacuum-energy mechanisms get their energy under closed-cycle
bookkeeping.

## Stage 6: Hardware-Faithful or Experimental Work

**Status:** not done.

**Purpose:** validate a narrow protocol or audit method against realistic
control, noise, and measurement constraints.

**Required before starting:**

- exact model passes,
- controller/battery ledger is explicit,
- bit-order and count-processing conventions are tested,
- hardware-independent null tests are defined,
- acceptable interpretation limits are written before looking at data.

**Candidate targets:**

- Qiskit/Aer noisy simulation,
- IBM-style small-QPU reproduction,
- superconducting-circuit QET or DCE-inspired model,
- quantum Hall or edge-channel QET-inspired model.

**Done criteria:**

- calibration and uncertainty assumptions are documented,
- direct leakage and cross-talk baselines are included,
- entanglement-off and scrambled-control nulls are included,
- the result is described as hardware validation or falsification, not proof of
  autonomous vacuum power.

## Closed-Cycle Acceptance Criterion

For any future vacuum-energy claim, the acceptance criterion is:

```text
net_load_gain =
    load_energy_gain
  - controller_work
  - measurement_and_reset_cost
  - switching_or_boundary_work
  - bath_or_refrigeration_cost
  - leakage_and_calibration_allowances
```

A claim only enters "possible vacuum-energy work extraction" territory if all of
these are true:

1. `net_load_gain > 0` with uncertainty bounds.
2. The protocol is cyclic for every non-load degree of freedom.
3. Entanglement-off, no-drive, scrambled-control, and classical-leakage nulls
   fail to explain the signal.
4. The source of energy cannot be attributed to a pump, controller, prepared
   non-passive state, thermal bath, reset process, or boundary switching.

The expected outcome under known physics is that candidate mechanisms fail this
criterion. A well-documented failure is still a valid research output because it
identifies exactly which resource pays.

## Recommended Next Sequence

1. Finish archive/DOI and hosted CI revalidation for the current QET benchmark.
2. Promote the controller-cost ledger from conservative bookkeeping to an
   explicit controller/environment model.
3. Build an explicit battery-coupled QET model.
4. Add many-body, distance, and finite-temperature QET studies only after the
   battery ledger is clear.
5. Start a separate DCE pump-work audit or Casimir switching-work audit as the
   first non-QET vacuum-mechanism module.
6. Treat hardware work as validation after the ledger and null tests are
   already specified.

