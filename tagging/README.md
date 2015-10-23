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

### Baseline Tagger

### Para entrenar:

```
tagging/scripts/train.py -m base -o <file>
```

* -o: Archivo de salida con el Tagger.

### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

* -i: Archivo con el Baseline Tagger



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

### Para entrenar:

```
tagging/scripts/train.py -m mlhmm -n <n> -o <file>
```

* -n: Modelo de n-gramas
* -o: Archivo de salida con el Tagger.

### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

* -i: Archivo con el MLHMM Tagger


### Resultados del MLHMM:


#### 1-grams:

* Global Accuracy: 89.01%

* Known Words Accuracy: 95.32%

* Unknown Words Accuracy: 31.80%

##### Tiempo de evaluación:

* real    0m7.090s

* user    0m6.937s

* sys     0m0.124s

##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|**nc** |  0     | 45    | 143   | 2105  | 2041  | 1935  | 0     | 0     | 297   | 12    |
|**sp** |  11    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
|**da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**vm** |  88    | 0     | 0     | 0     | 183   | 0     | 0     | 0     | 0     | 0     |
|**aq** |  471   | 0     | 0     | 167   | 0     | 1     | 0     | 0     | 29    | 0     |
|**np** |  4     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     |
|**fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
|**rg** |  32    | 5     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 46    |
|**cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


#### 2-grams:

* Global Accuracy: 92.72%

* Known Words Accuracy: 97.61%

* Unknown Words Accuracy: 48.42%

##### Tiempo de evaluación:

* real    0m13.513s

* user    0m13.408s

* sys     0m0.100s

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

##### Tiempo de evaluación:

* real    0m50.929s

* user    0m50.689s

* sys     0m0.248s

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

##### Tiempo de evaluación:

* real    4m40.195s

* user    4m39.519s

* sys     0m0.776s

##### Confusion Matrix

|       | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|-------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
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


Ejercicio 6)
------------

Implementación de features para utilizar en el MEMM (Maximum Entropy Markov Model)
del ejercicio 7.

Ejercicio 7)
------------

Implementación de un MEMM (Maximum Entropy Markov Model) para realizar el tagging de oraciones.
Se utiliza un formato de pipeline, usando scikit-learn, donde se entrena un vectorizador con los
features del práctico 6, más un clasificador, para predecir el tagging de las oraciones, donde se utiliza beam-inference con k=1.

Se testea con 3 clasificadores distintos:

* Logistic Regression

* Multinomial Naive Bayes

* Linear SVC

A continuación se presentan los resultados para cada uno de estos clasificadores.

### Logistic Regression

#### Para entrenar:

```
tagging/scripts/train.py -m memm -n <n> -c lr -o <file>
```

* -n: Modelo de n-gramas
* -o: Archivo de salida con el Tagger.

#### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

* -i: Archivo con el MEMM Tagger


#### Resultados de Logistic Regression:

#### 1-grams

* Global Accuracy: 92.70%

* Known Words Accuracy: 95.28%

* Unknown Words Accuracy: 69.32%

##### Tiempo de evaluación:

* real    0m29.870s

* user    0m29.651s

* sys 0m0.188s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 11    | 118   | 393   | 672   | 238   | 0     | 0     | 48    | 1     |
| **sp** |  9     | 0     | 0     | 1     | 5     | 2     | 0     | 0     | 16    | 1     |
| **da** |  6     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
| **vm** |  497   | 31    | 4     | 0     | 546   | 87    | 0     | 0     | 204   | 13    |
| **aq** |  535   | 41    | 0     | 494   | 0     | 23    | 0     | 0     | 292   | 2     |
| **np** |  115   | 0     | 4     | 167   | 44    | 0     | 0     | 0     | 32    | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  16    | 4     | 0     | 0     | 2     | 0     | 0     | 0     | 0     | 44    |
| **cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |

##### Confusion Matrix Plot:

![LR1](https://github.com/DiegoPiloni/PLN-2015/tree/practico2/tagging/ConfMatr/lr_1.png "Logistic Regression 1")

#### 2-grams

* Global Accuracy: 91.99%

* Known Words Accuracy: 94.55%

* Unknown Words Accuracy: 68.75%

##### Tiempo de evaluación:

* real    0m24.025s

* user    0m23.912s

* sys 0m0.117s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 25    | 118   | 534   | 913   | 244   | 0     | 0     | 166   | 3     |
| **sp** |  8     | 0     | 0     | 1     | 5     | 2     | 0     | 0     | 16    | 1     |
| **da** |  6     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
| **vm** |  543   | 34    | 3     | 0     | 539   | 88    | 0     | 0     | 207   | 13    |
| **aq** |  713   | 33    | 0     | 566   | 0     | 16    | 0     | 0     | 176   | 1     |
| **np** |  116   | 0     | 4     | 170   | 44    | 0     | 0     | 0     | 32    | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  11    | 4     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 45    |
| **cc** |  0     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |

##### Confusion Matrix Plot:

![LR2](https://github.com/DiegoPiloni/PLN-2015/tree/practico2/tagging/ConfMatr/lr_2.png "Logistic Regression 2")

#### 3-grams

* Global Accuracy: 92.18%

* Known Words Accuracy: 94.72%

* Unknown Words Accuracy: 69.19%

##### Tiempo de evaluación:

* real    0m23.847s

* user    0m23.723s

* sys 0m0.132s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 20    | 119   | 524   | 874   | 254   | 0     | 0     | 116   | 5     |
| **sp** |  10    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 16    | 1     |
| **da** |  6     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
| **vm** |  508   | 37    | 3     | 0     | 523   | 80    | 0     | 0     | 258   | 12    |
| **aq** |  696   | 36    | 0     | 534   | 0     | 19    | 0     | 0     | 181   | 3     |
| **np** |  113   | 0     | 4     | 168   | 44    | 0     | 0     | 0     | 32    | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  11    | 4     | 0     | 0     | 3     | 0     | 0     | 0     | 0     | 45    |
| **cc** |  0     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


##### Confusion Matrix Plot:

![LR3](https://github.com/DiegoPiloni/PLN-2015/tree/practico2/tagging/ConfMatr/lr_3.png "Logistic Regression 3")

#### 4-grams

* Global Accuracy: 92.23%

* Known Words Accuracy: 94.72%

* Unknown Words Accuracy: 69.63%

##### Tiempo de evaluación:

* real    0m33.623s

* user    0m33.384s

* sys 0m0.212s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 18    | 118   | 555   | 884   | 258   | 0     | 0     | 124   | 4     |
| **sp** |  10    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 16    | 1     |
| **da** |  4     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
| **vm** |  443   | 38    | 3     | 0     | 494   | 77    | 0     | 0     | 248   | 12    |
| **aq** |  704   | 35    | 0     | 538   | 0     | 21    | 0     | 0     | 192   | 3     |
| **np** |  113   | 0     | 4     | 171   | 44    | 0     | 0     | 0     | 32    | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  11    | 4     | 0     | 0     | 4     | 0     | 0     | 0     | 0     | 44    |
| **cc** |  0     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |

##### Confusion Matrix Plot:

![LR4](https://github.com/DiegoPiloni/PLN-2015/tree/practico2/tagging/ConfMatr/lr_4.png "Logistic Regression 4")

### Linear SVC

#### Para entrenar:

```
tagging/scripts/train.py -m memm -n <n> -c lsvc -o <file>
```

* -n: Modelo de n-gramas
* -o: Archivo de salida con el Tagger.

#### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

* -i: Archivo con el MEMM Tagger


#### Resultados de Linear SVC:


#### 1-gram

* Global Accuracy: 94.43%

* Known Words Accuracy: 97.04%

* Unknown Words Accuracy: 70.82%

##### Tiempo de evaluación:

* real    0m27.473s

* user    0m27.210s

* sys 0m0.232s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    | cc    |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 5     | 86    | 251   | 526   | 245   | 0     | 0     | 38    | 1     |
| **sp** |  10    | 0     | 0     | 1     | 6     | 3     | 0     | 0     | 17    | 1     |
| **da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **vm** |  331   | 11    | 1     | 0     | 388   | 59    | 0     | 0     | 73    | 10    |
| **aq** |  388   | 16    | 0     | 368   | 0     | 19    | 0     | 0     | 151   | 0     |
| **np** |  111   | 0     | 4     | 110   | 33    | 0     | 0     | 0     | 3     | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  19    | 4     | 0     | 0     | 10    | 0     | 0     | 0     | 0     | 45    |
| **cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |

#### 2-grams

* Global Accuracy: 94.29%

* Known Words Accuracy: 96.91%

* Unknown Words Accuracy: 70.57%

##### Tiempo de evaluación:

* real    0m28.431s

* user    0m28.228s

* sys 0m0.172s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 10    | 86    | 344   | 589   | 248   | 0     | 0     | 100   | 1     |
| **sp** |  10    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
| **da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 1     | 0     |
| **vm** |  344   | 11    | 1     | 0     | 375   | 57    | 0     | 0     | 72    | 10    |
| **aq** |  477   | 10    | 0     | 357   | 0     | 17    | 0     | 0     | 95    | 0     |
| **np** |  110   | 0     | 4     | 112   | 34    | 0     | 0     | 0     | 3     | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  12    | 4     | 0     | 0     | 9     | 0     | 0     | 0     | 0     | 45    |
| **cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |

#### 3-grams

* Global Accuracy: 94.40%

* Known Words Accuracy: 96.94%

* Unknown Words Accuracy: 71.38%


##### Tiempo de evaluación:

* real    0m33.176s

* user    0m32.892s

* sys 0m0.260s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 10    | 86    | 323   | 571   | 241   | 0     | 0     | 79    | 3     |
| **sp** |  10    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
| **da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **vm** |  319   | 11    | 1     | 0     | 349   | 63    | 0     | 0     | 94    | 5     |
| **aq** |  490   | 10    | 0     | 371   | 0     | 19    | 0     | 0     | 98    | 5     |
| **np** |  106   | 0     | 4     | 112   | 32    | 0     | 0     | 0     | 3     | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  12    | 4     | 0     | 0     | 8     | 0     | 0     | 0     | 0     | 47    |
| **cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 20    | 0     |

#### 4-grams

* Global Accuracy: 94.46%

* Known Words Accuracy: 96.96%

* Unknown Words Accuracy: 71.81%


##### Tiempo de evaluación:

* real    0m38.093s

* user    0m37.863s

* sys 0m0.212s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 10    | 87    | 348   | 579   | 242   | 0     | 0     | 78    | 3     |
| **sp** |  10    | 0     | 0     | 1     | 5     | 3     | 0     | 0     | 17    | 1     |
| **da** |  1     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **vm** |  275   | 13    | 0     | 0     | 343   | 61    | 0     | 0     | 99    | 6     |
| **aq** |  489   | 8     | 0     | 356   | 0     | 19    | 0     | 0     | 95    | 4     |
| **np** |  106   | 0     | 4     | 112   | 32    | 0     | 0     | 0     | 3     | 1     |
| **fc** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **fp** |  0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 0     |
| **rg** |  12    | 4     | 0     | 0     | 8     | 0     | 0     | 0     | 0     | 47    |
| **cc** |  1     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 21    | 0     |


### Multinomial Naive Bayes

#### Para entrenar:

```
tagging/scripts/train.py -m memm -n <n> -c mnb -o <file>
```

* -n: Modelo de n-gramas
* -o: Archivo de salida con el Tagger.

#### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

* -i: Archivo con el MEMM Tagger


#### Resultados de Multinomial Naive Bayes:


#### 1-gram

* Global Accuracy: 82.18%

* Known Words Accuracy: 85.85%

* Unknown Words Accuracy: 48.89%

##### Tiempo de evaluación:

* real    16m59.685s

* user    16m59.869s

* sys 0m0.772s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 10    | 107   | 479   | 1324  | 350   | 0     | 2     | 268   | 12    |
| **sp** |  406   | 0     | 0     | 625   | 1234  | 140   | 0     | 1     | 405   | 17    |
| **da** |  251   | 59    | 0     | 371   | 126   | 468   | 1     | 8     | 285   | 129   |
| **vm** |  98    | 0     | 0     | 0     | 302   | 21    | 0     | 1     | 154   | 1     |
| **aq** |  77    | 1     | 0     | 69    | 0     | 1     | 0     | 0     | 107   | 1     |
| **np** |  111   | 43    | 5     | 26    | 18    | 0     | 0     | 0     | 7     | 104   |
| **fc** |  10    | 1     | 0     | 60    | 46    | 1     | 0     | 0     | 32    | 0     |
| **fp** |  0     | 1     | 0     | 5     | 4     | 0     | 0     | 0     | 3     | 0     |
| **rg** |  2     | 2     | 0     | 0     | 0     | 0     | 0     | 0     | 0     | 46    |
| **cc** |  0     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 14    | 0     |

#### 2-grams

* Global Accuracy: 76.46%

* Known Words Accuracy: 80.41%

* Unknown Words Accuracy: 40.68%

##### Tiempo de evaluación:

* real    34m15.863s

* user    34m7.486s

* sys 0m0.949s


##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 39    | 127   | 525   | 1113  | 332   | 4     | 22    | 263   | 57    |
| **sp** |  1087  | 0     | 7     | 944   | 1396  | 288   | 0     | 0     | 413   | 20    |
| **da** |  724   | 211   | 0     | 758   | 394   | 536   | 5     | 76    | 449   | 407   |
| **vm** |  287   | 9     | 0     | 0     | 378   | 41    | 1     | 12    | 215   | 11    |
| **aq** |  200   | 1     | 0     | 173   | 0     | 2     | 0     | 0     | 133   | 3     |
| **np** |  123   | 49    | 4     | 37    | 17    | 0     | 0     | 2     | 13    | 110   |
| **fc** |  51    | 3     | 0     | 153   | 87    | 12    | 0     | 0     | 66    | 3     |
| **fp** |  1     | 1     | 0     | 6     | 4     | 0     | 0     | 0     | 2     | 0     |
| **rg** |  2     | 1     | 0     | 0     | 1     | 0     | 0     | 0     | 0     | 49    |
| **cc** |  0     | 0     | 0     | 0     | 0     | 1     | 0     | 0     | 12    | 0     |

#### 3-grams

* Global Accuracy: 71.47%

* Known Words Accuracy: 75.09%

* Unknown Words Accuracy: 38.59%

##### Tiempo de evaluación:

* real    30m51.393s

* user    30m51.061s

* sys 0m0.432s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 152   | 146   | 774   | 1267  | 399   | 28    | 42    | 332   | 111   |
| **sp** |  1092  | 0     | 34    | 1094  | 1281  | 299   | 0     | 2     | 511   | 41    |
| **da** |  887   | 509   | 0     | 1080  | 531   | 595   | 7     | 164   | 570   | 421   |
| **vm** |  342   | 33    | 2     | 0     | 360   | 63    | 4     | 18    | 233   | 11    |
| **aq** |  500   | 2     | 11    | 277   | 0     | 6     | 0     | 1     | 234   | 8     |
| **np** |  124   | 45    | 5     | 42    | 15    | 0     | 0     | 0     | 17    | 116   |
| **fc** |  80    | 18    | 4     | 175   | 77    | 9     | 0     | 0     | 61    | 3     |
| **fp** |  25    | 0     | 0     | 9     | 15    | 0     | 0     | 0     | 6     | 0     |
| **rg** |  6     | 1     | 0     | 4     | 9     | 0     | 0     | 0     | 0     | 43    |
| **cc** |  0     | 0     | 0     | 0     | 1     | 1     | 0     | 1     | 15    | 0     |


#### 4-grams

* Global Accuracy: 68.20%

* Known Words Accuracy: 71.31%

* Unknown Words Accuracy: 40.01%

##### Tiempo de evaluación:

* real    30m40.758s
* user    30m38.697s
* sys 0m0.777s

##### Confusion Matrix

|        | nc     | sp    | da    | vm    | aq    | np    | fc    | fp    | rg    |  cc   |
|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **nc** |  0     | 202   | 142   | 939   | 1261  | 419   | 28    | 85    | 362   | 233   |
| **sp** |  969   | 0     | 41    | 1155  | 1314  | 310   | 4     | 14    | 581   | 75    |
| **da** |  786   | 548   | 0     | 1169  | 484   | 558   | 35    | 173   | 624   | 350   |
| **vm** |  277   | 51    | 0     | 0     | 269   | 78    | 25    | 28    | 245   | 31    |
| **aq** |  781   | 4     | 29    | 447   | 0     | 11    | 0     | 1     | 346   | 23    |
| **np** |  192   | 52    | 20    | 88    | 51    | 0     | 0     | 6     | 54    | 128   |
| **fc** |  135   | 29    | 15    | 181   | 77    | 2     | 0     | 0     | 60    | 4     |
| **fp** |  74    | 35    | 11    | 63    | 61    | 3     | 0     | 0     | 23    | 1     |
| **rg** |  12    | 1     | 0     | 9     | 24    | 2     | 0     | 0     | 0     | 46    |
| **cc** |  15    | 2     | 0     | 0     | 34    | 1     | 0     | 2     | 35    | 0     |
