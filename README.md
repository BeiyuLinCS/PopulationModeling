Detect the change point based on the algorithm and matlab codes in the following links:

http://hips.seas.harvard.edu/files/adams-changepoint-tr-2007.pdf

http://hips.seas.harvard.edu/content/bayesian-online-changepoint-detection

1. If just need the python codes based on the matlab code, run anothorTEST.py and online_change...detection.py. We did a test based on a small test file (KB) to make sure that the results from Python codes were the same as that from Matlab codes. 

In the online_...._detection.py, it uses similar methods as in matlab codes. That is, the probabilities calculations have been doing on matrix (size of inputfile+2, size of inputfile+1). The matrix operation would have memory error if the input file is greater than 1MB. 

2. Then use anotherTEST.py and ocpd.py. ocpd.py uses sparse matrix instead of the regular matrix to avoid the memory error that is caused by the larger size of input file. Using sparse matrix would not have memory error, but it is time consuming(Input file is greater than 1MB) since the final matrix is an upper-triangle matrix.  (Also can run table.py which uses pyTable, but it is also time consuming to keep reading, modifying, and writing into the disk).

3. use LinearyMain.py and linear.py. The time complexity in linear.py is linear. Since we use array (size of inputfile+2, 2) to do the calcualtion instead of using sparse matrix. 
