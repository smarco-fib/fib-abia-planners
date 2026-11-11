(define (problem BinPacking-20paq-6containers)
   (:domain BinPackingFluents)
   (:objects p01 p02 p03 p04 p05 p06 p07 p08 p09 p10
	     p11 p12 p13 p14 p15 p16 p17 p18 p19 p20 - paquete
	     c01 c02 c03 c04 c05 c06 - contenedor	     
    )

  (:init
    (= (contenedoresOcupados) 0)
    (= (altura p01) 6)
    (= (altura p02) 6)
    (= (altura p03) 6)
    (= (altura p04) 6)
    (= (altura p05) 6)
    (= (altura p06) 6)
    (= (altura p07) 3)
    (= (altura p08) 1)
    (= (altura p09) 3)
    (= (altura p10) 1)
    (= (altura p11) 2)
    (= (altura p12) 1)
    (= (altura p13) 1)
    (= (altura p14) 1)
    (= (altura p15) 1)
    (= (altura p16) 2)
    (= (altura p17) 2)
    (= (altura p18) 2)
    (= (altura p19) 2)
    (= (altura p20) 1)
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


