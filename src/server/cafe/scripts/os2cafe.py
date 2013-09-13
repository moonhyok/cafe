import environ
from cafe.cafe_core.models import *

def create_cafe_user(user):
    cd = DiscussionComment.objects.filter(user = user, is_current=True)
    score = 0
    if len(cd) > 0:
        score = cd[0].normalized_score_sum
        
    eigenvector1 = OpinionSpaceEigenvector.objects.filter(is_current=True,eigenvector_number=0)
    eigenvector2 = OpinionSpaceEigenvector.objects.filter(is_current=True,eigenvector_number=1)
    ratings = UserRating.objects.filter(user=user,is_current=True).order_by('opinion_space_statement')
    x = 0
    y = 0
    if len(ratings) == len(eigenvector1):
	for i in range(0,len(ratings)):
	    x = x + ratings[i].rating*eigenvector1[i].value
	for i in range(0,len(ratings)):
	    y = y + ratings[i].rating*eigenvector2[i].value	
    cu = CafeUser(user = user,participation_score=0,primary_score=score,secondary_score=0,x=x,y=y)
    
    if len(cd) > 0:
        cc = CafeComment(user = cu, title="",comment = cd[0].comment, banished=cd[0].blacklisted, is_current=True,sampling_weight=cd[0].query_weight)
        print cc.comment
        cc.save()
    
    cu.save()
    
    print cu.user.username,x,y

for user in User.objects.all():
    create_cafe_user(user)
    
for statement in OpinionSpaceStatement.objects.all().order_by('statement_number'):
    cp = CafeProposition(statement = statement.statement, gauge_set = True, is_current = True)
    cp.save()
    print statement.statement
    for r in UserRating.objects.filter(opinion_space_statement = statement, is_current=True):
        cpr = CafePropositionRating(is_current=True,value = r.rating, proposition= cp, user = CafeUser.objects.filter(user=r.user)[0])
        cpr.save()
        
for a in CommentAgreement.objects.filter(is_current=True):
    c = CafeComment.objects.filter(user=CafeUser.objects.filter(user=a.comment.user)[0])
    if len(c) > 0:
        ccsr = CafeCommentSecondaryRating(is_current=True, value=a.agreement, comment = c[0], rater = CafeComment.objects.filter(user=CafeUser.objects.filter(user=a.rater)[0] ))
        ccsr.save()
    
for r in CommentRating.objects.filter(is_current=True):
    c = CafeComment.objects.filter(user=CafeUser.objects.filter(user=a.comment.user)[0])
    if len(c) > 0:
        ccpr = CafeCommentPrimaryRating(is_current=True,value=r.rating,comment = c[0], rater = CafeComment.objects.filter(user=CafeUser.objects.filter(user=r.rater)[0] ))
        ccpr.save()
    


