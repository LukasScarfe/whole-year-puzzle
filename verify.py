"""Check docs/data.js independently of the solver that produced it.

1. Every stored solution is a valid tiling: each piece used exactly once in one of its
   orientations, only the month and day cells left open, no duplicates.
2. Solution counts for a sample of dates match an independent exact-cover search
   (Knuth's Algorithm X), which does not share the solver's search order.

Run: python3 verify.py
"""
import json
import os
import random

import solve


def load():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'data.js')
    text = open(path).read()
    return json.loads(text[text.index('=') + 1:].rstrip().rstrip(';'))


def canon(pts):
    return min(solve.orientations(list(pts)))


def check_solutions(key, data):
    shape = solve.SHAPES[key]
    cells, _ = solve.board(shape)
    pieces = [canon(p) for p in shape['pieces'].values()]
    bad = total = 0
    for date, sols in data['solutions'].items():
        m, d = map(int, date.split('-'))
        if len(set(sols)) != len(sols):
            bad += 1
        for sol in sols:
            total += 1
            ok = len(sol) == len(cells) and {i for i, ch in enumerate(sol) if ch == '.'} == {m - 1, 11 + d}
            for pi, p in enumerate(pieces):
                pc = [cells[i] for i, ch in enumerate(sol) if ch == str(pi)]
                ok = ok and len(pc) == len(p) and canon(pc) == p
            bad += not ok
    return total, bad


def count_algorithm_x(shape, m, d):
    cells, _ = solve.board(shape)
    idx = {rc: i for i, rc in enumerate(cells)}
    open_cells = {m - 1, 11 + d}
    rows = {}
    for name, pts in shape['pieces'].items():
        for o in solve.orientations(pts):
            for r0 in range(-3, 8):
                for c0 in range(-3, 8):
                    ids = [idx.get((r0 + r, c0 + c)) for r, c in o]
                    if None not in ids and not open_cells & set(ids):
                        rows[(name, o, r0, c0)] = ['P' + name] + ids
    X = {c: set() for c in ['P' + p for p in shape['pieces']] + [i for i in range(len(cells)) if i not in open_cells]}
    for r, cols in rows.items():
        for c in cols:
            X[c].add(r)

    def search():
        if not X:
            return 1
        col = min(X, key=lambda c: len(X[c]))
        n = 0
        for r in list(X[col]):
            removed = []
            for j in rows[r]:
                for i in X[j]:
                    for k in rows[i]:
                        if k != j:
                            X[k].discard(i)
                removed.append(X.pop(j))
            n += search()
            for j, saved in zip(reversed(rows[r]), reversed(removed)):
                X[j] = saved
                for i in saved:
                    for k in rows[i]:
                        if k != j:
                            X[k].add(i)
        return n

    return search()


def main():
    data = load()
    random.seed(0)
    ok = True
    for key in solve.SHAPES:
        total, bad = check_solutions(key, data[key])
        print(f'{key}: {total:,} stored solutions checked, {bad} invalid')
        dates = [(random.randint(1, 12), random.randint(1, 31)) for _ in range(15)]
        mismatches = [(m, d) for m, d in dates
                      if count_algorithm_x(solve.SHAPES[key], m, d) != len(data[key]['solutions'][f'{m}-{d}'])]
        print(f'{key}: Algorithm X agrees on {len(dates) - len(mismatches)}/{len(dates)} sampled dates'
              + (f' (mismatch: {mismatches})' if mismatches else ''))
        ok = ok and not bad and not mismatches
    print('OK' if ok else 'FAILED')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
