# Worked flow example

A unit of flow travels from s to t. Its four parallel arcs are a cheap arc u of capacity 1/2, two uncapped flags f1 and f2, and a bypass. The displayed prices use zero slack cost. In order (u, f1, f2, bypass, slack), the tied-price optimum has endpoints (1/2, 1/2, 0, 0, 0) and (1/2, 0, 1/2, 0, 0). Every convex combination is optimal and the direction of the edge is the flag exchange. Making f1 cheaper gives only the first endpoint. A cheaper bypass makes the optimum (0, 0, 0, 1, 1/2).

The illustrative polytopes use the same feasible region, with six vertices and exactly two positive coordinates per vertex. The [replay](../verification/src/replay.py) verifies these statements for each displayed cost. The example illustrates the mechanism, while the proof embeds it in a reduction from satisfiability.

Extract the [offline explorer](flow-measurements-explorer.zip) and open index.html. Rebuild the ZIP and the 704 × 826 GIF by running python3 visualization/render.py with Python 3.11 or later, Pillow 13 and the Arial faces supplied with macOS. The optional --output argument writes the rebuilt files to another folder.
