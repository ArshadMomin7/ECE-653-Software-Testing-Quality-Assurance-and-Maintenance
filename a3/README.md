# ECE 653 : Assignment 3
```
1 assume (n >= 0);
2 r := 0;
3 i := 0;
4 p := 1;
5 while not (i = n) do
6 {
7 r = r - p;
8 p = 2 * p;
9 r = r + p;
10 i = i + 1;
11 }  
```

1. Using Hoare Logic method derived the validity of the above program.
2. Performed Verification using Dafny Verification tool. (_Refer Dafny folder_)
3. Extended the symbolic execution for while language to achieve 100% branch coverage (_Refer wlang folder_) and identified the missing inductive invariant for verification of the program.