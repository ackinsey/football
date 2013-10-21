from django import forms
from django.core.exceptions import ValidationError

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
	team_name=forms.CharField(max_length=30)
	password=forms.CharField(max_length=30)
	password_retype=forms.CharField(max_length=30)
	email_address=forms.EmailField()

	players=forms.ModelMultipleChoiceField(
		queryset=League.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True
		)

	def clean_form(self):
		if Team.objects.filter(team_name=self.team_name):
			raise ValidationError('ERROR: That team name exists')
			if Team.objects.filter(email_address=self.email_address):
				raise ValidationError('ERROR: That email address is taken')
				if self.password != self.passwordretype:
					raise ValidationError('ERROR: Your two passwords don\'t match')
