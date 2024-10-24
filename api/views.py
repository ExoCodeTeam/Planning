import json
import logging

import redis as red
from django.http import JsonResponse
from django.shortcuts import render
from timefold.solver import SolverJob, SolverStatus

from Planning import settings
from timefoldai.demo_data import generate_demo_data, DemoData
from timefoldai.domain import Timetable
from timefoldai.solver import solver_manager
from celery import shared_task

redis_client = red.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def index(request):
    calculate.delay()
    timetable_data_json = redis_client.get('ID')

    if timetable_data_json:
        timetable_data = json.loads(timetable_data_json)
        return render(request, 'timetable.html', {'timetable': timetable_data})
    else:
        timetable_data = None
        return render(request, 'loading.html')


@shared_task
def calculate():
    timetable = generate_demo_data(demo_data=DemoData(value='LARGE'))
    redis_client.set('ID', timetable.model_dump_json())
    solver_manager.solve_and_listen('ID', timetable,
                                    lambda solution: update_timetable('ID', solution))
    status = solver_manager.get_solver_status('ID')

    def update_timetable(problem_id: str, updated_timetable: Timetable):
        global timetable
        print(status)
        if status == SolverStatus.SOLVING_ACTIVE:
             timetable = updated_timetable
        elif status == SolverStatus.NOT_SOLVING:
             timetable = updated_timetable
             redis_client.set(problem_id, updated_timetable.model_dump_json())



def get(request):
    return JsonResponse(json.loads(redis_client.get('ID')), safe=False)


def timetable_view(request):
    timetable_data = redis_client.get('ID').dict()

    return render(request, 'timetable.html', {'timetable': timetable_data})
