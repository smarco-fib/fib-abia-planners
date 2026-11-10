; Problema: ¿funciona con acentos? sí — façana, l·l
(define (problem ok) (:domain tiny)
  (:objects a - block) ; objeto «a»
  (:init (clear a) (handempty))
  (:goal (held a)))
