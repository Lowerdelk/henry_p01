
# PROYECTO INDIVIDUAL Nº1

¡Bienvenidos al primer proyecto individual de la etapa de labs! En esta ocasión, deberán hacer un trabajo situándose en el rol de un MLOps Engineer.

Estare trabajando con varios CSV que contiene informacion sobre plataformas de streaming.

Tengo que realizar transformaciones, realizar una API con 6 funciones y un modelo de recomendacion.


## **Propuesta de trabajo (requerimientos de aprobación)**

**`Transformaciones`**: Transformaciones a los datos:


+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Reemplazar los valores nulos del campo rating por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

**`Desarrollo API`**:   Propones disponibilizar los datos de la empresa usando el framework ***FastAPI***, generando diferentes endpoints que se consumiran en la API.

Creas 6 funciones (recuerda que deben tener un decorador por cada una (@app.get(‘/’)):



## API Reference

#### get_max_duration

```http
  GET /get_max_duration/{anio}/{plataforma}/{dtype}
Get Max Duration
```

Devuelve la pelicula con mayor duracion segun año y plataforma.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `anio`    | `int`    | **Required**. Año de estreno. |
| `plataforma` | `string` | **Required**. Nombre de la plataforma. |
| `dtype` | `string` | **Required**. Tipo de duracion. |

#### get_score_count

```http
  GET /get_score_count/{plataforma}/{scored}/{anio}
```

Devuelve la cantidad de peliculas segun plataforma, con un score mayor a X en determinado año.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `plataforma`      | `string` | **Required**. Nombre de la plataforma. |
| `scored`      | `float` | **Required**. Puntaje entre 1 y 5. |
| `anio`      | `int` | **Required**. Año de estreno. |

#### get_count_platform

```http
  GET /get_count_platform/{plataforma}
```

Devuelve cantidad de peliculas totales disponibles segun plataforma.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `plataforma`      | `string` | **Required**. Nombre de la plataforma. |

#### get_actor

```http
  GET /get_actor/{plataforma}/{anio}
```

Devuelve actor que mas se repite segun plataforma y año.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `plataforma`      | `string` | **Required**. Nombre de la plataforma. |
| `anio`      | `int` | **Required**. Año de estreno. |

#### prod_per_county

```http
  GET /prod_per_county/{tipo}/{pais}/{anio}
```

Devuelve la cantidad total de contenidos/productos disponibles segun pais y año.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `tipo`      | `string` | **Required**. Tipo de contenido. |
| `pais`      | `string` | **Required**. Nombre del pais de origen. |
| `anio`      | `int` | **Required**. Año de estreno. |

#### get_contents

```http
  GET /get_contents/{rating}
```

Devuelve la cantidad de contenidos/productos disponibles segun clasificacion por edades.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `rating`      | `string` | **Required**. Clasificacion por edades. |

#### get_recomendation

```http
  GET /get_recomendation/{title}
```

Devuelve lista de Python con 5 peliculas/series recomendadas.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. Titulo de la pelicula o serie. |






