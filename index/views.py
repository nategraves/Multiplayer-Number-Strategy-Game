from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from giftalink.gifts.forms import GiftForm

def index(request):
	form = GiftForm()
	if request.method == 'POST':
		form = GiftForm(request.POST)
		if form.is_valid():
			new_gift = form.save()
			return HttpResponseRedirect('/gifts/view/%s/' % (new_gift.uuid))
	return render_to_response('index/index.html', {
		'form': form,
	}, context_instance=RequestContext(request))