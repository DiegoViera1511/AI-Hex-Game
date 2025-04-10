# Juego de Hex - Jugador Inteligente con Minimax

Este repositorio contiene un jugador inteligente para el juego de Hex que utiliza el algoritmo Minimax con poda alfa-beta para tomar decisiones. El jugador evalúa posiciones usando una función heurística que combina distancias calculadas con Dijkstra y conteo de "puentes".

## Características Principales

- **Algoritmo Minimax**: Búsqueda en árbol de decisiones alternando entre jugador maximizador y minimizador.
- **Poda Alfa-Beta**: Optimización para reducir el número de nodos evaluados.
- **Función de Evaluación Heurística**:
  - **Dijkstra Adaptado**: Calcula el costo mínimo para conectar los lados del jugador.
  - **Conteo de Puentes**: Evalúa posiciones estratégicas adyacentes a piezas propias.
  - **Conteo de Bloqueos**: Evalúa posiciones estratégicas bloqueando uno de los lados objetivo del oponente
- **Manejo de Profundidad**: Ajusta la profundidad de búsqueda según la fase del juego (en el inicio usa una menor profundidad).

## Estrategias
- Si la victoria se obtiene al poner una ficha se aprovecha la oportunidad.
- Para mejor eficiencia al inicio del juego se hace una búsqueda a menor profundidad.
- Si gana el jugador en un estado se retorna un score máximo, si gana el adversario se retorna un score mínimo y si se llega a la máxima profundidad se retorna un score que aumenta si: 
  - el camino del adversario es mas largo 
  - el camino del jugador es mas corto 
  - la cantidad de puentes del jugador es mayor, 
  - la cantidad de puentes del adversario es menor.
  - la cantidad de fichas del jugador en uno de los extremos del adversario es mayor

