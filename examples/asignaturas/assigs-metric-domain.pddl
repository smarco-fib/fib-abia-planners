(define (domain assig)
    (:requirements :adl :equality :typing :fluents)
    (:types assignatura quadrimestre)
    (:predicates
        (prerequisit ?x ?y - assignatura)
        (precorequisit ?x ?y - assignatura)
        (cursada ?x - assignatura)
        (assignat ?x - assignatura ?y - quadrimestre)
        (menor ?a ?b - quadrimestre)
    )
	(:constants
        Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 - quadrimestre
    )
	
	(:functions
		; Funcions especifiques per a l'extensio 4
		(credits-quatri ?q - quadrimestre)
		(total-credits)
		(credits-assig ?a - assignatura)
	)
	
    (:action assigna
        :parameters (?ass - assignatura ?q - quadrimestre)
        :precondition (and
			(and
				; comprova la restriccio de l'extensio 4
				(<= (+ (total-credits) (credits-assig ?ass)) 240)
				(<= (+ (credits-quatri ?q) (credits-assig ?ass)) 60)
			)
			
			; comprova que l'assignatura no estigui assignada o cursada ja
			(not (exists (?qo - quadrimestre) (assignat ?ass ?qo)))
			(not (cursada ?ass))
			
			; extensio 1
			(not (exists (?o - assignatura) (and 
				(prerequisit ?o ?ass)
				(and
					(not (exists (?qo - quadrimestre) (and
						(assignat ?o ?qo)
						(menor ?qo ?q)
					)))
					(not (cursada ?o))
				)
			)))
			
			; extensio 2
			(not (exists (?o - assignatura) (and 
				(precorequisit ?o ?ass)
				(and
					(not (exists (?qo - quadrimestre) (and
						(assignat ?o ?qo)
						(or
							(menor ?qo ?q)
							(= ?qo ?q)
						)
					)))
					(not (cursada ?o))
				)
			)))
        )
        :effect (and
        	(assignat ?ass ?q)
			; extensio 4:
			(increase (total-credits) (credits-assig ?ass))
			(increase (credits-quatri ?q) (credits-assig ?ass))
        )
    )
)
