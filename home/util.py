import random
from routing.models import feedback


def otp_handler():
    # generate otp
    otp = random.randint(100000, 999999)
    # send otp to user
    # return otp
    return otp

def cal_feedback(username):
    user_feedbacks = feedback.objects.filter(user = username)
    max_rating = user_feedbacks.__len__() * 5
    print(max_rating)
    total_rating = 0
    for i in user_feedbacks:
        total_rating = total_rating + i.rating
    
    if max_rating == 0:
        return 0
    else:
        return (total_rating/max_rating)*100