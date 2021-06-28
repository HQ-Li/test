#-- coding:utf8 --

import logging
import subprocess

class Common:
    def __init__(self):
        self.BaseUrl = 'dggcots'
        self.ActionAdd = 'add'
        self.ActionUpdate = 'modify'
        self.ActionDelete = 'delete'
        self.ThreadMaxWorker = 3

        self.SyncStateFailed = 'failed'
        self.SyncStateSuccess = 'success'
        self.SyncStateSyncing = 'Syncing'

        # file type
        self.SyncTypeFile = "file"
        self.SyncTypeDirectory = "directory"
        self.SyncTypeLink = "link"

        self.SyncTypeList = [self.SyncTypeFile, self.SyncTypeDirectory, self.SyncTypeLink]

        # timer sync
        self.TimerSyncInterval = 1 * 10  # 秒
        self.TimerReportInterval = 1 * 10  # 心跳



        pass

    def set_log(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console)
        return logger

    def checkHostLogin(self,host):
        # 检查主机是否可以免密登录
        cmd = 'ssh %s -o StrictHostKeyChecking=no  date' % host
        stat, out = subprocess.getstatusoutput(cmd)
        ret = False
        if stat == 0:
            # success
            ret = True

        return ret, out


goConfig = Common()
getLogger = Common().set_log


