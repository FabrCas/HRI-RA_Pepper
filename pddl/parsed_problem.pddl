(define (problem house-motion)
    (:domain house_sim)
    (:objects
        foyer living_room dining toilet studio bedroom kitchen outdoor          - room
        d_foyer_outdoor d_foyer_living  d_toilet_living d_studio_living         - door
        d_bedroom_living d_living_dining d_dining_kitchen                       - door
        wl_foyer  wl_toilet wl_studio wl_bedroom wl_dining wl_kitchen           - window
        wr_foyer  wr_toilet wr_studio wr_bedroom wr_dining wr_kitchen           - window
        green_marker pen pencil plate_empty cup_coffee plate_oranges            - item
        plate_apples orange1 orange2 orange3 apple1 apple2 smartphone           - item
        red_notebook green_notebook glasses yellow_notebook cards pink_notebook - item
        desk_studio pool_studio kitchenette table_kitchen bed cabinet_bedroom_l - furniture       ;_l -> left _r -> right
        cabinet_bedroom_r tv_bedroom water tub sink cabinet_toilet              - furniture
        tv_living sofa table_living armchair_l armchair_r table_dining          - furniture
    )
    
    (:init
    
        ;                           room connections
        (connected outdoor foyer  north)
        (connected foyer outdoor  south)
        (connected foyer living_room  west)
        (connected living_room foyer  east)
        (connected toilet living_room  south)
        (connected living_room toilet  north)
        (connected studio living_room  east)
        (connected living_room studio  west)
        (connected bedroom living_room  east)
        (connected living_room bedroom  west)
        (connected dining living_room  north)
        (connected living_room dining  south)
        (connected kitchen dining  east)
        (connected dining kitchen  west)
        
        
        ;                           free space rooms defintion
        (in free_space foyer)
        (in free_space living_room)
        (in free_space dining)
        (in free_space toilet)
        (in free_space studio)
        (in free_space bedroom)
        (in free_space outdoor)
        
        ;                           doors definition
        (in d_foyer_outdoor foyer)
        (in d_foyer_outdoor outdoor)
        (isPositioned d_foyer_outdoor foyer south)
        (isPositioned d_foyer_outdoor outdoor north)
        
        (in d_foyer_living foyer)
        (in d_foyer_living living_room)
        (isPositioned d_foyer_living foyer west)
        (isPositioned d_foyer_living living_room east)
        (openDoor d_foyer_living)
        
        (in d_toilet_living toilet)
        (in d_toilet_living living_room)
        (isPositioned d_toilet_living toilet south)
        (isPositioned d_toilet_living living_room north)
        
        (in d_studio_living studio)
        (in d_studio_living living_room)
        (isPositioned d_studio_living studio east)
        (isPositioned d_studio_living living_room west)
        
        (in d_bedroom_living bedroom)
        (in d_bedroom_living living_room)
        (isPositioned d_bedroom_living bedroom east)
        (isPositioned d_bedroom_living living_room west)
        
        (in d_living_dining living_room)
        (in d_living_dining dining)
        (isPositioned d_living_dining living_room south)
        (isPositioned d_living_dining dining north)
        (openDoor d_living_dining)
        
        (in d_dining_kitchen dining)
        (in d_dining_kitchen kitchen)
        (isPositioned d_dining_kitchen dining west)
        (isPositioned d_dining_kitchen kitchen east)
        
        ;                           window definition [left]
        (in wl_foyer foyer)
        (isPositioned wl_foyer foyer east)
        
        (in wl_toilet toilet)
        (isPositioned wl_toilet toilet north)
        (openWin wl_toilet)
        
        (in wl_studio studio)
        (isPositioned wl_studio studio north)
        
        (in wl_bedroom bedroom)
        (isPositioned wl_bedroom bedroom west)
        
        (in wl_kitchen kitchen)
        (isPositioned wl_kitchen kitchen south)
        
        (in wl_dining dining)
        (isPositioned wl_dining dining east)
        (openWin wl_dining)

        ;                           window definition [right]
        (in wr_foyer foyer)
        (isPositioned wr_foyer foyer east)
        
        (in wr_toilet toilet)
        (isPositioned wr_toilet toilet north)
        (openWin wr_toilet)
        
        (in wr_studio studio)
        (isPositioned wr_studio studio north)
        
        (in wr_bedroom bedroom)
        (isPositioned wr_bedroom bedroom west)
        
        (in wr_kitchen kitchen)
        (isPositioned wr_kitchen kitchen south)
        
        (in wr_dining dining)
        (isPositioned wr_dining dining east)
        (openWin wr_dining)
        
        
        ;                           house objects (movable)
        (in green_marker studio)
        (in pen studio)
        (in pencil studio)
        (in plate_empty kitchen)
        (in cup_coffee kitchen)
        (in plate_oranges kitchen)
        (in plate_apples kitchen)
        (in orange1 kitchen)
        (in orange2 kitchen)
        (in orange3 kitchen)
        (in apple1 kitchen)
        (in apple2 kitchen)
        (in smartphone bedroom)
        (in red_notebook bedroom)
        (in green_notebook bedroom)
        (in yellow_notebook toilet)
        (in cards living_room)
        (in pink_notebook dining)
        
        ;                           furniture
        (in desk_studio studio)
        (in pool_studio studio)
        (in kitchenette kitchen)
        (in table_kitchen kitchen)
        (in bed bedroom)
        (in cabinet_bedroom_l bedroom)
        (in cabinet_bedroom_r bedroom)
        (in tv_bedroom bedroom)
        (in water toilet)
        (in tub toilet)
        (in cabinet_toilet toilet)
        (in sink toilet)
        (in tv_living living_room)
        (in sofa living_room)
        (in table_living living_room)
        (in armchair_l living_room)
        (in armchair_r living_room)
        (in table_dining dining)
        
        (on green_marker desk_studio)
        (on pen desk_studio)
        (on pencil desk_studio)
        (on plate_empty kitchenette)
        (on cup_coffee kitchenette)
        (on plate_oranges table_kitchen)
        (on plate_apples table_kitchen)
        (on orange1 plate_oranges)
        (on orange2 plate_oranges)
        (on orange3 plate_oranges)
        (on apple1 plate_apples)
        (on apple2 plate_apples)
        (on smartphone bed)
        (on red_notebook cabinet_bedroom_l)
        (on green_notebook cabinet_bedroom_r)
        (on yellow_notebook cabinet_toilet)
        (on cards table_living)
        (on pink_notebook table_dining)
        
        ;                           pepper init 
        (openDoor d_studio_living)
        (openDoor d_toilet_living)
        (freeHands)

        (on glasses table_living)
        (PepperIn studio)
        (PepperAt free_space)
        (in glasses living_room)
    )
    
    (:goal
        (and (on glasses table_kitchen) (PepperAt sofa)  (freeHands))
    )
)
