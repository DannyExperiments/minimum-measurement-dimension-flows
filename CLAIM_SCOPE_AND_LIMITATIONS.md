# Claim scope and limitations

The inputs are rational standard-form LPs with every vertex supported on a full basis, and nonempty full-dimensional open rational H-polyhedral cost priors. A global dataset must recover the complete argmin set from exact linear queries for every cost in the prior.

Exact dimension and minimum-dataset construction are NP-hard under polynomial-time Turing reductions. Their upper bounds use logarithmically many NP queries for the dimension and an NP oracle for minimum-dataset construction. A supplied dataset can be verified in coNP, and the lower bound for that verification is by a many-one reduction. Empty-dataset verification has a polynomial-time algorithm.

The dimension-threshold problem’s many-one hardness and completeness, approximation, noisy measurements and adaptive pointwise querying are outside the claim. The finite diagnostics corroborate selected steps. The all-instance result follows from the proof. External peer review and formalization are pending.
