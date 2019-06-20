 id
 poi 3

 x_f 2 3 0 
 y_f 1 16 19  "North (m)"
 view 0.125 0.95 0.65 0.95
 read
 
 fit 1 1 A
 y_s -0.02 0.02
 pen 1 
 xmx -1 0
 ymx -1 0
 ymn -1 1 
 xmn -1 0

 pen 08
 draw
 pen 33
 fit 0
 pdr

 pen 10
 label 0.1 0.006 1 0 :h4
 label 0.1 0.003 1 0 :f
 pen 33
 label 4 0.035 1 0 :p2



 file #2
 read
 fit 1 0 A
 pen 10
 errb 2
 y_s -0.02 0.02
 draw
.

! key 

 file #1

 y_f 1 17 20 "East (m)"
 view 0.125 0.95 0.35 0.65
 read
 
 fit 1 1 A
 y_s -0.02 0.02
 pen 1 
 xmx -1 0
 ymx -1 0
 ymn -1 1 
 xmn -1 0

 pen 08
 draw
 pen 33
 fit 0
 pdr
 label 4 0.035 1 0 :p2

 pen 10

 file #2
 read
 fit 1 0 A
 pen 10
 errb 2
 y_s -0.02 0.02
 draw
.

 file #1

 y_f 1 18 21 "Height (m)"
 view 0.125 0.95 0.05 0.35 
 read
 
 fit 1 1 A
 y_s -0.075 0.075
 pen 1 
 xmx -1 0
 ymx -1 0
 ymn -1 1 
 xmn -1 1

 pen 8
 draw
 pen 33
 fit 0
 pdr
 label 0.1 0.14 1 0 :p2

 pen 10
 

 file #2
 read
 fit 1 0 A
 pen 10
 errb 2
 y_s -0.075 0.075
 draw
.

 key
