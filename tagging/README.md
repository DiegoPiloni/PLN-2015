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
------------

#### Resultados del Baseline Tagger.

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
|**fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**rg** |  32    | 5     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 46    |
|**cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


Ejercicio 4)
------------

Implementación de un HMM usando el algoritmo de Viterbi para encontrar el mejor tagging de una sentencia.

Ejercicio 5)
------------

Implementación de una MLHMM. Donde el HMM utilizado es el implementado en el ejercicio 4.

### Resultados del MLHMM:

#### 1-grams:

* Global Accuracy: 86.74%

* Known Words Accuracy: 94.29%

* Unknown Words Accuracy: 18.24%

##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 17    | 0     | 247   | 221   | 155   | 0     | 0     | 57    | 1     |
|**sp** |  10    | 0     | 0     | 1     | 0     | 3     | 0     | 0     | 17    | 0     |
|**da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**vm** |  113   | 0     | 0     | 0     | 154   | 0     | 0     | 0     | 0     | 0     |
|**aq** |  3638  | 28    | 143   | 2040  | 0     | 1779  | 0     | 0     | 245   | 11    |
|**np** |  4     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     |
|**fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**rg** |  39    | 11    | 0     | 1     | 19    | 0     | 0     | 0     | 0     | 46    |
|**cc** |  1     | 14    | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


#### 2-grams:

* Global Accuracy: 92.72%
* Known Words Accuracy: 97.61%
* Unknown Words Accuracy: 48.42%

##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 3     | 69    | 198   | 418   | 470   | 0     | 0     | 32    | 0     |
|**sp** |  69    | 0     | 4     | 339   | 146   | 51    | 0     | 0     | 65    | 1     |
|**da** |  168   | 13    | 0     | 86    | 98    | 37    | 0     | 0     | 25    | 0     |
|**vm** |  176   | 5     | 8     | 0     | 300   | 90    | 0     | 0     | 43    | 1     |
|**aq** |  344   | 1     | 1     | 195   | 0     | 148   | 0     | 0     | 51    | 0     |
|**np** |  471   | 4     | 40    | 120   | 149   | 0     | 0     | 0     | 68    | 10    |
|**fc** |  41    | 1     | 0     | 31    | 86    | 35    | 0     | 0     | 1     | 0     |
|**fp** |  1     | 0     | 0     | 1     | 4     | 2     | 0     | 0     | 0     | 0     |
|**rg** |  44    | 16    | 0     | 57    | 53    | 23    | 0     | 0     | 0     | 51    |
|**cc** |  2     | 4     | 0     | 2     | 1     | 1     | 0     | 0     | 22    | 0     |


#### 3-grams:

* Global Accuracy: 91.85%

* Known Words Accuracy: 97.18%

* Unknown Words Accuracy: 43.51%

##### Confusion Matrix:

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 2     | 72    | 278   | 502   | 605   | 0     | 0     | 47    | 0     |
|**sp** |  68    | 0     | 1     | 300   | 144   | 46    | 0     | 0     | 59    | 0     |
|**da** |  214   | 14    | 0     | 93    | 87    | 65    | 0     | 0     | 30    | 1     |
|**vm** |  204   | 3     | 10    | 0     | 246   | 91    | 0     | 0     | 22    | 1     |
|**aq** |  436   | 1     | 6     | 196   | 0     | 146   | 0     | 0     | 41    | 0     |
|**np** |  254   | 4     | 24    | 81    | 76    | 0     | 0     | 0     | 29    | 11    |
|**fc** |  55    | 1     | 1     | 54    | 131   | 34    | 0     | 0     | 9     | 0     |
|**fp** |  1     | 0     | 0     | 3     | 4     | 4     | 0     | 0     | 0     | 0     |
|**rg** |  74    | 14    | 0     | 87    | 70    | 85    | 0     | 0     | 0     | 61    |
|**cc** |  6     | 7     | 0     | 9     | 3     | 6     | 0     | 0     | 28    | 0     |

#### 4-grams

* Global Accuracy: 90.74%

* Known Words Accuracy: 96.59%

* Unknown Words Accuracy: 37.70%

##### Confusion Matrix:

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 7     | 51    | 245   | 426   | 479   | 0     | 0     | 24    | 0     |
|**sp** |  89    | 0     | 0     | 290   | 200   | 77    | 0     | 0     | 67    | 0     |
|**da** |  211   | 11    | 0     | 100   | 74    | 136   | 0     | 0     | 27    | 0     |
|**vm** |  183   | 4     | 6     | 0     | 246   | 94    | 0     | 0     | 19    | 1     |
|**aq** |  453   | 0     | 6     | 224   | 0     | 121   | 0     | 0     | 46    | 0     |
|**np** |  205   | 4     | 25    | 64    | 58    | 0     | 0     | 0     | 21    | 9     |
|**fc** |  52    | 2     | 2     | 67    | 133   | 39    | 0     | 0     | 5     | 0     |
|**fp** |  10    | 0     | 1     | 7     | 4     | 9     | 0     | 0     | 0     | 0     |
|**rg** |  78    | 15    | 1     | 91    | 99    | 79    | 0     | 0     | 0     | 54    |
|**cc** |  24    | 6     | 3     | 28    | 25    | 19    | 0     | 0     | 32    | 0     |

