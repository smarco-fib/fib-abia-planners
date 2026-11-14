(define (domain capacity-objects)
  (:requirements :strips)
  (:predicates (visited ?x) (pair ?x ?y))
  (:action visit
    :parameters (?x)
    :effect (visited ?x)))
