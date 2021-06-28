#-- coding:utf8 --

import os.path
import traceback
import time
import subprocess

from Common import goConfig, getLogger

logger = getLogger(__name__)


class SyncDataItem():

    def __init__(self, syncDataDict):
        self.syncDataInfo = syncDataDict
        logger.info("syspath: " + self.syncDataInfo.get("syncPath",""))
        pass

    def run(self):
        # time.sleep(10)

        syncInfo = self.syncDataInfo

        sycnState = goConfig.SyncStateFailed
        # msg = ''
        ret, ckMsg = self.checkParam(syncInfo)
        if ret is False:
            sycnState = goConfig.SyncStateFailed
            msg = ckMsg

        else:
            try:
                host = syncInfo["srcHost"]
                # TODO: 检查是否可以免密登录
                # ret, msg = goConfig.checkHostLogin(host)
                # if not ret:
                #     syncInfo["syncState"] = goConfig.SyncStateFailed
                #     syncInfo["msg"] = msg
                #     return syncInfo

                # 调用命令 添加、删除、修改
                action = syncInfo["syncAction"]
                if action == goConfig.ActionAdd or action == goConfig.ActionUpdate:
                    ret, msg = self.addOrUpdateData(syncInfo)

                elif action == goConfig.ActionDelete:
                    ret, msg = self.deleteData(syncInfo)
                else:
                    msg = "unknown action : %s" % action
                    ret = False

            except KeyboardInterrupt as ex:
                msg = traceback.format_exc()
                ret = False
            except BaseException as ex:
                msg = traceback.format_exc()
                ret = False

        # logger.info("%s %s\n" % (ret, msg))
        if ret:
            sycnState = goConfig.SyncStateSuccess

        syncInfo["syncState"] = sycnState
        syncInfo["msg"] = msg
        return syncInfo

    def addOrUpdateData(self, syncInfo):
        ret = False
        msg = ''
        host = syncInfo["srcHost"]

        path = syncInfo['syncPath']
        # 去除路径多余的斜杠
        path = os.path.normpath(path)

        # 调用rsyn 同步数据， 路径不存在自动创建
        fileType = syncInfo.get("fileType")

        parentPath = os.path.dirname(path)
        # if fileType == goConfig.SyncTypeFile or fileType == goConfig.SyncTypeLink:
        #     parentPath = os.path.dirname(path)
        # else:
        #     parentPath = path

        mode = 0o755
        group = ''
        if not os.path.exists(parentPath):
            pathspilt = parentPath.split("/")

            # 按层级创建目录，修改群组
            joinPath = '/'
            for pathLevel in pathspilt:
                joinPath = '%s/%s'.format(joinPath, pathLevel)
                logger.info("jonPath:" + joinPath)
                if os.path.exists(parentPath):
                    os.mkdir(joinPath)

                    # 修改目录的群组
                    if group is not '':
                        os.system("/bin/chgrp %s %s" % (group, joinPath))

        srcPath = '%s:%s' % (host, path)
        destPath = '%s' % parentPath  # 同步到父路径上面

        # # 查看目标路径是否存在,可能之前已经同步过了
        # if os.path.exists(destPath):
        #     #目标路径是 它的上一层
        #     destPath = os.path.dirname(destPath)

        # cmd = ["rsync", '-a', srcPath, destPath]
        cmd = "rsync -av '%s' '%s' " % (srcPath, destPath)
        logger.info(cmd)
        # 查看 rysnc 退出状态
        stat, out = subprocess.getstatusoutput(cmd)
        ret = False
        if stat == 0:
            # success
            ret = True

        return ret, out


    def deleteData(self, syncInfo):
        path = syncInfo['syncPath']
        # 去除路径多余的斜杠
        path = os.path.normpath(path)
        if len(path) < 12:
            return False, "path[%s] is too short unable delete" % path

        if os.path.exists(path):
            parentPath = os.path.dirname(path)
            tmpPath = parentPath + "/.tmp/"
            #os.mkdir(tmpPath)

            os.renames(path, tmpPath)
            logger.info("mv %s %s", path, tmpPath)

            cmd = "rm -rf %s " % tmpPath
            logger.info(cmd)
            # 查看 rysnc 退出状态
            stat, out = subprocess.getstatusoutput(cmd)
            ret = False
            if stat == 0:
                # success
                ret = True
        else:
            ret = True
            out = "file or directory not exists: %s" % path

        return ret, out


    def checkParam(self, syncInfo):
        msg = ''

        if "syncPath" not in syncInfo or syncInfo['syncPath'] is '':
            msg = 'syncPath is None'
            return False, msg

        if "srcHost" not in syncInfo or syncInfo['srcHost'] is '':
            msg = 'srcHost is None'
            return False, msg

        fileType = syncInfo.get('fileType', '')
        if fileType is '' or fileType not in goConfig.SyncTypeList:
            msg = 'fileType is None or  unknown file type:%s avalid type %s '.format(fileType, goConfig.SyncTypeList)
            return False, msg

        if "syncAction" not in syncInfo or syncInfo['syncAction'] is '':
            msg = 'fileType is None'
            return False, msg

        return True, msg

