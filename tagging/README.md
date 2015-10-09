Práctico 2 - PLN 2015
=====================

Ejercicio 1)
------------

### Estadísticas:

* Sents: 17379

* Tokens: 517300

* Words: 46483

* Tags: 48

#### 10 tags más frecuentes:

|Tag | Freq  |   %   | Descripción  | 5 most frequent words                                            |
|----|-------|-------|--------------|------------------------------------------------------------------|
|nc  | 92002 | 17.79 | Nombre Común          | 'años', 'presidente', 'millones', 'equipo', 'partido' |
sp  | 79904 | 15.45 | Preposición           | 'de', 'en', 'a', 'del', 'con'                          |
da  | 54552 | 10.55 | Articulo              | 'la', 'el', 'los', 'las', 'El'                         |
vm  | 50609 |  9.78 | Verbo principal       | 'está', 'tiene', 'dijo', 'puede', 'hace'               |
aq  | 33904 |  6.55 | Adjetivo calificativo | 'pasado', 'gran', 'mayor', 'nuevo', 'próximo'          |
fc  | 30148 |  5.83 | Puntuación            | ','                                                    |
np  | 29113 |  5.63 | Nombre Propio         | 'Gobierno', 'España', 'PP', 'Barcelona', 'Madrid'      |
fp  | 21157 |  4.09 | Puntuación            | '.', '(', ')'                                          |
rg  | 15333 |  2.96 | Adverbio General      | 'más', 'hoy', 'también', 'ayer', 'ya'                  |
cc  | 15023 |  2.90 | Conjunción Coordinada | 'y', 'pero', 'o', 'Pero', 'e'                          |

#### Niveles de Ambiguedad:

Ambig. Level | Words  | Percentage | 5 Most frequent words        |
------|--------|------------|-------------------------------------|
1     | 44110  | 94.89      | ',', 'el', 'en', 'con', 'por'       |
2     | 2194   | 4.72       | 'la', 'y', '"', 'los', 'del'        |
3     | 153    | 0.33       | '.', 'a', 'un', 'no', 'es'          |
4     | 19     | 0.04       | 'de', 'dos', 'este', 'tres', 'todo' |
5     | 4      | 0.01       | 'que', 'mismo', 'cinco', 'medio'    |
6     | 3      | 0.01       | 'una', 'como', 'uno'                |
7     | 0      | 0.00       |                                     |
8     | 0      | 0.00       |                                     |
9     | 0      | 0.00       |                                     |


Ejercicio 2)
------------

Implementación de un Baseline Tagger.

Se elige para cada palabra su etiqueta más frecuente observada en entrenamiento.
Para las palabras desconocidas, se devuelve la etiqueta más frecuente observada en entrenamiento.


Ejercicio 3)

Resultados del Baseline Tagger.

* Global Accuracy: 89.01%

* Known Words Accuracy: 95.32%

* Unknown Words Accuracy: 31.80%

#### Confusion Matrix:

La posición (x,y) indica la cantidad de veces que una palabra con el tag correcto de la columna x fue calificado incorrectamente por el tag de la fila y.

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 45    | 143   | 2105  | 2041  | 1935  | 0     | 0     | 297   | 12    |
|**sp** |  11    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
|**da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**vm** |  90    | 0     | 0     | 0     | 198   | 0     | 0     | 0     | 0     | 0     |
|**aq** |  469   | 0     | 0     | 160   | 0     | 1     | 0     | 0     | 29    | 0     |
|**np** |  4     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     |
|**fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**fp **|  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**rg** |  32    | 5     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 46    |
|**cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |