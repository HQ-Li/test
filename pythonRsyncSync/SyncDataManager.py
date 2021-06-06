#-- coding:utf8 --

import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from Common import goConfig,getLogger
from SyncDataItem import SyncDataItem

logger = getLogger(__name__)

class SyncDataManager:
    def __init__(self):
        self.reportErrorList = []
        pass

    def getSyncData(self):

        str = '''
        {
                "code":200,
                "count":2,
                "msg":"sss",
                "data":[
                    {
                        "srcHost":"192.168.56.1",
                        "syncPath":"/foundry/a/b/c/add",
                        "fileType":"directory",
                        "syncAction":"add",
                        "id":123
                    },
                    {
                        "srcHost":"192.168.56.1",
                        "syncPath":"/foundry/a/b/c/update",
                        "fileType":"directory",
                        "syncAction":"update",
                        "id":456
                    },
                    {
                        "srcHost":"dggcots03-hs",
                        "syncPath":"/foundry/a/b/c/delete",
                        "fileType":"directory",
                        "syncAction":"delete",
                        "id":789
                    },
                    {
                        "srcHost":"dggcots03-hs",
                        "syncPath":"/foundry/a/b/c/update",
                        "fileType":"directory",
                        "syncAction":"update",
                        "id":1000
                    },
                    {
                        "srcHost":"dggcots03-hs",
                        "syncPath":"/foundry/a/b/c/delete",
                        "fileType":"directory",
                        "syncAction":"delete",
                        "id":1002
                    }
                ]
            }
        '''
        ret = json.loads(str)
        # logger.info(str)
        return ret

    def updateSyncDataState(self, syncDataInfo):
        logger.info("update sync  state: %s msg:%s" % (syncDataInfo.get("syncState", ""), syncDataInfo.get("msg", "")) )
        # logger.info(syncDataInfo)
        # 更新同步状态

        # 保存更新失败的数据，定时重试更新
        self.reportErrorList.append(syncDataInfo)
        pass

    def syncWork(self):
        # 请求要同步的数据
        ret = self.getSyncData()

        if ret is None:
            logger.error('unable request data from service')
            return False

        # 校验参数
        if "code" not in ret or str(ret["code"]) != "200":
            logger.error(ret)
            return False

        if "data" not in ret or isinstance(ret["data"], list) is False:
            logger.error(ret)
            logger.error("unable get data")
            return False


        responseData = ret["data"]

        # 启动线程池
        with ThreadPoolExecutor(max_workers=goConfig.ThreadMaxWorker) as t:

            taskList = []
            # 遍历这些数据
            for syncDataDict in responseData:
                syncItem = SyncDataItem(syncDataDict)

                # 更新状态 同步中
                syncDataDict["syncState"] = goConfig.SyncStateSyncing
                # syncDataDict["msg"] = ''
                self.updateSyncDataState(syncDataDict)

                # 添加到线程池当中
                taskList.append(t.submit(syncItem.run))

            # 线程等待完成
            for future in as_completed(taskList):
                retData = future.result()
                logger.info(future.done())
                logger.info(retData)

                self.updateSyncDataState(retData)

        return True

    def reportState(self):
        # 更新状态
        logger.info("timer  update sync  state")
        pass
