(define (problem BinPacking-10paq-3containers)
   (:domain BinPackingFluents)
   (:objects p01 p02 p03 p04 p05 p06 p07 p08 p09 p10 - paquete
	     c01 c02 c03 - contenedor	     
    )

  (:init
    (= (contenedoresOcupados) 0)
    (= (altura p01) 1)
    (= (altura p02) 4)
    (= (altura p03) 2)
    (= (altura p04) 1)
    (= (altura p05) 3)
    (= (altura p06) 2)
    (= (altura p07) 3)
    (= (altura p08) 1)
    (= (altura p09) 3)
    (= (altura p10) 1)
    (= (alturaLibre c01) 10)
    (= (alturaLibre c02) 10)
    (= (alturaLibre c03) 10)
  )

  (:goal (forall (?p - paquete) (colocado ?p)))

  (:metric minimize (contenedoresOcupados))
)


