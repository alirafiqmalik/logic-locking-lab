import subprocess
import os
import shlex
from pathlib import Path
from src.netlist import Netlist

yosys_path = shlex.quote(os.environ.get("YOSYS", "yosys"))
abc_path = shlex.quote(os.environ.get("ABC", "yosys-abc"))
library_path = Path(__file__).resolve().parents[1] / "libraries" / "mycells.lib"


cmd1=yosys_path+""" -p '
read_verilog {inputfile}
hierarchy -check -top top
flatten
{getcpp}write_cxxrtl {cppfile}
proc; opt; fsm; opt; memory; opt
techmap; opt
{gettmpv}write_verilog -noattr {rtlv}
dfflibmap -liberty {library_path}
abc -liberty {library_path}

write_verilog -noattr {outputfile}
'
"""

cmd1 = cmd1.replace("{library_path}", '"' + str(library_path) + '"')

cmd2=abc_path+r" -c 'read_bench {};write_verilog {}'"
