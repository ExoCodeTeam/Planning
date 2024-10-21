from django.http import JsonResponse

from timefoldai.demo_data import generate_demo_data,DemoData
from timefoldai.domain import Timetable
from timefoldai.solver import solver_manager

data_sets = {}

# Create your views here.
def index(request):
        timetable = generate_demo_data(demo_data=DemoData(value='SMALL')).model_dump_json()
        data_sets['ID'] = timetable
        solver_manager.solve_and_listen('ID', timetable,
                                        lambda solution: update_timetable('ID', solution))

def update_timetable(problem_id: str, timetable: Timetable):
    global data_sets
    data_sets[problem_id] = timetable

def get(request):
    return JsonResponse(data_sets['ID'], safe=False)