from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.db.models import Count
from django.db.models import F
import json
def index(request,*args,**kwargs):
    # 获取当前URL
    print(request.path_info)

    condition = {}
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        condition['article_type_id'] = type_id

    article_list = models.Article.objects.filter(**condition)

    type_choice_list = models.Article.type_choices
    return render(
        request,
        'index.html',
        {
            'type_choice_list':type_choice_list,
            'article_list':article_list,
            'type_id':type_id
        }
    )

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        input_code = request.POST.get('code')
        session_code = request.session.get('code')
        if input_code.upper() == session_code.upper():
            pass
        else:
            pass


def check_code(request):
    # 读取硬盘中的文件，在页面显示
    # f = open('static/imgs/yj.png','rb')
    # data = f.read()
    # f.close()
    # return HttpResponse(data)

    # pip3 install pillow
    # from PIL import Image
    # f = open('code.png','wb')
    # img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
    # img.save(f,'png')
    # f.close()
    #
    # f = open('code.png','rb')
    # data = f.read()
    # f.close()

    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO
    """
    f = BytesIO()
    img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')
    draw.point([10, 10], fill="red")
    draw.point([20, 10], fill=(255, 255, 255))

    draw.line((15,10,50,50), fill='red')
    draw.line((45,20,100,100), fill=(0, 255, 0))

    draw.arc((0,0,30,30),0,360,fill="red")

    # draw.text([0,0],'python',"red")
    # font = ImageFont.truetype("kumo.ttf", 28)
    # draw.text([0,0],'python',(0, 255, 0),font=font)
    import random

    # char_list = []
    # for i in range(5):
    #     char = chr(random.randint(65,90))
    #     char_list.append(char)
    # ''.join(char_list)

    # v = ''.join([ chr(random.randint(65,90)) for i in range(5)])

    char_list = []
    for i in range(5):
        char = chr(random.randint(65,90))
        char_list.append(char)
        font = ImageFont.truetype("kumo.ttf", 28)
        draw.text([i*24,0],char,(random.randint(0,255), random.randint(0,255), random.randint(0,255)),font=font)
    img.save(f,'png')
    data = f.getvalue()
    code = ''.join(char_list)
    request.session['code'] = code
    """
    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())


from app01.forms import RegisterForm
from django.core.exceptions import NON_FIELD_ERRORS
def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = RegisterForm(request)
        return render(request,'register.html',{'obj':obj})

    else:
        # 验证码操作
        obj = RegisterForm(request,request.POST,request.FILES)
        if obj.is_valid():
            pass
        else:
            print(obj.errors['__all__'])
            print(obj.errors[NON_FIELD_ERRORS])
            # obj.errors
            """
            {
                __all__: [错误1，错误2]
                user: [错误1，错误2]
                password: [错误1，错误2]
            }
            """
        return render(request,'register.html',{'obj':obj})

def home(request,site):
    """
    访问个人博客主页 http://127.0.0.1:8000/fangshaowei/
    :param request:  请求相关信息
    :param site: 个人博客后缀，如： www.xxx.com/xxxxx/
    :return:
    """

    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照：分类，标签，时间
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))
    # select xxx as x

    article_list = models.Article.objects.all()

    return render(
        request,
        'home.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'article_list':article_list,
        }
    )


def filter(request,site,key,val):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照：分类，标签，时间
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))
    # select xxx as x

    if key == 'category':
        article_list = models.Article.objects.filter(blog=blog,category_id=val)
    elif key == 'tag':
        # v= models.Article.objects.filter(blog=blog,article2tag__tag__title=val)
        # print(v.query)
        # 自定义第三张表，
        # 自己反向关联
        # v= models.Article.objects.filter(blog=blog,article2tag__tag=val)
        # 通过M2M字段
        # v= models.Article.objects.filter(blog=blog,tags__nid=val)
        article_list = models.Article.objects.filter(blog=blog,tags__nid=val)
    else:
        # val = 2017-09
        # 2018- 01-12 11：11:111
        article_list = models.Article.objects.filter(blog=blog).extra(where=["strftime('%%Y-%%m',create_time)=%s"],params=[val,])


    return render(
        request,
        'filter.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'article_list':article_list,
        }
    )

def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照：分类，标签，时间
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))
    # select xxx as x

    obj = models.Article.objects.filter(blog=blog,nid=nid).first()


    # ####################### 评论 #############################
    msg_list = [
        {'id':1,'content':'写的太好了','parent_id':None},
        {'id':2,'content':'你说得对','parent_id':None},
        {'id':3,'content':'顶楼上','parent_id':None},
        {'id':4,'content':'你眼瞎吗','parent_id':1},
        {'id':5,'content':'我看是','parent_id':4},
        {'id':6,'content':'鸡毛','parent_id':2},
        {'id':7,'content':'你是没呀','parent_id':5},
        {'id':8,'content':'惺惺惜惺惺想寻','parent_id':3},
    ]
    msg_list_dict = {}
    for item in msg_list:
        item['child'] = []
        msg_list_dict[item['id']] = item

    # #### msg_list_dict用于查找,msg_list
    result = []
    for item in msg_list:
        pid = item['parent_id']
        if pid:
            msg_list_dict[pid]['child'].append(item)
        else:
            result.append(item)
    # ########################### 打印 ###################
    from utils.comment import comment_tree
    comment_str = comment_tree(result)

    return render(
        request,
        'article.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'obj':obj,
            'comment_str':comment_str
        }
    )

def up(request):
    # 是谁？文章?赞或踩 1赞，0踩
    # 是谁？当前登录用户，session中获取
    # 文章？
    response = {'status':1006,'msg':None}

    try:
        user_id = request.session.get('user_id')
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))
        obj = models.UpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if obj:
            # 已经赞或踩过
            pass
        else:
            from django.db import transaction
            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                else:
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count')+1)
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)

    return HttpResponse(json.dumps(response))

def lizhi(request,**kwargs):
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    print(condition)
    # 大分类
    type_list = models.Article.type_choices

    # 个人分类
    category_list = models.Category.objects.filter(blog_id=1)

    # 个人标签
    tag_list = models.Tag.objects.filter(blog_id=1)

    # 进行筛选
    condition['blog_id'] = 1
    article_list = models.Article.objects.filter(**condition)

    return render(request,'lizhi.html',{
        'type_list':type_list,
        'category_list':category_list,
        'tag_list':tag_list,
        'article_list':article_list,
        'kwargs':kwargs


    })


CONTENT = ""
from app01.forms import ArticleForm
def wangzhe(request):
    if request.method == "GET":
        obj = ArticleForm()
        return render(request,'wangzhe.html',{'obj':obj})
    else:
        obj = ArticleForm(request.POST)
        if obj.is_valid():
            content = obj.cleaned_data['content']
            global CONTENT
            CONTENT = content
            print(content)
            return HttpResponse('...')


def see(request):

    return render(request,'see.html',{'con': CONTENT})

def upload_img(request):
    import os
    upload_type = request.GET.get('dir')
    file_obj = request.FILES.get('imgFile')
    file_path = os.path.join('static/imgs',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '错误了...'
    }
    import json
    return HttpResponse(json.dumps(dic))


def comments(request,nid):
    response = {'status':True,'data':None,'msg':None}
    try:
        msg_list = [
            {'id':1,'content':'写的太好了','parent_id':None},
            {'id':2,'content':'你说得对','parent_id':None},
            {'id':3,'content':'顶楼上','parent_id':None},
            {'id':4,'content':'你眼瞎吗','parent_id':1},
            {'id':5,'content':'我看是','parent_id':4},
            {'id':6,'content':'鸡毛','parent_id':2},
            {'id':7,'content':'你是没呀','parent_id':5},
            {'id':8,'content':'惺惺惜惺惺想寻','parent_id':3},
        ]
        msg_list_dict = {}
        for item in msg_list:
            item['child'] = []
            msg_list_dict[item['id']] = item
        result = []
        for item in msg_list:
            pid = item['parent_id']
            if pid:
                msg_list_dict[pid]['child'].append(item)
            else:
                result.append(item)
        response['data'] = result
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)

    return HttpResponse(json.dumps(response))












