# Lean certificate

**Signed perturbations**

An integer combination of consecutive powers of four with coefficients in {−1, 0, 1} vanishes exactly when all its coefficients vanish. Clearing a common denominator gives this form for combinations of the internal-vertex demands.

The basis arguments, separate large right-hand-side entries, and complexity theorems are proved in the paper.

The principal checked declaration is `FlowPerturbation.zero_iff`. See [A nondegenerate flow polytope](../paper/manuscript.tex#L51) in the manuscript. [Lean source](Q438.lean) · [Verification workflow](../.github/workflows/lean.yml)

Replay with Lean 4.30.0 and its standard library from the repository root.

```sh
lean -DwarningAsError=true formalization/Q438.lean
```
