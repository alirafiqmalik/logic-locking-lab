# Historical experiments

These files preserve the original final-year project working material. They are outside the supported quick start and automated test discovery.

- `post_sat_batch.py` and `batch_locking.py` preserve the old benchmark drivers.
- `scratch/`, `legacy-python/`, and `legacy-locking/` contain exploratory implementations.
- `oracle/` contains C++/Yosys oracle experiments; the compiled executable is ignored.
- `artifacts/` contains historical intermediate netlists and circuit key examples. These keys are circuit test data, not service credentials.
- `results/` contains the original CSV logs and spreadsheet, without normalization or deduplication.

Expect machine-specific `/home/alira/FYP` paths, optional dependencies such as MonoSAT, external benchmark assumptions, and scripts that execute work when imported. Inspect and adapt a script before running it. Use the root README and `tests/` for the maintained demonstration workflow.

The recorded timing files lack a complete environment specification and include repeated rows. They are retained for reference; no comparative performance or locking-security claim is derived from them.
