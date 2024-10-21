import json

from django.http import JsonResponse
from django.shortcuts import render

from timefoldai.demo_data import generate_demo_data, DemoData
from timefoldai.domain import Timetable
from timefoldai.solver import solver_manager

data_sets = {}


# Create your views here.
def index(request):
    timetable = generate_demo_data(demo_data=DemoData(value='SMALL'))
    data_sets['ID'] = timetable
    solver_manager.solve_and_listen('ID', timetable,
                                    lambda solution: update_timetable('ID', solution))


def update_timetable(problem_id: str, timetable: Timetable):
    global data_sets
    data_sets[problem_id] = timetable


def get(request):
    return JsonResponse(data_sets['ID'].model_dump_json(), safe=False)


def timetable_view(request):
    # Assuming 'data_sets["ID"]' contains your timetable JSON string
    timetable_data = json.loads(data_sets["ID"].model_dump_json())  # Convert the JSON string to a Python dictionary


    return render(request, 'timetable.html', {'timetable': timetable_data})