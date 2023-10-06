from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from robots.models import Robot


@method_decorator(csrf_exempt, name='dispatch')
class CreateRobotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            serial = f'{version}-{model}'

            Robot.objects.create(model=model, version=version, created=created, serial=serial)

            return JsonResponse({'message': 'New robot!'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'error'}, status=400)