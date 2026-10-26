# Project layout and migration

The maintained entry point is `python -m satattack.run`, or the installed `logic-locking-attack` command. Install the checkout with `python -m pip install -e .` first. Direct execution of `satattack/run.py` is replaced by module execution so package imports resolve consistently.

| Previous location | Current location |
| --- | --- |
| `NPS.py` generator | `src/post_sat.py`; `NPS.py` keeps the import compatible |
| `NPS.py` batch experiment | `experiments/post_sat_batch.py` |
| `Misc/` | `experiments/scratch/` |
| `python/` | `experiments/legacy-python/` |
| `src/Misc/` | `experiments/legacy-locking/` |
| `oracle/` | `experiments/oracle/` |
| Original machine-specific `src/cmds.py` scripts | `experiments/legacy_commands.py` |
| `vlib/` | `libraries/` |
| Root `log*` files | `experiments/results/` |
| Root temporary Verilog and `tmp/` | `experiments/artifacts/` |
| `tmpwork.py` | `experiments/batch_locking.py` |
| `satattack/tmp.py` | `experiments/attack_timing.py` |
| `satattack/benchmarks_test.py` | `experiments/parser_probe.py` (an exploratory script, not a test suite) |
| `src/genmain.py` | `experiments/generate_oracle.py` |

Tracked bytecode, editor settings, a compiled oracle executable, the absolute `linux` symlink, and the unconfigured `Benchmarks` gitlink were removed from the index. Local environment files can remain ignored. Put new generated output in `build/` and external benchmark downloads in `benchmarks/external/`.

The legacy drivers are preserved as historical source. Their hardcoded paths and assumptions are not automatically migrated. Reusable `src.cmds` synthesis templates now use configurable executables and the checkout-relative cell library. An editable source installation is the supported setup.

The public repository is now `alirafiqmalik/logic-locking-lab`; existing local folders can retain their names. To update an older clone:

```bash
git remote set-url origin https://github.com/alirafiqmalik/logic-locking-lab.git
```
