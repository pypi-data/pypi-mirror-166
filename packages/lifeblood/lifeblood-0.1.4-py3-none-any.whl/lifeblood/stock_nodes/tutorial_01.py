from lifeblood.basenode import BaseNode, ProcessingResult, ProcessingContext
from lifeblood.enums import NodeParameterType
from typing import Iterable


def node_class():
    return LogSomeAttribute


class InnerClass:
    def __init__(self, node: "LogSomeAttribute"):
        print(node.my_plugin())


class LogSomeAttribute(BaseNode):
    def __init__(self, name):
        super().__init__(name)
        ui = self.get_ui()
        self.test = InnerClass(self)
        with ui.initializing_interface_lock():
            ui.add_parameter('where to write', 'Log File Path', NodeParameterType.STRING, '')
            ui.add_parameter('what to write', 'Saved Data', NodeParameterType.STRING, "`task['some_attr']`")

    @classmethod
    def label(cls) -> str:
        return 'log an attribute'

    @classmethod
    def tags(cls) -> Iterable[str]:
        return 'tutorial', 'log', 'attribute'

    @classmethod
    def type_name(cls) -> str:
        return 'tutorial::logattr'

    def process_task(self, context: ProcessingContext) -> ProcessingResult:
        with open(context.param_value('where to write'), 'w') as f:
            f.write(str(context.param_value('what to write')))
        return ProcessingResult()
