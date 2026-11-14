(define (domain capacity-chain)
  (:requirements :strips)
  (:predicates (at ?x) (next ?x ?y))
  (:action move
    :parameters (?x ?y)
    :precondition (and (at ?x) (next ?x ?y))
    :effect (and (at ?y) (not (at ?x)))))
