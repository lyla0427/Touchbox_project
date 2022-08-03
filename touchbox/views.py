from django.db.models import Q, Sum

from touchbox.fusioncharts import FusionCharts
from touchbox.models import Competition, Player, TouchMap


def playerList(request):
    season = request.GET.get("season", None)
    players = Player.objects.filter(season=season)
    context = {'players': players, 'season': season, }
    return render(request, 'touchbox/player.html', context)


def playerDetail(request, pk):
    season = request.GET.get("season", None)
    player = Player.objects.get(id=pk, season=season)
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
    mta_list = list(touchmap.values_list("most_touched_area", flat=True))
    for i in range(1, 22):
        chartData[f"{i}"] = mta_list.count(i)

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

    # The `chartConfig` dict contains key-value pairs data for chart attribute

    categoryConfig = OrderedDict()
    categoryConfig["verticallinedashed"] = "1"
    categoryConfig["verticallinedashlen"] = "1"
    categoryConfig["verticallinedashgap"] = "1"
    categoryConfig["verticallinethickness"] = "1"
    categoryConfig["verticallinecolor"] = "#000000"
    categoryConfig["category"] = [
        {
            "x": "0",
            "label": "0%",
            "showverticalline": "0"
        },
        {
            "x": "20",
            "label": "20%",
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
    mta_string = player.most_touched_area
    mta_list = mta_string.split(',')
    scatter_chart_dic = {"output2_1": "",
                         "output2_2": "",
                         "output2_3": "",
                         "output2_4": "",
                         "output2_5": ""}
    for i in range(0, len(mta_list)):
        scatterdataSource = OrderedDict()
        chartConfig = OrderedDict()
        chartConfig["xAxisName"] = "Most Touched Area Percentage"
        chartConfig["yAxisName"] = "Rating"
        chartConfig["theme"] = "fusion"
        chartConfig["xaxisminvalue"] = "0"
        chartConfig["xaxismaxvalue"] = "100"
        chartConfig["ynumberprefix"] = ""
        chartConfig["yaxisminvalue"] = "0"
        chartConfig["xnumbersuffix"] = "%"
        chartConfig["showlegend"] = "0"
        chartConfig[
            "plottooltext"] = "The player's rating was <b>$yDataValue</b>, <br>when the area was touched <b>$xDataValue</b> in the game"
        chartConfig["caption"] = f"Regression of Most Touched Area({mta_list[i]}) and Rating"
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
            ]
        }
        ]
        chartData = OrderedDict()
        for queryset in touchmap:
            if queryset.most_touched_area == int(mta_list[i]):
                total = queryset.total if queryset.total != 0 else 1
                most_touched_area = mta_list[i]
                mta_dic = {
                    "1": queryset.area1,
                    "2": queryset.area2,
                    "3": queryset.area3,
                    "4": queryset.area4,
                    "5": queryset.area5,
                    "6": queryset.area6,
                    "7": queryset.area7,
                    "8": queryset.area8,
                    "9": queryset.area9,
                    "10": queryset.area10,
                    "11": queryset.area11,
                    "12": queryset.area12,
                    "13": queryset.area13,
                    "14": queryset.area14,
                    "15": queryset.area15,
                    "16": queryset.area16,
                    "17": queryset.area17,
                    "18": queryset.area18,
                    "19": queryset.area19,
                    "20": queryset.area20,
                    "21": queryset.area21,
                    "22": queryset.area22,
                }
                mtc_percentage = round(mta_dic[most_touched_area] / total, 5) * 100
                if queryset.rating != 0:
                    chartData[mtc_percentage] = queryset.rating

        # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
        # The data for the chart should be in an array wherein each element of the array is a JSON object
        # having the `label` and `value` as keys.

        # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
        for key, value in chartData.items():
            data = {}
            data["x"] = key
            data["y"] = value
            scatterdataSource["dataset"][0]["data"].append(data)
            scatter_chart_dic[f"output2_{i + 1}"] = FusionCharts('scatter', f'ex2-{i + 1}', '600', '400',
                                                                 f'chart-2-{i + 1}',
                                                                 'json',
                                                                 scatterdataSource)

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

    linechartObj = FusionCharts('line', 'ex3', '600', '400', 'chart-3', 'json', linedataSource)

    # soccerfieldChart

    soccerfieldChart = OrderedDict()
    total = touchmap.aggregate(total=Sum("total", default=1))["total"]
    area_list = ["area1",
                 "area2",
                 "area3",
                 "area4",
                 "area5",
                 "area6",
                 "area7",
                 "area8",
                 "area9",
                 "area10",
                 "area11",
                 "area12",
                 "area13",
                 "area14",
                 "area15",
                 "area16",
                 "area17",
                 "area18",
                 "area19",
                 "area20",
                 "area21",
                 "area22"
                 ]
    soccerfieldChart["area1"] = round(
        touchmap.aggregate(area=Sum("area1", filter=Q(area1__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area2"] = round(
        touchmap.aggregate(area=Sum("area2", filter=Q(area2__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area3"] = round(
        touchmap.aggregate(area=Sum("area3", filter=Q(area3__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area4"] = round(
        touchmap.aggregate(area=Sum("area4", filter=Q(area4__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area5"] = round(
        touchmap.aggregate(area=Sum("area5", filter=Q(area5__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area6"] = round(
        touchmap.aggregate(area=Sum("area6", filter=Q(area6__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area7"] = round(
        touchmap.aggregate(area=Sum("area7", filter=Q(area7__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area8"] = round(
        touchmap.aggregate(area=Sum("area8", filter=Q(area8__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area9"] = round(
        touchmap.aggregate(area=Sum("area9", filter=Q(area9__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area10"] = round(
        touchmap.aggregate(area=Sum("area10", filter=Q(area10__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area11"] = round(
        touchmap.aggregate(area=Sum("area11", filter=Q(area11__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area12"] = round(
        touchmap.aggregate(area=Sum("area12", filter=Q(area12__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area13"] = round(
        touchmap.aggregate(area=Sum("area13", filter=Q(area13__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area14"] = round(
        touchmap.aggregate(area=Sum("area14", filter=Q(area14__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area15"] = round(
        touchmap.aggregate(area=Sum("area15", filter=Q(area15__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area16"] = round(
        touchmap.aggregate(area=Sum("area16", filter=Q(area16__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area17"] = round(
        touchmap.aggregate(area=Sum("area17", filter=Q(area17__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area18"] = round(
        touchmap.aggregate(area=Sum("area18", filter=Q(area18__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area19"] = round(
        touchmap.aggregate(area=Sum("area19", filter=Q(area19__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area20"] = round(
        touchmap.aggregate(area=Sum("area20", filter=Q(area20__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area21"] = round(
        touchmap.aggregate(area=Sum("area21", filter=Q(area21__gt=1), default=0))["area"] / total, 5) * 100
    soccerfieldChart["area22"] = round(
        touchmap.aggregate(area=Sum("area22", filter=Q(area22__gt=1), default=0))["area"] / total, 5) * 100
    renderData = {'output1': column2D.render(), 'chartTitle1': 'Column',
                  'output3': linechartObj.render(), 'chartTitle3': 'line',
                  'output4': soccerfieldChart, 'chartTitle5': 'soccer',
                  'player': player,
                  'competitions': competition}

    for key, value in scatter_chart_dic.items():
        if value != "":
            renderData[key] = value.render()
    return render(request, 'touchbox/playerDetail.html',
                  renderData)


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
    total = touchmap.total if touchmap.total != 0 else 1
    touchmap_percentage_dic = {"area1": round(touchmap.area1 / total, 5) * 100,
                               "area2": round(touchmap.area2 / total, 5) * 100,
                               "area3": round(touchmap.area3 / total, 5) * 100,
                               "area4": round(touchmap.area4 / total, 5) * 100,
                               "area5": round(touchmap.area5 / total, 5) * 100,
                               "area6": round(touchmap.area6 / total, 5) * 100,
                               "area7": round(touchmap.area7 / total, 5) * 100,
                               "area8": round(touchmap.area8 / total, 5) * 100,
                               "area9": round(touchmap.area9 / total, 5) * 100,
                               "area10": round(touchmap.area10 / total, 5) * 100,
                               "area11": round(touchmap.area11 / total, 5) * 100,
                               "area12": round(touchmap.area12 / total, 5) * 100,
                               "area13": round(touchmap.area13 / total, 5) * 100,
                               "area14": round(touchmap.area14 / total, 5) * 100,
                               "area15": round(touchmap.area15 / total, 5) * 100,
                               "area16": round(touchmap.area16 / total, 5) * 100,
                               "area17": round(touchmap.area17 / total, 5) * 100,
                               "area18": round(touchmap.area18 / total, 5) * 100,
                               "area19": round(touchmap.area19 / total, 5) * 100,
                               "area20": round(touchmap.area20 / total, 5) * 100,
                               "area21": round(touchmap.area21 / total, 5) * 100,
                               "area22": round(touchmap.area22 / total, 5) * 100,
                               }

    context = {'touchmap': touchmap_dic, 'touchmap_percentage': touchmap_percentage_dic, "opponent": opponent,
               "player_name": player_name,
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
