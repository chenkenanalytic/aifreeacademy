from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('課程主題名稱', max_length=256)
    slug = models.CharField('主題網址', max_length=256, db_index=True, unique=True)
    intro = models.TextField('主題簡介', default='')
    display = models.BooleanField('主題顯示', default=False)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    # id 為默認值如下所示
    id = models.AutoField(primary_key=True)

    cate = models.ManyToManyField(Category, verbose_name='歸屬主題')
    title = models.CharField('課程名稱', max_length=256)
    subtitle = models.CharField('課程副標題', max_length=256)
    slug = models.CharField('課程網址', max_length=256, db_index=True, unique=True)
    img_link = models.CharField('課程圖片連結', max_length=2560, default="/static/story/assets/AI_free_logo.png")
    bar_img_link = models.CharField('課程圖片連結', max_length=2560, default="/static/bootstrap/assets/img/blog/single_blog_11.png")

    pub_date = models.DateTimeField('課程上架時間', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('課程更新時間', auto_now=True, null=True)
    
    author = models.ForeignKey(
    	'auth.User',
    	 blank=True,
    	 null=True,
    	 verbose_name='作者',
    	 on_delete=models.CASCADE)
    content = models.TextField('內文', default='')
 
    published = models.BooleanField('正式發布', default=True)
    price = models.PositiveIntegerField(default=9999)
    rating = models.FloatField(default=5.0)
