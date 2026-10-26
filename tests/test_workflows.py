"""Regression checks for the documented workflows after reorganization."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from satattack.sat_attack import SatAttack
from satattack.benchmarks import read_ckt
from satattack.circuit_solver import solve_ckt
from src.LL import LogicLocking
from src.conv import bench_to_verilog
from src.post_sat import PostSAT_LL

ROOT = Path(__file__).resolve().parents[1]
CIRCUITS = ROOT / 'examples/circuits'

class WorkflowTests(unittest.TestCase):
    def test_attack_recovers_equivalent_circuit_in_both_formats(self):
        for extension, mode in [('bench', 'b'), ('v', 'v')]:
            with self.subTest(mode=mode):
                attack = SatAttack(str(CIRCUITS / f'and_locked.{extension}'), str(CIRCUITS / f'and_oracle.{extension}'), mode)
                output = StringIO()
                with redirect_stdout(output):
                    attack.run()
                self.assertIn('Found key:    0', output.getvalue())
                self.assertIn('Locked and unlocked circuits match', output.getvalue())
                self.assertEqual(attack.iterations, 1)
                self.assertFalse(attack._check_key({'keyinput0': True}))

    def test_oracle_truth_table(self):
        circuit = read_ckt(str(CIRCUITS / 'and_oracle.bench'), 'b')
        for a in [False, True]:
            for b in [False, True]:
                self.assertEqual(solve_ckt(circuit, {'a': a, 'b': b}), {'y': a and b})

    def test_lock_export_attack_round_trip(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(StringIO()):
            # An internal wire gives RLL an insertion point.
            original = 'INPUT(a)\nINPUT(b)\nOUTPUT(y)\nn = AND(a,b)\ny = NOT(n)\n'
            oracle = Path(directory) / 'oracle.bench'
            locked = Path(directory) / 'locked.bench'
            oracle.write_text(original)
            circuit = LogicLocking(original)
            circuit.RLL(1, 1)
            circuit.graph_to_bench(str(locked))
            attack = SatAttack(str(locked), str(oracle), 'b')
            attack.run()
            self.assertTrue(attack._check_key({'keyinput_0': True}))
            self.assertFalse(attack._check_key({'keyinput_0': False}))

    def test_post_sat_generators_import_and_emit_modules(self):
        with redirect_stdout(StringIO()):
            circuit = PostSAT_LL((CIRCUITS / 'and_oracle.v').read_text())
            for result in [circuit.AntiSat(key_lengthi=2), circuit.SFLL(key=1, key_lengthi=2, log=True)]:
                self.assertIn('module top', result)
                self.assertIn('module org', result)
                self.assertIn('keyinput', result)

    def test_conversion(self):
        verilog, counts = bench_to_verilog((CIRCUITS / 'and_oracle.bench').read_text())
        self.assertEqual(counts['AND'], 1)
        self.assertEqual(sum(counts.values()), 1)
        self.assertIn('a & b', verilog)

    def test_cli_outside_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, '-m', 'satattack.run', str(CIRCUITS / 'and_locked.bench'), str(CIRCUITS / 'and_oracle.bench'), 'b'], cwd=directory, capture_output=True, text=True, check=True)
        self.assertIn('Locked and unlocked circuits match', result.stdout)

if __name__ == '__main__':
    unittest.main()
