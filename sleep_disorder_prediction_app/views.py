from django.shortcuts import render
from joblib import load

model = load('savedModels\sleep_disorder_model.joblib')

def form(request):
    return render(request,'index.html')

def predictor(request):
    if request.method =='POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = float(request.POST.get('age'))
        occupation = request.POST.get('occupation')
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        heartRate = float(request.POST.get('heartRate'))
        systolicPressure = float(request.POST.get('systolicPressure'))
        diastolicPressure = float(request.POST.get('diastolicPressure'))
        activityLevel = float(request.POST.get('activityLevel'))
        dailySteps = float(request.POST.get('dailySteps'))
        sleepDuration = float(request.POST.get('sleepDuration'))
        sleepQuality = float(request.POST.get('sleepQuality'))
        stressLevel = float(request.POST.get('stressLevel'))

        gender_mapping = {'Female': 0, 'Male': 1,'Others':2}
        occupation_mapping = {
        'Accountant': 0, 'Doctor': 1, 'Engineer': 2, 'Lawyer': 3, 'Manager': 4,
        'Nurse': 5, 'Sales Representative': 6, 'Salesperson': 7, 'Scientist': 8,
        'Software Engineer': 9, 'Teacher': 10,'Others':11}

        encoded_gender = gender_mapping[gender]
        encoded_occupation = occupation_mapping[occupation]

        height_m = height / 100

        # Calculate BMI
        bmi = weight / (height_m ** 2)

        # Classify BMI according to the given 'BMI Category' mapping
        bmi_category_mapping = {'Normal': 0, 'Obese': 1, 'Overweight': 2, 'Underweight': 3}
        bmi_category = None

        if bmi < 18.5:
            bmi_category = bmi_category_mapping['Underweight']
        elif 18.5 <= bmi < 24.9:
            bmi_category = bmi_category_mapping['Normal']
        elif 25 <= bmi < 29.9:
            bmi_category = bmi_category_mapping['Overweight']
        else:
            bmi_category = bmi_category_mapping['Obese']
        
        features = [
            float(encoded_gender), age, float(encoded_occupation), sleepDuration, sleepQuality, activityLevel,
            stressLevel, float(bmi_category), heartRate, dailySteps, systolicPressure, diastolicPressure
        ]
        
        y_pred = model.predict([features])

        if y_pred[0] == 0:
            y_pred = 'Insomnia'
        elif y_pred[0] == 1:
            y_pred = 'No Sleep Disorder'
        elif y_pred[0] == 2:
            y_pred = 'Sleep Apnea'
        
        return render(request,'result.html',{'name':name,'result':y_pred})
    
    return render(request,'index.html')    
        








