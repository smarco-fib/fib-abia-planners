(define (domain smart-bus)
    (:requirements :strips :adl)
    
    (:types bus parada plaza persona - object
            asiento reducida - plaza
            movtotal movreducida - persona)
    (:predicates
        (origen ?x - persona ?y - parada)
        (destino ?x - persona ?y - parada)
        (transportada ?x - persona)
        (asignado ?x - persona ?a - plaza)
        (ocupado ?a - plaza)
        (en-bus ?x - persona)
        (en-parada ?b - bus ?p - parada)
        (en ?x - persona ?p - parada)
        )
        
    (:action montar-movtotal
        :parameters (?b - bus ?x - movtotal ?a - plaza ?p - parada)
        :precondition (and 
            (not (en-bus ?x))
            (not (ocupado ?a))
            (en-parada ?b ?p)
            (en ?x ?p)
        )
        :effect (and (not (en ?x ?p))
                     (ocupado ?a) (en-bus ?x) (asignado ?x ?a)))

    (:action montar-reducida
        :parameters (?b - bus ?x - movreducida ?a - reducida ?p - parada)
        :precondition (and 
            (not (en-bus ?x))
            (not (ocupado ?a))
            (en-parada ?b ?p)
            (en ?x ?p)
        )
        :effect (and (not (en ?x ?p))
                     (ocupado ?a) (en-bus ?x) (asignado ?x ?a)))

    (:action desmontar
        :parameters (?b - bus ?x - persona ?a - plaza ?p - parada)
        :precondition (and 
            (en-bus ?x)
            (ocupado ?a)
            (asignado ?x ?a)
            (en-parada ?b ?p)
        )
        :effect (and 
            (not (en-bus ?x))
            (not (ocupado ?a))
            (not (asignado ?x ?a))
            (en ?x ?p)
        ))

    (:action acabar-viaje
        :parameters (?x - persona ?p - parada)
        :precondition (and
            (not (transportada ?x))
            (en ?x ?p)
            (destino ?x ?p)
        )
        :effect (and 
            (transportada ?x)
        ))

    (:action mover
        :parameters (?b - bus ?p1 - parada ?p2 - parada)
        :precondition (and 
            (en-parada ?b ?p1)
        )
        :effect (and 
            (not (en-parada ?b ?p1))
            (en-parada ?b ?p2)
        ))
    )


