# TRF
A parser and dumper for the fide approved tournament report format: trf
The trf file format is used by the [Fide](https://en.wikipedia.org/wiki/FIDE) to report tournament results and calculate elo ratings based on them.

- Specification: <https://tec.fide.com/wp-content/uploads/2025/04/TRF-2026.pdf>
- Example: <https://tec.fide.com/2024/09/04/draft-trf-2025-extensions-for-team-pairing-and-tie-breaks/>

This project is based on https://github.com/sklangen/TRF which only implements TRF16.

## Simple usage example

```python
import trf

with open('example_trf16.trf') as f:
    tour = trf.load(f)

print(tour.name)
for player in tour.players:
    print(player.name, '-', player.points)
```
