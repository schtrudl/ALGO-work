Tipično se za take probleme naredi program ki sprejme le en vhod in vrne en izhod (bodisi v obliki datoteke bodisi preko stdin/stdout).
Tukaj pa program prejme ime mape, kar oteži delo (recimo merjenje hitrosti saj nas zanima hitrost na posameznem primeru).

Namesto BigDecimal se lahko uporabi `double`, saj v navodilih piše:

> zaporedje n decimalnih števil, ki predstavljajo velikosti predmetov v vrstnem redu prihajanja
(velikosti bodo omejene na petnajst decimalnih mest)

in vsi podatki so oblike `0.xx`, ker je mantisa `double` velika 52 bitov je to ravno natančnost do 15 decimalnega mesta (ta omejitev je v navodilih ravno zato da se lahko uporabi `double`)

V opisu algoritma že tudi sama podata lastnosti najslabšega primera (`n = k`), ki je skonstruiran v input_6.txt
Mogoče bi bila tukaj rešitev da hranita odprte koše v urejenem povezanem seznamu (tako lahko delaš bisekcijo, ki je log k) in se tako izogneš prgledovanju vseh odprtih košev