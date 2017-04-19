Detect the change point based on the algorithm and matlab codes in the following links:

http://hips.seas.harvard.edu/files/adams-changepoint-tr-2007.pdf
http://hips.seas.harvard.edu/content/bayesian-online-changepoint-detection

1. If just need the python codes based on the matlab code, run anothorTEST.py and online_change...detection.py
2. If the input data is large (>= 1MB), run anotherTEST.py and ocpd.py. Since ocpd.py uses sparse matrix instead of the regular matrix to avoid the memory error that is caused by the larger size of input file. (Also can run table.py which uses pyTable)
3. If the input data is much larger and need to save time, use LinearyMain.py and linear.py. The time complexity in linear.py is linear. Since we use array to do the calcualtion instead of using matrix. 
