# Navodila

## Drevesna struktura

- `*.in` so vhodne datoteke
- `*.out` so izhodne datoteke (pričakovan izhod)
- `algo1.cpp` je implementiran algoritem
- `reference.py` je referenčna implementacija (počasna a vedno vrne pravilno rešitev)
- `verify.py` za preverjanje pravilnosti rešitve (pravilnih rešitev je več)

## Navodila za poganjanje

prevajanje z: `clang -O3 -march=native algo1.cpp -o algo1` (lahko tudi gcc)

pri poganjanju se na stdin postavi vhodne podatke: `./algo1 < test00.in` izhod je na stdout

vse python scripte pa podpirajo `--help`
