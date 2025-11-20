from django.shortcuts import render, redirect
from course.models import Category, Lesson
from web.models import achievement, contact_email, collect_email
from django.contrib import messages
import threading
#系統 email 通知
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading

# Create your views here.
### TEST
def get_index(request):
	courses = Lesson.objects.all().filter(published=True)
	stars = range(round(courses[0].rating))
	half_star = courses[0].rating % 1 != 0
	print(half_star)
	return render(request, 'index.html', locals())

def story(request):
	return render(request, 'story.html', locals())

def career(request):
	return render(request, 'career.html', locals())

def achievements(request):
	all_achievements = achievement.objects.all().order_by('year')

	return render(request, 'achievements.html', locals())

def register_email(request):
	if request.method == 'POST':
		previous_url = request.META.get('HTTP_REFERER')
		try:
			exist_email = collect_email.objects.get(email = request.POST['email'])
			messages.info(request,"您已經曾經註冊過囉！")
		except:
			add_email = collect_email.objects.create(email = request.POST['email'])
			add_email.save()
			messages.info(request,"您已經成功註冊囉！")

		return redirect(previous_url)

	else:
		messages.info(request,"網址錯誤，請重新確認網址...")
		return redirect('/')

	return render(request, 'achievements.html', locals())

def contact(request):
	return render(request, 'contact.html', locals())

def email_alert(receiver, title, email_content):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = f"{title}"  #郵件標題
    content["from"] = "makalot.sys@gmail.com"  #寄件者
    content["to"] = f"ai.free.team@gmail.com; {receiver}" #收件者
    content.attach(MIMEText(f"{email_content}","html"))  #郵件內容
    
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("makalot.sys@gmail.com", "whnhceuycqwaykpf")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
            return True
        except Exception as e:
            print("Error message: ", e)
            return False

def post_email(request):
	if request.method == 'POST':
		new_email = contact_email.objects.create(
			contact_name = request.POST['name'],
			contact_need = request.POST['need'],
			contact_phone = request.POST['phone'],
			contact_email = request.POST['email'],
			contact_message = request.POST['message']
		)
		new_email.save()

		html_email = f"""
		<!DOCTYPE html>
			<html>
				<head>
					<title>{request.POST['name'] + request.POST['need']}</title>
				</head>
				<body>
					<p>客戶名稱：{request.POST['name']}</p>
					<p>客戶信箱：{request.POST['email']}</p>
					<p>客戶電話：{request.POST['phone']}</p>
					<p>客戶需求：{request.POST['need']}</p>
					<p>需求說明：</p>
					<p>{request.POST['message']}</p>
				</body>
		</html>"""
		# email_alert("", '【客戶訊息】'+ request.POST['name'] + request.POST['need'], html_email)

		# Create a new thread
		thread = threading.Thread(target=email_alert, args=("", '【客戶訊息】'+ request.POST['name'] + request.POST['need'], html_email))
		# Start the thread
		thread.start()


		messages.info(request,"已收到您的留言，請耐心等候 1-3 個工作天，自由團隊將以最快的速度跟您聯繫。")
		return redirect('/contact')

	else:
		messages.info(request,"網址錯誤，請重新確認網址...")
		return render(request, 'contact.html', locals())

