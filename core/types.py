from typing import Tuple, Union

# (x, y)
Coordinate = Tuple[int, int]
# (width, height)
Size = Tuple[int, int]

Tic = int
FrameState = Union[int, str]
Frame = Tuple[Tic, FrameState]
Animation = Tuple[Frame]
