#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-20
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : identity.py
# @Software: zawn_utils
# @Function:
from io import BytesIO
from typing import List

from zawn_orm.database import Operation
from zawn_workflow.context.context import BaseContext


class WorkFlowIdentity(BaseContext):
    """ 工作流程身份 """

    def import_data(self, data: list, **kwargs) -> BaseContext:
        """ 导入身份信息列表 """

        # 整理用户和用户组的数据，写入数据库
        user_dict = {}
        new_data = []
        for row in data:
            user_id = row.pop('用户编号', None)
            user_name = row.get('用户姓名', None)

            # 无效的数据，或者已经存在的数据，则跳过
            if (not (user_id and user_name)) or (user_name in user_dict):
                continue

            # 整理映射数据和新的列表
            user_dict[user_name] = user_id
            new_data.append(row)

        for user_name, user_id in user_dict.items():
            # 用户数据
            self.operation_list.append(self.data_factory.work_user.new_operation(
                'insert',
                filter={},
                update=self.data_factory.work_user.to_db({'user_id': user_id, 'user_name': user_name, **kwargs}),
            ))

        for row in new_data:
            user_id = user_dict[row.pop('用户姓名')]
            # 用户组数据
            for group_name, value in row.items():
                if value in ['', '-']:
                    continue

                # 如果关联结果存在于用户字典，则以关联类型新增记录
                if value in user_dict:
                    self.operation_list.append(self.data_factory.work_group.new_operation(
                        'insert',
                        filter={},
                        update=self.data_factory.work_group.to_db({
                            'group_type': 'relation',
                            'group_name': group_name,
                            'user_id': user_id,
                            'target_id': user_dict[value],
                            **kwargs,
                        }),
                    ))

                # 如果关联结果不存在于用户字典，则以用户组类型新增记录
                else:
                    self.operation_list.append(self.data_factory.work_group.new_operation(
                        'insert',
                        filter={},
                        update=self.data_factory.work_group.to_db({
                            'group_type': 'group',
                            'group_name': group_name,
                            'user_id': user_id,
                            'target_id': '_',
                            **kwargs,
                        }),
                    ))

        return self

    def import_xlsx(self, xlsx_data: BytesIO, **kwargs) -> BaseContext:
        """ 导入身份信息表格 """

        # 读取xlsx文件，读取失败将返回0
        # 清空所有用户和用户组数据，重新写入最新数据

        # 读取xlsx文件，读取失败将返回0
        data = self.read_xlsx(xlsx_data, 0)
        if not data:
            return self

        # 清空所有用户和用户组数据，重新写入最新数据
        self.operation_list: List[Operation] = [
            self.data_factory.work_user.new_operation(
                'delete',
                filter=kwargs,
                update={}
            ),
            self.data_factory.work_group.new_operation(
                'delete',
                filter=kwargs,
                update={}
            ),
        ]

        self.import_data(data, **kwargs)
        return self
