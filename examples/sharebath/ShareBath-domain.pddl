(define (domain sharebath)
  (:requirements :adl :typing)
  (:types persona accion itemCompartido - object
    ducha servicio lavamanos secador - itemCompartido
  )           

  (:predicates
   (quiere ?p - persona ?a - accion)	
   (tiene ?p - persona ?i - itemCompartido)
   (libre ?i - itemCompartido)
   (independiente ?a - accion) 
   (precede ?a1 ?a2 - accion)
   (necesitaDucha ?a - accion) 
   (necesitaWC ?a - accion) 
   (necesitaLavamanos ?a - accion) 
   (necesitaSecador ?a - accion)
  )
 
  (:action obtener_item
    :parameters (?p - persona ?i - itemCompartido)
    :precondition (libre ?i)     
    :effect (and (not (libre ?i)) (tiene ?p ?i))
  )
 
  (:action liberar_item
    :parameters (?p - persona ?i - itemCompartido)
    :precondition (tiene ?p ?i)     
    :effect (and (not (tiene ?p ?i)) (libre ?i))
  )
 
  (:action realizar_accion_independiente
    :parameters (?p - persona ?a - accion)
    :precondition (and (quiere ?p ?a) (independiente ?a)
                       (imply (necesitaDucha ?a) (exists (?i - ducha)(tiene ?p ?i)))
                       (imply (necesitaWC ?a) (exists (?i - servicio)(tiene ?p ?i)))
                       (imply (necesitaLavamanos ?a) 
                              (exists (?i - lavamanos)(tiene ?p ?i)))
                       (imply (necesitaSecador ?a) (exists (?i - secador)(tiene ?p ?i)))
                   )    
    :effect (not (quiere ?p ?a))
  )
  
  (:action realizar_accion_dependiente
    :parameters (?p - persona ?a - accion ?ant - accion)
    :precondition (and (quiere ?p ?a) 
                       (precede ?ant ?a) (not (quiere ?p ?ant))
                       (imply (necesitaDucha ?a) (exists (?i - ducha)(tiene ?p ?i)))
                       (imply (necesitaWC ?a) (exists (?i - servicio)(tiene ?p ?i)))
                       (imply (necesitaLavamanos ?a) 
                              (exists (?i - lavamanos)(tiene ?p ?i)))
                       (imply (necesitaSecador ?a) (exists (?i - secador)(tiene ?p ?i)))
                   )    
    :effect (not (quiere ?p ?a))
  )
  
)
 