from pca_class import PrincipalComponentAnalysis as pcamdp

################### Principal Component Analysis using MDP ##########################

def pca_mdp(X, inputDim, desiredDim):
    """
    
    PCA using MDP library and training nodes, code for which is in pca_class.PrincipalComponentAnalysis
    
    @param X: 2-dimensional matrix of number data. 
    @type X: numpy array
    
    @param standardize: Wheter X should be standardized or not.
    @type standardize: bool

    @param inputDim: rank of X
    @type inputDim: int

    @param desiredDim: desired rank after PCA
    @type desiredDim: int
    
    @return: 2-dimensional matrix after PCA
    @type return: numpy array

    """
    pcaAlgo = pcamdp(X, inputDim, desiredDim)
    return pcaAlgo.runAlgorithm()