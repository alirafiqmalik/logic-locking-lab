"""Command-line entry point for the circuit SAT attack."""
import argparse
import time
from .sat_attack import SatAttack


def main():
    parser = argparse.ArgumentParser(description="Perform a SAT attack on a locked circuit.")
    parser.add_argument("locked_ckt", help="Locked circuit file")
    parser.add_argument("oracle", help="Unlocked circuit file")
    parser.add_argument("file_type", choices=("b", "v"), help="BENCH (b) or gate-level Verilog (v)")
    args = parser.parse_args()
    attack = SatAttack(args.locked_ckt, args.oracle, args.file_type)
    start = time.perf_counter()
    attack.run()
    print("\nIterations: %i" % attack.iterations)
    print("Elapsed time: %.3fs" % (time.perf_counter() - start))


if __name__ == "__main__":
    main()
