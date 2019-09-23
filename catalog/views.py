import datetime
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
# from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm


# Create your views here.
# def index(request):
#     obj = Book.objects.all()
#     context = {'someVar': obj, }
#     return render(request, 'catalog/index.html', context)

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    count_genre_contians = Genre.objects.filter(name__startswith='Drama').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'count_genre_contians': count_genre_contians,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Book
    paginate_by = 4

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='o').order_by('due_back')


class borrowedListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = "catalog/borrowed_List.html"

    def get_queryset(self):
        return BookInstance.objects.filter(status='o').order_by('due_back')


@permission_required('catalog.Show_borrowers')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        # form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-author'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    template_name = "catalog/author_form.html"
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(AuthorCreate, self).dispatch(request, *args, **kwargs)


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = {'first_name', 'last_name', 'date_of_birth', 'date_of_death'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(AuthorUpdate, self).dispatch(request, *args, **kwargs)


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(AuthorDelete, self).dispatch(request, *args, **kwargs)


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(BookCreate, self).dispatch(request, *args, **kwargs)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(BookUpdate, self).dispatch(request, *args, **kwargs)


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.Show_borrowers'):
            return HttpResponseForbidden()
        return super(BookDelete, self).dispatch(request, *args, **kwargs)

