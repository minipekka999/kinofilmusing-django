from django.contrib.auth import logout, login
from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated

from .permissions import IsAdminOrReadOnly
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from kino.forms import *
from kino.models import *
from .utils import *

class MovieAPIList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrReadOnly, )

class MovieAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )

class MovieAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAdminOrReadOnly,)


# class MovieViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     # queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#         if not pk:
#             return Movie.objects.all()[:3]
#         return Movie.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats':cats.name})

# class MovieAPIList(generics.ListCreateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
# class MovieAPIUpdate(generics.UpdateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#
# class MovieAPIDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

# class MovieAPIView(APIView):
#     def get(self, request):
#         m = Movie.objects.all()
#         return Response({'posts': MovieSerializer(m, many=True).data})
#
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Movie.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = MovieSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})




# class MovieAPIView(generics.ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

class MovieHome(DataMixin, ListView):
    paginate_by = 3
    model = Movie
    template_name = 'kino/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# def index(request):
#     posts = Movie.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'kino/index.html', context=context)


def about(request):
    contact_list = Movie.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'kino/about.html', {'page_obj': page_obj, 'menu' : menu, 'title': 'О сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'kino/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление фильма")
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#            form.save()
#            return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'kino/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление фильма'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'kino/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def login(request):
#     return HttpResponse("Авторизация")

# def show_post(request, post_slug):
#     post = get_object_or_404(Movie, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'kino/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Movie
    template_name = 'kino/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, * , object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class MovieCategory(DataMixin, ListView):
    paginate_by = 3
    model = Movie
    template_name = 'kino/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Movie.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - '+ str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) +list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Movie.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'kino/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'kino/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'kino/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('loginn')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = "all"
