Hevristika algoritma velike elemente (>0.5) daje v najmanjši obstoječi koš.
Ta odločitev vodi do suboptimalnih parov, saj je algoritem je "online" in ne more čakati na prihodnje idealne kombinacije.

Ta konkreten skonstruiran primer ponavljajpčega vzorca 0.51, 0.51, 0.49, 0.49 dobro ponazori to slabost:
- 0.51 + 0.51 = 1.02 - koš se zapre z waste-om 0.02
- 0.49 + 0.49 = 0.98 - koš ostane odprt (ne dosega 1)

Konkretno tako dobimo suboptimalen izhod pri vhodu 500 elementov s ponavljajočim vzorcem, ki je 208 pokritih košev in 1 odprt
Optimalno bi bilo v tem primeru 250 pokritih košev ter noben odprt.

Online greedy algoritem torej ne more optimalno parčkati obstoječih elementov in je prisiljen na hitre lokalne paritve, ki niso globalno optimalne.
