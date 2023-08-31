(define (domain house_sim)
    (:requirements :strips  :adl)
    (:types
        room            - object
        direction       - object 
        room_element    - object            ; superclass
        item            - room_element
        window          - room_element
        door            - room_element
        furniture       - room_element

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
        (connected ?r1 - room ?r2 - room  ?d - direction)                   ; used to connect rooms
        (in ?o - room_element ?r - room)                                    ; for object, window, door in room
        (on ?i - item  ?f - room_element)                                   ; for object on furtniture or on another item
        (isPositioned ?o - room_element ?r - room ?d - direction)         ;generic predicate for define the cardinal position of windows and doors.
        
        
        ;Interaction with doors and windows  (closed wolrd assumption for closed elements)
        (openDoor  ?w - door)
        (openWin   ?w   - window)
        
        
        ;Pepper information
        (PepperIn  ?r - room)
        (PepperAt  ?o - room_element)                                     ;generic to indicate pepper near to window/door/furniture (now can interact)
        (PepperHas ?i - item)
        (freeHands)
    )
    
    
    ;                               [motion action]
    (:action move2
        :parameters (?r - room ?from ?to -room_element)
        :precondition (and (PepperIn ?r) (PepperAt ?from) (in ?from ?r) (in ?to ?r))
        :effect (and (PepperAt ?to) (not(PepperAt ?from)))
    )
    
    (:action move2room
        :parameters (?from ?to - room  ?d - door ?side - direction)
        :precondition (and (connected ?from ?to ?side) (isPositioned ?d ?from ?side) (PepperIn ?from) (PepperAt ?d) (openDoor ?d) (in ?d ?from)(in ?d ?to))
        :effect (and (not(PepperIn ?from)) (PepperIn ?to))
    )
    
    ;                               [action with windows and doors]
    (:action open_door
        :parameters (?e - door ?r -room)
        :precondition (and (not(openDoor ?e)) (in ?e ?r) (freeHands) (PepperIn ?r) (PepperAt ?e))
        :effect (and (openDoor ?e))
    )
    
    (:action close_door
        :parameters (?e - door ?r -room)
        :precondition (and (openDoor ?e) (in ?e ?r) (freeHands) (PepperIn ?r) (PepperAt ?e))
        :effect (and (not (openDoor ?e)))
    )
    
    (:action open_win
        :parameters (?e - window ?r -room)
        :precondition (and (not(openWin ?e)) (in ?e ?r) (freeHands) (PepperIn ?r) (PepperAt ?e))
        :effect (and (openWin ?e))
    )
    
    (:action close_win
        :parameters (?e - window ?r -room)
        :precondition (and (openWin ?e) (in ?e ?r) (freeHands) (PepperIn ?r) (PepperAt ?e))
        :effect (and (not (openWin ?e)))
    )
    
    ;                               [action with house objects]
    
    (:action grab_object
        :parameters (?i - item ?r - room ?f - room_element)
        :precondition (and (in ?i ?r) (in ?f ?r) (on ?i ?f) (freeHands) (PepperAt ?f) (PepperIn ?r))
        :effect (and (not(freeHands)) (not(on ?i ?f)) (not(in ?i ?r)) (PepperHas ?i)) 
    )
    
    (:action place_object
        :parameters (?i - item ?r - room ?f - furniture)
        :precondition (and (in ?f ?r) (PepperHas ?i) (PepperIn ?r) (PepperAt ?f) )
        :effect (and (not (PepperHas ?i)) (freeHands) (in ?i ?r) (on ?i ?f))
    )
)
