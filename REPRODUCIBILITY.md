# Reproducibility

Run from the repository root with Python 3.11 or later and Git.

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay uses rational arithmetic to test 80 path fixtures and 59,048 signed right-hand-side patterns. It enumerates every vertex of the illustrated two-node polytope and checks the optimal vertices for tied flags, ordered flags and the cheaper bypass. [Expected output](verification/logs/replay.txt)

[Build the manuscript](paper/BUILD.md) · [Rebuild the figure and offline explorer](visualization/README.md)
