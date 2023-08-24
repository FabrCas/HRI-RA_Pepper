(define (problem grid1)
(:domain grid1)
(:objects
pos11 pos12 pos13 pos14 pos21 pos22 pos23 pos24 pos31 pos32 pos33 pos34 pos41 pos42 pos43 pos44 
)
(:init

(adj pos11 pos12) (adj pos11 pos21) (adj pos11 pos22) 
(adj pos12 pos11) (adj pos12 pos22) (adj pos12 pos13) (adj pos12 pos21) (adj pos12 pos23)
(adj pos13 pos12) (adj pos13 pos14) (adj pos13 pos23) (adj pos13 pos22) (adj pos13 pos24)
(adj pos14 pos13) (adj pos11 pos24) (adj pos11 pos23)

(adj pos21 pos11) (adj pos21 pos22) (adj pos21 pos31) (adj pos21 pos12) (adj pos21 pos32) 
(adj pos22 pos21) (adj pos22 pos23) (adj pos22 pos12) (adj pos22 pos32) (adj pos22 pos11) (adj pos22 pos13) (adj pos22 pos31) (adj pos22 pos33)  
(adj pos23 pos22) (adj pos23 pos24) (adj pos23 pos13) (adj pos23 pos34) (adj pos23 pos12) (adj pos23 pos14) (adj pos23 pos32) (adj pos23 pos34)
(adj pos24 pos23) (adj pos24 pos14) (adj pos24 pos34) (adj pos24 pos13) (adj pos24 pos33)

(adj pos31 pos21) (adj pos31 pos32) (adj pos31 pos41) (adj pos31 pos22) (adj pos31 pos42) 
(adj pos32 pos31) (adj pos32 pos33) (adj pos32 pos22) (adj pos32 pos42) (adj pos32 pos21) (adj pos32 pos23) (adj pos32 pos41) (adj pos32 pos43)  
(adj pos33 pos32) (adj pos33 pos34) (adj pos33 pos23) (adj pos33 pos44) (adj pos33 pos22) (adj pos33 pos24) (adj pos33 pos42) (adj pos33 pos44)
(adj pos34 pos33) (adj pos34 pos24) (adj pos34 pos44) (adj pos34 pos23) (adj pos34 pos43)

(adj pos41 pos42) (adj pos41 pos31) (adj pos41 pos32) 
(adj pos42 pos32) (adj pos42 pos41) (adj pos42 pos43) (adj pos42 pos31) (adj pos42 pos33)
(adj pos43 pos33) (adj pos43 pos42) (adj pos43 pos44) (adj pos43 pos32) (adj pos43 pos34)
(adj pos44 pos43) (adj pos44 pos34) (adj pos44 pos33)

(block pos13) (block pos22) (block pos23) (block pos33)
(at pos31)

)
(:goal (at pos34)
)
)

