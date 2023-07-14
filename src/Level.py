import numpy as np
import random


class Level(object):
    def __init__(self, shape):
        self.Layout = np.zeros(shape, dtype=int).tolist()

    def getDirection(self, room, size):
        if room == 0:
            direction = 1
        elif room == size:
            direction = -1
        else:
            direction = pow(-1, random.randint(0, 1))

        return direction

    def createPath(self, size):
        (ChooseStartState, AdjacentRoomState, NextFloorState) = (1, 2, 3)

        height = len(self.Layout) - 1
        room = 0
        state = ChooseStartState
        floor = 0
        direction = 0
        done = False
        floorChance = 0.6
        while not done:
            roomType = "hall"
            if state == ChooseStartState:
                room = random.randint(0, size)
                direction = self.getDirection(room, size)
                state = AdjacentRoomState
                roomType = "start"
            elif state == AdjacentRoomState:
                room += direction
                if direction != 0 and ((room == 0 or room == size) or random.random() < floorChance):
                    state = NextFloorState
                    roomType = "drop"
                    if floor == height:
                        done = True
                        roomType = "end"
            elif state == NextFloorState:
                floor += 1
                direction = self.getDirection(room, size)
                state = AdjacentRoomState

            self.Layout[floor][int(room)] = roomType

    def generate_as_text(self, rooms):
        mapLines = []
        size = len(self.Layout[0]) - 1
        if size <= 0:
            return mapLines

        self.createPath(size)
        for floor in self.Layout:
            lines = np.zeros(len(rooms[0][0])).tolist()
            lines = list(map(lambda x: "w", lines))

            for room in floor:
                select = random.randint(0, len(rooms[room]) - 1)
                for index, line in enumerate(lines):
                    lines[index] += (rooms[room])[select][index]

            for line in lines:
                mapLines.append(line + "w")

        return mapLines
