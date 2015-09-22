Ejercicio 2
===========

Para poder calcular las probabilidades condicionales en un modelo de n-gramas, agregué internamente en la representación de sentencias, n-1 símbolos de inicio de sentencia, y un símbolo de fin de sentencia.
Esta representación es usada en el método init de la clase NGram, para poder guardar así los counts de los n-gramas y n-1 gramas de cada sentencia.
Luego para calcular la probabilidad de una sentencia, se utiliza nuevamente esta representación, para poder calcular la probabilidad condicional de un token dados n-1 tokens previos.

Otros detalles menores que tuve que tener en cuenta en la implementación:

* Manipular correctamente el caso en que en el cálculo de la probabilidad de una sentencia el denominador de una de las probabilidades condicionales sea 0, lo que generaría una excepción de división por cero. La manera de solucionar esto es notar que esto sucede únicamente en el caso en que la probabilidad anterior alla dado cero, por lo que se puede evitar este problema sin modificar el resultado final, de manera que al encontrar un factor cuyo resultado es 0 terminar el calculo y dar como resultado 0.

* Manipular el caso en que se desea calcular la log_prob de una sentencia con probabilidad 0. Para resolver esto, se devuelve usando f una representación de menos infinito.


Para entrenar:
--------------
```
train.py -n <n> [-m ngram] -o <file> [-g <file>]
```

* -n: Orden del modelo

* -o: Archivo de salida con el Modelo.

* -g: Archivo de salida con Generador.


Para evaluar:
-------------

```
eval.py -i <file>
```

* -i: Archivo con el Modelo


Ejercicio 3
===========

Implementé la clase NGramGenerator. En ella se guardan las probabilidades condicionales de cada palabra dado un
n-1 grama fijo. Además se cuentan con estas probabilidades ordenadas de manera descendiente lo cual
hará más eficiente poder generar de manera aleatoria una palabra dado un n-1 grama fijo.

Metodos implementados:
----------------------


* generate_token(previus_tokens): Dado un n-1 grama (previus_tokens), se genera de manera aleatoria un
token. Para ello utilicé las probabilidades condicionales ordenadas decrecientemente y luego usando
el método de transformada inversa, generando un número aleatorio, se escoge de acuerdo a la distribución
condicional un token.


* generate_sent(): Genero tokens comenzando de n-1 simbolos de comienzo, hasta que se encuentre
un token de fin de sentencia. En ese caso devuelvo la oración generada.

Para generar:
-------------

```
generate.py -s <n> -i <file>
```

* -s: Cantidad de oraciones a generar.

* -i Archivo con el generador (Archivo creado con train.py)


Sentencias generadadas (Austen-Emma)
------------------------------------

| ngram | sents                                                                                                                                                                                                                                                                                                                                                                                            |
|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | dream that do , , enough in at . embarrassment But never s I the Abbey                                                                                                                                                                                                                                                                                                                           |
|       |  be and It to been proof you to ." nothing be the my They ,                                                                                                                                                                                                                                                                                                                                      |
|       | disposed Yes dare on to her in Mr remove reply very " to herself himself hastily of his                                                                                                                                                                                                                                                                                                          |
|       | solicitous sure winter                                                                                                                                                                                                                                                                                                                                                                           |
| 2     | She feared would be long .                                                                                                                                                                                                                                                                                                                                                                       |
|       | The decree is the meanwhile , but Mr . Elton .                                                                                                                                                                                                                                                                                                                                                   |
|       | It seemed to indulge her daughter , nor resentment .                                                                                                                                                                                                                                                                                                                                             |
|       | " Well --( but it . Weston , to think her with only wanted on reaching home very interesting to prevent it ; for his particular friend was rather surprize .-- On that is the moment , when their bringing a " Your word , of all that she knew I recollect any happiness at Hartfield after he would give up by himself , and do you answer !-- What blindness to her that he had due decorum . |
| 3     | Do you imagine such a change to her !"                                                                                                                                                                                                                                                                                                                                                           |
|       | " I do not think any possible good .                                                                                                                                                                                                                                                                                                                                                             |
|       | Mr . Knightley saw no fault in Mr . Woodhouse had treated her all you describe .                                                                                                                                                                                                                                                                                                                 |
|       | For half an hour or two )-- but it was .                                                                                                                                                                                                                                                                                                                                                         |
| 4     | When the gloves were bought , and they looked it over together .-- Emma took the opportunity of whispering ,                                                                                                                                                                                                                                                                                     |
|       | You make the best of her way by a short cut back to Highbury .                                                                                                                                                                                                                                                                                                                                   |
|       | Miss Nash , that as he was sleeping on the sofa , removing to a seat by her sister , and giving her the opportunity of pleasing some one worth having ; I ought not to have failed of .                                                                                                                                                                                                          |
|       |                                                                                                                                                                                                                                                                                                                                                                                                  |

Ejercicio 4
===========

Complementando la clase NGram, agregué un nuevo atributo en el init, para guardar el largo del vocabulario que servirá para calcular la nueva probabilidad condicional.

Modifique el método cond_prob, de manera que se aplique allí el add-one smoothing.

Agregué un metodo V(), el cual retorna el tamaño del vocabulario.

Resultados Perplexity:
----------------------

| n | Perplexity |
|---|------------|
| 1 | 570        |
| 2 | 1007       |
| 3 | 4590       |
| 4 | 6975       |


Para entrenar:
--------------
```
train.py -n <n> -m addone -o <file>
```

* -n: Orden del modelo

* -o: Archivo de salida con el Modelo.


Para evaluar:
-------------

```
eval.py -i <file>
```

* -i: Archivo con el Modelo


Ejercicio 5
===========

Implementé en la super clase LanguageModel tres nuevos métodos:

* log_probability(sents)

* cross_entropy(sents)

* perplexity(sents)

Implementé el script eval que permite tomar el último 10% del training corpus como test-data, y calcular con ese conjunto de test la perplejidad del modelo.


Ejercicio 6
===========

Implementé la clase InterpolatedNGram.

Algunos métodos destacados:

* best_gamma(): Se encarga de hacer un barrido para encontrar el gamma que de mejor perplexity
a los datos held_out.

* lambdas(tokens): Dado un n-1 grama devuelva una lista de los n lambdas correspondientes al
método de interpolación utilizando el parametro gamma.

* cond_prob_ML(token, prev_tokens): Devuelve maximum-likelihood estimation.

* cond_prob(token, prev_tokens): La probabilidad_condicional definida por el método de interpolación.

Resultados Perplexity:
----------------------

| n | Perplexity |
|---|------------|
| 1 | 575        |
| 2 | 199        |
| 3 | 190        |
| 4 | 190        |


Para entrenar:
--------------
```
train.py -n <n> -m interpolated -o <file>
```

* -n: Orden del modelo

* -o: Archivo de salida con el Modelo.


Para evaluar:
-------------

```
eval.py -i <file>
```

* -i: Archivo con el Modelo


Ejercicio 7
===========

Implemeté la clase BackOffNGram.

Como datos importantes se guardo al hacer init de la instancia, los conjuntos A,
los alpha, y denom, para luego mejorar la eficiencia del cálculo recursivo de 
cond_prob.

Resultados Perplexity:
----------------------

| n | Perplexity |
|---|------------|
| 1 | 575        |
| 2 | 166        |
| 3 | 149        |
| 4 | 163        |


Para entrenar:
--------------
```
train.py -n <n> -m backoff -o <file>
```

* -n: Orden del modelo

* -o: Archivo de salida con el Modelo.


Para evaluar:
-------------

```
eval.py -i <file>
```

* -i: Archivo con el Modelo