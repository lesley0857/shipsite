from django.shortcuts import render
from django.template.loader import render_to_string
import base64
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage,send_mail
from django.utils import timezone
from django.contrib.auth.models import Group
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from.forms import  *
from django.contrib.admin.views.decorators import staff_member_required
import datetime
import folium
from django.contrib import messages
from django.utils.encoding import is_protected_type,force_str,smart_str,force_bytes,force_text,smart_bytes,smart_text,DjangoUnicodeDecodeError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,get_list_or_404,_get_queryset
from django.views.generic import View,DetailView,TemplateView

# Create your views here.
from allauth.account.views import SignupView
from .decorator import *
from django.db.models.signals import post_save
from allauth.utils import build_absolute_uri

class CustomAllauthAdapter(DefaultAccountAdapter):
    def send_mail(self,template_prefix,email,context):
        account_confirm_email = 'accounts/confirm-email'
        context['activate_url'] = (
            settings.BASE_URL + account_confirm_email + context['key']
        )
        msg = self.render_mail(template_prefix,email,context)
        msg.send()

def res_page(request):
    # this page deletes all users that do not have a customer attached
    all_users = User.objects.all()
    all_cust = Customer.objects.all()
    all_cust_cont = customer_container.objects.all()
    for i in all_cust_cont:
        if i.tracking_number == None:
            print(i, 'has no tracking no:')
            c = customer_container.objects.get(id=i.id)
            c.delete()

    # loop 1
    for i in all_users:
        d = 0
        #loop 2
        for j in all_cust:
            if i.username == j.user.username:
                print('match',i,'matches',j)
                d = 1
                break
        # after the loop 2 runs each time this if statement will check if there is a match
        if d != 1:
            print(i,'does not match')
            try:
                c = User.objects.get(id=i.id)
                c.delete() # this deletes all users that have an ufinshed registration or no customer model
            except:
                pass






global u
u=''
class AccountSignupView(DetailView,SignupView):
    # Signup View extended
    success_url = 'tracking:home'
    # change template's name and path
    template_name = "account/signup.html"



    def get_object(self,**kwargs):
        k = self.kwargs.get('id')
        print(k)
        global u
        u= k
        #userr = User.objects.get(username=k)
        #customer = Customer.objects.get(user=userr)
        try:
            userr = User.objects.get(username=k)
            print('true')
            return k

        except:
            print('klo')
            return redirect('invalid_view')

 # django Signal
    def create_customer(sender,instance, created, **kwargs):

        if created:
            if kwargs:
                print(kwargs)

            print('here',u)
            c = Customer.objects.create(user=instance,name=instance.username)
            n = Customer.objects.get(user=instance,id=c.id)
            j = n.create_url_link()
            print(j)
            n.url_link = j
            n.save()
            print('customer created')


    post_save.connect(create_customer, sender=User)



account_signup_view = AccountSignupView



def error_404_view(request,exception):
    context = {}
    return render(request,'account/404.html',context)

def report(request):
    name = request.POST.get('name')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    reports.objects.create(user=request.user,
                          message = message,
                          subject = subject)
    messages.info(request, 'Your message has been sent successfully....')
    return redirect('account_login')

class customer_view(View):


    def get(self,request,*args,**kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')
        print(request.COOKIES)
        if 'username' in request.COOKIES and 'last_conn' in request.COOKIES:
            username = request.COOKIES['username']
            last_conn = request.COOKIES['last_conn']
            last_conn_time = datetime.datetime.strptime(last_conn[:-7],
                                                        '%Y-%m-%d %H:%M:%S')
            print(last_conn_time)
            print(last_conn)
            print(datetime.datetime.now().second - last_conn_time.second)
            if (datetime.datetime.now() - last_conn_time).seconds > 20:
                print((datetime.datetime.now() - last_conn_time).seconds)
        print('kfdfj')
        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'
        # conn = request.COOKIES['last_conn']
        # print(conn)
        containers = Container.objects.all()
        show = 'show'
        cust_cont = customer_container.objects.filter(user__username=request.user.username)
    # container_items = container_item.objects.filter(user=request.user.id)
        m = folium.Map(location=[5,8])
        m = m._repr_html_()
        context = {
            'm':m,
            'show':show,
            'cust_cont': cust_cont,
            'containers': containers,
            'mapbox_access_token': mapbox_access_token
        }
        return render(request, 'account/customer.html', context)

    def post(self,request,*args,**kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')

        t = request.POST.get('tracking_id')
        s = request.POST.get('container_tracking_id')
        print(s)

        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'
        # conn = request.COOKIES['last_conn']
        # print(conn)

        customer = Customer.objects.get(user=a)
        print(customer.user.username)
        containers = Container.objects.all()
        container = Container.objects.get(id=1)
        cust_cont = customer_container.objects.filter(user__username=customer.name)
        container_items = container_item.objects.filter(tracking_number=t,user=request.user)
        customer_containers = customer_container.objects.filter(tracking_number=s,user=request.user)
        print(customer_containers)



        if  not container_items and not customer_containers:
            v='invalid value'
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                       'v':v,
                       'm': m,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html',context)

        elif not container_items and customer_containers:
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,

                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)

        elif container_items and not customer_containers:
            print(container_items[0].longitude)
            m = folium.Map(location=[55, 88])
            folium.Marker(location=[55,88]).add_to(m)
            m = m._repr_html_()
            v='invalid value'
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                        'p':v,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)



       #container_items = container_item.objects.filter(tracking_number=t)
        print(container_items)

        context = {"container_items":container_items,
                   'customer_containers': customer_containers,
                   'm': m,
            'cust_cont': cust_cont, "customer": customer,
            'containers': containers,
            'mapbox_access_token': mapbox_access_token}
        return render(request, 'account/customer.html', context)




class truck_views(View):


    def get(self,request,*args,**kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')

        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'

        containers = Container.objects.all()
        show = 'show'
        cust_cont = customer_container.objects.filter(user__username=request.user.username)
    # container_items = container_item.objects.filter(user=request.user.id)
        m = folium.Map(location=[5,8])
        m = m._repr_html_()
        context = {
            'm':m,
            'show':show,
            'cust_cont': cust_cont,
            'containers': containers,
            'mapbox_access_token': mapbox_access_token
        }
        return render(request, 'account/customer.html', context)

    def post(self,request,*args,**kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')

        t = request.POST.get('tracking_id')
        s = request.POST.get('container_tracking_id')
        print(s)

        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'
        # conn = request.COOKIES['last_conn']
        # print(conn)

        customer = Customer.objects.get(user=a)
        print(customer.user.username)
        containers = Container.objects.all()
        container = Container.objects.get(id=1)
        cust_cont = customer_container.objects.filter(user__username=customer.name)
        container_items = container_item.objects.filter(tracking_number=t,user=request.user)
        customer_containers = customer_container.objects.filter(tracking_number=s,user=request.user)
        print(customer_containers)



        if  not container_items and not customer_containers:
            v='invalid value'
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                       'v':v,
                       'm': m,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html',context)

        elif not container_items and customer_containers:
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,

                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)

        elif container_items and not customer_containers:
            print(container_items[0].longitude)
            m = folium.Map(location=[5, 8])
            folium.Marker(location=[5,8]).add_to(m)
            m = m._repr_html_()
            v='invalid value'
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                        'p':v,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)



       #container_items = container_item.objects.filter(tracking_number=t)
        print(container_items)

        context = {"container_items":container_items,
                   'customer_containers': customer_containers,
                   'm': m,
            'cust_cont': cust_cont, "customer": customer,
            'containers': containers,
            'mapbox_access_token': mapbox_access_token}
        return render(request, 'account/truck.html', context)


class aircargo_views(View):

    def get(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')

        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'

        containers = Container.objects.all()
        show = 'show'
        cust_cont = customer_container.objects.filter(user__username=request.user.username)
        # container_items = container_item.objects.filter(user=request.user.id)
        m = folium.Map(location=[5, 8])
        m = m._repr_html_()
        context = {
            'm': m,
            'show': show,
            'cust_cont': cust_cont,
            'containers': containers,
            'mapbox_access_token': mapbox_access_token
        }
        return render(request, 'account/customer.html', context)

    def post(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('account_login')

        t = request.POST.get('tracking_id')
        s = request.POST.get('container_tracking_id')
        print(s)

        a = request.user
        mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'
        # conn = request.COOKIES['last_conn']
        # print(conn)

        customer = Customer.objects.get(user=a)
        print(customer.user.username)
        containers = Container.objects.all()
        container = Container.objects.get(id=1)
        cust_cont = customer_container.objects.filter(user__username=customer.name)
        container_items = container_item.objects.filter(tracking_number=t, user=request.user)
        customer_containers = customer_container.objects.filter(tracking_number=s, user=request.user)
        print(customer_containers)

        if not container_items and not customer_containers:
            v = 'invalid value'
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                       'v': v,
                       'm': m,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)

        elif not container_items and customer_containers:
            m = folium.Map(location=[5, 8])
            m = m._repr_html_()
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,

                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)

        elif container_items and not customer_containers:
            print(container_items[0].longitude)
            m = folium.Map(location=[5, 8])
            folium.Marker(location=[5, 8]).add_to(m)
            m = m._repr_html_()
            v = 'invalid value'
            context = {"container_items": container_items,
                       'customer_containers': customer_containers,
                       'm': m,
                       'cust_cont': cust_cont, "customer": customer,
                       'containers': containers,
                       'p': v,
                       'mapbox_access_token': mapbox_access_token}
            return render(request, 'account/customer.html', context)

        # container_items = container_item.objects.filter(tracking_number=t)
        print(container_items)

        context = {"container_items": container_items,
                   'customer_containers': customer_containers,
                   'm': m,
                   'cust_cont': cust_cont, "customer": customer,
                   'containers': containers,
                   'mapbox_access_token': mapbox_access_token}
        return render(request, 'account/aircargo.html', context)



@login_required(login_url='account_login')
def updatecustomer(request):
    cust = request.user.customer
    containers = Container.objects.all()
    form = updatecustomerform(instance=cust)
    if request.method == 'POST':
        form = updatecustomerform(request.POST,request.FILES,instance=cust)
        if form.is_valid():
            form.save()

        return redirect('customer')

    context = {'form':form,'containers': containers}
    return render(request, 'account/update.html', context)

def pricing(request):
    containers = Container.objects.all()


    context = {'containers': containers}
    return render(request, 'pricing.html', context)

def booking(request):
    containers = Container.objects.all()

    context = {'containers': containers}
    return render(request, 'account/booking.html', context)

@login_required(login_url='account_login')
def create_cust_container_view(request,id):

    print(id)
    try:
        container = Container.objects.get(id=id)
        cust_cont = customer_container.objects.get(user_id=request.user.id, tracking_number='sdw')
        print('customer container available')
    except:
        c = customer_container.objects.create(user_id=request.user.id, container_id=container.id)
        token = c.create_tracking_id()
        c.tracking_number = token
        c.save()
    context = {
               }
    return render(request, 'account/customer.html', context)


def home_view(request):
    lang='en-gb'
    print(request.COOKIES)
    language = request.session._get_session_key()
    #request.session['lang']
    print(language)
    containers =  Container.objects.all()
    V = 'V'
    context = {'language':language,
               "V":V,
               'containers':containers,}
    response =  render(request,'account/base.html',context)
    response.set_cookie('last_conn',datetime.datetime.now())
    response.set_cookie('username',datetime.datetime.now())
    return response





"""
from allauth.account.views import SignupView

class AccountSignupView(SignupView):
    # Signup View extended

    # change template's name and path
    #template_name = "users/custom_signup.html"
    def customer_create(self):
        print('hello')


account_signup_view = AccountSignupView.as_view()



class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
):
    template_name = "account/signup." + app_settings.TEMPLATE_EXTENSION
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "signup", self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(
            self.request, reverse("account_login"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret


signup = SignupView.as_view()



class LoginView(
    RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, FormView
):
    form_class = LoginForm
    template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    success_url = None
    redirect_field_name = "next"

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "login", self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(
            self.request, reverse("account_signup"), self.redirect_field_name
        )
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
            }
        )
        return ret


login = LoginView.as_view()




"""