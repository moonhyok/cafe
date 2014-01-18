from django.db.models import *
from django.contrib.auth.models import User
from opinion.settings_local import CONFIGURABLES


class ZipCode(Model):
    # TODO: should be primary key next time we rebuild database
    code = CharField(max_length=5, db_index = True)
    city = TextField()
    state = CharField(max_length=2)
    county = TextField()

class ZipCodeLog(Model):
    user = ForeignKey(User)
    location = ForeignKey(ZipCode)

class NeverSeenCache(Model):
	#value = CharField(max_length = 8192)
	value = TextField()
	created = DateTimeField(auto_now_add = True, db_index = True)
	class Meta:
		db_table = 'never_seen_cache'
		
class ReviewerScore(Model):
	user = ForeignKey(User, db_index = True, blank = True, null = True)
	reviewer_score = FloatField(null = True)
	#normalized_reviewer_score = FloatField(null = True)
	#num_current_ratings = IntegerField(null = True)
	class Meta:
		db_table = 'reviewer_score'
	
class UserDemographics(Model):
    user = ForeignKey(User, db_index = True, blank = True, null = True)
    gender = CharField(max_length = 1, choices = (('M', 'Male'), ('F', 'Female')), blank = True)
    year_born = SmallIntegerField(blank = True, null = True)
    location = CharField(max_length = 30, blank = True)
    political_party = CharField(max_length = 128, blank = True)
    heard_about = CharField(max_length = 1024, blank = True)
    
    class Meta:
        db_table = 'user_demographics'

class UserSettings(Model):
    user = ForeignKey(User, db_index = True)
    key = CharField(max_length = 128, db_index = True)
    value = CharField(max_length = 1024)
    updated = DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'user_settings'

class BanishedUser(Model):
	user = ForeignKey(User, related_name='banished', db_index = True)
	banisher = ForeignKey(User)
	created = DateTimeField(auto_now_add = True)
	
	class Meta:
		db_table = 'banished_user'
	
class OpinionSpace(Model):
    name = CharField(max_length = 128, unique = True)
    created_by = ForeignKey(User)
    created = DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'opinion_space'

# If an is_current field is ever added to this, make sure to go through and fix all queries using this table
class OpinionSpaceStatement(Model):
    opinion_space = ForeignKey(OpinionSpace, related_name = 'statements', db_index = True)
    statement_number = PositiveSmallIntegerField()
    statement = CharField(max_length = 512)
    short_version = CharField(max_length = 128)
    created = DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.statement
        
    class Meta:
        db_table = 'opinion_space_statement'
        ordering = ['statement_number']

class DiscussionStatement(Model):
    opinion_space = ForeignKey(OpinionSpace, related_name = 'discussion_statements', db_index = True)
    statement = CharField(max_length = 512)
    short_version = CharField(max_length = 512)
    is_current = BooleanField(db_index = True)
    created = DateTimeField(auto_now_add = True, db_index = True)
    
    def __unicode__(self):
        return self.statement
        
    class Meta:
        db_table = 'discussion_statement'

class OpinionSpaceEigenvector(Model):
    opinion_space = ForeignKey(OpinionSpace, related_name = 'eigenvectors', db_index = True)
    eigenvector_number = PositiveSmallIntegerField()
    coordinate_number = PositiveSmallIntegerField()
    value = FloatField()
    is_current = BooleanField(db_index = True)
    created = DateTimeField(auto_now_add = True)
        
    class Meta:
        db_table = 'opinion_space_eigenvector'
        ordering = ['eigenvector_number', 'coordinate_number']

class UserRating(Model):
    user = ForeignKey(User, db_index = True)
    opinion_space = ForeignKey(OpinionSpace, related_name = 'ratings', db_index = True)
    opinion_space_statement = ForeignKey(OpinionSpaceStatement, related_name = 'ratings', db_index = True)
    rating = FloatField()
    is_current = BooleanField(db_index = True)
    created = DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return unicode(self.rating)
        
    class Meta:
        db_table = 'user_rating'
        ordering = ['user', 'opinion_space_statement']

class DiscussionComment(Model):
    user = ForeignKey(User, db_index = True)
    opinion_space = ForeignKey(OpinionSpace, related_name = 'comments', db_index = True)
    discussion_statement = ForeignKey(DiscussionStatement, related_name = 'comments', db_index = True)
    comment = CharField(max_length = 1024)
    average_rating = FloatField(null = True)
    average_score = FloatField(null = True)
    score_sum = FloatField(null = True)
    normalized_score = FloatField(null = True)
    normalized_score_sum = FloatField(null = True)
    confidence = FloatField(null = True)
    blacklisted = BooleanField()
    is_current = BooleanField(db_index = True)
    query_weight = FloatField(null = True, db_index = True)
    created = DateTimeField(auto_now_add = True, db_index = True)
    
    def __unicode__(self):
        return unicode(self.comment)
    
    class Meta:
        db_table = 'discussion_comment'

# Represents an internal text-tag of a comment, for classification
class AdminCommentTag(Model):
    comment = ForeignKey(DiscussionComment)
    tag = TextField()

class CachedRisingComment(Model):
	comment = ForeignKey(DiscussionComment, db_index = True)
	updated = DateTimeField(auto_now_add = True)

	class Meta:
		db_table = 'cached_rising_comment'	

class AdminApprovedComment(Model):
	comment = ForeignKey(DiscussionComment, db_index = True)
	admin = ForeignKey(User)
	created = DateTimeField(auto_now_add = True)
	
	class Meta:
		db_table = 'admin_approved_comment'
	

class CommentRating(Model):
    comment = ForeignKey(DiscussionComment, related_name = 'ratings', db_index = True)
    rater = ForeignKey(User, db_index = True)
    rating = FloatField(db_index = True)
    score = FloatField(db_index = True, null = True, blank = True)
    #z_score = FloatField(db_index = True, null = True, blank = True)
    reviewer_score = FloatField(db_index = True, null = True, blank = True)
    is_current = BooleanField(db_index = True)
    early_bird = NullBooleanField(db_index = True, blank = True)
    created = DateTimeField(auto_now_add = True, db_index = True)
    
    def __unicode__(self):
        return unicode(self.rating)
    
    class Meta:
        db_table = 'comment_rating'
        ordering = ['-created']

class CommentAgreement(Model):
    comment = ForeignKey(DiscussionComment, related_name = 'agreeance', db_index = True)
    rater = ForeignKey(User, db_index = True)
    agreement = FloatField(db_index = True)
    is_current = BooleanField(db_index = True)
    created = DateTimeField(auto_now_add = True, db_index = True)
    
    def __unicode__(self):
        return unicode(self.rating)
    
    class Meta:
        db_table = 'comment_agreement'
        ordering = ['-created']
		
class Landmark(Model):
    opinion_space = ForeignKey(OpinionSpace, related_name = 'landmarks', db_index = True)
    name = CharField(max_length = 64)
    description = CharField(max_length = 256)
    guess_text = CharField(max_length = 256, blank = True)
    image_path = CharField(max_length = 128)
    ratings_json = CharField(max_length = 256)
    is_current = BooleanField(db_index = True)
    created = DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'landmark'
                        
# User feedback models

class FlaggedComment(Model):
    comment = ForeignKey(DiscussionComment, related_name = 'flags', db_index = True)
    reporter = ForeignKey(User)
    created = DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'flagged_comment'

class Feedback(Model):
    user = ForeignKey(User, null = True, blank = True)
    feedback = TextField()
    created = DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'feedback'

# Logging models

class Visitor(Model):
    user = ForeignKey(User, null = True, blank = True)
    created = DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'visitor'

# For Errors
class LogHTTPErrors(Model):
	logger_id = IntegerField(db_index = True)
	is_visitor = BooleanField(db_index = True) 
	opinion_space = ForeignKey(OpinionSpace, db_index = True)
	error_type = SmallIntegerField(db_index = True)
	url = CharField(max_length = 100, db_index = True)
	message = CharField(max_length = 250, db_index = True) 
	created = DateTimeField(auto_now_add = True, db_index = True)

	class Meta:
		db_table = 'log_http_errors'
		ordering = ['-created']

# For User Events
class LogUserEvents(Model):
	logger_id = IntegerField(db_index = True)
	is_visitor = BooleanField(db_index = True)
	opinion_space = ForeignKey(OpinionSpace, db_index = True)
	log_type = SmallIntegerField(db_index = True)
	details = CharField(max_length = 124, blank = True, null = True, default = None)
	created = DateTimeField(auto_now_add = True, db_index = True)

	#class variables for event types
	login = 0
	logout = 1
	sys_load = 2
	sys_exit = 3
	first_time_incomplete = 10
	notification_detail = 'ViewNotifications'
	
	"""
	From Log.as in Flash Client code:
	public static const USER_LEAVE:int = 4;
	public static const USER_BUTTONCLICK:int = 5;
	public static const USER_PLOTCLICK:int = 6;
	public static const USER_CLICKUSERDOT:int = 7;
	"""

	class Meta:
		db_table = 'log_user_events'

# Comment Events
class LogCommentView(Model):
	logger_id = IntegerField(db_index = True)
	is_visitor = BooleanField(db_index = True)
	comment = ForeignKey(DiscussionComment, db_index = True)
	created = DateTimeField(auto_now_add = True, db_index = True)

	class Meta:
		db_table = 'log_comment_view'

class LogCommentsReturned(Model):
	logger_id = IntegerField(db_index = True)
	is_visitor = BooleanField(db_index = True)
	opinion_space = ForeignKey(OpinionSpace, db_index = True)
	query_type = SmallIntegerField(db_index = True)
	comments_list = CharField(max_length = 4096, db_index = True)
	created = DateTimeField(auto_now_add = True, db_index = True)


	#class variables for event codes
	unrated = 0; # get unrated users and shuffle
	leaderboard = 1; # leaderboard
	i_rated= 2; # users i've rated
	rated_by = 3; # users who have rated me

	class Meta:
		db_table = 'log_comments_returned'

class LogLandmarkView(Model):
    logger_id = IntegerField(db_index = True)
    is_visitor = BooleanField(db_index = True)
    opinion_space = ForeignKey(OpinionSpace, db_index = True)
    landmark = ForeignKey(Landmark, db_index = True)
    landmark_name = CharField(max_length = 128)
    created = DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        db_table = 'log_landmark_view'

class LogLandmarkRatingsShown(Model):
    logger_id = IntegerField(db_index = True)
    is_visitor = BooleanField(db_index = True)
    opinion_space = ForeignKey(OpinionSpace, db_index = True)
    landmark = ForeignKey(Landmark, db_index = True)
    ratings_shown_json = CharField(max_length = 256)
    created = DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        db_table = 'log_landmark_ratings_shown'

#Admin Panel users model
class AdminPanelUser(Model):
	user = ForeignKey(User, db_index = True)
	created = DateTimeField(auto_now_add = True)
	
	class Meta:
		db_table = 'adminpanel_users'

class ProfanityFlaggedComment(Model):
    comment = ForeignKey(DiscussionComment, db_index = True)
    profanity = CharField(max_length = 512)
    original_words = CharField(max_length = 512)
    created = DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'profanity_flagged_comment'

class ProfanityFlaggedUsername(Model):
    user = ForeignKey(User, db_index = True)
    profanity = CharField(max_length = 30)
    created = DateTimeField(auto_now = True)

    class Meta:
        db_table = 'profanity_flagged_username'

class ForeignCredential(Model):
	user = ForeignKey(User, db_index = True)
	foreignid = CharField(max_length = 64)

	class Meta:
		db_table = 'foreign_credential'

class UserData(Model):
    user = ForeignKey(User, db_index = True)
    key = CharField(max_length = 128, db_index = True)
    value = CharField(max_length = 1024)
    updated = DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'user_data'

class EntryCode(Model):
	username = CharField(max_length = 30)
	code = CharField(max_length = 64)
	first_login = BooleanField(db_index = True)

	class Meta:
		db_table = 'entry_code'

class Suggestion(Model):
	suggester = ForeignKey(User, db_index = True)
	comment = ForeignKey(DiscussionComment, db_index = True)
	suggestion = CharField(max_length = 1024)
	q = FloatField(null = True)
	score = FloatField(null = True)	
	created = DateTimeField(auto_now_add = True)
	updated = DateTimeField(auto_now = True)

	class Meta:
		db_table = 'suggestion'

class SuggesterScore(Model):
	user = ForeignKey(User,db_index = True)
	score_sum = FloatField(null = True)
	normalized_score_sum = FloatField(null = True)

	class Meta:
		db_table = 'suggester_score'
		
class SettingsManager(Manager):		
	def get_settings(self, key):
		setting = Settings.objects.filter(key=key)
		if len(setting) > 0:
			setting = setting[0].value
		elif key in CONFIGURABLES:
			setting = CONFIGURABLES[key]['default']
		else:
			setting = None
		return setting
	
	def boolean(self, key):
		return self.get_settings(key) == u'true'
	
	def int(self, key):
		val = self.get_settings(key)
		if val:
			return int(val)
		else:
			return None
	
	def string(self, key):
		return self.get_settings(key)
		
	def float(self, key):
		val = self.get_settings(key)
		if val:
			return float(val)
		else:
			return None
	
	
class Settings(Model):
	key = CharField(max_length = 128)
	value = CharField(max_length = 10240)
	updated = DateTimeField(auto_now = True)
	objects = SettingsManager()
	    
	class Meta:
		db_table = 'settings'
		
