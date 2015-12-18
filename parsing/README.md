Práctico 4 - PLN 2015
=====================

Implementación de un Parser de Dependencias Greedy Basado en Transiciones.


### Introducción

Se implementa un Parser de Dependencias, en particular, intentando imitar el modelo voraz
propuesto por MaltParser y su algoritmo *Nivre arc-eager*. http://www.maltparser.org/

El algoritmo se encarga de manipular en cada sentencia a parsear dos estructuras distintas, una pila, con palabras de la oración con posibles nuevas dependencias y un buffer, el cual posee las palabras de la oración todavía no analizadas. Con estas estructuras el algoritmo intenta predecir usando un Modelo basado en historias (History-based model for predicting the next parser action) cual de las cuatros posibles transiciones 4 posibles debe ser aplicada.

Estas posibles acciones son:

* **SHIFT**
* **REDUCE**
* **RIGHT ARC**
* **LEFT ARC** 

Siendo las ultimas dos aquellas que generan nuevas dependencias entre palabras de la oración.

Lo que se intenta lograr en este trabajo es hacer una buena traducción entre Arboles de dependencias
a secuencias de Historias y acciones, de manera que usando un clasificador, se pueda luego deducir acciones que sean nuevamente traducidas a Arboles de dependencia.

En este trabajo solo se intentará generar dependencias no etiquetadas, quedando pendiente el trabajo
de completar el parseo de dependencias etiquetado.


### Herramientas utilizadas en la implementación

Se utlizan las siguientes librerias de python:

* *scikit-learn*: Provee los clasificadores SVM y LR, utilizados en este trabajo. 
Además provee la posibilidad de generar un Pipeline el cual toma como argumentos un Vectorizer de features, y el clasificador, para entrenar y luego hacer la predicción de acciones.

* *feature-forge*: Facilita la implementación de features y la creación del Vectorizer dado como argumento
al Pipeline de scikit-learn.

* *csv*: De esta libreria se utiliza el metodo cvs_reader que se encarga de parsear los datos del corpus
que se encuentran en formato .csv


### Instrucciones para entrenar modelos:

```
python parsing/scripts/train.py -c <classifier> -o <file>
```

* -c: Clasificador a usar:
  * svm: Support vector Machine
  * lr: Logistic Regression
* -o: Archivo de salida con el Parser.


### Instrucciones para evaluar los modelos entrenados:

```
python parsing/scripts/eval.py -i <file>
```

* -i: Archivo con el modelo entrenado.


### Resultados para experimentos realizados con la versión de dependencias del corpus Ancora:

#### SVM:

* Global Accuracy: 64.01%

##### Tiempo de evaluación:


* real    0m34.912s

* user    0m34.699s

* sys     0m0.212s


#### Logistic Regression:

* Global Accuracy: 64.24%

##### Tiempo de evaluación:

* real    0m33.316s

* user    0m33.099s

* sys     0m0.220s

### Recursos utilizados:

Se utiliza el corpus anotado Ancora.

Utilizando las secciones:

* *CESS-CAST-A*, *CESS-CAST-AA*, *CESS-CAST-P*, para entrenamiento.

* *3LB-CAST*, para evaluación.


#### Conclusión

Se pueden apreciar algunas de las ventajas de los metodos data-driven, que es su relativamente bajo tiempo de desarrollo tanto como su gran eficiencia en velocidad de parseo con respecto a los metodos dinámicos, como el algoritmo CKY.

Si bien los resultados obtenidos al experimentar no son tan buenos como se esperan, se cree fuertemente que con una mejor elección de features mejoraría notablemente la Accuracy obtenida.


### Referencia principal utilizada en el trabajo:

[Greedy Transition-Based Dependency Parsing - Stanford NLP Video Lectures by Dan Jurafsky, Christopher Manning](https://class.coursera.org/nlp/lecture/177)

### Referencia adicional:

* http://lrec-conf.org/proceedings/lrec2006/pdf/162_pdf.pdf

* https://spacy.io/blog/parsing-english-in-python

* http://www.maltparser.org/