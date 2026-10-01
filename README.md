# The Whole Year Puzzle

Every solution to [The Whole Year Puzzle](https://quilici.us/TheWholeYearPuzzle/index.php) calendar
puzzle, Puzzle Shapes 1 and 2, for every date, plus an original Heart board (two piece-set variants),
with a static site to browse them and explore statistics.

**Site:** https://yearpuzzle.michelleyap.ca/

The board selector offers Shape 1, Shape 2 and **Heart**; picking Heart reveals a *Set 1 / Set 2*
switch for its two piece sets (the same board, different pieces). Everything below works for whichever
puzzle is selected.

- **Play:** try the puzzle yourself for the selected shape and date: drag pieces onto the board,
  rotate and flip them (buttons, tapping a selected piece, or A / D to rotate, W / S to flip, Space to send back to the tray). When it's solved,
  confetti and a popup tell you which numbered solution you found, open it in Solutions, or share it:
  one link to try the same date yourself and a separate, clearly marked spoiler link to your solution.
  An optional Timer (remembered between visits) starts with your first piece, stops when it's solved,
  and adds your time to the popup and the share text.
- **Solutions:** pick a shape and a date to see every solution, ordered by the piece in each cell
  reading from the top-left. The *Find your solution* picker narrows the list one cell at a time. A found or enlarged
  solution has the same Share button as Play, for solves done on a physical puzzle.
- **Statistics:** calendar heatmap, which months/days/cells are easiest and hardest, the full
  distribution, where each piece likes to sit, counts for every pair of open cells (including ones
  that aren't dates), and the easiest and hardest month, date number and open-cell combination, all
  for the selected shape, plus a comparison scatter on log axes whose two axes you can set to any
  pair of the four puzzles.

## Results (366 real dates)

| | Shape 1 | Shape 2 | Heart · Set 1 | Heart · Set 2 |
|---|---|---|---|---|
| Pieces | 9: L, l (4-cell L), O (square), P, S, T, U, X, Z | 8: L, N, P, R (2×3 rectangle), U, V, Y, Z | 9: N, P, U, V, W, l, o, s, t | 9: F, L, P, U, Y, l, o, s, t |
| Total solutions | 40,219 | 24,405 | 43,993 | 64,781 |
| Fewest | May 21 (11) | Oct 6 (7) | Jun 10, Oct 18 (17) | Feb 4 (25) |
| Most | Jan 28 (734) | Jan 25 (216) | May 13, Nov 15 (384) | Mar 9, Jul 1 (766) |

Shape 2 is the well-known "DragonFjord" calendar puzzle set, and its totals match published counts.
The Heart is an original 9×7 board (two square lobes over a body tapering to a three-wide point) from
the sister [calendar-puzzle-designs](../calendar-puzzle-designs) search. Both sets are solvable on
every date; they run a bit easier than the two Shapes (higher medians, higher minimums).

Placements are anchored over the whole bounding box, not just over board cells, so pieces whose
normalised corner lands off a *concave* board (as on the Heart) are still counted — see `solve.py`.

## Files

| File | What it does |
|---|---|
| `solve.py` | Exhaustive search over all four puzzles. Writes `docs/data.js` with every solution for all 12 × 31 month/day pairs (including dates like Feb 30) and tiling counts for every pair of open cells. Python stdlib only, uses all cores, ~10 min on 12 cores. |
| `verify.py` | Re-checks `docs/data.js`: every solution is a valid tiling, and counts for sample dates match an independent Algorithm X search. |
| `docs/` | The static site (`index.html` + `data.js`), served by GitHub Pages. |

```sh
python3 solve.py      # regenerate docs/data.js
python3 verify.py     # check it
python3 -m http.server -d docs   # view locally at http://localhost:8000
```
