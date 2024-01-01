from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
import datetime, os

from .forms import (
    CompleteUserForm,
    UserUpdateForm,
)
from .models import (
    UserProfile,
    dinoName,
    strikeType,
    banLength,
    Rule,
    revTicket,
)


# Base views (login, logout, initialize admin, welcome, index) #
@user_passes_test(lambda user: not User.objects.filter(is_superuser=True).exists(), login_url='login_view')
def initialize_admin(request):
    print("Initialize admin request received")
    if User.objects.filter(is_superuser=True).exists():
        print("Admin users exists")
        return redirect('index')  # Redirect to home page if admin users already exist

    if request.method == 'POST':
        form = CompleteUserForm(request.POST)
        password = request.POST.get('password')
        print("Password: " + str(password))
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            
            user.save()
            return redirect('login_view')  # Redirect to the login page
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CompleteUserForm()

    return render(request, 'registration/initialize_admin.html', {'form': form})

def welcome(request):
    if not User.objects.filter(is_superuser=True).exists():
        print("No admin users exist")
        return redirect('initialize_admin')  # Redirect to the initialize_admin view if no admin users exist
    else:
        print("Admin users exists")
        return redirect('index')  # Redirect to the home view if admin users exist

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Redirect to the home page or dashboard
        else:
            # Return an 'invalid login' error message
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required
@csrf_exempt
def index(request):
    print("Index request received")
    return render(request, 'staff/index.html')

@login_required
class HeaderSearch(LoginRequiredMixin, TemplateView):
    template_name = 'staff/search.html'
    pass
    

# STAFF VIEWS #
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'staff/user_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        return context

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    template_name = 'staff/editprofile.html'

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        user = form.instance.user
        user.email = form.cleaned_data['email']
        user.save()
        return super(UserUpdateView, self).form_valid(form)

    def test_func(self):
        user_profile = self.get_object()
        return self.request.user == user_profile.user

    def get_object(self, queryset=None):
        # Assuming you're using the user's ID in the URL
        return UserProfile.objects.get(user__pk=self.kwargs['pk'])

class ticketList(LoginRequiredMixin, ListView):
    pass

class ticketDetail(LoginRequiredMixin, DetailView):
    pass

class ticketUpdate(LoginRequiredMixin, UpdateView):
    pass

class ticketDelete(LoginRequiredMixin, DeleteView):
    pass

class ticketCreate(LoginRequiredMixin, TemplateView):
    template_name = 'staff/ticket_create.html'


# ADMIN VIEWS #
# User views (list, update, delete, create) #
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin/user_list.html'
    context_object_name = 'users'
    ordering = ['username']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'admin/user_delete.html'
    success_url = '/staff/users'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'staff/user_create.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False



# Server Configs #
# @login_required
# def GameConfig(request):
#     # Game Config File
#     # config_file =  'S:\Servers\BoB\WindowsServer\BeastsOfBermuda\Saved\Config\WindowsServer\Game.ini'
#     config_file = '/ticketApp/database/game/game.ini'
#     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     if request.method == 'POST':
#         form = ConfigForm(request.POST)
#         if form.is_valid():
#             os.rename(config_file, config_file + "_" + dt + ".ini")
#             with open(config_file, 'w') as f:
#                 f.write(form.cleaned_data.get('config'))
#                 f.close()
#             return redirect('kits:game_config')
#     else:
#         form = ConfigForm()
#         f = open(config_file, 'r+')
#         file_content = f.read()
#         f.close()
#         form.fields['config'].initial = file_content
#         return render(request, 'kits/server_config.html', {'form': form})

# @login_required
# def ServerConfig(request):
#     # Server Config File
#     # config_file = 'S:\Utils\Server Watchdog\server.settings'
#     config_file = '/ticketApp/database/server/server.settings'
#     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     if request.method == 'POST':
#         form = ConfigForm(request.POST)
#         if form.is_valid():
#             os.rename(config_file, config_file + "_" + dt + ".settings")
#             with open(config_file, 'w') as f:
#                 f.write(form.cleaned_data.get('config'))
#                 f.close()
#             return redirect('kits:server_config')
#     else:
#         form = ConfigForm()
#         f = open(config_file, 'r+')
#         file_content = f.read()
#         f.close()
#         form.fields['config'].initial = file_content
#         return render(request, 'kits/server_config.html', {'form': form})


# TEMPLATES #

def about(request):
    return render(request, 'ltr/about.html')

def accordion(request):
    return render(request, 'ltr/accordion.html')

def alerts(request):
    return render(request, 'ltr/alerts.html')

def avatarradius(request):
    return render(request, 'ltr/avatarradius.html')

def avatarround(request):
    return render(request, 'ltr/avatarround.html')

def avatarsquare(request):
    return render(request, 'ltr/avatarsquare.html')

def badge(request):
    return render(request, 'ltr/badge.html')

def blog(request):
    return render(request, 'ltr/blog.html')

def breadcrumbs(request):
    return render(request, 'ltr/breadcrumbs.html')

def buttons(request):
    return render(request, 'ltr/buttons.html')

def calendar(request):
    return render(request, 'ltr/calendar.html')

def calendar2(request):
    return render(request, 'ltr/calendar2.html')

def cards(request):
    return render(request, 'ltr/cards.html')

def carousel(request):
    return render(request, 'ltr/carousel.html')

def cart(request):
    return render(request, 'ltr/cart.html')

def chart(request):
    return render(request, 'ltr/chart.html')

def chartchartist(request):
    return render(request, 'ltr/chartchartist.html')

def chartdonut(request):
    return render(request, 'ltr/chartdonut.html')

def chartechart(request):
    return render(request, 'ltr/chartechart.html')

def chartflot(request):
    return render(request, 'ltr/chartflot.html')

def chartline(request):
    return render(request, 'ltr/chartline.html')

def chartmorris(request):
    return render(request, 'ltr/chartmorris.html')

def chartnvd3(request):
    return render(request, 'ltr/chartnvd3.html')

def chartpie(request):
    return render(request, 'ltr/chartpie.html')

def charts(request):
    return render(request, 'ltr/charts.html')

def chat(request):
    return render(request, 'ltr/chat.html')

def checkout(request):
    return render(request, 'ltr/checkout.html')

def colors(request):
    return render(request, 'ltr/colors.html')

def construction(request):
    return render(request, 'ltr/construction.html')

def counters(request):
    return render(request, 'ltr/counters.html')

def cryptocurrencies(request):
    return render(request, 'ltr/cryptocurrencies.html')

def datatable(request):
    return render(request, 'ltr/datatable.html')

def dropdown(request):
    return render(request, 'ltr/dropdown.html')

def editprofile(request):
    return render(request, 'ltr/editprofile.html')

def email(request):
    return render(request, 'ltr/email.html')

def emailservices(request):
    return render(request, 'ltr/emailservices.html')

def empty(request):
    return render(request, 'ltr/empty.html')

def error400(request):
    return render(request, 'ltr/error400.html')

def error401(request):
    return render(request, 'ltr/error401.html')

def error403(request):
    return render(request, 'ltr/error403.html')

def error404(request):
    return render(request, 'ltr/error404.html')

def error500(request):
    return render(request, 'ltr/error500.html')

def error503(request):
    return render(request, 'ltr/error503.html')

def faq(request):
    return render(request, 'ltr/faq.html')

def footers(request):
    return render(request, 'ltr/footers.html')

def forgotpassword(request):
    return render(request, 'ltr/forgotpassword.html')

def formadvanced(request):
    return render(request, 'ltr/formadvanced.html')

def formelements(request):
    return render(request, 'ltr/formelements.html')

def formvalidation(request):
    return render(request, 'ltr/formvalidation.html')

def formwizard(request):
    return render(request, 'ltr/formwizard.html')

def gallery(request):
    return render(request, 'ltr/gallery.html')

def headers(request):
    return render(request, 'ltr/headers.html')

def icons(request):
    return render(request, 'ltr/icons.html')

def icons2(request):
    return render(request, 'ltr/icons2.html')

def icons3(request):
    return render(request, 'ltr/icons3.html')

def icons4(request):
    return render(request, 'ltr/icons4.html')

def icons5(request):
    return render(request, 'ltr/icons5.html')

def icons6(request):
    return render(request, 'ltr/icons6.html')

def icons7(request):
    return render(request, 'ltr/icons7.html')

def icons8(request):
    return render(request, 'ltr/icons8.html')

def icons9(request):
    return render(request, 'ltr/icons9.html')

def icons10(request):
    return render(request, 'ltr/icons10.html')

def invoice(request):
    return render(request, 'ltr/invoice.html')

def list(request):
    return render(request, 'ltr/list.html')

def loaders(request):
    return render(request, 'ltr/loaders.html')

def lockscreen(request):
    return render(request, 'ltr/lockscreen.html')

# def login(request):
#     return render(request, 'ltr/login.html')

def maps(request):
    return render(request, 'ltr/maps.html')

def maps1(request):
    return render(request, 'ltr/maps1.html')

def maps2(request):
    return render(request, 'ltr/maps2.html')

def mediaobject(request):
    return render(request, 'ltr/mediaobject.html')

def modal(request):
    return render(request, 'ltr/modal.html')

def navigation(request):
    return render(request, 'ltr/navigation.html')

def notify(request):
    return render(request, 'ltr/notify.html')

def pagination(request):
    return render(request, 'ltr/pagination.html')

def panels(request):
    return render(request, 'ltr/panels.html')

def pricing(request):
    return render(request, 'ltr/pricing.html')

def profile(request):
    return render(request, 'ltr/profile.html')

def progress(request):
    return render(request, 'ltr/progress.html')

def rangeslider(request):
    return render(request, 'ltr/rangeslider.html')

def rating(request):
    return render(request, 'ltr/rating.html')

def register(request):
    return render(request, 'ltr/register.html')

def scroll(request):
    return render(request, 'ltr/scroll.html')

def search(request):
    return render(request, 'ltr/search.html')

def services(request):
    return render(request, 'ltr/services.html')

def shop(request):
    return render(request, 'ltr/shop.html')

def shopdescription(request):
    return render(request, 'ltr/shopdescription.html')

def sweetalert(request):
    return render(request, 'ltr/sweetalert.html')

def tables(request):
    return render(request, 'ltr/tables.html')

def tabs(request):
    return render(request, 'ltr/tabs.html')

def tags(request):
    return render(request, 'ltr/tags.html')

def terms(request):
    return render(request, 'ltr/terms.html')

def thumbnails(request):
    return render(request, 'ltr/thumbnails.html')

def timeline(request):
    return render(request, 'ltr/timeline.html')

def tooltipandpopover(request):
    return render(request, 'ltr/tooltipandpopover.html')

def treeview(request):
    return render(request, 'ltr/treeview.html')

def typography(request):
    return render(request, 'ltr/typography.html')

def userslist(request):
    return render(request, 'ltr/userslist.html')

def widgets(request):
    return render(request, 'ltr/widgets.html')

def wishlist(request):
    return render(request, 'ltr/wishlist.html')

def wysiwyag(request):
    return render(request, 'ltr/wysiwyag.html')
