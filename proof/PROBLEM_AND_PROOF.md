# Problem and proof

A fixed dataset of linear measurements is sufficient when it determines the whole set of optimal solutions for every cost in an open convex prior. Bennouna et al.’s characterization identifies its minimum size with the dimension of differences between reachable optimal vertices. The question is whether exact minimum-size hardness persists when every feasible vertex has exactly the row rank in positive coordinates.

Start with the inverse shortest-path DAG for 3-SAT. The strict open cost prior gives two behaviors. A satisfiable formula allows a path through the distinguished arc that beats all bypasses. For an unsatisfiable formula every such path has a strictly better shortcut at every allowed cost.

Replace the distinguished arc with a cheaper half-capacity arc and two uncapped flags. Give internal vertices tiny demands in a geometric sequence. Total unimodularity and dominance in every nonzero signed sum of demands imply that all basic coordinates are nonzero.

Compare the prior allowing a price tie between the flags with the same prior restricted to the first flag strictly cheaper. Merging the flags gives the same reachable optimal set in both priors. For satisfiable formulas the tied case yields positive flag flow and therefore an exchange direction. For unsatisfiable formulas both flags stay unused in every optimum. Thus the dimension difference detects satisfiability through two oracle calls.

A supplied dataset measuring all other coordinates and the sum of the flags is sufficient precisely when no exchange direction occurs. Reachable vertices have polynomially checkable basis certificates, giving coNP membership. These certificates also give NP-oracle upper bounds for dimension and construction. The empty dataset has a direct polynomial check by testing whether one vertex’s unique optimality cone contains the entire prior.

[Full proof](../paper/manuscript.pdf) · [Exact replay](../verification/src/replay.py)
