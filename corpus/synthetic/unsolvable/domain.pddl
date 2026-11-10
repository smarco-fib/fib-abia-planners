(define (domain switches)
  (:requirements :strips)
  (:predicates (on ?s) (off ?s) (broken ?s))
  (:action turn-on
    :parameters (?s)
    :precondition (and (off ?s) (broken ?s))
    :effect (and (on ?s) (not (off ?s)))))
