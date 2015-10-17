from sklearn.decomposition import PCA
import numpy
import algorithm_api as api

class PrincipalComponentAnalysis(api.Algorithm):

	''' @param targetMatrix must be a numpy array.
		@param nComponents is the number of desired components after PCA.
	'''
	def __init__(self, targetMatrix, nComponents):
		self.matrix = targetMatrix
		self.numComponents = nComponents

	def setTargetMatrix(self, targetMatrix, inputDim):
		self.matrix = targetMatrix
		self.startingDimension = inputDim

	def setTargetDimension(self, desiredDim):
		self.targetDimension = desiredDim

	''' Call this function to execute PCA.
		@return principal components
	'''
	def runAlgorithm(self):
		pca = PCA(n_components=self.numComponents)
		pca.fit(self.matrix)
		return pca.components_