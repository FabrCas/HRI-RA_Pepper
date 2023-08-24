(define (domain grid1)
(:requirements :adl)

(:predicates (at ?pos) (block ?pos) (adj ?pos1 ?pos2)
)

(:action move
:parameters(?posagent ?nextpos)
:precondition (and (at ?posagent) (adj ?posagent ?nextpos) (not (block ?nextpos)) ) 
:effect (and (at ?nextpos) (not(at ?posagent)) )
)
)