from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course,Enrollment,Forum
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from django.urls import reverse_lazy
from .forms import EnrollmentForm,ForumForm
# Create your views here.



class CourseCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Course
    template_name = 'course_new.html'
    fields = ('name', 'description','category') 
    login_url = 'login' 
    success_url = reverse_lazy('my_courses')

    def test_func(self) :
        return self.request.user.is_teacher_user()

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

class CourseListView(LoginRequiredMixin,ListView):
    model = Course
    template_name = 'course_list.html'
    login_url = 'login' 

class CourseDetailView(LoginRequiredMixin,DetailView): 
    model = Course
    template_name = 'course_detail.html'
    login_url = 'login' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = self.get_object()
        
        is_enrolled = Enrollment.objects.filter(student=user, course=course).exists()
        
        context['is_enrolled'] = is_enrolled
        return context
    
class CourseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView): 
    model = Course
    fields = ('name', 'description','category',)
    template_name = 'course_edit.html'
    login_url = 'login' 
    success_url = reverse_lazy('my_courses')
    def test_func(self): 
        obj = self.get_object()

        return obj.teacher == self.request.user or self.request.user.is_admin()

class CourseDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView): 
    model = Course
    template_name = 'course_delete.html'
    success_url = reverse_lazy('my_courses')
    login_url = 'login' 
    def test_func(self): 
        obj = self.get_object()
        return obj.teacher  == self.request.user 
class ForumDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Forum
    template_name = 'forum_confirm_delete.html'  
    def get_success_url(self):
        course = get_object_or_404(Course, id=self.object.course.id)
        return reverse_lazy('forum_list', kwargs={'course_pk': course.id})

    def test_func(self): 
        obj = self.get_object()
        return obj.customer_id  == self.request.user.id 





from django.http import HttpResponse

@login_required
def enroll_in_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_student_user():
        enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    else:
        return(HttpResponse('oops'))
    return redirect('/')

@login_required
def complete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_student_user():
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        enrollment.completed=True
        enrollment.save()
    else:
        return(HttpResponse('oops'))
    return redirect('/course/my_courses')
@login_required
def uncomplete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_student_user():
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        enrollment.completed=False
        enrollment.save()
    else:
        return(HttpResponse('oops'))
    return redirect('/course/my_courses')



@login_required   
def my_courses(request):
    user = request.user 
    print(request.user.is_student_user())
    if request.user.is_student_user():
        
        courses = Course.objects.filter(enrollments__student=user).distinct()        
        course_data = []
        for course in courses:
            enrollment = Enrollment.objects.filter(student=user, course=course).first()
            course_data.append({
                'pk':course.id,
                'name': course.name,
                'description': course.description,
                'completed': enrollment.completed if enrollment else False,
            })
        
        return render(request, 'my_courses.html', {'courses': course_data})
    
    else:
        
        course_data=Course.objects.all().filter(teacher_id=user.id)
        print(course_data)
        return render(request, 'my_courses.html', {'courses': course_data})
        
def get_messages(request,pk):
    
    context =Forum.objects.all().filter(course=pk)
    return render(request,'forum.html',{'context':context})



def forum_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    forums = Forum.objects.filter(course=course)
    form = ForumForm()
    return render(request, 'forum.html', {'course': course, 'forums': forums, 'form': form})

@login_required
def create_forum_post(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.customer = request.user
            forum.course = course
            forum.save()
            return redirect('forum_list', course_pk=course.pk)
    else:
        form = ForumForm()
    return render(request, 'create_forum_post.html', {'form': form, 'course': course})