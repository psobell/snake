from typing import Optional
from game_display import GameDisplay
import game_display
import game_utils


class SnakeGame:

    def __init__(self, height, width, apples, debug, walls, rounds) -> None:
        '''
        Creates game, receives args, creates attributes
        '''
        self.height = height
        self.width = width
        self.apples = apples
        self.debug = debug
        self.walls = walls
        self.rounds = rounds
        self.__x = self.width//2
        self.__y = self.height//2
        self.__key_clicked = None
        self.body_coord = [(self.__x, self.__y), (self.__x, self.__y - 1),
                           (self.__x, self.__y - 2)]
        self.prev_key = "Up"
        self.turn = 0
        self.apples_coord = []
        self.turns_to_grow = 0
        self.ate = False
        self.grew_this_turn = False
        self.score = 0
        self.walls_coord = []
        self.snake_crash_wall = False

    def read_key(self, key_clicked: Optional[str])-> None:
        self.__key_clicked = key_clicked

    def update_objects(self)-> None:
        '''
        moves the snake and the walls, adds walls and apples if necessary
        '''
        if not self.debug:
            self.cut_snake()
            self.move_snake()
            self.hungry_snake()
        self.move_wall()
        self.update_walls()
        self.update_apples()
        self.check_wall_crash()

    def check_crash(self):
        '''
        checks if snake crashes into edge, itself or a wall, returns True if so
        '''
        if ((self.__key_clicked == 'Left') and (self.__x < 0
                or ((self.__x-1, self.__y) in self.body_coord))):
            return True
        elif ((self.__key_clicked == 'Right')
                and (not self.__x in range(self.width)
                or (self.__x+1, self.__y) in self.body_coord)):
            return True
        elif (self.__key_clicked == 'Up'
                and (self.__y not in range(self.height)
                or (self.__x, self.__y+1) in self.body_coord)):
            return True
        elif ((self.__key_clicked == 'Down') and (self.__y < 0
                or ((self.__x, self.__y-1) in self.body_coord))):
            return True
        for wall in self.walls_coord:
            if (self.__x, self.__y) in wall:
                return True
        if len(self.body_coord) == 1:
            return True
        return False

    def valid_direction(self):
        '''
        Checks previous direction and new direction, and if it's valid
        '''
        if ((self.__key_clicked == 'Up' and self.prev_key == 'Down')
                or (self.__key_clicked == 'Down' and self.prev_key == 'Up')
                or (self.__key_clicked == 'Left' and self.prev_key == 'Right')
                or (self.__key_clicked == 'Right' and self.prev_key =='Left')):
            self.__key_clicked = self.prev_key

    def move_snake(self):
        '''
        Removes last coordinate of snake, and adds a new head to beginning,
        checks if crashed
        '''
        if self.turns_to_grow != 0:  # if the snake ate an apple, don't remove
            self.grew_this_turn = True  # last coordinate
        self.valid_direction()
        if not self.__key_clicked:
            self.__key_clicked = self.prev_key
        if (self.__key_clicked == 'Left') and not self.check_crash():
            self.__x -= 1
            self.body_coord.insert(0, (self.__x, self.__y))
            if self.turns_to_grow == 0:
                self.body_coord.pop()
            else:
                self.turns_to_grow -= 1
            self.prev_key = 'Left'
        if self.__key_clicked == 'Right' and not self.check_crash():
            self.__x += 1
            self.body_coord.insert(0, (self.__x, self.__y))
            if self.turns_to_grow == 0:
                self.body_coord.pop()
            else:
                self.turns_to_grow -= 1
            self.prev_key = 'Right'
        if (self.__key_clicked == 'Up') and not self.check_crash():
            self.__y += 1
            self.body_coord.insert(0, (self.__x, self.__y))
            if self.turns_to_grow == 0:
                self.body_coord.pop()
            else:
                self.turns_to_grow -= 1
            self.prev_key = 'Up'
        if (self.__key_clicked == 'Down') and not self.check_crash():
            self.__y -= 1
            self.body_coord.insert(0, (self.__x, self.__y))
            if self.turns_to_grow == 0:
                self.body_coord.pop()
            else:
                self.turns_to_grow -= 1
            self.prev_key = 'Down'
        if self.check_crash():  # if snake crashed, remove head
            self.body_coord.pop(0)

    def update_walls(self):
        '''
        If necessary adds walls, makes sure it's on an empty cell
        '''
        for wall in self.walls_coord:
            if len(wall) == 1:  # if wall left the board, remove from list
                self.walls_coord.remove(wall)
        if len(self.walls_coord) < self.walls:
            mid_wall = game_utils.get_random_wall_data()
            col, row, direction = mid_wall[0], mid_wall[1], mid_wall[2]
            if direction == "Up" or direction == "Down":
                wall_body = [(col, row-1), (col, row), (col, row+1), direction]
                if row == self.height - 1:
                    wall_body.pop(2)
                if row == 0:
                    wall_body.pop(0)
            if direction == "Right" or direction == "Left":
                wall_body = [(col-1, row), (col, row), (col+1, row), direction]
                if col == self.width-1:
                    wall_body.pop(2)
                if col == 0:
                    wall_body.pop(0)
            for coord in wall_body[:-1]:  # wall_body without directon
                if coord in self.apples_coord or coord in self.body_coord:
                    return
                for wall in self.walls_coord:
                    for coordinate in wall[:-1]:
                        if coordinate == coord:
                            return
            self.walls_coord.append(wall_body)  # updates walls_coord

    def update_apples(self):
        '''
        Adds apples if necessary, makes sure it's on an empty cell
        '''
        if len(self.apples_coord) < self.apples:
            location = game_utils.get_random_apple_data()
            if (location not in self.body_coord
                    and location not in self.apples_coord):
                self.apples_coord.append(location)

    def hungry_snake(self):
        '''
        checks if the snake ate an apples, adds three turns that
        the snake will grow
        '''
        if self.body_coord[0] in self.apples_coord:
            self.apples_coord.remove(self.body_coord[0])
            self.turns_to_grow += 3
            self.update_apples()  # adds another apple to board
            self.ate = True

    def special_case(self, coords, direction):
        '''
        in a case that the wall starts off the board so its lenth is two and it
        doesn't leave the board, we have to add one cell
        '''
        if len(coords) == 3:
            if direction == "Up" and coords[0][1] == 0:
                return True
            if direction == "Down" and coords[-1][1] == self.height - 1:
                return True
            if direction == "Right" and coords[0][0] == 0:
                return True
            if direction == "Left" and coords[-1][0] == self.width - 1:
                return True

    def move_wall(self):
        '''
        moves the walls on even turns, checks if the wall leaves the board
        '''
        if self.turn % 2 == 0:
            for wall in range(len(self.walls_coord)):
                direction = self.walls_coord[wall][-1]
                coords = [coord for coord in self.walls_coord[wall][:-1]]
                first_col, first_row = coords[0][0], coords[0][1]  # lowest/leftmost
                if direction == "Up":
                    if first_row + len(coords) != self.height:
                        coords.append((first_col, first_row + len(coords)))
                    if not self.special_case(coords, direction):
                        coords.pop(0)
                if direction == "Down":
                    if first_row != 0:
                        coords.insert(0, (first_col, first_row-1))
                    if not self.special_case(coords, direction):
                        coords.pop()
                if direction == "Right":
                    if first_col + len(coords) != self.width:
                        coords.append((first_col + len(coords), first_row))
                    if not self.special_case(coords, direction):
                        coords.pop(0)
                if direction == "Left":
                    if first_col != 0:
                        coords.insert(0, (first_col - 1, first_row))
                    if not self.special_case(coords, direction):
                        coords.pop()
                self.walls_coord[wall] = coords
                self.walls_coord[wall].append(direction)

    def check_wall_crash(self):
        '''
        Checks if a wall hits the snake's body.  If so, saves the coordinate
        in snake_crash_wall
        Also, checks if a wall hits an apple, and removes the apple
        '''
        for wall in self.walls_coord:
            for coord in wall[:-1]:
                if coord in self.body_coord:
                    self.snake_crash_wall = coord
                if coord in self.apples_coord:
                    self.apples_coord.remove(coord)

    def cut_snake(self):
        '''
        if a wall hit the snake, cuts the snake at the coordinate in
        snake_crash_wall
        '''
        if self.snake_crash_wall:
            idx = self.body_coord.index(self.snake_crash_wall)
            self.body_coord = self.body_coord[:idx]
            self.snake_crash_wall = False

    def draw_board(self, gd: GameDisplay) -> None:
        '''
        adds all of the updated objects to the board
        '''
        if not self.debug:
            for cell in self.body_coord:
                x = cell[0]
                y = cell[1]
                gd.draw_cell(x, y, "black")
        if self.turn == 0:
            self.update_walls()
            self.update_apples()
        for cell in self.apples_coord:
            x = cell[0]
            y = cell[1]
            gd.draw_cell(x, y, "green")
        for wall in self.walls_coord:
            for cell in range(len(wall)-1):
                x = wall[cell][0]
                y = wall[cell][1]
                gd.draw_cell(x, y, "blue")
        if self.ate:
            if self.grew_this_turn:
                self.score += int(len(self.body_coord)-1**0.5)
                gd.show_score(self.score)
            else:
                self.score += int(len(self.body_coord)**0.5)
                gd.show_score(self.score)
            self.ate = False

    def end_round(self) -> None:
        '''
        updates turn
        '''
        self.grew_this_turn = False
        self.turn += 1

    def is_over(self) -> bool:
        '''
        if snake crashed or turn reaches max rounds, ends game
        '''
        if self.rounds == 0:
            return True
        if self.turn == self.rounds:
            return True
        if self.check_crash():
            return True
        return False
