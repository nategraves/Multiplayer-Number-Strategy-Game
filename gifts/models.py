from django.db import models
from giftalink.plusplus.models import ModelBase

def pkgen():
    from base64 import b32encode
    from hashlib import sha1
    from random import random
    rude = ('fuck', 'shit', 'cunt', 'ass', 'hell', 'damn', 'fuk', 'bitch', 'bastard', 'kike','pussy','dick','cock')
    bad_pk = True
    while bad_pk:
        pk = b32encode(sha1(str(random())).digest()).lower()[:10]
        bad_pk = False
        for rw in rude:
            if pk.find(rw) >= 0: bad_pk = True
    return pk

class Gift(ModelBase):
	gift_to = models.CharField(max_length=255)
	gift_from = models.CharField(max_length=255)
	message = models.TextField(blank=True, null=True)
	url = models.URLField(verify_exists=True)
	uuid = models.CharField(max_length=8, default=pkgen)

	class Meta:
		db_table = 'gift'
	
	def __unicode__(self):
		return ("%s gifted to %s from %s" % (self.url, self.gift_to, self.gift_from))