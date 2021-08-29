from rest_framework import viewsets
from apps.users.serializers import UserSerializer
from apps.users.models import User
from django.shortcuts import redirect,render

class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
def activate(request):
    if request.method == 'POST':
        email = request.POST.get('email_data')
        print(email)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return redirect('http://www.youtube.com')
    return render(request, 'users/email-confirm.html', {'email': email})
