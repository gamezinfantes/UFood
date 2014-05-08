from django.db import models
from django.contrib.auth.models import User

class Cliente (models.Model):
	# Referesncia al model de usuarios
	user = models.OneToOneField(User)

	# Atributos extra del cliente

	def __unicode__(self):
		return self.user.username