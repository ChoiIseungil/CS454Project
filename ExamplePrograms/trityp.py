#https://www.cs.mtsu.edu/~untch/4900/public/trityp.c

def trityp(i,j,k):
    TRIANG = 0
    # TRIANG = 1 IF TRIANGLE IS SCALENE
	# TRIANG = 2 IF TRIANGLE IS ISOSCELES
	# TRIANG = 3 IF TRIANGLE IS EQUILATERAL
	# TRIANG = 4 IF NOT A TRIANGLE

    if (i<=0)or(j<=0)or(k<=0): 
        TRIANG = 4
        return TRIANG

    TRIANG = 0
    if (i==j): 
        TRIANG=TRIANG+1
    if (i==k): 
        TRIANG=TRIANG+1
    if (j==k): 
        TRIANG=TRIANG+1
    
    # Confirm it's a legal triangle before declaring it to be scalene
    if (TRIANG==0):
        if (i+j)<=k or (j+k)<=i or (i+k)<=j:
            TRIANG = 4
        else:
            TRIANG = 1
        return TRIANG

    if (TRIANG>3):
        TRIANG = 3
    else if (TRIANG==1) and (i+j)>k:
        TRIANG = 2
    else if (TRIANG==2) and (i+k)>j:
        TRIANG = 2
    else if (TRIANG==3) and (j+k)>i:
        TRIANG = 2
    else:
        TRIANG = 4
    return TRIANG
    
