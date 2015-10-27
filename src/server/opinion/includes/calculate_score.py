
import numpy as np
from opinion.opinion_core.models import *

def get_score(comment):
	"""
	Returns the score (average rating + 2 SDs)
	of comment, and the SD
	"""
        ca = CommentAgreement.objects.filter(comment=comment)
        result = (np.nan,)
        rating_se = np.nan
        if ca.count() > 0:
                ca_vl = ca.values_list('agreement')
                rating_mean = np.mean(ca_vl)
                rating_se = 1.96*np.std(ca_vl)/np.sqrt(ca.count())
                result = (rating_mean + rating_se, ca.count(), comment)
        return result[0], rating_se
