# StatisticalDenoiser

## DROR 
DROR stands for dynamic radius outlier removal. To clean your point cloud using  DROR use the following step
1. Read your point cloud into a numpy nd array with a shape of nx3 where the number of total pints is n and the three fields are x, y, and z coordinates.
2. Create a DROR object. 
3. Call the clean function from the object, set k_min, alpha, beta and sr_min values. k_min is the minimum number of nearest neighbor to consider, alpha is the horizontal angular resolution of the lidar, beta is the multiplication factor, sr_min is the minimum search radius. 
4. Save the output as a file.

The output will be an numpy nd array with 0 as inlier and 1 as outlier. 

If you want to have a better technical understanding about how DROR works please read the paper by Charron et al. (https://ieeexplore.ieee.org/document/8575761)

## DSOR
DSOR stands for Dynamic Statistical Outlier Removal 

To clean your point cloud using  DSOR use the following step
1. Read your point cloud into a numpy nd array with a shape of nx3 where the number of total pints is n and the three fields are x, y, and z coordinates.
2. Create a DSOR object. 
3. Call the clean function from the object, set k, s and r values. k is the minimum number of nearest neighbors to consider, s is the multiplicaiton factor for standard deviation and r is the multiplication factor for range. 
4. Save the output as a file.

The output will be an numpy nd array with 0 as inlier and 1 as outlier. 

For technical details, please read the paper by Kurup and Bos (https://arxiv.org/pdf/2109.07078)

## Dummy Code
```
# this is a dummy code not actual
import numpy as np
from sklearn.metrics import jaccard_score 
# read the point cloud and create a nx3 array
data = ...
# read the label for validation 
label = ...
cleaner = DSOR() # or cleaner = DROR
output = cleaner.clean(data[:, :3], k=3, s=-0.1, r=0.05)
iou = jaccard_score(label, output)
```

## Hyperparameter Search
Data should be separated for validation such that the test data does not overlap with the validation data. 
For a fair test evaluation, hyperparameters search should be performed on validation data. Ideally the validation
set should be about 20% of the total data and should contain sample from all the ODD test cases present in the data. 
Once the validation data is ready, hyperparameters can be searched. There are many libraries that can help you search 
the hyperparameters, but simplest way is to use nested loops. E.g., if you have 3 hyperparameters like DSOR, you can use
3 nested loops each one generating value for one parameter. This will create a list of hyperparameters to choose from. 
in the innner most loop, evaluate the iou and keep it in a dictionary to keep track of which set of hyperparameter is giving which iou. 
Once you are done with the loops, take the hyperparameter set that gives the best iou. 


#### Dummy Code
```
# this is a dummy code not actual
cleaner = DSOR()
data = ... 
label = ... 
best_iou = 0 
for k in range(some range you had decided): 
    for s in range(some range you had decided): 
        for r in range(some range yo had decided): 
            output = cleaner.clean(data[:, :3], k=k, s=s, r=r)
            iou = jaccard_score(label, output)
            if iou > best_iou:
                best_iou = iou 
                save_variable(k,s, r)
print(saved k, s, r)
            
```
