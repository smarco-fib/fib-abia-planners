(define (domain swap)
  (:requirements :strips)
  (:predicates (at ?x ?y) (adj ?a ?b))
  (:action step
    :parameters (?t ?a ?b)
    :precondition (and (at ?t ?a) (adj ?a ?b))
    :effect (and (at ?t ?b) (not (at ?t ?a)))))
