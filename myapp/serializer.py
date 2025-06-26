from rest_framework import serializers
from .models import match

# used for listing all matches and creating new match
# if a match isnt over it will show the current score, teamp batting and the innings
# if its over then it shows the score of both teams and then who won 
class matchserializer(serializers.ModelSerializer):
    class Meta:
        model= match
        exclude = ['team1runs', 'team1wickets', 'innings']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.innings == 3: # we start with inning = 1 then inning 2, when its over, the match is over and inning is 3
            winner = instance.bawlingteam  if instance.team1runs > instance.runs else instance.battingteam

            rep = {
                'id': instance.id, #instance.pk bhi chlti
                'TEAM 1': f"{instance.bawlingteam} Scored {instance.team1runs}-{instance.team1wickets}",
                'TEAM 2': f"{instance.battingteam} Scored {instance.runs}-{instance.wickets}",
                'WINNER': winner
            }
        return rep

class patchmatchserializer(serializers.ModelSerializer):

    class Meta:
        model = match
        fields = ['runs', 'wickets', 'wideballs', 'balls', 'batsman', 'bawler']
        read_only_fields = ['team1runs', 'team1wickets', 'innings']

    def update(self,instance,validated_data):
        instance = super().update(instance, validated_data)
        if instance.wickets == 10 or instance.balls == 300:
            instance.innings+=1
            if instance.innings == 2:
                instance.team1runs = instance.runs
                instance.team1wickets = instance.wickets
                instance.battingteam, instance.bawlingteam = instance.bawlingteam, instance.battingteam
                instance.runs = 0
                instance.wickets = 0
                instance.balls = 0
                instance.wideballs = 0
                instance.batsman = ""
                instance.bawler = ""
            instance.save()
        return instance

    def to_representation(self,instance):
        rep = super().to_representation(instance)
        if instance.innings==3:
            winner = instance.bawlingteam  if instance.team1runs > instance.runs else instance.battingteam
            rep = {'WINNING TEAM': winner}
        return rep