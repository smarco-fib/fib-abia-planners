(define (domain capacity-dense)
  (:requirements :strips)
  (:predicates (at ?x) (link ?x ?y ?z))
  (:action go
    :parameters (?x ?y ?z)
    :precondition (and (at ?x) (link ?x ?y ?z))
    :effect (and (at ?z) (not (at ?x)))))
