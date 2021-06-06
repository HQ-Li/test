#-- coding:utf8 --

import threading

import traceback
import time

from Common import goConfig, getLogger
from SyncDataManager import SyncDataManager

logger = getLogger(__name__)


if __name__ == '__main__':

    mgr = SyncDataManager()
    global timerSync
    global timerReportError

    try:
        timerSync = threading.Timer(goConfig.TimerSyncInterval, mgr.syncWork)
        timerSync.start()

        timerReportError = threading.Timer(goConfig.TimerSyncInterval, mgr.reportState)
        timerReportError.start()

    except BaseException as ex:
        traceback.print_stack()
