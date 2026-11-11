(define (problem blocksproblemslides) (:domain blocksworld)
(:objects
	A B C D 
)
(:init
   (clear A)
   (clear B)
   (clear C)
   (clear D)
   (ontable B)
   (ontable A)
   (ontable C)
   (ontable D)
   (handempty)
)
(:goal (and
           (on D C)
           (on C B)
           (on B A)
        )
))
