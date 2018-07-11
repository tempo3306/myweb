import pickle

from myweb.wsgi import *
from django.contrib.auth.models import User, Group
from bid.models import Bid_hander, Bid_auction
from forums.models import Topic, Board, ForumUser
from django.contrib.auth.models import Group, Permission
from bid.models import Yanzhengma
import pickle

def create_new_yanzhengma():
    with open('color0_300.pkl', 'rb') as yfile:
        name_qa = pickle.load(yfile)
        print(name_qa)
    query_list = []
    lenth_name_qa = len(name_qa)

    for i in range(lenth_name_qa):
        lenth = len(name_qa[i][1])
        for j in range(lenth):
            query_list.append(Yanzhengma(picture=name_qa[i][0],
                                         question=name_qa[i][1][j][0],
                                         answer=name_qa[i][1][j][1],
                                         ))
    Yanzhengma.objects.bulk_create(query_list)




if __name__ == '__main__':
    create_new_yanzhengma()