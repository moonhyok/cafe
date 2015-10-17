from opinion.opinion_core.models import *
from django.contrib import admin
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.db import connection
from opinion.includes.jsonutils import *

def flag_count(comment):
    return comment.flags.count()

class OSAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')

class OSStatementAdmin(admin.ModelAdmin):
    list_display = ('opinion_space', 'statement_number', 'statement')

class DiscussionStatementAdmin(admin.ModelAdmin):
    list_display = ('opinion_space', 'statement', 'is_current')

class OSEigenvectorAdmin(admin.ModelAdmin):
    list_display = ('opinion_space', 'eigenvector_number', 'coordinate_number', 'value', 'is_current', 'created')

class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'opinion_space', 'opinion_space_statement', 'rating', 'is_current')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'discussion_statement', flag_count)
    list_filter = ('is_current',)

class CommentRatingAdmin(admin.ModelAdmin):
    list_display = ('comment', 'rater', 'rating', 'score')
    
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('opinion_space', 'name', 'description', 'image_path', 'ratings_json', 'is_current')
    
class UserDemographicsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'year_born', 'location', 'political_party', 'heard_about')
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback', 'created')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    
class LogHTTPErrorsAdmin(admin.ModelAdmin):
    list_display = ('logger_id', 'is_visitor', 'opinion_space', 'error_type', 'url', 'message', 'created')

class LogUserEventsAdmin(admin.ModelAdmin):
    list_display = ('logger_id', 'is_visitor', 'opinion_space', 'log_type', 'details', 'created')

class LogCommentViewAdmin(admin.ModelAdmin):
    list_display = ('logger_id', 'is_visitor', 'comment', 'created')

class LogCommentsReturnedAdmin(admin.ModelAdmin):
    list_display = ('logger_id', 'is_visitor', 'opinion_space', 'query_type', 'comments_list', 'created')

admin.site.register(OpinionSpace, OSAdmin)
admin.site.register(OpinionSpaceStatement, OSStatementAdmin)
admin.site.register(DiscussionStatement, DiscussionStatementAdmin)
admin.site.register(OpinionSpaceEigenvector, OSEigenvectorAdmin)
admin.site.register(UserRating, UserRatingAdmin)
admin.site.register(DiscussionComment, CommentAdmin)
admin.site.register(CommentRating, CommentRatingAdmin)
admin.site.register(Landmark, LandmarkAdmin)
admin.site.register(UserDemographics, UserDemographicsAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(LogHTTPErrors, LogHTTPErrorsAdmin)
admin.site.register(LogUserEvents, LogUserEventsAdmin)
admin.site.register(LogCommentView, LogCommentViewAdmin)
admin.site.register(LogCommentsReturned, LogCommentsReturnedAdmin)

# Comment admin view
def comment_admin(request):
    if not request.user.is_superuser:
        raise Http404
    
    erase_ids = request.POST.getlist('erase_ids')
    if erase_ids:
        DiscussionComment.objects.filter(id__in = erase_ids).update(is_current = False)
        return HttpResponseRedirect('/admin/comments/')
    
    # Get all flagged comments
    cursor = connection.cursor()
    cursor.execute("""SELECT user_rating_comment.id, user_rating_comment.comment, COUNT(flagged_comment.reporter_id) as flag_count
                      FROM user_rating_comment, flagged_comment
                      WHERE user_rating_comment.is_current = 1 AND flagged_comment.comment_id = user_rating_comment.id
                      GROUP BY user_rating_comment.id
                      ORDER BY flag_count DESC""")
    
    return render_to_response('admin/comments.html', {'comments': cursor.fetchall()})