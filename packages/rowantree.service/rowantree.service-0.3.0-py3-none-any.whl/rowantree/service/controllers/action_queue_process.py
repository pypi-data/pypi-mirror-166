from rowantree.contracts import ActionQueue

from .abstract_controller import AbstractController


class ActionQueueProcessController(AbstractController):
    def execute(self, action_queue: ActionQueue) -> None:
        self.dao.process_action_queue(action_queue=action_queue)
