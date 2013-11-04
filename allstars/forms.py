from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from allstars.models import Player, Team, League

class RosterForm(forms.Form):
    players=forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    def clean_players(self):
		active_roster=[]
		num_qb=0
		num_rb=0
		num_wr=0
		num_te=0

		for plyr in self.cleaned_data['players']:
			active_roster.append(plyr)
			plyr.is_active=True
			if plyr.position=='QB':
				num_qb+=1
			elif plyr.position=='RB':
				num_rb+=1
			elif plyr.position=='WR':
				num_wr+=1
			elif plyr.position=='TE':
				num_te+=1
		if num_qb != 1 or num_rb == 0 or num_wr < 3 or num_te == 0:
			raise ValidationError('ERROR: You must select 1 QB, at least 1 RB, at least 3 WR, and at least one TE.')		
		if len(active_roster) != 7:
			raise ValidationError('ERROR: You must select exactly 7 players!')		
	
class RegisterForm(forms.Form):
	username=forms.CharField(max_length=30)
	team_name=forms.CharField(max_length=30)
	password=forms.CharField(widget=forms.PasswordInput())
	password_retype=forms.CharField(widget=forms.PasswordInput())
	email_address=forms.EmailField()

	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']):
			raise ValidationError('ERROR: That username exists')
			if User.objects.filter(email=self.cleaned_data['email_address']):
				raise ValidationError('ERROR: That email address is taken')
				if self.cleaned_data['password'] != self.cleaned_data['password_retype']:
					raise ValidationError('ERROR: Your two passwords don\'t match')
