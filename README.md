# Test Train Split CLI
## Abstract
This program is a python based CLI that should assist in spliting protein datasets into multiple groups while minimalizing data leakage.  
It achieves this by using a combination of different methods for classifying similarities between chains and splitting the chains based on that information. 


## Code structure 
### Main process
The process is divided into four main parts:
  1. Loading Assets (*class AssetLoader*, *class AssetManager*)
  2. Calculating the similarities between all chains supplied (*class DistanceCalculator*)
  3. Saving the similarities (*class DistanceMatrix*)
  4. Splitting the chains into groups (*class Splitter*)

Each part is represented by a class that needs to implement the respective interface. Types and interfaces are found in a separate [GitHub repository](https://github.com/jiricekcz/test-train-split-common) linked to this as a git submodule. This is done to minimize duplicate code, in cases where other repositories (for example remote workers for distributed calculation of large datasets) need to use the same types.  
  
The currently implemented classes are:
#### AssetLoader
Used to load chains for the process
  - *class FastaAssetLoader* - A simple loader that loads chains from a fasta file.
#### AssetManager
Used to manage the assets during the process. Main purpose is storage
  - *class MemoryAssetManager* - A simple asset manager that holds the chains in memory as strings using python variables.
#### DistanceCalculator
Used to calculate the similarity (distance) between every combination of two chains and fill it into a matrix. This is handled in such a way, that paralelization is an option (both local and remote).
  - *class PairwiseAlignmentDistanceCalculator* - Calculates the distance based on the best pairwise alignment of the two chains. Runs **single core only**. 
#### DistanceMatrix
Used to store the distance data in matrix form. Does not need to be filled sequentially.
  - *class NumpyDistanceMatrix* - Matrix that saves distances as 16 bit integers using *class numpy.ndarray*
  - *class NumpyDistanceMatrixDiskBackup* - a variation of *class NumpyDistanceMatrix*, that saves and loads the matrix in given intervals to the disk.
 #### Splitter
 Used to generate options for splits with different balances between matching the expected group size ratios and minimizing data leakage.
  - *class AglomerativeClusteringSplitter* - Splits the set into a tree using single linkage aglomerative clustring. Then generates splits with gradually increasing number of divisions of the tree. A headstart factor paramater can determine how many splits will happen at a time (can be used to speed up spliting and generate less useless splits).  
The tree is created using scikits *class cluster.AgglomerativeClustering*. It is then transformed into a binary tree structure (saved using the node-references method). The function generates a split for every number of subclusters (the irrelevant ones can be skipped using the headstart factor parameter) in the following way:  
    1. We have:
        - subclusters - Array of tree nodes. Starting value is an array with one element - the root node. 
        - a distance function - Function that determines the distance from perfection of a given distribution of subclusters into the final groups. This function should take into consideration the requested sizes of the final groups and the subclusters currenly in every final group. The exact form of this function is not as important as it seems, as will be explained bellow.
    2. We take all the subclusters and sort them by their leaf count in descending order.
    3. We iterate trough the subclusters and for every subcluster (in descending order) we find a final group, where the distance function is minimized. Then we assign this subcluster to this final group and continue with the next subcluster until all subclusters are assigned into a final group.
    4. We flatten the final groups to include the leaves, not the subclusters.
    5. We calculate the minimal distance between groups (in some cases it can be larger, than determined by the clustering because of imperfections in the algorithm).
    6. We yield the split containing the leafs in each group and a minimal distance matrix for each group.
    7. We split the node with the highest clustering score into two, add them to the subclusters array and remove the original cluster.
    8. If the headstart factor is used, we repeat step 7 mutliple times according to the headstart factor and the value of the distance function for the current split. If the headstart factor is bigger, the number of steps is bigger. If the current split is further from perfection, the number of steps is bigger.
    9. We repeat from step 2 until the iteration is stopped or we split the tree into only leafs.  
  
Notes: The tree has many size 1-5 subclusters from the begining, even if the tree has thousands of leaves in total. This is absolutly expected behaviour, as these small subclusters are chains, that are completly different from the others and as such have no real impact when it comes to data leakage and can essentially be used as infill. Mainly what we are trying to do, is prevent extremely similar chains from being in different final groups, which is achived, because the extremely similar chains will be at the bottom of the tree, not at the top. The fact, that there are many small subclusters also means, that the distribution of subclusters into final groups isn't that difficult, as simply putting the large subclusters where they fit and infilling the rest with microclusters is enough to reach an almost-optimal solution. This problem is a variation of the [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem), so the perfect solution would need to be computed in exponential time which is, for the amount of chains expected, not an option (and extreme overkill for reasons explained above). 
    
### Wrapper
The main process is wrapped in a few wrapper functions, that make space for possible CLI implementations as well as non-CLI usage.  
The main file calls *def pre_use()*, a function, that is run as the first thing in the whole program. If it is imported as a module, then it just exports the API.  
If it is run as CLI (*\_\_name\_\_ == "\_\_main\_\_"*), it runs *def pre_cli_only()*, initilizes *class CLI* and calls *CLI.run()*. *CLI.run()* is then responsible for running the CLI (using the API that would otherwise be exported).

### Utilities
Utility functions
  - *def abs_path(__file, file)* - Used to calculate the absolute path of a file based on the path to the calle. This is used to make the execution predictable regardless of where the program is run from and its current working directory.
 
### Exceptions
Custom exceptions the program can raise
  - *class AssetAppendException* - Exception raised when an asset cannot be appended to the asset manager.

### File structure
All code is in */src/*. Files outside of */src/* are human readable files and config files with selfexplenatory or standardised names.

#### Source folder - */src/*
All code is here. The files in this directory are parts of the wrapper (they do not handle logic of the split, they just provide an interface and place for the CLI code).

#### Common - */src/common/*
The common folder is an imported git submodule containing type definitions.

#### Logic - */src/logic*
The logic folder contains all files with classes regarding the logic of the split itself. Most classes extend (implement) interfaces from */src/common/*. It contains the individual components of the split, not the managing *class SplitManager*.

#### Utilities - */src/util/*
The utils folder contains helper functions, that have an isolated purpouse. This can be for example parsing functions, string formatters, network functions etc.


## Next steps
  - User friendly CLI design  
The program doesn't really have CLI aspect as of now, everything is controlled in *CLI.run()*. The preferable state would be that you can operate the program without touching the Python code itself.
  - More algorithm options
