import numpy as np
import matplotlib.pyplot as plt

def percolation(prints, gridXDim, gridYDim, p):
    # Form the grid two indexes larger in x and y so that a border of zeroes
    # surrounds the sites of interest
    grid = np.zeros((gridYDim+2, gridXDim+2))
    
    # Fill the grid such that the sites of interest have a probability, p, of 
    # being 1 and the border has values of 0
    for y in range(1,len(grid)-1):
        for x in range(1,len(grid[0])-1):
            if np.random.random()<p:
                grid[x][y]=1
            else:
                grid[x][y]=0
    
    if prints==True:
        print(grid[1:-1, 1:-1])
    
        # Show grid with the border
        plt.matshow(grid, cmap=plt.cm.gray_r)
        plt.show()
        
        # Show grid without the border
        plt.matshow(grid[1:-1, 1:-1], cmap=plt.cm.gray_r)
        plt.show()
    
    # Count how many cells are non-zer0 in the grid, this ignores the border
    # as the border is always zero
    occupiedCells = np.count_nonzero(grid)
    
    # numpy.arange will create an array of values from 0 to occupiedCells with
    # step 1, these will be the inital ids of each cell
    IDs = np.arange(0, occupiedCells, 1)
    #print(IDs)
    
    # 2-D array that stores the [y,x] coordinates of occupied cells
    cellCoords = [list(i) for i in np.argwhere(grid>0)]
    
    #print(coords) gives:
    #[[1, 3], [2, 4], [2, 5], [3, 1], [3, 4], [3, 5], [4, 2], [4, 3], [4, 4], 
    #[4, 5], [5, 1], [5, 3], [5, 5]] as an example
    
    while True:
        # Array to store the IDs that need to be corrected at the end
        wrongIDs = []
        
        # iterate through every cell that is 1
        for i in np.arange(occupiedCells):
            y,x = cellCoords[i]
            
            # If one neighbor is occupied, the ID of the current cell is changed 
            # to the ID of that neighbor.
        
            if grid[y-1][x]==1 and grid[y][x-1]==0:
                IDs[i] = IDs[cellCoords.index([y-1,x])]
                
            elif grid[y][x-1]==1 and grid[y-1][x]==0:
                IDs[i] = IDs[cellCoords.index([y,x-1])]
    
            # if both neighbors are occupied then the smaller label of the two is 
            # assigned
            elif grid[y-1][x]==1 and grid[y][x-1]==1:
                ID1 = IDs[cellCoords.index([y-1,x])]
                ID2 = IDs[cellCoords.index([y,x-1])]
                IDs[i] = np.min([ID1, ID2])
    
                # if IDs are unequal then they are also stored to correct later
                # this is because two clusters can be connected with different IDs
                if ID1!=ID2:
                    wrongIDs.append([ID1,ID2])
    
        # Quit the loop if there are no more wrong IDs
        if wrongIDs==[]:
            break
        # else correct IDs
        else:
            for i,j in wrongIDs:
                # Finds the ID that is the greater of the two and assignes it 'wrongID'
                wrongID = np.max([i,j])
                # Finds the ID that is the lesser of the two and assignes it 'correctID'            
                correctID = np.min([i,j])
                # Every ID that has the wrongID is given the correctID
                IDs[IDs==wrongID] = correctID
                
    # Define new array to store the coordiates of every cell in each cluster
    arrayClusterCells = []
    for i in np.unique(IDs):
        arrayClusterCells.append([cellCoords[j] for j in range(len(IDs)) if IDs[j]==i])
        
    # print(arrayClusterCells) gives: [[[1, 1]], [[1, 2]], [[1, 3]], [[1, 4]],
    # [[1, 5]], [[2, 3]], [[2, 4]], [[3, 2]], [[4, 1]], [[4, 2]], [[5, 1]], 
    # [[4, 5]], [[5, 3]], [[5, 4]], [[5, 5]]] as an example
    
    # Search for percolation
    toptobottom = False
    lefttoright = False
    for cluster in arrayClusterCells:
        #numpy.array.T transposes the array
        cluster = np.array(cluster).T
        if (1 in cluster[0]) and (gridYDim in cluster[0]):
            toptobottom = True
    
        if (1 in cluster[1]) and (gridXDim in cluster[1]):
            lefttoright = True
    
    if prints==True:
        if toptobottom and not lefttoright:
            print("There is percolation from top to bottom")
        elif not toptobottom and lefttoright:
            print("There is percolation from left to right")
        elif toptobottom and lefttoright:
            print("There are both types of percolation")
        else:
            print("There is no percolation")
    
    if toptobottom and not lefttoright:
        return 'toptobottom'
    elif not toptobottom and lefttoright:
        return 'lefttoright'
    elif toptobottom and lefttoright:
        return 'both'
    else:
        return 0

def percolationGraph():
    # Define grids to percolate over
    gridDims = [[5, 5],[10,10],[15,15]]
    # number of tests for each probability
    testsNum = 1000
    
    # 1 over pStep for the number of probabilties tested
    pStep = 0.02
    
    # Array of all the probabilites that are tested
    pArray = np.arange(pStep, 1.0, pStep)
    
    for gridYDim,gridXDim in gridDims:
        # Define an array to hold the percolation ratio for each probability
        percolationRatio = []
        
        for p in pArray:
            percolationCount = 0
            for i in range(testsNum):
                result = percolation(False, gridXDim, gridYDim, p)
                
                if result=='upwards' or result=='lefttoright' or result=='both':
                    percolationCount += 1

            percolationRatio.append(percolationCount/testsNum)

            # Counter in real time so that the user understands if the code has
            # finished running
            print('\r{}x{}: {:.2f}'.format(gridXDim, gridYDim, p), end='')
        
        print()

        plt.plot(pArray, percolationRatio, label='{}x{}, N={}'.format(gridXDim, gridYDim, testsNum))

    plt.legend()
    plt.xlabel("p")
    plt.ylabel("Percolation ratio")

    plt.show()

# Call functions
percolation(True,5,5,0.5)
percolationGraph()
