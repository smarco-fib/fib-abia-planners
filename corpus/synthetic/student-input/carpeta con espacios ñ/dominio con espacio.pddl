(define (domain tiny)
  (:requirements :strips :typing)
  (:types block)
  (:predicates (clear ?b - block) (held ?b - block) (handempty))
  (:action pick
    :parameters (?b - block)
    :precondition (and (clear ?b) (handempty))
    :effect (and (held ?b) (not (clear ?b)) (not (handempty)))))
