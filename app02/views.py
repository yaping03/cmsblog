from django.shortcuts import render,HttpResponse
from app02 import models
import re
from rbac.service import permission_session
def login(request):
    if request.method == "GET":
        return render(request,'login2.html')
    else:
        # rbac中的user表检测用户名密码是否合法

        permission_session(1,request)
        return HttpResponse('登录成功')

def index(request):
    # http://127.0.0.1:8000/auth-index.html?md=GET
    return HttpResponse('登陆，并且有权限才能看见我')

def test(request):
    # obj = models.User.objects.filter(username='杨明').first()
    #
    # # x = models.User2Role.objects.filter(user_id=obj.id)
    # # [User2Role,User2Role,User2Role]
    #
    # role_list = models.Role.objects.filter(users__user_id=obj.id)
    # # [Role,]
    # from django.db.models import Count
    # # permission_list = models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url','action__code').annotate(c=Count('id'))
    # permission_list = models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url','action__code').distinct()
    """
    [
        {permission_url: '/index.html', action_code:'GET'},
        {permission_url: '/index.html', action_code:'POST'},
        {permission_url: '/index.html', action_code:'DEL'},
        {permission_url: '/index.html', action_code:'Edit'},
        {permission_url: '/order.html', action_code:'GET'},
        {permission_url: '/order.html', action_code:'POST'},
        {permission_url: '/order.html', action_code:'DEL'},
        {permission_url: '/order.html', action_code:'Edit'},
    ]
    放在Session中
    /index.html?md=GET

    {
        '/index.html': [GET,POST,DEL,Edit],
        '/order.html': [GET,POST,DEL,Edit],
    }

    """

def menu(request):
    """
    需要用户名或用户ID，产出：用户关联所有菜单
    :param request:
    :return:
    """

    # 所有菜单：处理成当前用关联的菜单
    all_menu_list = models.Menu.objects.all().values('id','caption','parent_id')
    """
    [
        {'id':1, 'caption':'菜单1', parent_id:None},
        {'id':2, 'caption':'菜单2', parent_id:None},
        {'id':3, 'caption':'菜单3', parent_id:None},
        {'id':4, 'caption':'菜单1-1', parent_id:1},
    ]

    {
        1:{'id':1, 'caption':'菜单1', parent_id:None,status:False,opened:False,child:[]},
        2:{'id':2, 'caption':'菜单2', parent_id:None,status:False,opened:False,child:[]},
        3:{'id':3, 'caption':'菜单3', parent_id:None,status:False,opened:False,child:[]},
        5:{'id':4, 'caption':'菜单1-1', parent_id:1,status:False,opened:False,child:[]},
    }
   """
    user = models.User.objects.filter(username='youqingbing').first()
    role_list = models.Role.objects.filter(users__user=user)
    permission_list = models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__id','permission__url','permission__menu_id','permission__caption').distinct()
    """
    [
        {'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 1 },
        {'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 2 },
        {'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 3 },
        {'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 4 },
    ]
    """
    ##### 将权限挂靠到菜单上 ########
    all_menu_dict = {}
    for row in all_menu_list:
        row['child'] = []      # 添加孩子
        row['status'] = False # 是否显示菜单
        row['opened'] = False # 是否默认打开
        all_menu_dict[row['id']] = row


    for per in permission_list:
        if not per['permission__menu_id']:
            continue

        item = {
            'id':per['permission__id'],
            'caption':per['permission__caption'],
            'parent_id':per['permission__menu_id'],
            'url': per['permission__url'],
            'status': True,
            'opened': False
        }
        # if re.match(per['permission__url'],request.path_info):
        # if re.match(per['permission__url'],"/jieke.html"):
        if re.match(per['permission__url'],"/yuhao.html"):
            item['opened'] = True
        pid = item['parent_id']
        all_menu_dict[pid]['child'].append(item)

        # 将当前权限前辈status=True
        temp = pid # 1.父亲ID
        while not all_menu_dict[temp]['status']:
            all_menu_dict[temp]['status'] = True
            temp = all_menu_dict[temp]['parent_id']
            if not temp:
                break

        # 将当前权限前辈opened=True
        if item['opened']:
            temp1 = pid # 1.父亲ID
            while not all_menu_dict[temp1]['opened']:
                all_menu_dict[temp1]['opened'] = True
                temp1 = all_menu_dict[temp1]['parent_id']
                if not temp1:
                    break
    # ############ 处理菜单和菜单之间的等级关系 ############
    """
    all_menu_dict = {
        1:{'id':1, 'caption':'菜单1', parent_id:None,status:False,opened:False,child:[{'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 1 },]},
        2:{'id':2, 'caption':'菜单2', parent_id:None,status:False,opened:False,child:[]},
        3:{'id':3, 'caption':'菜单3', parent_id:None,status:False,opened:False,child:[]},
        5:{'id':4, 'caption':'菜单1-1', parent_id:1,status:False,opened:False,child:[]},
    }


    all_menu_list= [
        {'id':1, 'caption':'菜单1', parent_id:None,status:False,opened:False,child:[{'permission__url':'/order.html','permission__caption': '订单管理','permission__menu_id': 1 }, {'id':4, 'caption':'菜单1-1', parent_id:1,status:False,opened:False,child:[]},]},
        {'id':2, 'caption':'菜单2', parent_id:None,status:False,opened:False,child:[]},
        {'id':3, 'caption':'菜单3', parent_id:None,status:False,opened:False,child:[]},

    ]
    """

    result = []
    for row in all_menu_list:
        pid = row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)


    ##################### 结构化处理结果 #####################
    for row in result:
        print(row['caption'],row['status'],row['opened'],row)

    ##################### 通过结构化处理结果，生成菜单开始 #####################
    """
    result = [
	    {'id':1, 'caption':'菜单1', parent_id:None,status:False,opened:False,child:[5:{'id':4, 'caption':'菜单1-1', parent_id:1,status:False,opened:False,child:[]},2:{'id':2, 'caption':'菜单2', parent_id:1,status:False,opened:False,child:[]},]}
        {'id':2, 'caption':'菜单2', parent_id:None,status:True,opened:False,child:[]},
        {'id':3, 'caption':'菜单3', parent_id:None,status:true,opened:False,child:[url...]},
    ]

    status=False ,不生产成
    opened=True  ,true不加，false，加hide

    <div class='menu-item'>
        <div class='menu-header'>菜单1</div>
        <div class='menu-body %s'>
            <a>权限1</a>
            <a>权限2</a>
             <div class='menu-item'>
                <div class='menu-header'>菜单11</div>
                <div class='menu-body hide'>
                    <a>权限11</a>
                    <a>权限12</a>
                </div>
            </div>
        </div>
    </div>
    <div class='menu-item'>
        <div class='menu-header'>菜单2</div>
        <div class='menu-body hide'>
            <a>权限1</a>
            <a>权限2</a>
        </div>
    </div>
    <div class='menu-item'>
        <div class='menu-header'>菜单3</div>
        <div class='menu-body hide'>
            <a>权限1</a>
            <a>权限2</a>
        </div>
    </div>


    """

    def menu_tree(menu_list):
        tpl1 = """
        <div class='menu-item'>
            <div class='menu-header'>{0}</div>
            <div class='menu-body {2}'>{1}</div>
        </div>
        """
        tpl2 = """
        <a href='{0}' class='{1}'>{2}</a>
        """

        menu_str = ""
        for menu in menu_list:
            if not menu['status']:
                continue
            # menu: 菜单，权限（url）
            if menu.get('url'):
                # 权限
                menu_str += tpl2.format(menu['url'],'active' if menu['opened'] else "",menu['caption'])
            else:
                # 菜单
                if menu['child']:
                    child_html = menu_tree(menu['child'])
                else:
                    child_html = ""
                menu_str += tpl1.format(menu['caption'], child_html,"" if menu['opened'] else 'hide')

        return menu_str

    menu_html = menu_tree(result)


    return render(request,'menu.html',{'menu_html':menu_html})
    ##################### 通过结构化处理结果，生成菜单结束 #####################
    # return HttpResponse('...')















