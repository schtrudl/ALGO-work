# Opis algoritma

Graf shranimo kot matriko v enodimentionalnem polju "data" velikosti `n`x`n` pri čemer `n` predstavlja število vozlišč, vrednost `data[i*n + j] = 1` pomeni, da med vozliščema i in j obstaja povezava.
Pred začetkom iskanja ustvarimo še seznam vseh povezav iz matrike in sicer tako, da obhodimo samo zgornji trikotnik matrike, saj je graf neusmerjen in je posledično matrika simetrična, tako se izognemo duplikatom.

Med iskanjem vzdržujemo dve pomožni polji: trenutno, ki hrani množico kompatibilnih povezav, ki jo trenutno gradimo, in najboljse, ki hrani največjo do sedaj najdeno množico.

Iskanje poteka tako, da rekurzivno gradimo množico kompatibilnih povezav tako, da za vsako preostalo povezavo preverimo ali je kompatiilna z že izbranimi in jo v tem primeru dodamo ter od nje naprej rekurzivno nadaljujemo.
Ob koncu posameznega rekurzivnega klica povezavo odstranimo in s tem povrnemo množico kompatibilnih povezav v stanje pred dodajanjem, tako da res izčrpno preverimo vse možnosti. Da se izognemo preverjanju enakih kombinacij v drugčnem vrstnem redu, vsak rekurzivni klic gleda samo naprej po seznamu, kar zagotovimo z indexom.

Glavna optimizacija v algoritmu pa prepreči obhode, ki tudi če bi sprejeli vse še znotraj obhoda nepreverjene povezave, ne bi presegli največjega do sedaj najdenega števila nepovezanih povezav. To storimo s pogojem:

```c
if (trenutno.size() + povezave.size() - idx <= najboljse.size()) {
    return;
}
```
