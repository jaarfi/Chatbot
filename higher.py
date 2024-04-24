import Jaarfivts.models as models
from collections import deque
from typing import Coroutine, Callable, Union, Optional
from dataclasses import dataclass
from time import process_time


@dataclass
class WorkItem:
    work_to_be_done: Union[models.BaseRequest, Coroutine]
    response: Optional[models.BaseResponse]
    callback_function: Optional[Callable] = None


def flip(duration: float, rotations: int):
    t = process_time()
    deq = deque()
    number_of_frames = int(duration * 60)
    rotation_per_frame = rotations * 360 / number_of_frames
    for i in range(number_of_frames):
        deq.append(
            WorkItem(
                work_to_be_done=models.MoveModelRequest(
                    data=models.MoveModelRequestData(
                        time_in_seconds=0,
                        values_are_relative_to_model=True,
                        rotation=rotation_per_frame,
                        size=0,
                    )
                ),
                response=models.MoveModelResponse,
            )
        )
    diff = process_time() - t
    print("sokcing took", diff)
    return deq


def rainbow():
    deq = deque()
    increase = True
    colors = [0, 255, 0]
    change = 20
    for i in range(2):
        for color in range(3):
            for i in range(int(255 / change)):
                if increase:
                    colors[color] = colors[color] + change
                    if colors[color] > 255:
                        colors[color] = 255
                else:
                    colors[color] = colors[color] - change
                    if colors[color] < 0:
                        colors[color] = 0
                deq.append(
                    WorkItem(
                        work_to_be_done=models.ColorTintRequest(
                            data=models.ColorTintRequestData(
                                color_tint=models.ColorTint(
                                    color_r=colors[1],
                                    color_b=colors[2],
                                    color_g=colors[0],
                                ),
                                art_mesh_matcher=models.ArtMeshMatcher(tint_all=True),
                            )
                        ),
                        response=models.ColorTintResponse,
                    )
                )
            increase = not increase
    return deq


def getCurrentModelSize(callback: Callable):
    deq = deque()
    deq.append(
        WorkItem(
            work_to_be_done=models.CurrentModelRequest(),
            response=models.CurrentModelResponse,
            callback_function=callback,
        )
    )
    return deq


def saveExpressions(callback: Callable):
    deq = deque()
    deq.append(
        WorkItem(
            work_to_be_done=models.ExpressionStateRequest(),
            response=models.ExpressionStateResponse,
            callback_function=callback,
        )
    )
    return deq


def toggleExpression(current_expressions, file: str):
    expression_currently_active = [
        exp.active for exp in current_expressions if exp.file == file
    ]
    expression_currently_active = expression_currently_active[0]

    deq = deque()
    deq.append(
        WorkItem(
            work_to_be_done=models.ExpressionActivationRequest(
                data=models.ExpressionActivationRequestData(
                    expression_file=file, active=not expression_currently_active
                )
            ),
            response=models.ExpressionActivationResponse,
        )
    )
    return deq


def putCoroIntoDeque(coro):
    deq = deque()
    deq.append(WorkItem(work_to_be_done=coro, response=models.BaseResponse))
    return deq
