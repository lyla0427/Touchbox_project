from django.db.models import Sum

from touchbox.fusioncharts import FusionCharts
from touchbox.models import Competition, Player, TouchMap


def playerList(request):
    season = request.GET.get("season", None)
    players = Player.objects.filter(season=season)
    context = {'players': players, 'season': season, }
    return render(request, 'touchbox/player.html', context)


def playerDetail(request, pk):
    season = request.GET.get("season", None)
    player = Player.objects.get(id=pk)
    competition = Competition.objects.filter(season=season)
    touchmap = TouchMap.objects.filter(player=pk, competition__season=season).order_by("competition__matchdate")

    # COLUMN CHART
    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    columndataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Most Touched Area(aggregate)"
    chartConfig["xAxisName"] = "Most Touched Area"
    chartConfig["yAxisName"] = "Frequency"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["1"] = touchmap.aggregate(Sum("area1"))["area1__sum"]
    chartData["2"] = touchmap.aggregate(Sum("area2"))["area2__sum"]
    chartData["3"] = touchmap.aggregate(Sum("area3"))["area3__sum"]
    chartData["4"] = touchmap.aggregate(Sum("area4"))["area4__sum"]
    chartData["5"] = touchmap.aggregate(Sum("area5"))["area5__sum"]
    chartData["6"] = touchmap.aggregate(Sum("area6"))["area6__sum"]
    chartData["7"] = touchmap.aggregate(Sum("area7"))["area7__sum"]
    chartData["8"] = touchmap.aggregate(Sum("area8"))["area8__sum"]
    chartData["9"] = touchmap.aggregate(Sum("area9"))["area9__sum"]
    chartData["10"] = touchmap.aggregate(Sum("area10"))["area10__sum"]
    chartData["11"] = touchmap.aggregate(Sum("area11"))["area11__sum"]
    chartData["12"] = touchmap.aggregate(Sum("area12"))["area12__sum"]
    chartData["13"] = touchmap.aggregate(Sum("area13"))["area13__sum"]
    chartData["14"] = touchmap.aggregate(Sum("area14"))["area14__sum"]
    chartData["15"] = touchmap.aggregate(Sum("area15"))["area15__sum"]
    chartData["16"] = touchmap.aggregate(Sum("area16"))["area16__sum"]
    chartData["17"] = touchmap.aggregate(Sum("area17"))["area17__sum"]
    chartData["18"] = touchmap.aggregate(Sum("area18"))["area18__sum"]
    chartData["19"] = touchmap.aggregate(Sum("area19"))["area19__sum"]
    chartData["20"] = touchmap.aggregate(Sum("area20"))["area20__sum"]
    chartData["21"] = touchmap.aggregate(Sum("area21"))["area21__sum"]
    chartData["22"] = touchmap.aggregate(Sum("area22"))["area22__sum"]

    columndataSource["chart"] = chartConfig
    columndataSource["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        columndataSource["data"].append(data)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1", "600", "400", "chart-1", "json", columndataSource)

    # SCATTER CHART

    scatterdataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Regression of Most Touched Area and Rating"
    chartConfig["xAxisName"] = "Most Touched Area Percentage"
    chartConfig["yAxisName"] = "Rating"
    chartConfig["theme"] = "fusion"
    chartConfig["xaxisminvalue"] = "20"
    chartConfig["xaxismaxvalue"] = "100"
    chartConfig["ynumberprefix"] = ""
    chartConfig["yaxisminvalue"] = "0"
    chartConfig["xnumbersuffix"] = "%"
    chartConfig["showlegend"] = "0"
    chartConfig[
        "plottooltext"] = "<b>$yDataValue</b> worth <b>$seriesNames</b> were sold,<br>when temperature was <b>$xDataValue</b>"

    categoryConfig = OrderedDict()
    categoryConfig["verticallinedashed"] = "1"
    categoryConfig["verticallinedashlen"] = "1"
    categoryConfig["verticallinedashgap"] = "1"
    categoryConfig["verticallinethickness"] = "1"
    categoryConfig["verticallinecolor"] = "#000000"
    categoryConfig["category"] = [
        {
            "x": "20",
            "label": "20%",
            "showverticalline": "0"
        },
        {
            "x": "40",
            "label": "40%"
        },
        {
            "x": "60",
            "label": "60%"
        },
        {
            "x": "80",
            "label": "80%"
        },
        {
            "x": "100",
            "label": "100%"
        }
    ]

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    for queryset in touchmap:
        chartData["20"] = queryset.rating

    scatterdataSource["chart"] = chartConfig
    scatterdataSource["categories"] = categoryConfig
    scatterdataSource["dataset"] = [{
        "seriesname": "Ice Cream",
        "anchorbgcolor": "5D62B5",
        "showregressionline": "1",
        "regressionlinecolor": "#808080",
        "anchorbordercolor": "#808080",
        "anchorsides": "1",
        "anchorradius": "3",
        "data": [
            {
                "x": "34",
                "y": "0.2"
            },
        ]
    }
    ]

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["x"] = key
        data["y"] = value
        scatterdataSource["dataset"][0]["data"].append(data)

    scatterchartObj = FusionCharts('scatter', 'ex2', '600', '400', 'chart-2', 'json', scatterdataSource)

    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    linedataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Relationship between game and playing time"
    chartConfig["xAxisName"] = "game"
    chartConfig["yAxisName"] = "playing time"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    linedataSource["chart"] = chartConfig
    linedataSource["data"] = []

    chartData = OrderedDict()
    for queryset in touchmap:
        chartData[queryset.competition.opponent] = queryset.playingtime

    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        linedataSource["data"].append(data)

    # linedataSource["data"] = [
    #     {
    #         "label": "barnley",
    #         "value": "89.45"
    #     },
    #     {
    #         "label": "2006",
    #         "value": "89.87"
    #     },
    #     {
    #         "label": "2007",
    #         "value": "89.64"
    #     },
    #     {
    #         "label": "2008",
    #         "value": "90.13"
    #     },
    #     {
    #         "label": "2009",
    #         "value": "90.67"
    #     },
    #     {
    #         "label": "2010",
    #         "value": "90.54"
    #     },
    #     {
    #         "label": "2011",
    #         "value": "90.75"
    #     },
    #     {
    #         "label": "2012",
    #         "value": "90.8"
    #     },
    #     {
    #         "label": "2013",
    #         "value": "91.16"
    #     },
    #     {
    #         "label": "2014",
    #         "value": "91.37"
    #     },
    #     {
    #         "label": "2015",
    #         "value": "91.66"
    #     },
    #     {
    #         "label": "2016",
    #         "value": "91.8"
    #     }
    # ]

    linechartObj = FusionCharts('line', 'ex3', '600', '400', 'chart-3', 'json', linedataSource)
    # data = {
    #     "chart": {
    #         "caption": "Average Fastball Velocity",
    #         "yaxisname": "Velocity (in mph)",
    #         "subcaption": "[2005-2016]",
    #         "numbersuffix": " mph",
    #         "rotatelabels": "1",
    #         "setadaptiveymin": "1",
    #         "theme": "fusion"
    #     },
    #     "data":
    # }

    return render(request, 'touchbox/playerDetail.html',
                  {'output1': column2D.render(), 'chartTitle1': 'Simple Chart Using Array',
                   'output2': scatterchartObj.render(), 'chartTitle2': 'Simple Chart Using Array',
                   'output3': linechartObj.render(), 'chartTitle3': 'Simple Chart Using Array',

                   'player': player,
                   'competitions': competition})


def competitionList(request):
    season = request.GET.get("season", None)
    competition = Competition.objects.filter(season=season)
    context = {'competitions': competition}
    return render(request, 'touchbox/competition.html', context)


def touchMap(request):
    competition = request.GET.get("competition", None)
    player = request.GET.get("player", None)
    player_name = Player.objects.get(id=player).name
    player_number = Player.objects.get(id=player).number
    opponent = Competition.objects.get(id=competition).opponent
    touchmap = TouchMap.objects.get(competition=competition, player=player)
    touchmap_dic = {"area1": touchmap.area1,
                    "area2": touchmap.area2,
                    "area3": touchmap.area3,
                    "area4": touchmap.area4,
                    "area5": touchmap.area5,
                    "area6": touchmap.area6,
                    "area7": touchmap.area7,
                    "area8": touchmap.area8,
                    "area9": touchmap.area9,
                    "area10": touchmap.area10,
                    "area11": touchmap.area11,
                    "area12": touchmap.area12,
                    "area13": touchmap.area13,
                    "area14": touchmap.area14,
                    "area15": touchmap.area15,
                    "area16": touchmap.area16,
                    "area17": touchmap.area17,
                    "area18": touchmap.area18,
                    "area19": touchmap.area19,
                    "area20": touchmap.area20,
                    "area21": touchmap.area21,
                    "area22": touchmap.area22,
                    }

    context = {'touchmap': touchmap_dic, "opponent": opponent, "player_name": player_name,
               "player_number": player_number}
    print(context)
    return render(request, 'touchbox/touchmap.html', context)


from django.shortcuts import render

from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.

# Loading Data from a Ordered Dictionary
# Example to create a column 2D chart with the chart data passed as Dictionary format.
# The `chart` method is defined to load chart data from Dictionary.

# def chart(request):
