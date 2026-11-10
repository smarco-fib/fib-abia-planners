; Dominio de prueba. Comentarios con acentos: camión, niño, açúcar, col·lecció, ÀÉÍÓÚ ü €
(define (domain tiny)
  (:requirements :strips :typing)
  (:types block) ; tipo «bloque»
  (:predicates (clear ?b - block) (held ?b - block) (handempty))
  ;; acción: coger un bloque (señal ñ)
  (:action pick
    :parameters (?b - block)
    :precondition (and (clear ?b) (handempty))
    :effect (and (held ?b) (not (clear ?b)) (not (handempty)))))
