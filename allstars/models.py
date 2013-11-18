from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Q
from django.contrib.auth.models import User
import random

class League(models.Model):
    name=models.CharField(max_length=30)
    week=models.IntegerField()
    draft_index=models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s' %(self.name)

class Team(models.Model):
    team_name=models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User)
    league = models.ForeignKey(League)
    wins=models.IntegerField(default=0)
    loss=models.IntegerField(default=0)

   # def __init__(self, team_name,user):
   #     self.team_name=team_name
   #     self.league=League.objects.all()[0]

    def __unicode__(self):
        return u'%s' %(self.team_name)

class Game(models.Model):
    team_1 = models.ForeignKey(Team, related_name="team_1")
    team_2 = models.ForeignKey(Team, related_name="team_2")
    week = models.IntegerField()
    #Game's results are randomly generated, but they do make use of player ratings which means
    #teams with higher skilled players are more likely to win.

    def __unicode__(self):
        return u'%s vs %s ' %(self.team_1, self.team_2)

    def generate_result(self):
        for player in Player.objects.filter(Q(team=self.team_1) | Q(team=self.team_2)).filter(is_active=True):
            stat=Statistic(player=player,game=self,week=self.week)
            rush_rating=((int(player.rushing_ability)+random.randint(1,50))/1.5) if int(player.rushing_ability) > 0 else 0
            pass_rating=((int(player.passing_ability)+random.randint(1,50))/1.5) if int(player.passing_ability) > 0 else 0
            catch_rating=((int(player.receiving_ability)+random.randint(1,50))/1.5) if int(player.receiving_ability) > 0 else 0
            stat.rushing_yards=rush_rating*1.5
            stat.rushing_touchdowns=rush_rating/30
            stat.passing_yards=pass_rating*2.9
            stat.passing_touchdowns =pass_rating/24
            stat.receiving_yards=catch_rating*1.2
            stat.receiving_touchdowns=catch_rating/35
            stat.save()

class Player(models.Model):
    team = models.ForeignKey(Team,default=None, null=True, blank=True)
    name = models.CharField(max_length=40)
    #should be date field
    date_of_birth = models.CharField(max_length=20, null=True, blank=True)
    college = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    position = models.CharField(max_length=2,
                            choices=(
                                ('QB', 'Quarterback'),
                                ('RB', 'Running Back'),
                                ('WR', 'Wide Receiver'),
                                ('TE', 'Tight End'),
                            )
                        )

    passing_ability = models.IntegerField(default=0)
    rushing_ability = models.IntegerField(default=0)
    receiving_ability = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "{{settings.ABS_URL}}player/%s" %name

    def as_dict(self):
        return {'name':self.name}

    def generate_ratings(self):
        if self.position=='QB':
            if random.randint(100,199)%4==0:
                self.passing_ability=random.randint(50, 90)
                self.rushing_ability=random.randint(10, 40)
            else:
                self.rushing_ability=random.randint(0,7)
                self.passing_ability=default=random.randint(70, 99)
        elif self.position=='RB':
            self.rushing_ability=random.randint(65, 99)
            self.receiving_ability=random.randint(0, 15)
        elif self.position=='WR':
            self.receiving_ability=random.randint(70, 99)
        elif self.position=='TE':
            self.receiving_ability=random.randint(50, 95)
    #missing rushing in this calculation
    def calculate_points():
        return (receiving_yards/10)+(passing_yards/25)+(receiving_touchdowns*6)+(passing_touchdowns*4)

class Statistic(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    week = models.IntegerField()
    rushing_yards=models.IntegerField()
    rushing_touchdowns=models.IntegerField()
    receiving_yards=models.IntegerField()
    receiving_touchdowns=models.IntegerField()
    passing_yards=models.IntegerField()
    passing_touchdowns=models.IntegerField()