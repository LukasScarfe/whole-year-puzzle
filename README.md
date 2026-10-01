# The Whole Year Puzzle Solutions

Every solution to [The Whole Year Puzzle](https://quilici.us/TheWholeYearPuzzle/index.php) calendar
puzzle, Puzzle Shapes 1 and 2, for every date, plus a static site to browse them and explore
statistics.

**Site:** https://world-puzzle.michelleyap.ca/

- **Play:** try the puzzle yourself for the selected shape and date: drag pieces onto the board,
  rotate and flip them (buttons, tapping a selected piece, or A / D to rotate, W / S to flip, Space to send back to the tray). When it's solved,
  confetti and a popup tell you which numbered solution you found, open it in Solutions, or share it:
  one link to try the same date yourself and a separate, clearly marked spoiler link to your solution.
- **Solutions:** pick a shape and a date to see every solution, ordered by the piece in each cell
  reading from the top-left. The *Find your solution* picker narrows the list one cell at a time.
- **Statistics:** calendar heatmap, which months/days/cells are easiest and hardest, the full
  distribution, where each piece likes to sit, counts for every pair of open cells (including ones
  that aren't dates), and the easiest and hardest month, date number and open-cell combination, all
  for the selected shape, plus a Shape 1 vs Shape 2 scatter on log axes.

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
