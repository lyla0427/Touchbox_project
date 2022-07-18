from django.shortcuts import render

from touchbox.models import Competition, Players, TouchMap


def playerList(request):
    season = request.GET.get("season", None)
    players = Players.objects.filter(season=season)
    context = {'players': players}
    return render(request, 'touchbox/player.html', context)


def playerDetail(request, pk):
    season = request.GET.get("season", None)
    print(season)
    player = Players.objects.get(id=pk)
    competition = Competition.objects.filter(season=season)
    context = {'player': player, 'competitions': competition}
    return render(request, 'touchbox/playerDetail.html', context)


def competitionList(request):
    season = request.GET.get("season", None)
    competition = Competition.objects.filter(season=season)
    context = {'competitions': competition}
    return render(request, 'touchbox/competition.html', context)


def touchMapDetail(request):
    touchmap = TouchMap.objects.all()
    context = {'touchmap': touchmap}
    return render(request, 'touchbox/touchmap.html', context)
