# ECE653 : Assignment 1

# Fault error detection and Error state identification  
```def matmul(a, b):
 """  
 Returns the result of multiplying two input matrices.  
  
 Raises an exception when the input is not valid.  
 """  
 n, p = len(a), len(a[0])  
 q, p1 = len(b), len(b[0])  
 if p != p1:  
 raise ValueError("Incompatible dimensions")  
 c = [[0] * q for i in range(n)]  
 for i in range(n):  
 for j in range(q):  
 c[i][j] = sum(a[i][k] * b[k][j] for k in range(p))  
 return c ``` 

 From the above Python program we identified the fault, error identification, the first error state and failure in execution from various test cases.
 We generated a Control Flow graph of the function using graphviz considering line of code as node number. (Reference : https://dreampuf.github.io/GraphvizOnline/)  

   Various operations as follows:
   1. Generated (Abstract syntax tree) and computed Natural Operational Semantics without using rules of while loop.
   2. Used test cases to obtain 100% statement coverage. Included mutations in the test unit to obtain the same coverage percentage.
   3. Computed Branch coverage by using proper test cases.
