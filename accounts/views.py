from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.db import transaction

from .forms import UserRegistrationForm, UserAddressForm

User = get_user_model()


class UserRegistrationView(TemplateView):
    template_name = "accounts/user_registration.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy("transactions:transaction_report")
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "registration_form" not in context:
            context["registration_form"] = UserRegistrationForm()

        if "address_form" not in context:
            context["address_form"] = UserAddressForm()

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(request.POST)
        address_form = UserAddressForm(request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            # Create user + bank account
            user = registration_form.save()

            # Create address
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(request, user)

            messages.success(
                request,
                (
                    "Thank you for creating a bank account. "
                    f"Your Account Number is {user.account.account_no}."
                )
            )

            return HttpResponseRedirect(
                reverse_lazy("transactions:deposit_money")
            )

        return self.render_to_response(
            {
                "registration_form": registration_form,
                "address_form": address_form,
            }
        )


class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = "home"

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
