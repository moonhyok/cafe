import environ
from opinion.opinion_core.models import *
import numpy as np
from scipy.stats.stats import pearsonr

np.set_printoptions(threshold=np.nan)

LIMIT = 100

comments = list(DiscussionComment.objects.filter(blacklisted=False).order_by('id')) [-LIMIT:]
users = list(User.objects.all().order_by('id')) [-LIMIT:]
means, ratings = {}, {}

for i, comment in enumerate(comments):
    comment_ratings = CommentRating.objects.filter(comment=comment)
    means[i] = np.mean(comment_ratings.values_list('rating') or 0)
    for r in comment_ratings:
        ratings[(r.rater.id, comment.id)] = r.rating

num_users = len(users)
        
# comment_vec[i] is a vector of length num_users, with all ratings of comment i
comment_vec = {}
for c, comment in enumerate(comments):
    v = np.zeros(num_users)
    for u, user in enumerate(users):
        v[u] = ratings.get((user.id, comment.id), 0)
    comment_vec[c] = v

N = len(comments)
D = np.zeros((N, N))
W = np.zeros((N, N))
for i in range(N):
    w = 0
    for j in range(N):
        coeff, pval = pearsonr(comment_vec[i], comment_vec[j])
        if np.isnan(coeff):
            coeff = 0
        W[i][j] = (1 - coeff)**2 * (means[i] + means[j])
        w += W[i][j]
    D[i][i] = w

# Solve (D - W)v = \lambda D v
eigenvalues, eigenvectors = np.linalg.eig(np.identity(N) - np.linalg.inv(D) * W)

# score vector corresponds to the second highest eigenvalue
second_highest_eigenvalue = np.sort(eigenvalues)[-2]
e_index = np.where(eigenvalues == second_highest_eigenvalue)
# print eigenvectors[e_index]
