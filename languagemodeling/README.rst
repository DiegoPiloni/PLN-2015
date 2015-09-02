Ejercicio 1
===========

Para poder calcular las probabilidades condicionales en un modelo de n-gramas, agregué internamente en la representación de sentencias, n&minus;1 símbolos de inicio de sentencia, y un símbolo de fin de sentencia.
Esta representación es usada en el método init de la clase NGram, para poder guardar así los counts de los n-gramas y n&minus;1 gramas de cada sentencia.
Luego para calcular la probabilidad de una sentencia, se utiliza nuevamente esta representación, para poder calcular la probabilidad condicional de un token dados n&minus;1 tokens previos.

Otros detalles menores que tuve que tener en cuenta en la implementación:

* Manipular correctamente el caso en que en el cálculo de la probabilidad de una sentencia el denominador de una de las probabilidades condicionales sea 0, lo que generaría una excepción de división por cero. La manera de solucionar esto es notar que esto sucede únicamente en el caso en que la probabilidad anterior alla dado cero, por lo que se puede evitar este problema sin modificar el resultado final, de manera que al encontrar un factor cuyo resultado es 0 terminar el calculo y dar como resultado 0.

* Manipular el caso en que se desea calcular la log_prob de una sentencia con probabilidad 0. Para resolver esto, se devuelve usando f una representación de menos infinito.

Ejercicio 2
===========

Implementé la clase NGramGenerator. En ella se guardan las probabilidades condicionales de cada palabra dado un
n&minus;1 grama fijo. Además se cuentan con estas probabilidades ordenadas de manera descendiente lo cual
hará más eficiente poder generar de manera aleatoria una palabra dado un n&minus;1 grama fijo.

Metodos implementados:
----------------------


* generate_token(previus_tokens): Dado un n-1 grama (previus_tokens), se genera de manera aleatoria un
token. Para ello utilicé las probabilidades condicionales ordenadas decrecientemente y luego usando
el método de transformada inversa, generando un número aleatorio, se escoge de acuerdo a la distribución
condicional un token.


* generate_sent(): Genero tokens comenzando de n&minus;1 simbolos de comienzo, hasta que se encuentre
un token de fin de sentencia. En ese caso devuelvo la oración generada.
