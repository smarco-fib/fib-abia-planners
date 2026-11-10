(DEFINE (Domain Tiny)
  (:Requirements :STRIPS :Typing)
  (:TYPES Block)
  (:predicates (Clear ?B - block) (HELD ?b - BLOCK) (HandEmpty))
  (:ACTION Pick
    :Parameters (?b - Block)
    :Precondition (AND (clear ?b) (handempty))
    :Effect (and (Held ?B) (NOT (clear ?b)) (not (HANDEMPTY)))))
