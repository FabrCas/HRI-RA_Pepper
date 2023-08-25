(define (domain house_sim)
    (:requirements :strips  :adl)
    (:types
        room            - object
        room_element    - object
        ;item            - room_element
        ;window          - room_element
        door            - room_element
        direction       - object 
    )
    
    (:constants
        north           - direction 
        south           - direction
        west            - direction
        east            - direction
        free_space      - room_element    ; to characterize pepper not in proximity of room elements
        ;pepper          - object
    )
    
    
    (:predicates
        
        ; Define house environment composition
        (connected ?r1 - room ?r2 - room  ?d - direction)
        (in ?o - room_element ?r - room)
        (isPositioned ?o - room_element ?r - room ?d - direction)         ;generic predicate for define the cardinal position of windows and doors.
        
        
        ;Interaction with doors and windows  (closed wolrd assumption for closed elements)
        (openDoor  ?w - door)
        ;(openWindow   ?w   - window)
        
        
        ;Pepper information
        (PepperIn  ?r - room)
        (PepperAt  ?o - room_element)                                     ;generic to indicate pepper near to windowd or door (now can interact)
        ;(PepperHas ?i - item)
        (freeHands)
    )
    
    (
    :action move2
        :parameters (?in - room ?from ?to -room_element)
        :precondition (and (PepperIn ?in) (PepperAt ?from))
        :effect (and (PepperAt ?to) (not(PepperAt ?from)))
    )
    
    (
    :action open_door
        :parameters (?e - door ?r -room)
        :precondition (and (not(openDoor ?e)) (in ?e ?r) (freeHands) (PepperIn ?r) (PepperAt ?e))
        :effect (and (openDoor ?e))
    )
    
    
    
)
