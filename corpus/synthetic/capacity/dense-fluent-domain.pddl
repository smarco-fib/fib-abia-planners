(define (domain capacity-dense-fluent)
  (:requirements :strips :fluents)
  (:predicates (at ?x))
  (:functions (cost ?x ?y ?z) (total-cost))
  (:action go
    :parameters (?x)
    :precondition (at o1)
    :effect (and (at ?x) (not (at o1)) (increase (total-cost) (cost o1 o2 ?x)))))
