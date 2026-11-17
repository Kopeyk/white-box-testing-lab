# -*- coding: utf-8 -*-
"""Побудова CFG, цикломатична складність, шляхи і покриття ребер CFG тестами."""
import importlib, inspect, subprocess, sys, os
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Вузли CFG = номери рядків у файлі модуля. Ребра: (з, до, мітка)
CFGS = {
    "process_data": {
        "module": "process_data", "entry": 2, "exit": 9,
        "edges": [(2, 3, ""), (3, 4, "є i"), (3, 9, "кінець"), (4, 5, "T"), (4, 6, "F"),
                  (5, 3, "continue"), (6, 7, "є j"), (6, 3, "кінець"), (7, 8, "T"), (7, 6, "F"), (8, 6, "")],
    },
    "check_access": {
        "module": "check_access", "entry": 2, "exit": "EXIT",
        "edges": [(2, 3, "T"), (2, 4, "F"), (3, "EXIT", ""), (4, "EXIT", "")],
    },
    "process_matrix": {
        "module": "process_matrix", "entry": 2, "exit": 8,
        "edges": [(2, 3, ""), (3, 4, "є i"), (3, 8, "кінець"), (4, 5, "є j"), (4, 3, "кінець"),
                  (5, 6, "T"), (5, 4, "F"), (6, 7, "є k"), (6, 4, "кінець"), (7, 6, "")],
    },
    "validate_input": {
        "module": "validate_input", "entry": 2, "exit": "EXIT",
        "edges": [(2, 3, "T"), (2, 4, "F"), (4, 5, "T"), (4, 6, "F"), (6, 7, "T"), (6, 8, "F"),
                  (3, "EXIT", ""), (5, "EXIT", ""), (7, "EXIT", ""), (8, "EXIT", "")],
    },
    "update_task_status": {
        "module": "update_task_status", "entry": 2, "exit": "EXIT",
        "edges": [(2, 9, ""), (9, 10, "T"), (9, 12, "F"), (12, 13, "T"), (12, 15, "F"),
                  (15, 16, "T"), (15, 18, "F"), (18, 19, ""),
                  (10, "EXIT", ""), (13, "EXIT", ""), (16, "EXIT", ""), (19, "EXIT", "")],
    },
    "authenticate_user": {
        "module": "auth", "entry": 2, "exit": "EXIT",
        "edges": [(2, 3, "T"), (2, 4, "F"), (4, 5, "T"), (4, 7, "F"), (7, 8, ""), (8, 9, "T"), (8, 11, "F"),
                  (11, 12, "T"), (11, 15, "F"), (12, 13, ""), (15, 16, ""),
                  (3, "EXIT", ""), (5, "EXIT", ""), (9, "EXIT", ""), (13, "EXIT", ""), (16, "EXIT", "")],
    },
}


def graph(name):
    d = CFGS[name]
    G = nx.DiGraph()
    for a, b, lab in d["edges"]:
        G.add_edge(a, b, label=lab)
    return G


def source_lines(name):
    mod = importlib.import_module(CFGS[name]["module"])
    return open(mod.__file__, encoding="utf8").read().split("\n")


def to_dot(name):
    G = graph(name); src = source_lines(name); d = CFGS[name]
    out = ['digraph CFG {', 'rankdir=TB; nodesep=0.35; ranksep=0.35;',
           'node [shape=box, style="rounded,filled", fillcolor="#F2F5F4", fontname="DejaVu Sans Mono", fontsize=10];',
           'edge [fontname="DejaVu Sans", fontsize=9];']
    for n in G.nodes:
        if n == "EXIT":
            out.append('"EXIT" [shape=doublecircle, label="exit", fillcolor="#FFFFFF", width=0.4];')
            continue
        text = src[n - 1].strip().replace("\\", "\\\\").replace('"', '\\"')
        if len(text) > 46:
            text = text[:44] + "…"
        dec = G.out_degree(n) > 1
        shape = 'shape=diamond, style="filled", fillcolor="#FFF4D6", ' if dec and not text.startswith("for") else ""
        if dec and text.startswith("for"):
            shape = 'style="rounded,filled", fillcolor="#E3ECF7", '
        out.append(f'{n} [{shape}label="{n}: {text}"];')
    out.append(f'START [shape=circle, label="", width=0.25, style=filled, fillcolor=black]; START -> {d["entry"]};')
    for a, b, lab in d["edges"]:
        aa = f'"{a}"' if a == "EXIT" else a; bb = f'"{b}"' if b == "EXIT" else b
        out.append(f'{aa} -> {bb} [label="{lab}"];')
    out.append("}")
    return "\n".join(out)


def cyclomatic(name):
    G = graph(name)
    E, N = G.number_of_edges(), G.number_of_nodes()
    decisions = sum(1 for n in G.nodes if G.out_degree(n) > 1)
    return E, N, E - N + 2, decisions + 1


def simple_paths(name):
    d = CFGS[name]
    return list(nx.all_simple_paths(graph(name), d["entry"], d["exit"]))


# ---------- покриття ребер CFG тестами (трасування рядків) ----------
def trace_edges(name, call):
    d = CFGS[name]; G = graph(name)
    mod = importlib.import_module(d["module"])
    fn = getattr(mod, name)
    code = fn.__code__; first = code.co_firstlineno
    seq = []

    def tracer(frame, event, arg):
        if frame.f_code is code:
            if event == "line":
                ln = frame.f_lineno - first + 1
                if not seq or seq[-1] != ln:
                    seq.append(ln)
            elif event == "return":
                seq.append("RET")
            return tracer
        return None

    sys.settrace(tracer)
    try:
        call(fn)
    finally:
        sys.settrace(None)
    nodes = set(G.nodes)
    path = []
    for x in seq:
        if x == "RET":
            if d["exit"] == "EXIT":
                path.append("EXIT")
            continue
        if x in nodes:
            if path and path[-1] == x:
                continue
            path.append(x)
    edges = {(a, b) for a, b in zip(path, path[1:]) if G.has_edge(a, b)}
    return path, edges


if __name__ == "__main__":
    os.makedirs("cfg", exist_ok=True)
    for name in CFGS:
        dot = to_dot(name)
        open(f"cfg/{name}.dot", "w", encoding="utf8").write(dot)
        subprocess.run(["dot", "-Tpng", "-Gdpi=150", f"cfg/{name}.dot", "-o", f"cfg/{name}.png"], check=True)
        E, N, M, M2 = cyclomatic(name)
        print(f"{name}: E={E} N={N} M=E-N+2={M}  (рішень+1 = {M2}); простих шляхів: {len(simple_paths(name))}")
