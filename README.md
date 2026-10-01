# The Whole Year Puzzle Solutions

Every solution to [The Whole Year Puzzle](https://quilici.us/TheWholeYearPuzzle/index.php) calendar
puzzle, Puzzle Shapes 1 and 2, for every date, plus a static site to browse them and explore
statistics.

**Site:** https://lukasscarfe.github.io/whole-year-puzzle/

- **Solutions:** pick a shape and a date to see every solution, ordered by the piece in each cell
  reading from the top-left. The *Find your solution* picker narrows the list one cell at a time.
- **Statistics:** calendar heatmap, which months/days/cells are easiest and hardest, the full
  distribution, a Shape 1 vs Shape 2 comparison, where each piece likes to sit, counts for every
  pair of open cells (not just dates), and the easiest and hardest month, date number, day and
  open-cell combination for each shape.

## Results (366 real dates)

| | Shape 1 | Shape 2 |
|---|---|---|
| Pieces | 9: L, l (4-cell L), O (square), P, S, T, U, X, Z | 8: L, N, P, R (2×3 rectangle), U, V, Y, Z |
| Total solutions | 40,219 | 24,405 |
| Fewest | May 21 (11) | Oct 6 (7) |
| Most | Jan 28 (734) | Jan 25 (216) |

Shape 2 is the well-known "DragonFjord" calendar puzzle set, and its totals match published counts.

## Files

| File | What it does |
|---|---|
| `solve.py` | Exhaustive search. Writes `docs/data.js` with every solution for all 12 × 31 month/day pairs (including dates like Feb 30) and tiling counts for every pair of open cells. Python stdlib only, uses all cores, ~4 min on 12 cores. |
| `verify.py` | Re-checks `docs/data.js`: every solution is a valid tiling, and counts for sample dates match an independent Algorithm X search. |
| `docs/` | The static site (`index.html` + `data.js`), served by GitHub Pages. |

```sh
python3 solve.py      # regenerate docs/data.js
python3 verify.py     # check it
python3 -m http.server -d docs   # view locally at http://localhost:8000
```
