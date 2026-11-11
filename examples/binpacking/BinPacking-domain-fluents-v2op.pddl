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

  ; (:action mover_paquete
  ;   :parameters (?p - paquete ?c1 - contenedor ?c2 - contenedor)
  ;   :precondition (and (colocadoEn ?p ?c1) 
  ;                      (>= (alturaLibre ?c2) (altura ?p))
  ;                  )    
  ;   :effect (and (increase (alturaLibre ?c1) (altura ?p))
  ;                (decrease (alturaLibre ?c2) (altura ?p))
  ;                (when (= (alturaLibre ?c1) 10) 
  ;                      (decrease (contenedoresOcupados) 1)
  ;                )  
  ;                (not (colocadoEn ?p ?c1)) (colocadoEn ?p ?c2)
  ;           )
  ; )

  (:action intercambiar_paquete
    :parameters (?p1  - paquete ?p2 - paquete ?c1 - contenedor ?c2 - contenedor)
    :precondition (and (colocadoEn ?p1 ?c1) (colocadoEn ?p2 ?c2)
                       (>= (alturaLibre ?c1) (- (altura ?p2) (altura ?p1)))
                       (>= (alturaLibre ?c2) (- (altura ?p1) (altura ?p2)))
                   )    
    :effect (and (increase (alturaLibre ?c1) (altura ?p1))
                 (decrease (alturaLibre ?c2) (altura ?p1))
                 (increase (alturaLibre ?c2) (altura ?p2))                  
                 (decrease (alturaLibre ?c1) (altura ?p2))
                 (not (colocadoEn ?p1 ?c1)) (colocadoEn ?p1 ?c2)
                 (not (colocadoEn ?p2 ?c2)) (colocadoEn ?p2 ?c1)
            )
  )
)