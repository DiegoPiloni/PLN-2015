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

### Test de ambiguedad:

Realice un test de ambiguedad para ver que el parser resolviera correctamente 
los casos de ambiguedad.

Dada la siguiente PCFG:

| Producciones    | Probs. |
|-----------------|--------|
|VP -> Vt NP      | [0.75] |
|VP -> VP PP      | [0.25] |
|NP -> DT NN      | [0.8]  |
|NP -> NP PP      | [0.2]  |
|PP -> IN NP      | [1.0]  |
|Vt -> 'saw'      | [1.0]  |
|NN -> 'telescope'| [0.2]  |
|NN -> 'dog'      | [0.8]  |
|DT -> 'the'      | [1.0]  |
|IN -> 'with'     | [1.0]  |

Se analiza y resuelve correctamente entre las dos siguientes posibilidades:

#### Arbol 1

![T1](https://github.com/DiegoPiloni/PLN-2015/raw/practico3/parsing/Images/t1 "Arbol 1")

#### Arbol 2

![T2](https://github.com/DiegoPiloni/PLN-2015/raw/practico3/parsing/Images/t2 "Arbol 2")

Donde se elige el Arbol 1, ya que es el que tiene mayor probabilidad con respecto a la gramática dada.
Notar que solo difieren en el uso de una producción:

En el arbol 1 se utiliza: VP -> VP PP, con probabilidad 0.25

Mientras en el arbol 2 se utiliza: NP -> NP PP, con probabilidad 0.2

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

Ejercicio 4)
------------

Posibilidad de pasar como parámetro al entrenar el orden de Markovización Horizontal
para la UPCFG del ejercicio 3.

### Para entrenar:

```
tagging/scripts/train.py -m upcfg -n <n> -o <file>
```
* -n: Orden de Markovización Horizontal.
* -o: Archivo de salida con el Tagger.

### Para evaluar:

```
tagging/scripts/eval.py -i <file>
```

Se evaluan las mismas sentencias que en el ejercicio 3 con distintos valores de orden.

### Resultados:

#### UPCFG - Orden de Markovización Horizontal: 0

* Labeled
  * Precision: 70.25% 
  * Recall: 70.02% 
  * F1: 70.14% 
* Unlabeled
  * Precision: 72.11% 
  * Recall: 71.88% 
  * F1: 72.00% 

#### UPCFG - Orden de Markovización Horizontal: 1

* Labeled
  * Precision: 74.71% 
  * Recall: 74.62% 
  * F1: 74.66% 
* Unlabeled
  * Precision: 76.58% 
  * Recall: 76.48% 
  * F1: 76.53% 

#### UPCFG - Orden de Markovización Horizontal: 2

* Labeled
  * Precision: 74.78% 
  * Recall: 74.26% 
  * F1: 74.52% 
* Unlabeled
  * Precision: 76.70% 
  * Recall: 76.17% 
  * F1: 76.43%

#### UPCFG - Orden de Markovización Horizontal: 3

* Labeled
  * Precision: 74.01% 
  * Recall: 73.37% 
  * F1: 73.69% 
* Unlabeled
  * Precision: 76.17% 
  * Recall: 75.51% 
  * F1: 75.84%
