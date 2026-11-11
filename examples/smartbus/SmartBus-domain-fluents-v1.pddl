(define (domain SmartBusFluents)
  (:requirements :adl :typing :fluents)

  (:types persona lugar SBus - object
          asiento parada - lugar
	  butaca plazaMreducida - asiento
	  pasajeroNormal pasajeroMreducida - persona
  )           

  (:predicates
   (estacionado ?bus - SBus ?l - lugar)
   (dentro ?p - persona ?bus - SBus)
   (destino ?p - persona ?g - parada)
   (en ?p - persona ?l - lugar)
   (pendiente ?p - persona)
   (servido ?p - persona)
  )

  (:functions
    (butacasLibres ?bus - SBus)
    (plazasMrLibres ?bus - SBus)
  )

  (:action montar_en_SBus
    :parameters (?p - pasajeroNormal ?bus - SBus ?l - parada)
    :precondition (and (pendiente ?p) (en ?p ?l) 
                       (estacionado ?bus ?l)
                       (> (butacasLibres ?bus) 0)
                   )    
    :effect (and (decrease (butacasLibres ?bus) 1) (dentro ?p ?bus)
                 (not (en ?p ?l)) (not (pendiente ?p))
            )
  )

  (:action montar_en_SBus_Mreducida
    :parameters (?p - pasajeroMreducida ?bus - SBus ?l - parada)
    :precondition (and (pendiente ?p) (en ?p ?l) 
                       (estacionado ?bus ?l)
                       (> (plazasMrLibres ?bus) 0)
                   )    
    :effect (and (decrease (plazasMrLibres ?bus) 1) (dentro ?p ?bus)
                 (not (en ?p ?l)) (not (pendiente ?p))
            )
  )
  
  (:action bajar_de_SBus
    :parameters (?p - pasajeroNormal ?bus - SBus ?l - parada)
    :precondition (and (dentro ?p ?bus) 
                       (estacionado ?bus ?l)
                       (destino ?p ?l) 
                  )
    :effect (and (en ?p ?l) (servido ?p) 
                  (not (dentro ?p ?bus))
                  (increase (butacasLibres ?bus) 1)
            )
  )

  (:action bajar_de_SBus_Mreducida
    :parameters (?p - pasajeroMreducida ?bus - SBus ?l - parada)
    :precondition (and (dentro ?p ?bus) 
                       (estacionado ?bus ?l)
                       (destino ?p ?l) 
                  )
    :effect (and (en ?p ?l) (servido ?p) 
                  (not (dentro ?p ?bus))
                  (increase (plazasMrLibres ?bus) 1)
            )
  )

  (:action mover_SBus
    :parameters (?bus - SBus ?ori - parada ?des - parada)
    :precondition (estacionado ?bus ?ori)
    :effect (and (estacionado ?bus ?des) (not (estacionado ?bus ?ori))
            )
  )
)