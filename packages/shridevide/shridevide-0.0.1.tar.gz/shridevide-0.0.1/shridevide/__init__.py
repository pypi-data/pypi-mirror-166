def devide(x,y):
 i=min(x,y)

 while i>=1:
     if x%i==0:
         if y%i==0:
           break
     i-=1
    
 return "("+str(x)+"/"+str(y)+")=("+str(x/i)+"/"+str(y/i)+")"
