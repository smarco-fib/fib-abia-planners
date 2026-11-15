(define (domain capacity-dense-negated)
  (:requirements :strips :negative-preconditions)
  (:predicates (at ?x) (link ?x ?y ?z))
  (:action go
    :parameters (?x ?y ?z)
    :precondition (and (at ?x) (not (link ?x ?y ?z)))
    :effect (and (at ?z) (not (at ?x)))))
