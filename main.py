from JDmaimiao import JDmaimiao
from WeiChat import main_itchat
import threading
import sys


if __name__ == '__main__':
    weichat = threading.Thread(target=main_itchat)
    weichat.start()
    jd = JDmaimiao()
    jd_t = threading.Thread(target=jd.main)
    jd_t.start()
    jd_t.join()
    jd.driver.quit()
    sys.exit()
