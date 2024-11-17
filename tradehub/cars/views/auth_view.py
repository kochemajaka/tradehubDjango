from ..utils.position_required import position_required
from ..utils.imports import *
class TradehubLoginView(LoginView):
    template_name = "login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy("home")

def LogoutView(request):
    logout(request)
    return redirect("login_page")

