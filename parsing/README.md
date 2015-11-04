Práctico 3 - PLN 2015
=====================

Ejercicio 1)
------------

Implementación de un evaluador de parsers donde se calcula tanto Labeled como Unlabeled Precision, 
Recall y F1.

### Para entrenar:

```
tagging/scripts/train.py -m <model> -o <file>
```

* -m: Model to use:
  * flat: Flat trees
  * rbranch: Right branching trees
  * lbranch: Left branching trees

* -o: Archivo de salida con el Tagger.

### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```


### Resultados para Baseline Parsers:

Parsed 1444 sentences

#### Flat:

* Labeled
  * Precision: 99.93%
  * Recall: 14.57%
  * F1: 25.43%
* Unlabeled
  * Precision: 100.00%
  * Recall: 14.58%
  * F1: 25.45%


#### RBranch:

* Labeled
  * Precision: 8.81%
  * Recall: 14.57%
  * F1: 10.98%
* Unlabeled
  * Precision: 8.87%
  * Recall: 14.68%
  * F1: 11.06%

#### LBranch:

* Labeled
  * Precision: 8.81%
  * Recall: 14.57%
  * F1: 10.98%
* Unlabeled
  * Precision: 14.71%
  * Recall: 24.33%
  * F1: 18.33%

Ejercicio 2)
------------

Implementación de un CKY Parser. El cual dada una CFG en Chomsky Normal Form
devuelve el parseo de mayor probabilidad para una oración del lenguaje.

Ejercicio 3)
------------

Implementación de una UPCFG.
Dado un corpus de parsed sents genera una CFG en Chosmky Normal Form.
El parser utilizado es el CKY del Ejercicio 2.

### Para entrenar:

```
tagging/scripts/train.py -m upcfg -o <file>
```

* -o: Archivo de salida con el Tagger.

### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

### Resultados UPCFG:

#### UPCFG

* Labeled
  * Precision: 73.16%
  * Recall: 72.86%
  * F1: 73.01%
* Unlabeled
  * Precision: 75.27%
  * Recall: 74.96%
  * F1: 75.12%

##### Tiempo de evaluación

* real  3m12.866s
* user  3m12.289s
* sys 0m0.572s
