from opinion.settings import *
from opinion.opinion_core.models import *
from math import sqrt, pow

def calculate_reputation_score(os_id, comment_rater, comment_ratee, comment_rating, constant_offset=False):
    """
    Takes the comment rater, comment ratee, and comment rating, and produces
    a reputation score
    """
    score = None
    rater_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = comment_rater))
    ratee_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = comment_ratee))
    new_bounds_comment_rating = change_rating_bounds(comment_rating)
    # If either rater or ratee have no ratings, return False
    if len(rater_ratings) == 0 or len(ratee_ratings) == 0:
        return None
    else:
        distance = get_euclidean_distance(rater_ratings, ratee_ratings)
        if distance is False:
            return None
        vector_length = len(rater_ratings)
        min_ratings = list(change_rating_bounds(MIN_RATING) for i in range(0, vector_length))
        max_ratings = list(change_rating_bounds(MAX_RATING) for i in range(0, vector_length))
        max_distance = get_euclidean_distance(min_ratings, max_ratings)
        if new_bounds_comment_rating >= 0:
            score = new_bounds_comment_rating * distance
        else:
            score = abs(new_bounds_comment_rating) * (distance - max_distance)
        # offset all values to positive value
        if constant_offset:
            score += max_distance * change_rating_bounds(MAX_RATING)
    return score

def calculate_distance(os_id, comment_rater, comment_ratee):
    distance = None
    rater_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = comment_rater))
    ratee_ratings = compress_user_ratings_objects(os_id, UserRating.objects.filter(is_current = True, opinion_space = os_id, user = comment_ratee))
    # If either rater or ratee have no ratings, return False
    if len(rater_ratings) == 0 or len(ratee_ratings) == 0:
        return None
    else:
        distance = get_euclidean_distance(rater_ratings, ratee_ratings)
    return distance
        
def compress_user_ratings_objects(os_id, user_rating_objects):
    """
    Compresses user ratings objects into a single list of ratings,
    and also changes the bounds of those ratings from (0, 1) to (-1, 1)
    """
    user_ratings_list = []
    user_ratings_dict = {}
    for user_rating_object in user_rating_objects:
        statement_number = user_rating_object.opinion_space_statement.statement_number
        rating = user_rating_object.rating
        user_ratings_dict[statement_number] = rating
    num_statements = len(OpinionSpaceStatement.objects.filter(opinion_space = os_id))
    for i in range(0, num_statements):
        user_ratings_list.append(change_rating_bounds(user_ratings_dict.get(i, ((MAX_RATING - MIN_RATING) / 2))))
    return user_ratings_list
    
def change_rating_bounds(rating):
    """
    Changes bounds from (0, 1) to (-1, 1)
    """
    return (rating * 2) - 1
    
def get_euclidean_distance(list_1, list_2):
    """
    Returns the euclidean distance between two lists (vectors)
    """
    pre_sqrt_sum = 0
    # If the two lists are not the same length, return False
    if len(list_1) != len(list_2):
        return False
    for i in range(0, len(list_1)):
         pre_sqrt_sum += pow((list_1[i] - list_2[i]), 2)
    distance = sqrt(pre_sqrt_sum)
    return distance