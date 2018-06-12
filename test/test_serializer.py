

from bid.models import Bid_action
from bid.api.serializers import Bid_actionSerializer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

p = Bid_action.objects.first()
s = Bid_actionSerializer(instance=p, context=serializer_context)

print (s.data)

