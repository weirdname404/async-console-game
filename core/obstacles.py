from core.event_loop import Sleep
from core.types import Coordinate, Size
from utils.curses_tools import draw_frame, get_frame_size
from utils import Singleton


class ObstacleManager(metaclass=Singleton):
    __slots__ = ('objects',)

    def __init__(self):
        self.objects = {}

    def __iter__(self):
        return iter(self.objects.values())

    def add_object(self, obj):
        self.objects[obj.uid] = obj
        # memory leak
        if len(self.objects) > 10:
            raise Exception

    def get_front_objects(self, x: int, x1: int = 1):
        '''Yields object that has intersection on X axis with given x and x1'''
        for obj in self.objects.values():
            if obj.x <= x <= obj.x1 or obj.x <= x1 <= obj.x1:
                yield obj

    def remove_object(self, obj_id):
        self.objects.pop(obj_id)


obstacle_manager = ObstacleManager()


class Obstacle:
    __slots__ = (
        'x', 'x1', 'y',
        'width', 'height',
        'uid', 'term', 'frame'
    )

    def __init__(self, pos, frame: str = None, uid: int = None):
        x, y = pos

        if frame is None:
            w, h = (1, 1)
        else:
            w, h = get_frame_size(frame)

        self.x, self.y = x, y
        self.x1 = x + w
        self.width, self.height = w, h
        self.frame = frame
        self.uid = uid
        self.term = False

    def get_center_pos(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def terminate(self):
        self.term = True

    def get_bounding_box_frame(self):
        # increment box size to compensate obstacle movement
        return '\n'.join(
            _get_bounding_box_lines(self.width + 1, self.height + 1)
        )

    def get_bounding_box_pos(self):
        return self.x - 1, self.y - 1

    def get_bounding_box(self):
        x, y = self.get_bounding_box_pos()
        return x, y, self.get_bounding_box_frame()

    def has_collision(self, obj_pos: Coordinate, obj_size: Size = (1, 1)):
        '''Determine if collision has occured. Return True or False.'''
        return has_collision(
            obstacle_pos=(self.x, self.y),
            obstacle_size=(self.width, self.height),
            obj_pos=obj_pos,
            obj_size=obj_size
        )


def _get_bounding_box_lines(width, height):

    yield ' ' + '-' * width + ' '
    for _ in range(height):
        yield '|' + ' ' * width + '|'
    yield ' ' + '-' * width + ' '


async def show_obstacles(canvas):
    """Display bounding boxes of every obstacle in a list"""

    while True:
        boxes = []

        for obstacle in obstacle_manager:
            boxes.append(obstacle.get_bounding_box())

        for x, y, frame in boxes:
            draw_frame(canvas, x, y, frame)

        await Sleep(0)

        for x, y, frame in boxes:
            draw_frame(canvas, x, y, frame, negative=True)


def _is_point_inside(x, y, width, height, point_x, point_y):
    x_flag = x <= point_x <= x + width
    y_flag = y <= point_y <= y + height

    return x_flag and y_flag


def has_collision(obstacle_pos: Coordinate,
                  obstacle_size: Size,
                  obj_pos: Coordinate,
                  obj_size: Size = (1, 1)):
    '''Determine if collision has occured. Return True or False.'''

    opposite_obstacle_corner = (
        obstacle_pos[0] + obstacle_size[0] - 1,
        obstacle_pos[1] + obstacle_size[1] - 1,
    )

    opposite_obj_corner = (
        obj_pos[0] + obj_size[0] - 1,
        obj_pos[1] + obj_size[1] - 1,
    )

    return any([
        _is_point_inside(*obstacle_pos, *obstacle_size, *obj_pos),
        _is_point_inside(*obstacle_pos, *obstacle_size, *opposite_obj_corner),

        _is_point_inside(*obj_pos, *obj_size, *obstacle_pos),
        _is_point_inside(*obj_pos, *obj_size, *opposite_obstacle_corner),
    ])
