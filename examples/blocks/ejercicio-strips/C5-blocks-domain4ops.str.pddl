(define (domain blocksworldStrips2PDDL)
        (:requirements :strips)

 (:predicates
      (clear ?x)
      (ontable ?x) (handempty) (holding ?x)
      (on ?x ?y)
 )

(:action pick-up
    :parameters (?x)
    :precondition (and  (clear ?x) (ontable ?x) (handempty))
    :effects (and   (not(clear ?x)) (not (ontable ?x)) (not (handempty))
                    (holding ?x))
 )

OP: put-down(x):
PRE: holding(x).
DEL: holding(x).
ADD:clear(x),handempty(),ontable(x).

(:action stack
    :parameters (?x ?y)
PRE: holding(x),clear(y).
DEL: holding(x),clear(y).
ADD: clear(x),handempty(),on(x,y).
)

OP: unstack(x,y):
PRE: on(x,y),clear(x),handempty().
DEL: on(x,y),clear(x),handempty().
ADD: holding(x),clear(y).

)