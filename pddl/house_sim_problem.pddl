(define (problem house-motion)
    (:domain house_sim)
    (:objects
        foyer living_room dining toilet studio bedroom kitchen outdoor - room
        d_foyer_outdoor d_foyer_living  d_toiler_living d_studio_living d_bedroom_living d_living_dining d_dining_kitchen - door
        ;- window
        ;- item 
    )
    
    (:init
    
        ;                           room connections
        (connected outdoor foyer  north)
        (connected foyer outdoor  south)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        ; (connected ?r1 - room ?r2 - room  ?d - direction)
        
        ;                           doors definition
        (in d_foyer_outdoor foyer)
        (in d_foyer_outdoor outdoor)
        (isPositioned d_foyer_outdoor foyer south)
        (isPositioned d_foyer_outdoor outdoor north)
        (openDoor d_foyer_outdoor)
        
        (in d_foyer_living foyer)
        (in d_foyer_living living_room)
        (isPositioned d_foyer_living foyer west)
        (isPositioned d_foyer_living living_room east)

        ;                           pepper init 
        (PepperIn foyer)
        (PepperAt free_space)
        (freeHands)
    )
    
    (:goal
        (and (openDoor d_foyer_living))
    )
)
