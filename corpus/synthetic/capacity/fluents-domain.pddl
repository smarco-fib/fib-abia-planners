(define (domain capacity-fluents)
  (:requirements :strips :fluents)
  (:predicates (obj ?x))
  (:functions (level ?x) (total-cost))
  (:action raise
    :parameters (?x)
    :precondition (and (obj ?x) (< (level ?x) 1))
    :effect (and (increase (level ?x) 1) (increase (total-cost) 1))))
