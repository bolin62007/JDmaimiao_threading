# coding:utf-8
# 登录
login_url = 'http://www.zo15.cn'
username = 'feishicheng'
passwd = '322199'
id_input_username = 'lusername'
id_input_passwd = 'lpassword'
id_button_submit = 'login_btn'

# 设置筛选条件
task_filter_url = 'http://www.zo15.cn/site/taobaoTask/platform/2/payWay/noVal/BuyerJifen/noVal/isMobile' +\
                  '/noVal/task_type/noVal/MinLi/noVal/txtPrice/noVal/ddlOKDay/noVal.html'

# 去除公告
class_a_known = 'layui-layer-btn0'

# 刷新
class_a_refresh = 'rw_sx1'

# 自动接单
partial_class_a_confirm = 'layui-layer'
class_a_btn = 'layui-layer-btn0'
class_div_content = 'layui-layer-content'
partial_confirm_content1 = '当前任务金额超出您的垫付立反额度'
partial_confirm_content2 = '选择接此任务的买号'
partial_confirm_content3 = '您已经成功接手此任务'

# 定义一个全局变量类完成在模块WeiChat.py和JDmaimiao之间的通信
class GlobalParams(object):
    params = {}
    # 发送给小号的消息
    params['msg'] = ''
    # 从小号接收到的等待时间
    params['time_in_minute'] = 30
    # 信号事件
    import threading
    params['signal'] = threading.Event()

    @classmethod
    def get(cls, key):
        if key in cls.params.keys():
            return cls.params[key]
        else:
            print('key: %s' % key)

    @classmethod
    def set(cls, key, value):
        if key in cls.params.keys():
            cls.params[key] = value
        else:
            print('key: %s\nvalue: %s' % (key, value))

if __name__ == '__main__':
    print(GlobalParams.params)
