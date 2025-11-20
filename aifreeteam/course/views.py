from django.shortcuts import render
from .models import Category, Lesson
# Create your views here.

def courses(request):

	paging = request.GET.get('page') if (request.META.get('page') is not None) else 1
	category = request.GET.get('category')

	categories = Category.objects.filter(display=True)
	categories = list(categories.values())

	for i in categories:
		i['category_lesson_num'] = len(Lesson.objects.filter(cate__name=i['name']))

	all_lessons = Lesson.objects.all().order_by('-pub_date')
	if category:
		print(category)
		all_lessons = all_lessons.filter(cate__name=category)

	pages_max = len(all_lessons)//10 if len(all_lessons)%10 == 0 else len(all_lessons)//10 + 1
	pages = []
	for i in range(5):
		pages_num = paging - 2 + i
		if pages_num > 0 and pages_num <= pages_max:
			pages.append(pages_num)

	cur_lessons = all_lessons[10*(paging-1):10*paging]
	latest_courses = all_lessons[:5]

	return render(request, 'courses.html', locals())

def get_course(request, slug):
	course = Lesson.objects.get(slug=slug)
	prev_course = Lesson.objects.filter(id=course.id-1)
	next_course = Lesson.objects.filter(id=course.id+1)

	categories = Category.objects.filter(display=True)
	categories = list(categories.values())

	for i in categories:
		i['category_lesson_num'] = len(Lesson.objects.filter(cate__name=i['name']))

	latest_courses = Lesson.objects.all().order_by('-pub_date')[:5]
	return render(request, 'course.html', locals())


