"""Render the README circuit directly from the checked-in BENCH fixture.

Requires Graphviz's `dot` executable. Run from an editable installation.
"""
import json
from pathlib import Path
import subprocess
from satattack.benchmarks import read_nodes_b

ROOT = Path(__file__).resolve().parents[1]

def main():
    nodes, outputs = read_nodes_b(ROOT / "examples/circuits/and_locked.bench")
    lines = [
        'digraph circuit {',
        'graph [rankdir=LR, bgcolor="#0f172a", pad="0.5", nodesep="0.65", ranksep="0.85",',
        'label="LOGIC LOCKING LAB\\nAND circuit with XOR locking", labelloc=t,',
        'fontname="DejaVu Sans", fontsize=24, fontcolor="#f8fafc"];',
        'node [shape=box, style="rounded,filled", fontname="DejaVu Sans",',
        'fontsize=16, color="#475569", fillcolor="#1e293b", fontcolor="#f8fafc", margin="0.22,0.15"];',
        'edge [color="#94a3b8", arrowsize=0.8];',
    ]
    for name, node in nodes.items():
        label = name if 'Input' in node.type else f'{node.type.upper()} → {name}'
        color = '#115e59' if node.type == 'Key Input' else '#1e293b'
        lines.append(f'{json.dumps(name)} [label={json.dumps(label, ensure_ascii=False)}, fillcolor="{color}"];')
        for child in node.inputs:
            lines.append(f'{json.dumps(child)} -> {json.dumps(name)};')
    for name in outputs:
        lines.append(f'{json.dumps(name)} [color="#2dd4bf", penwidth=2];')
    lines.append('}')
    dot = '\n'.join(lines) + '\n'
    target = ROOT / 'docs/assets/locked-circuit'
    target.with_suffix('.dot').write_text(dot)
    subprocess.run(['dot', '-Tsvg', '-o', str(target.with_suffix('.svg'))], input=dot, text=True, check=True)

if __name__ == '__main__':
    main()
