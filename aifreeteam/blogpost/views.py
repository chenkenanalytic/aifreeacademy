from django.shortcuts import render
from .models import Column, Article
# Create your views here.

def blog(request):

	paging = request.GET.get('page') if (request.META.get('page') is not None) else 1
	category = request.GET.get('category')

	filtered_columns = Column.objects.filter(display__exact=True)
	columns = list(filtered_columns.values())

	for i in columns:
		i['column_post_num'] = len(Article.objects.filter(column__name=i['name']))

	all_posts = Article.objects.filter(column__in=filtered_columns).order_by('-pub_date')
	if category:
		print(category)
		all_posts = all_posts.filter(column__name=category)

	pages_max = len(all_posts)//10 if len(all_posts)%10 == 0 else len(all_posts)//10 + 1
	pages = []
	for i in range(5):
		pages_num = paging - 2 + i
		if pages_num > 0 and pages_num <= pages_max:
			pages.append(pages_num)

	cur_posts = all_posts[10*(paging-1):10*paging]
	latest_posts = all_posts[:5]

	return render(request, 'blog.html', locals())


def post(request, slug):
	post = Article.objects.get(slug=slug)
	prev_post = Article.objects.filter(id=post.id-1)
	next_post = Article.objects.filter(id=post.id+1)

	columns = Column.objects.filter(display=True)
	columns = list(columns.values())

	for i in columns:
		i['column_post_num'] = len(Article.objects.filter(column__name=i['name']))

	latest_posts = Article.objects.all().order_by('-pub_date')[:5]

	return render(request, 'post.html', locals())