from django.db import models
from django.contrib.auth.models import User

import random

class League(models.Model):
    name=models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Team(models.Model):
    user = models.ForeignKey(User)
    league = models.ForeignKey(League)
    name=models.CharField(max_length=30)
    wins=models.IntegerField(default=0)
    loss=models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Game(models.Model):
    team_1 = models.ForeignKey(Team, related_name="team_1")
    team_2 = models.ForeignKey(Team, related_name="team_2")
    week = models.IntegerField()
    #Game's results are randomly generated, but they do make use of player ratings which means
    #teams with higher skilled players are more likely to win.

    def __unicode__(self):
        return u'%s vs %s ' %(self.team_1, self.team_2)

    def generate_result():
        pass
        #insert whatever logic we're going to use to decide the results here.

class Player(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=40)
    #should be date field
    date_of_birth = models.CharField(max_length=20, null=True, blank=True)
    college = models.CharField(max_length=20, null=True, blank=True)
    is_active = False
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

    #Probably not the most accurate random rating general, but it's a start
    def generate_ratings(self):
        #Accounting for running quarterbacks. "Traditional" pocket passers will on
        #average pass better, but they will rarely gain rushing points.
        if self.position=='QB':
            if random.randint%4==0:
                passing_ability=models.IntegerField(default=random.randint(50, 95))
                rushing_ability=models.IntegerField(default=random.randint(25, 60))
            else:
                rushing_ability=models.IntegerField(default=random.randint(0,25))
                passing_ability=models.IntegerField(default=random.randint(70, 99))
        elif self.position=='RB':
            rushing_ability=models.IntegerField(default=random.randint(65, 99))
            receiving_ability=models.IntegerField(default=random.randint(20, 45))
        elif self.position=='WR':
            rushing_ability=models.IntegerField(default=random.randint(0,20))
            receiving_ability=models.IntegerField(default=random.randint(70, 99))
        elif self.position=='TE':
            receiving_ability=models.IntegerField(default=random.randint(50, 95))
    #missing rushing in this calculation
    def calculate_points():
        return (receiving_yards/10)+(passing_yards/25)+(receiving_touchdowns*6)+(passing_touchdowns*4)

class Statistic(models.Model):
    #receiving and rushing touchdowns/yards are worth the same so I'm lumping them into one attribute.
    player = models.ForeignKey(Player)
    receiving_yards=models.IntegerField()
    passing_yards=models.IntegerField()
    receiving_touchdowns=models.IntegerField()
    passing_touchdowns=models.IntegerField()