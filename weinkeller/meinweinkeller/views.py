from django.shortcuts import render
from django.http import JsonResponse
from .models import Wine, Tasting
import json
from datetime import datetime
import uuid

def meinweinkeller(request):
    return render(request, 'index.html')

def importweine(request):
    return render(request, 'import.html')

def import_api(request):
    if request.method == 'POST':
        try:
            json_data = request.POST.get('json_data')
            if json_data:
                wines_data = json.loads(json_data)
                imported_count = 0

                for wine_data in wines_data:
                    # Convert string ID to UUID
                    wine_id = uuid.UUID(wine_data['id'])
                    
                    # Get or create wine
                    wine, created = Wine.objects.update_or_create(
                        id=wine_id,
                        defaults={
                            'type': wine_data.get('type', ''),
                            'winename': wine_data.get('winename', ''),
                            'year': wine_data.get('year', ''),
                            'alcohol': wine_data.get('alcohol'),
                            'price': wine_data.get('price'),
                            'currency': wine_data.get('currency'),
                            'wineryName': wine_data.get('wineryName', ''),
                            'wineryLocation': wine_data.get('wineryLocation', ''),
                            'wineryWebsite': wine_data.get('wineryWebsite', ''),
                            'originCountry': wine_data.get('originCountry', ''),
                            'originRegion': wine_data.get('originRegion', ''),
                            'merchantName': wine_data.get('merchantName', ''),
                            'merchantWebsite': wine_data.get('merchantWebsite', ''),
                            'tastingnotes': wine_data.get('tastingnotes', ''),
                            'bottlesbought': wine_data.get('bottlesbought', 0),
                        }
                    )

                    # Handle tastings
                    if 'tastings' in wine_data and wine_data['tastings']:
                        for tasting_data in wine_data['tastings']:
                            tasting_id = uuid.UUID(tasting_data['id'])
                            tasting_date = datetime.strptime(
                                tasting_data['tastingdate'], 
                                "%Y-%m-%dT%H:%M:%SZ"
                            )
                            
                            Tasting.objects.update_or_create(
                                id=tasting_id,
                                defaults={
                                    'wine': wine,
                                    'tastingdate': tasting_date,
                                    'degurating': tasting_data.get('degurating'),
                                    'degunotes': tasting_data.get('degunotes', ''),
                                    'foodpairing': tasting_data.get('foodpairing', ''),
                                    'bottlesDrunken': tasting_data.get('bottlesDrunken', 0),
                                }
                            )

                    imported_count += 1

                return JsonResponse({
                    'success': True,
                    'message': f'Successfully imported {imported_count} wines'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No JSON data received'
                })
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid JSON format: {str(e)}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Method not allowed'
        })