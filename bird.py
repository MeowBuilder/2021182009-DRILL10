# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image
from state_machine import *
import game_framework

# Bird Run Speed
PIXEL_PER_METER = (100.0 / 3.0) # 100pixel 30cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Move:
    @staticmethod
    def enter(bird, e):
        bird.frame = 0
        bird.dir = 1
        bird.action = 2
        bird.x = 0
        pass

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if bird.frame > 4:
            bird.frame = 0
            bird.action -= 1
        elif bird.action == 0 and bird.frame > 3:
            bird.action = 2
            bird.frame = 0

        print(f'{bird.x=}, {bird.y=}')
        print(f'{bird.dir=}')
        print(f'{RUN_SPEED_PPS=}, {game_framework.frame_time=}')
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) * 180, bird.action * 160, 180, 160, bird.x, bird.y, 100,100)
        elif bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 180, bird.action * 160, 180, 160, 0, 'v', bird.x, bird.y,100,100)

class Bird:
    def __init__(self):
        self.x, self.y = 400, 90
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Move)
        self.state_machine.set_transitions({
            Move : {}
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()