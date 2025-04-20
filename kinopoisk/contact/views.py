from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Contact
from .forms import ContactForm
# Create your views here.
from django.views.generic import CreateView

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact/tags/form.html"
    # success_url = reverse_lazy("home")  # Убедитесь, что у вас есть URL с именем 'home'
    def get_success_url(self):
        return reverse_lazy('home')  # Явно указываем URL для перенаправления

    # def form_valid(self, form):
    #     # Проверяем, существует ли уже такой email
    #     email = form.cleaned_data['email']
    #     if Contact.objects.filter(email=email).exists():
    #         # Если email уже существует, возвращаем ошибку
    #         form.add_error('email', 'Этот email уже подписан')
    #         return self.form_invalid(form)
        
    #     # Сохраняем форму
    #     self.object = form.save()
    #     return HttpResponseRedirect(self.get_success_url())
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
