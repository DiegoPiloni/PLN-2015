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

* Global Accuracy: 89.01%

* Known Words Accuracy: 95.32%

* Unknown Words Accuracy: 31.80%


##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc   |  0     | 45    | 143   | 2105  | 2041  | 1935  | 0     | 0     | 297   | 12    |
|**sp   |  11    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
|**da   |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**vm   |  88    | 0     | 0     | 0     | 183   | 0     | 0     | 0     | 0     | 0     |
|**aq   |  471   | 0     | 0     | 167   | 0     | 1     | 0     | 0     | 29    | 0     |
|**np   |  4     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     |
|**fc   |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**rg** |  32    | 5     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 46    |
|**cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


#### 2-grams:

* Global Accuracy: 92.72%

* Known Words Accuracy: 97.61%

* Unknown Words Accuracy: 48.42%


##### Confusion Matrix

|       |  nc    | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
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

* Global Accuracy: 93.17%

* Known Words Accuracy: 97.67%

* Unknown Words Accuracy: 52.31%


##### Confusion Matrix


|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 2     | 82    | 243   | 439   | 567   | 0     | 0     | 43    | 0     |
|**sp** |  41    | 0     | 0     | 309   | 94    | 47    | 0     | 0     | 58    | 0     |
|**da** |  158   | 14    | 0     | 73    | 70    | 36    | 0     | 0     | 25    | 1     |
|**vm** |  146   | 6     | 7     | 0     | 239   | 77    | 0     | 0     | 24    | 1     |
|**aq** |  339   | 2     | 4     | 197   | 0     | 132   | 0     | 0     | 45    | 0     |
|**np** |  298   | 5     | 29    | 74    | 77    | 0     | 0     | 0     | 31    | 8     |
|**fc** |  23    | 1     | 0     | 59    | 75    | 24    | 0     | 0     | 10    | 0     |
|**fp** |  3     | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 0     | 0     |
|**rg** |  40    | 14    | 0     | 62    | 54    | 52    | 0     | 0     | 0     | 60    |
|**cc** |  7     | 3     | 0     | 12    | 4     | 4     | 0     | 0     | 21    | 0     |

#### 4-grams

* Global Accuracy: 93.14%

* Known Words Accuracy: 97.44%

* Unknown Words Accuracy: 54.16%

##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|**nc** |  0     | 1     | 74    | 241   | 454   | 515   | 0     | 0     | 43    | 0     |
|**sp** |  42    | 0     | 3     | 309   | 93    | 40    | 0     | 0     | 60    | 1     |
|**da** |  137   | 13    | 0     | 70    | 66    | 39    | 0     | 0     | 27    | 1     |
|**vm** |  119   | 5     | 8     | 0     | 259   | 85    | 0     | 0     | 26    | 1     |
|**aq** |  348   | 1     | 4     | 185   | 0     | 126   | 0     | 0     | 51    | 3     |
|**np** |  280   | 5     | 37    | 71    | 65    | 0     | 0     | 0     | 30    | 6     |
|**fc** |  28    | 1     | 1     | 48    | 93    | 21    | 0     | 0     | 7     | 0     |
|**fp** |  6     | 0     | 1     | 0     | 2     | 1     | 0     | 0     | 0     | 0     |
|**rg** |  39    | 16    | 0     | 64    | 61    | 42    | 0     | 0     | 0     | 58    |
|**cc** |  7     | 3     | 0     | 12    | 13    | 11    | 0     | 0     | 29    | 0     |

