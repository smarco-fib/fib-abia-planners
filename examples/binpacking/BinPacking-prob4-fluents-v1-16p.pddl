(define (problem BinPacking-16paq-6containers)
   (:domain BinPackingFluents)
   (:objects p01 p02 p03 p04 p05 p06 p07 p08 p09 p10
	     p11 p12 p13 p14 p15 p16 - paquete
	     c01 c02 c03 c04 c05 c06 - contenedor	     
    )

  (:init
    (= (contenedoresOcupados) 0)
    (= (altura p01) 6)
    (= (altura p02) 5)
    (= (altura p03) 6)
    (= (altura p04) 5)
    (= (altura p05) 6)
    (= (altura p06) 3)
    (= (altura p07) 4)
    (= (altura p08) 1)
    (= (altura p09) 3)
    (= (altura p10) 1)
    (= (altura p11) 2)
    (= (altura p12) 2)
    (= (altura p13) 2)
    (= (altura p14) 2)
    (= (altura p15) 2)
    (= (altura p16) 1)
    (= (alturaLibre c01) 10)
    (= (alturaLibre c02) 10)
    (= (alturaLibre c03) 10)
    (= (alturaLibre c04) 10)
    (= (alturaLibre c05) 10)
    (= (alturaLibre c06) 10)
  )

  (:goal (forall (?p - paquete) (colocado ?p)))

  (:metric minimize (contenedoresOcupados))
)


