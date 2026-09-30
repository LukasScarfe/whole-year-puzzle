"""Brute-force every solution of The Whole Year Puzzle (quilici.us) for Puzzle Shapes 1 and 2.

For every month/day pair (all 12 x 31, including dates that don't exist like Feb 30), the two
date cells are left uncovered and every tiling of the remaining 41 cells is enumerated.

Also counts tilings for every pair of uncovered cells (not just month + day), for the statistics page.

Output: docs/data.js, which defines `window.PUZZLE_DATA` for the web viewer. Each solution is a
string with one character per board cell (in `cells` order): the piece index, or '.' for the two
uncovered date cells.

Run: python3 solve.py   (stdlib only; uses all CPU cores)
"""
import json
import os
import time
from itertools import combinations
from multiprocessing import Pool

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Both shapes: months in rows 0-1 (6 per row), days 1-28 in rows 2-5 (7 per row).
# They differ only in where days 29-31 sit on row 6.
SHAPES = {
    'shape1': {
        'name': 'Puzzle Shape 1',
        'row6_start': 2,
        'pieces': {
            'U': [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
            'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
            'X': [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
            'S': [(0, 1), (1, 0), (1, 1), (2, 0)],
            'T': [(0, 1), (1, 0), (1, 1), (2, 1)],
            'l': [(0, 0), (0, 1), (0, 2), (1, 0)],
            'P': [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
            'L': [(0, 1), (1, 1), (2, 1), (3, 0), (3, 1)],
            'Z': [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        },
    },
    'shape2': {
        'name': 'Puzzle Shape 2',
        'row6_start': 0,
        'pieces': {
            'R': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
            'Z': [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1)],
            'U': [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
            'Y': [(0, 2), (1, 0), (1, 1), (1, 2), (1, 3)],
            'V': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
            'N': [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)],
            'P': [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
            'L': [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)],
        },
    },
}


def board(shape):
    s = shape['row6_start']
    cells = [(r, c) for r in range(2) for c in range(6)] + \
            [(r, c) for r in range(2, 6) for c in range(7)] + [(6, s + i) for i in range(3)]
    labels = MONTHS + [str(d) for d in range(1, 32)]
    return cells, labels


def orientations(shape):
    """All distinct rotations and reflections, each normalised to a (0, 0) origin."""
    out = set()
    pts = shape
    for _ in range(2):
        for _ in range(4):
            pts = [(c, -r) for r, c in pts]
            mr = min(r for r, _ in pts)
            mc = min(c for _, c in pts)
            out.add(tuple(sorted((r - mr, c - mc) for r, c in pts)))
        pts = [(r, -c) for r, c in pts]
    return sorted(out)


def build_placements(shape):
    """placements[cell] = [(piece_index, orientation_index, mask)] whose lowest cell is `cell`."""
    cells, _ = board(shape)
    idx = {rc: i for i, rc in enumerate(cells)}
    placements = [[] for _ in cells]
    for pi, pts in enumerate(shape['pieces'].values()):
        for oi, o in enumerate(orientations(pts)):
            for r0, c0 in cells:
                ids = [idx.get((r0 + r, c0 + c)) for r, c in o]
                if None not in ids:
                    mask = sum(1 << i for i in ids)
                    placements[min(ids)].append((pi, oi, mask))
    return placements


def solve_date(args):
    """Enumerate all tilings with cells `month_cell` and `day_cell` left uncovered."""
    shape_key, month_cell, day_cell = args
    shape = SHAPES[shape_key]
    placements = build_placements(shape)
    n_cells = len(placements)
    full = (1 << n_cells) - 1
    all_pieces = (1 << len(shape['pieces'])) - 1
    grid = ['.'] * n_cells
    sols = []

    def rec(filled, used):
        if used == all_pieces:
            sols.append(''.join(grid))
            return
        free = ~filled & full
        cell = (free & -free).bit_length() - 1
        for pi, _, mask in placements[cell]:
            if not (used >> pi) & 1 and not (filled & mask):
                m = mask
                while m:
                    low = m & -m
                    grid[low.bit_length() - 1] = str(pi)
                    m ^= low
                rec(filled | mask, used | (1 << pi))
        # Cells are overwritten on the next placement; reset this cell for cleanliness.
        grid[cell] = '.'

    rec((1 << month_cell) | (1 << day_cell), 0)
    return sols


def count_pair(args):
    """Number of tilings with any two cells `a` and `b` left uncovered (not only month + day)."""
    shape_key, a, b = args
    shape = SHAPES[shape_key]
    placements = build_placements(shape)
    full = (1 << len(placements)) - 1
    all_pieces = (1 << len(shape['pieces'])) - 1

    def rec(filled, used):
        if used == all_pieces:
            return 1
        free = ~filled & full
        cell = (free & -free).bit_length() - 1
        return sum(rec(filled | mask, used | (1 << pi)) for pi, _, mask in placements[cell]
                   if not (used >> pi) & 1 and not (filled & mask))

    return rec((1 << a) | (1 << b), 0)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = {}
    t0 = time.time()
    with Pool() as pool:
        for key, shape in SHAPES.items():
            cells, labels = board(shape)
            jobs = [(key, m, 12 + d) for m in range(12) for d in range(31)]
            results = pool.map(solve_date, jobs, chunksize=4)
            sols = {f'{m + 1}-{d - 11}': r for (_, m, d), r in zip(jobs, results)}
            total = sum(len(v) for v in sols.values())
            print(f'{shape["name"]}: {total:,} solutions across 372 month/day pairs '
                  f'({time.time() - t0:.1f}s)')
            # Counts for every pair of uncovered cells, in itertools.combinations(range(43), 2) order.
            pairs = list(combinations(range(len(cells)), 2))
            pair_counts = pool.map(count_pair, [(key, a, b) for a, b in pairs], chunksize=4)
            placements = build_placements(shape)
            possible = [sum(1 for lst in placements for pi, _, _ in lst if pi == p)
                        for p in range(len(shape['pieces']))]
            print(f'{shape["name"]}: counted all {len(pairs)} hole pairs ({time.time() - t0:.1f}s)')
            out[key] = {
                'name': shape['name'],
                'cells': cells,
                'labels': labels,
                'pieces': [{'name': n, 'shape': p, 'orientations': len(orientations(p))}
                           for n, p in shape['pieces'].items()],
                'solutions': sols,
                'pairs': pair_counts,
                'possiblePlacements': possible,
            }
    os.makedirs(os.path.join(here, 'docs'), exist_ok=True)
    path = os.path.join(here, 'docs', 'data.js')
    with open(path, 'w') as f:
        f.write('window.PUZZLE_DATA = ')
        json.dump(out, f, separators=(',', ':'))
        f.write(';\n')
    print(f'wrote {path} ({os.path.getsize(path) / 1e6:.1f} MB) in {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
