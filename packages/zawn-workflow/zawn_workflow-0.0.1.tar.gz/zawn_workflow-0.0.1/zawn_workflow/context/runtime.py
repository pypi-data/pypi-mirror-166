#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-08-20
# @Author  : wuxiangbin
# @Site    : www.0-9.ink
# @File    : runtime.py
# @Software: zawn_utils
# @Function:
import datetime

from zawn_workflow.context.base import NodeFactory
from zawn_workflow.context.context import BaseContext
from zawn_workflow.context.searcher import WorkFlowSearcher
from zawn_workflow.data.exception import ModelNotFoundError


class WorkFlowRuntime(BaseContext):
    """ 工作流程运行时 """

    def task_tick(self, instance_id: str, task_list: list) -> BaseContext:
        """ 任务列表载入工作流程引擎执行 """

        work_task = self.data_factory.work_task
        task_field_mapping = {
            'node_id': 'task_id',
            'node_name': 'task_name',
            'node_type': 'task_type',
        }
        context = NodeFactory.make_node(task_list, mapping=task_field_mapping).tick()
        new_task_list = context.to_node_list(mapping=task_field_mapping)
        for task in new_task_list:
            self.operation_list.append(work_task.new_operation(
                'insert', filter={}, update=work_task.to_db(task),
            ))

        return self

    def copy_node_to_task(self, node_list: list, instance_id: str, **kwargs) -> BaseContext:
        """ 复制节点数据到任务数据 """

        now = datetime.datetime.now().astimezone()
        op = kwargs.get('op', 'system')

        work_instance = self.data_factory.work_instance

        # 创建任务id，组合成映射表
        id_dict = {}
        for node in node_list:
            id_dict[node['node_id']] = work_instance.new_id()

        # 组装任务操作列表
        task_list = []
        for node in node_list:
            node_id = node['node_id']
            parent_id = node['parent_id']
            task_id = id_dict[node_id]
            task = {
                'task_id': task_id,
                'parent_id': id_dict[parent_id],
                'task_name': node['node_name'],
                'task_type': node['node_type'],
                'sort': node['sort'],
                'handler_type': node['handler_type'],
                'handler_id': node['handler_id'],
                'instance_id': instance_id,
                **kwargs,
                'status': work_instance.state.SUBMIT,
                'create_at': now,
                'create_by': op,
            }
            task_list.append(task)

        # 执行工作流程
        self.task_tick(instance_id, task_list)

        return self

    def create_instance(self, model_id: str, **kwargs) -> BaseContext:
        """ 创建工作实例 """

        # 1. 复制
        work_flow_searcher = WorkFlowSearcher()
        meta, detail_list = (await work_flow_searcher.search_model_detail(model_id, **kwargs)).search()
        if meta['total'] == 0:
            raise ModelNotFoundError(f'工作模型未找到:{model_id}')

        work_instance = self.data_factory.work_instance
        work_task = self.data_factory.work_task
        work_record = self.data_factory.work_record
        work_store = self.data_factory.work_store

        for model in detail_list:
            model_id = model['model_id']
            instance_id = work_instance.new_id()
            nodes = model.pop('nodes', None) or []
            forms = model.pop('forms', None) or []
            if not nodes:
                self.logger.info(f'模型没有配置节点信息:{model_id}')
                continue

            self.operation_list.append(work_instance.new_operation(
                'insert', filter={}, update=work_instance.to_db({
                    'instance_id': instance_id,
                    'instance_name': model['model_name'],
                    'step': 0,
                    'completion_rate': 0,
                    'model_id': model_id,
                })
            ))
            self.copy_node_to_task(nodes, instance_id)

        return self

    def start(self, model_key: str, handler_id: str, **kwargs) -> BaseContext:
        """ 启动 """

        # 启动事件过程
        # 1、检查模型和用户是否存在，如果不存在则返回提示
        # 2、创建实例
        # 3、复制节点到任务
        # 4、执行一次tick
        # 5、执行一次同意时间

        work_flow_searcher = WorkFlowSearcher()
        meta, model_list = await (await work_flow_searcher.search_model(model_key=model_key, **kwargs)).search()
        if meta['total'] != 1:
            return self

        meta, user_list = await (await work_flow_searcher.search_user([handler_id], **kwargs)).search()
        if meta['total'] == 0:
            return self

        return self

    async def agree(
            self, instance_id: str, handler_id: str, form_data: dict, **kwargs):
        """ 同意事件 """
        pass

    async def reject(
            self, instance_id: str, handler_id: str, form_data: dict, **kwargs):
        """ 拒绝事件 """
        pass

    async def assign(
            self, instance_id: str, handler_id: str, form_data: dict, **kwargs):
        """ 指派事件 """
        pass

    async def entrust(
            self, instance_id: str, handler_id: str, form_data: dict, **kwargs):
        """ 委托事件 """
        pass
