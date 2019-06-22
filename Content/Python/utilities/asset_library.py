# -*- coding: utf-8 -*-

import unreal


class ProcessSlotTask:

    @classmethod
    def execute(cls, label, callback, iteratable):
        if len(iteratable) != 0:
            with unreal.ScopedSlowTask(len(iteratable), label) as task:
                task.make_dialog(True)

                for row in iteratable:
                    if task.should_cancel():
                        break

                    callback(row)
                    task.enter_progress_frame(1)

    @classmethod
    def filter(cls, label, callback, iteratable):
        result = []
        if len(iteratable) != 0:
            with unreal.ScopedSlowTask(len(iteratable), label) as task:
                task.make_dialog()

                result = filter(lambda x: ProcessSlotTask.filter_internal(
                    task, x, callback), iteratable)

        return result

    @classmethod
    def filter_internal(cls, task, it, callback):
        b_result = callback(it)
        task.enter_progress_frame(1)
        return b_result

    @classmethod
    def map(cls, label, callback, iteratable):
        result = []
        if len(iteratable) != 0:
            with unreal.ScopedSlowTask(len(iteratable), label) as task:
                task.make_dialog()

                result = map(lambda x: ProcessSlotTask.map_internal(
                    task, x, callback), iteratable)

        return result

    @classmethod
    def map_internal(cls, task, it, callback):
        result = callback(it)
        task.enter_progress_frame(1)
        return result


class AssetStatics:

    @classmethod
    def isinstance(cls, asset_data, class_info, b_strictly=False):
        if asset_data.is_valid():
            if class_info.static_class().get_name() == asset_data.asset_class:
                return True
            elif b_strictly:
                asset_obj = asset_data.get_asset()
                if asset_obj is not None:
                    return isinstance(asset_obj, class_info)
        return False

    @classmethod
    def filter_by_class(cls, class_info, asset_data_list, b_include_that, b_strictly=True):
        return ProcessSlotTask.filter(
            'filtering by class',
            lambda x: b_include_that == cls.isinstance(
                x, class_info, b_strictly),
            asset_data_list
        )
