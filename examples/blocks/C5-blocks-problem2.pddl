(define (problem blocksproblem2) (:domain blocksworld)
(:objects
	A B C D
)
(:init
   (clear A)
   (clear B)
   (clear C)
   (clear D)
   (ontable A)
   (ontable B)
   (ontable C)
   (ontable D)
   (handempty)
)
(:goal (and
           (on C D)
           (on B C)
           (on A B)
        )
))
