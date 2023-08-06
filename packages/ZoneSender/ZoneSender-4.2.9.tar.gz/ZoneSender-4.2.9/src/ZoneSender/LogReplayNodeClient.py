import typing
from pathlib import Path

import grpc

from . import ZoneSenderData
from .BlfIo import BlfIoObjs, BlfObjFromBytes
from .ObjIo import *
from .Protos import LogReplayNode_pb2, LogReplayNode_pb2_grpc
from .SharedMemory import IndexNode, SharedMemZoneSender


class LogReplayNodeClient(object):
    def __init__(self) -> None:
        '''
        ZoneSender 用于记录和回放的客户端
        '''
        self._logReplayStub = LogReplayNode_pb2_grpc.LogReplayNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'.format(ZoneSenderData.LOG_REPLAY_NODE_IP, ZoneSenderData.LOG_REPLAY_NODE_PORT),
                options=ZoneSenderData.GRPC_OPTIONS
            )
        )
        self._shareMemReplayData = SharedMemZoneSender(None, name='ZoneSenderReplay')

    def AddLinDecodeRole(
        self, 
        channels: typing.List[int],
        ldfs: typing.List[str],
        **kwargs) -> int:
        '''
        添加一个 LIN 数据的解析规则
        可以重复添加
        :param channels:list[int] LIN 通道列表
        :param ldfs:list[int] ldf 文件列表
        :return:int
            - 0: 添加成功
            - 1000: raise
        '''
        try:
            ldfs = [str(Path(x_).absolute()) for x_ in ldfs]
            res_ = self._logReplayStub.AddLinDecodeRole(LogReplayNode_pb2.lin_decode_role(
                channels = channels,
                ldfs = ldfs,
            ))
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.AddLinDecodeRole Exception reason {0}'.format(e_))
            return 1000

    def AddCanDecodeRole(
        self,
        can_db_file_path:str,
        channels:typing.List[int],
        cluster_names:typing.List[str],
        **kwargs
        ) -> int:
        '''
        添加一个 CAN 数据的解析规则
        可以重复添加
        :param can_db_file_path:str CAN DB 文件的路径
        :param channels:list[int] LIN 通道列表
        :param ldfs:list[int] ldf 文件列表
        :return:int
            - 0: 添加成功
            - 1000: raise
        '''
        try:
            res_ = self._logReplayStub.AddCanDecodeRole(LogReplayNode_pb2.can_decode_role(
                can_db_file_path = str(Path(can_db_file_path).absolute()),
                channels = channels,
                cluster_names = cluster_names,
            ))
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.AddCanDecodeRole Exception reason {0}'.format(e_))
            return 1000

    def Reset(self) -> int:
        '''
        复位
            - 清空解析配置文件
            - 关闭所有正在解析的文件
        :return:int
            - 0: 复位成功
            - 1000: raise
        '''
        try:
            res_ = self._logReplayStub.Reset(LogReplayNode_pb2.Common__pb2.empty())
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.Reset Exception reason {0}'.format(e_))
            return 1000

    def ReplayNextN(
        self, 
        blf_file_path: str, 
        count: int, 
        result_l_obj: typing.List[BlfIoObjs.BlfIoStruct], 
        reslut_l_time_stamp: typing.List[int]) -> int:
        '''
        解包 N 个数据
        :param blf_file_path:str 要读的 Blf 文件名
        :param count:int 要解析下面的多少个数据 不能超过 131000
        :param result_l:list[BlfIoObjs.BlfIoStruct] 解析后的数据 里面会放 BlfIoObjs.CanISignalIPduPy | BlfIoObjs.LinFramePy
        :return:int
            - 0:成功
            - 1:读结束
        '''
        try:
            res_ = self._logReplayStub.ReplayNextN(LogReplayNode_pb2.decode_n(
                blf_file_path = blf_file_path,
                count = count,
                )
            )
            result_ = int(res_.result.result)    # 结果
            reason_ = str(res_.result.reason)    # 原因
            start_index_ = int(res_.start_index)    # 起始 index
            stop_index_ = int(res_.stop_index)    # 结束 index
            is_stop_ = bool(res_.is_stop)    # 是否读完了
            
            # 写数据 >>>>>>>>
            result_l_obj.clear()
            reslut_l_time_stamp.clear()
            for i_ in range(start_index_, stop_index_):
                node_ = self._shareMemReplayData.GetIndexNode(i_)
                blf_obj_ = BlfObjFromBytes(self._shareMemReplayData.ReadFrame(i_))
                reslut_l_time_stamp.append(node_.time_stamp_ns)
                result_l_obj.append(blf_obj_)
                # pass
            print(res_.result.reason)
            return res_.result.result
            # return 1
        except Exception as e_:
            print('LogReplayNodeClient.DecodeNextN Exception reason {0}'.format(e_))
            return 1000

    def OpenReplayFile(self, blf_file_path: str) -> int:
        '''
        打开回放的文件
        :param blf_file_path:str 要打开的文件路径
        :return:int
            - 0:成功
            - other:失败
        '''
        try:
            res_ = self._logReplayStub.OpenReplayFile(
                LogReplayNode_pb2.Common__pb2.file_path(
                    path=blf_file_path,
                )
            )
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.OpenReplayFile Exception reason {0}'.format(e_))
            return 1000

    def CloseReplayFile(self, blf_file_path: str) -> int:
        '''
        关闭回放的文件
        :param blf_file_path:str 要关闭的文件路径
        :return:int
            - 0:成功
            - other:失败
        '''
        try:
            res_ = self._logReplayStub.CloseReplayFile(
                LogReplayNode_pb2.Common__pb2.file_path(
                    path=blf_file_path,
                )
            )
            print(res_.reason)
            return res_.result
        except Exception as e_:
            print('LogReplayNodeClient.CloseReplayFile Exception reason {0}'.format(e_))
            return 1000

    def GetReplayFileInfo(self, blf_file_path: str, file_info:dict) -> int:
        '''
        获取文件信息
        :param blf_file_path:str 要关闭的文件路径
        :param file_info:dict 文件信息的描述
        :return:int
            - 0:成功
            - other:失败
        '''
        try:
            return 0
        except Exception as e_:
            print('LogReplayNodeClient.GetReplayFileInfo Exception reason {0}'.format(e_))
            return 1000

    def StartLog(self,filepath:str,proto:str) -> tuple:
        '''
        开始录制数据
        :param filepath:str 要录制的文件路径
        :param proto:str 录制的协议，比如CAN/LIN
        :return:tuple (结果,原因)
        '''
        try:
            res_ = self._logReplayStub.StartLog(LogReplayNode_pb2.log_request(
                file_path = LogReplayNode_pb2.Common__pb2.file_path(
                    path = filepath
                ),
                log_flag = 0x1 if proto == 'can' else 0x2 ,
            ))
            if res_.result == 0 :
                return (0,'开始记录成功')
            else :
                raise Exception(f'{res_.reason}')
        except Exception as e_ :
            return (1000,e_)

    def StopLog(self,filepath:str,proto:str) -> int:
        '''
        结束录制数据
        :param filepath:str 要关闭的文件路径
        :param proto:str 录制的协议，比如CAN/LIN
        :return:int
            - 0:成功
            - 1000:失败
        '''
        try:
            res_ = self._logReplayStub.StopLog(LogReplayNode_pb2.log_request(
                file_path = LogReplayNode_pb2.Common__pb2.file_path(
                    path = filepath
                ),
                log_flag = 0x1 if proto == 'can' else 0x2 ,
            ))
            if res_.result == 0 :
                return (0,'停止记录成功')
            else :
                print(res_.reason)
                raise Exception(f'{res_.reason}')
        except Exception as e_ :
            print(e_)
            return (1000,e_)

    def GetLogStatus(self) -> int:
        return 0