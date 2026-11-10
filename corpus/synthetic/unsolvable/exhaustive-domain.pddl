(define (domain ring)
  (:requirements :strips)
  (:predicates (at ?x) (link ?x ?y) (token ?x) (holding) (free))
  (:action move
    :parameters (?x ?y)
    :precondition (and (at ?x) (link ?x ?y))
    :effect (and (at ?y) (not (at ?x))))
  (:action pick
    :parameters (?x)
    :precondition (and (at ?x) (token ?x) (free))
    :effect (and (holding) (not (token ?x)) (not (free))))
  (:action drop
    :parameters (?x)
    :precondition (and (at ?x) (holding))
    :effect (and (token ?x) (free) (not (holding)))))
