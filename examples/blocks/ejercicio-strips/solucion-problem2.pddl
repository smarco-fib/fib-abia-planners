;; Solución del ejercicio: el problema C5-blocks-problem2.str en PDDL correcto.
;; Cambios: (domain ...) -> (:domain ...), y el nombre del problema no puede
;; empezar por un número (Metric-FF lo leería como un número).

(define (problem blocks-strips2pddl-1)
  (:domain blocksworldStrips2PDDL)

  (:objects A B C D E F)

  (:init
    (clear A) (clear B) (clear E) (clear C) (clear D) (ontable F) (ontable B)
    (ontable E) (ontable C) (ontable D) (on A F) (handempty))

  (:goal
    (and (on E F) (on F C) (on C B) (on B A) (on A D)))
)
