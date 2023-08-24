(define (domain grid-world)

(:requirements :adl)

(:predicates
    (at ?x)(is-agent ?x)(has-obstacle ?x)(is-pos ?x)(adj ?x ?y)
)

(:action move
    :parameters (?agent ?from ?to)
    :precondition (and
        (is-agent ?agent)
        (at ?from)
        (is-pos ?from)
        (is-pos ?to)
        (adj ?from ?to)
        (not(has-obstacle ?to))
    )
    :effect (and
        (not(at ?from))
        (at ?to)
    )
)

)