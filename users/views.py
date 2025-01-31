
import json
from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_integration import settings

from django.contrib import messages

def send_whatsapp_message(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {"code": "en_US"}
            }
        }

        response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200 and "messages" in response_data:
            messages.success(request, "Message sent successfully!")
        else:
            error_detail = response_data.get("error", {}).get("message", "Failed to send message.")
            messages.error(request, f"Error: {error_detail}")

        return render(request, 'account/homepage.html')

    return render(request, 'account/homepage.html')



@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == 'WEBHOOK_VERIFY_TOKEN':
            return HttpResponse(challenge) 
        return JsonResponse({'error': 'Invalid verification token'}, status=403)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)