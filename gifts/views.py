from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from giftalink.gifts.models import Gift
from giftalink.gifts.forms import GiftForm

def view(request, uuid):
	gift = get_object_or_404(Gift, uuid=uuid)
	return render_to_response('gifts/view.html',{
		'gift': gift,
	}, context_instance=RequestContext(request))