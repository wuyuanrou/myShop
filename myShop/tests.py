from django.test import TestCase


# Create your tests here.
def like_activities(activity_list, like_list, cart_list):
    like_activity_list = [like.activity_id for like in like_list]
    cart_activity_list = [cart.activity_id for cart in cart_list]
    result = []
    for activity in activity_list:
        isLike = True if activity in like_activity_list else False
        isCart = True if activity in cart_activity_list else False
        like_activity = {
            'activity': activity,
            'isLike': isLike,
            'isCart': isCart
        }
        result.append(like_activity)
    return result


def raw_activities(activity_list):
    result = []
    for activity in activity_list:
        like_activity = {
            'activity': activity,
            'isLike': False,
            'isCart': False
        }
        result.append(like_activity)
    return result
