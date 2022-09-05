# Test Train Split CLI
## Abstract
This program is a python based CLI that should assist in spliting protein datasets into multiple groups while minimalizing data leakage.  
It can achive this using a combination of different methods for classifying similarity between chains and methods for spliting the chains based on that information.  


## Code structure 
### Main process
The process is divided into four main parts:
  1. Loading Assets (*class AssetLoader*, *class AssetManager*)
  2. Calculating the similarity between all chains supplied (*class DistanceCalculator*)
  3. Saving the similarities (*class DistanceMatrix*)
  4. Splitting the chains into groups (*class Splitter*)

Each part is represented by a class that needs to implement the respective interface. Types and interfaces are found in a separate [GitHub repository](https://github.com/jiricekcz/test-train-split-common) linked to this as a git submodule. This is done to minimize duplicate code, in cases where other repositories (for example remote workers for distributed calculation of large datasets) need to use the same types.  
  
The currently implemented classes are:
#### AssetLoader
Used to load chains for the process
  - *class FastaAssetLoader* - A simple loader that loads chains from a fasta file
#### AssetManager
Used to manage the assets during the process. Main purpose is storage
  - *class MemoryAssetManager* - A simple asset manager, that holds the chains in memory as strings using python variables
#### DistanceCalculator
Used to calculate the similarity (distance) between every combination of two chains a fill it into a matrix. Handled in such way, that paralelization is an option (both local and remote).
  - *class PairwiseAlignmentDistanceCalculator* - Calculates the distance based on the best pairwise alignment of the two chains. Runs **single core only**. 
#### DistanceMatrix
Used to store the distance data in a matrix form. Does not need to be filled sequentially.
  - *class NumpyDistanceMatrix* - Matrix that saves distances as 16 bit integers using *class numpy.ndarray*
  - *class NumpyDistanceMatrixDiskBackup* - a variation of the *class NumpyDistanceMatrix*, that saves and loads the matrix in given intervals to the disk.
 #### Splitter
 Used to generate options for splits with different balances between matching the expected group size ratios and minimizing data leakage.
  - *class AglomerativeClusteringSplitter* - Splits the set into a tree using single linkage aglomerative clustring. Then generates splits with gradually increasing number of divisions of the tree. A headstart factor paramater can determine how many splits will happen at a time (can be used to speed up spliting and generate less useless splits)
 
### Wrapper
The main process is wrapped in a few wrapper functions, that make space for possible CLI implementations as well as non-CLI usage.  
The main file calls *def pre_use()*, a function, that is run as the first thing in the whole program. If it is imported as a module, then it just exports the API.  
If it is run as CLI (*__name__ == "__main__"*), it runs *def pre_cli_only()*, initilizes *class CLI* and calls *CLI.run()*. *CLI.run()* is then responsible for running the CLI (using the API that would otherwise be exported).

### Utilities
Utility functions
  - *def abs_path(__file, file)* - Used to calculate the absolute path of a file based on the path to the calle. This is used to make the execution predictable regardless of where the program is run from and its current working directory.
 
### Exceptions
Custom exceptions the program can raise
  - *class AssetAppendException* - Exception raised when an asset cannot be appended to the asset manager.


## Next steps
  - User friendly CLI design
  - More algorithm options
