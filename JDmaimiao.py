# coding:utf-8
from params import *
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys

global GlobalParams


class JDmaimiao(object):
    def __init__(self):
        # 计数
        self.refresh_count = 0
        # 新建浏览器驱动
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        # 有效任务
        self.valid_tasks = []

    def main(self):
        self.login()
        self.clear_alert()
        self.set_task_filter()
        print(time.strftime('%H:%M:%S') + ': Finding task...')
        while 1:
            try:
                self.refresh()
                self.refresh_count += 1
                print('%s: Page refreshed %d times' % (time.strftime('%H:%M:%S'), self.refresh_count))
                if self.refresh_count % 50 == 0:
                    GlobalParams.set('msg', 'Page refreshed %d times' % self.refresh_count)
                    GlobalParams.get('signal').set()
                    time.sleep(10)
                    GlobalParams.get('signal').clear()
                time.sleep(30)
                if self.notify():
                    print(time.strftime('%H:%M:%S') + ': Task found.')
                    try:
                        self.auto_take_order(self.valid_tasks)
                    except:
                        pass
                    GlobalParams.set('msg', 'Task found. ' +
                          'Script is waiting for sleep time input within 60 seconds' +
                          '(input 999 to end script).')
                    GlobalParams.get('signal').set()
                    time.sleep(60)
                    GlobalParams.get('signal').clear()
                    if GlobalParams.get('time_in_minute') == 999:
                        sys.exit()
                    print(time.strftime('%H:%M:%S') + 'Sleep %d minutes' % GlobalParams.get['time_in_minute'])
                    time.sleep(GlobalParams.get('time_in_minute') * 60)
            except:
                time.sleep(30)

    def login(self):
        self.driver.get(login_url)
        self.driver.find_element_by_id(id_input_username).send_keys(username)
        self.driver.find_element_by_id(id_input_passwd).send_keys(passwd)
        self.driver.find_element_by_id(id_button_submit).click()

    def clear_alert(self):
        try:
            self.driver.find_element_by_class_name(class_a_known).click()
        except:
            pass

    def set_task_filter(self):
        self.driver.get(task_filter_url)

    def refresh(self):
        self.driver.find_element_by_class_name(class_a_refresh).click()

    def get_valid_task_number(self):
        return int(self.driver.page_source.count('qcrw taskTask'))

    def get_max_task_coin(self, valid_tasks):
        coins = [float(task.parent.find(attrs={'title': '完成任务后，您能获得的任务奖励，可兑换成RMB'}).span.string.strip()) for task in valid_tasks]
        return max(coins)

    def get_valid_task_by_account_level(self, valid_tasks):
        temp_task = []
        for task in valid_tasks:
            if task.parent.parent.find(attrs={'class': 'BuyerJifen'}) is None:
                temp_task.append(task)
        return temp_task

    def notify(self):
        if self.get_valid_task_number() > 0:
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            valid_tasks = soup.find_all(attrs={'class': 'qcrw taskTask'})
            valid_tasks = self.get_valid_task_by_account_level(valid_tasks)
            if len(valid_tasks) > 0 and self.get_max_task_coin(valid_tasks) > 5:
                self.valid_tasks = valid_tasks
                return True
        return False

    def auto_take_order(self, valid_tasks):
        # 对valid_tasks按照金币与垫付金额的比值进行递减排序
        def get_ratio(task):
            coins = float(task.parent.find(attrs={'title': '完成任务后，您能获得的任务奖励，可兑换成RMB'}).span.string.strip())
            money = float(task.parent.find(attrs={'title': '平台担保：此任务卖家已缴纳全额担保存款，接手可放心购买，任务完成后，买家平台账号自动获得相应存款'}).span.string.strip())
            return coins / money
        valid_tasks.sort(key=get_ratio, reverse=True)

        for task in valid_tasks:
            # 点击抢此任务
            alt = task.get('alt')
            self.driver.find_elements_by_css_selector('[alt=%s]' % alt).click()
            # 判断跳出来的div标签是否包含'当前任务金额超出您的垫付立反额度'
            div_text = self.driver.find_elements_by_class_name(class_div_content).text
            if partial_confirm_content1 in div_text:
                self.driver.find_element_by_class_name(class_a_btn).click()
            # 判断跳出来的div标签是否包含'选择接此任务的买号'
            div_text = self.driver.find_elements_by_class_name(class_div_content).text
            if partial_confirm_content2 in div_text:
                self.driver.find_element_by_class_name(class_a_btn).click()
            # 判断跳出来的div标签是否包含'您已经成功接手此任务'
            div_text = self.driver.find_elements_by_class_name(class_div_content).text
            if partial_confirm_content3 in div_text:
                return
            else:
                continue
