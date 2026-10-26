# Contributing

Install an editable checkout in a virtual environment using the root README, then run:

```bash
python -m unittest discover -s tests -v
```

For a parser or solver issue, include the smallest circuit pair that reproduces it, the exact command, Python/dependency versions, and expected versus actual output. Share only circuit files you have permission to distribute.

Keep reusable code in `src/` or `satattack/`, runnable circuit examples in `examples/circuits/`, and regression checks in `tests/`. Historical scripts belong in `experiments/`; generated local outputs belong in ignored `build/`. Update documentation when changing supported input syntax or command behavior.

The README diagram comes from `scripts/render_circuit.py`. Regenerate it with Graphviz when its fixture changes. Keep capability and performance statements tied to an example, test, or reproducible measurement.
