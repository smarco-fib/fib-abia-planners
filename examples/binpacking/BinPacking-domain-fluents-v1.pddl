(define (domain BinPackingFluents)
  (:requirements :adl :typing :fluents)

  (:types paquete contenedor - object
  )           

  (:predicates
   (colocadoEn ?p - paquete ?c - contenedor)
   (colocado ?p - paquete)
  )

  (:functions
    (contenedoresOcupados) 
    (altura ?p - paquete)
    (alturaLibre ?c - contenedor)
  )

  (:action colocar_paquete
    :parameters (?p - paquete ?c - contenedor)
    :precondition (and (not (colocado ?p)) 
                       (>= (alturaLibre ?c) (altura ?p))
                   )    
    :effect (and (when (= (alturaLibre ?c) 10) 
                       (increase (contenedoresOcupados) 1)
                 ) 
                 (decrease (alturaLibre ?c) (altura ?p)) 
                 (colocado ?p) (colocadoEn ?p ?c)
            )
  )
)