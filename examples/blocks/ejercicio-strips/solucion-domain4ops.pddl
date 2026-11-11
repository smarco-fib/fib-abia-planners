;; Solución del ejercicio: traducción completa a PDDL del dominio de bloques
;; con 4 operadores escrito en notación STRIPS (C5-blocks-domain4ops.str.pddl).
;; Cada operador STRIPS (PRE / DEL / ADD) se convierte en una acción PDDL:
;;   PRE -> :precondition
;;   ADD -> literales positivos de :effect
;;   DEL -> literales (not ...) de :effect

(define (domain blocksworldStrips2PDDL)
  (:requirements :strips)

  (:predicates
    (clear ?x)
    (ontable ?x)
    (handempty)
    (holding ?x)
    (on ?x ?y))

  ;; OP: pick-up(x)
  (:action pick-up
    :parameters (?x)
    :precondition (and (clear ?x) (ontable ?x) (handempty))
    :effect (and (not (clear ?x)) (not (ontable ?x)) (not (handempty))
                 (holding ?x)))

  ;; OP: put-down(x)
  ;;   PRE: holding(x).  DEL: holding(x).  ADD: clear(x), handempty(), ontable(x).
  (:action put-down
    :parameters (?x)
    :precondition (holding ?x)
    :effect (and (not (holding ?x))
                 (clear ?x) (handempty) (ontable ?x)))

  ;; OP: stack(x,y)
  ;;   PRE: holding(x), clear(y).  DEL: holding(x), clear(y).
  ;;   ADD: clear(x), handempty(), on(x,y).
  (:action stack
    :parameters (?x ?y)
    :precondition (and (holding ?x) (clear ?y))
    :effect (and (not (holding ?x)) (not (clear ?y))
                 (clear ?x) (handempty) (on ?x ?y)))

  ;; OP: unstack(x,y)
  ;;   PRE: on(x,y), clear(x), handempty().  DEL: on(x,y), clear(x), handempty().
  ;;   ADD: holding(x), clear(y).
  (:action unstack
    :parameters (?x ?y)
    :precondition (and (on ?x ?y) (clear ?x) (handempty))
    :effect (and (not (on ?x ?y)) (not (clear ?x)) (not (handempty))
                 (holding ?x) (clear ?y)))
)
