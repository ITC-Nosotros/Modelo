from django.shortcuts import render, HttpResponse
from .forms import CarForm
from .models import CarSelection
from .car_recommended import recommend_and_predict, load_and_prepare_data
import pandas as pd
# Create your views here.
def homepage(request):

    return render(request,'ProyectoWebApp/homepage.html')
def contact(request):

    return render(request,'ProyectoWebApp/contact.html')

def homepage(request):
    success = False
    similar_cars = None
    predicted_price = None
    user_input = {}
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
        

        car_choice = form.cleaned_data.get("car_choice")
        location = form.cleaned_data.get("location")
        price_range = form.cleaned_data.get("price_range")
        km_range = form.cleaned_data.get("km_range")
        yearmodel_range = form.cleaned_data.get("yearmodel_range")

        user_input = {
                'car_model': car_choice,
                'location': location,
                'price': price_range,
                'kms': km_range,
                'year_model' : yearmodel_range
            }
        
        
        data, model = load_and_prepare_data()

            # Convertir los datos del usuario en un DataFrame
        test_data_recommended = pd.DataFrame([user_input])

            # Obtener coches similares y precio predicho j
        similar_cars, predicted_price = recommend_and_predict(test_data_recommended, data, model)

        success = True

    else:
        form = CarForm()

    return render(request, 'ProyectoWebApp/homepage.html', {'form': form, 'success': success, 'similar_cars': similar_cars,'predicted_price': predicted_price})