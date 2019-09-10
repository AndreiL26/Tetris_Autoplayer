''' Implement an AI to play tetris '''
from random import Random
from te_settings import Direction

class AutoPlayer():
    def __init__(self, controller):
        self.controller = controller
        self.rand = Random()
        self.cnt = 0
        self.first_block = True
        self.extiles = []
        for _ix in range(0, 20):
            self.extiles.append([0] * 10)
        self.moves_to_do = []
        self.rotations_to_do = []
        self._ix = 0
       
        

    def next_move(self, gamestate):
        ''' next_move() is called by the game, once per move.
            gamestate supplies access to all the state needed to autoplay the game.'''
        
        tiles = gamestate.get_tiles ()
        if (not self.Equal (tiles, self.extiles)) or self.first_block == True:
            self.extiles = tiles
            self.cnt = (self.cnt + 1) % 3
            (max_score, self.moves_to_do, self.rotations_to_do) = self.compute_best(gamestate, 1)
            self._ix = 0
            self.first_block = False

        self.do_next_move (self._ix, self.moves_to_do, self.rotations_to_do, gamestate)
        self._ix += 1

    def move_when_possible (self, crt_Direction, gamestate, crt_Recursion):
        if crt_Recursion <= 2:

            move_By = rotate_By = Dir = 0
            landed = False
            max_Score = None
            crt_Moves = []
            best_Moves = []
            crt_Rotates = []
            best_Rotates = []
            top_Five = []
            Score = 0
            prv_Score = 0
            lines_Score = 0

            if crt_Recursion == 1:
                for _ix in range (0, 5):
                    top_Five.append ([-99999, gamestate, crt_Moves, crt_Rotates])

            if crt_Direction == 1:
                move_Direction = Direction.RIGHT
            else:
                move_Direction = Direction.LEFT

            while (move_By <= 5):
                for _wantedRotation in range (0, 4):
                    crt_Moves.clear()
                    crt_Rotates.clear()
                    crt_Simulation = gamestate.clone (True)
                    aux = move_By
                    crt_Rotation = crt_Simulation.get_falling_block_angle ()
                    (rotate_By, Dir) = self.compute_rotation (crt_Rotation, _wantedRotation)
                    if Dir == 1:
                        rotate_Direction = Direction.RIGHT
                    else:
                        rotate_Direction = Direction.LEFT

                    while aux is not 0 or rotate_By is not 0:
                        if aux is not 0 and rotate_By is not 0:
                            crt_Simulation.move (move_Direction)
                            crt_Moves.append (move_Direction)
                            crt_Simulation.rotate (rotate_Direction)
                            crt_Rotates.append (rotate_Direction)
                            aux -= 1
                            rotate_By -= 1
                        elif aux is not 0 and rotate_By is 0:
                            crt_Simulation.move (move_Direction)
                            crt_Moves.append (move_Direction)
                            aux -= 1
                        elif aux is 0 and rotate_By is not 0:
                            crt_Simulation.rotate (rotate_Direction)
                            crt_Rotates.append (rotate_Direction)
                            rotate_By -= 1

                        landed = crt_Simulation.update ()

                    while not landed:
                        landed = crt_Simulation.update ()
                        prv_Score = lines_Score
                        lines_Score = crt_Simulation.get_score()

                    if lines_Score - prv_Score < 100:
                        lines_Cleared = 0
                    elif lines_Score - prv_Score < 400:
                        lines_Cleared = 1
                    elif lines_Score - prv_Score < 800:
                        lines_Cleared = 2
                    elif lines_Score - prv_Score < 1600:
                        lines_Cleared = 3
                    else:
                        lines_Cleared = 4


                    if crt_Recursion == 2:
                        crt_Score = self.compute_score (crt_Simulation, lines_Cleared)
                        if max_Score is None or crt_Score > max_Score:
                            max_Score = crt_Score 
                            best_Moves = crt_Moves.copy()
                            best_Rotates = crt_Rotates.copy()  
                    elif crt_Recursion == 1:
                        crt_Score = self.compute_score (crt_Simulation, lines_Cleared)
                        for _ix in range (4, -1, -1):
                            if crt_Score > top_Five[_ix][0]:
                                for _jx in range (0, _ix):
                                    top_Five[_jx][0] = top_Five[_jx+1][0]
                                    top_Five[_jx][1] = top_Five[_jx+1][1]
                                    top_Five[_jx][2] = top_Five[_jx+1][2].copy()
                                    top_Five[_jx][3] = top_Five[_jx+1][3].copy()
                                top_Five[_ix][0] = crt_Score
                                top_Five[_ix][1] = crt_Simulation
                                top_Five[_ix][2] = crt_Moves.copy()
                                top_Five[_ix][3] = crt_Rotates.copy()
                                break                                                                                           
                                        
                move_By += 1

            if crt_Recursion == 1:
                for _ix in range (0, 5):
                    Score = self.compute_best (top_Five[_ix][1], crt_Recursion + 1)[0]
                    Score += top_Five[_ix][0]
                    if max_Score is None or Score > max_Score:
                        max_Score = Score 
                        best_Moves = top_Five[_ix][2].copy()
                        best_Rotates = top_Five[_ix][3].copy()  
        return (max_Score, best_Moves, best_Rotates)                    

    def compute_rotation (self, crt_Rotation, _wantedRotation):
        left_moves = self.compute_moves (_wantedRotation, crt_Rotation, -1)
        right_moves = self.compute_moves (_wantedRotation, crt_Rotation, 1)
        if left_moves >= right_moves:
            return (right_moves, 1)
        return (left_moves, -1)
        
    def compute_moves (self, _wantedRotation, crt_Rotation, rotation_Direction):
        moves = 0
        while crt_Rotation != _wantedRotation:
            crt_Rotation = (crt_Rotation + rotation_Direction) % 4
            moves += 1
        return moves

    def compute_best (self, gamestate, crt_Recursion):
        right_Score = left_Score = 0
        (left_Score, left_Moves, left_Rotates) = self.move_when_possible (-1, gamestate, crt_Recursion)
        (right_Score, right_Moves, right_Rotates) = self.move_when_possible (1, gamestate, crt_Recursion)
       
        if right_Score > left_Score:
            return (right_Score, right_Moves, right_Rotates)
        else:
            return (left_Score, left_Moves, left_Rotates)
     
    def compute_score (self, crt_state, lines_Cleared):
        heights_sum  = 0
        row_Height = 0
        bump = 0
        columns_height = []
        total_holes = 0
        tiles = crt_state.get_tiles()

        for _col in range (0, 10):
            search = True
            for _row in range (0, 20):
                if tiles[_row][_col] != 0 and search is True:
                    row_Height = 20 - _row
                    search = False
                    heights_sum += row_Height     
                    columns_height.append (row_Height)
            for _row in range (0, 20):
                if tiles[_row][_col] != 0 and (20 - _row) < row_Height:
                    total_holes += 1

        for _ix in range (0, columns_height.__len__() - 1):
            bump += abs(columns_height[_ix] - columns_height[_ix+1])

        score = -1.46*heights_sum + 2.18*lines_Cleared + -1*total_holes + -0.51*bump
    
        return score
                    
    def do_next_move (self, _ix, moves_to_do, rotations_to_do, gamestate):
        moves_number = moves_to_do.__len__ ()
        rotations_number = rotations_to_do.__len__ ()

        if _ix < moves_number and _ix < rotations_number:
            gamestate.move (moves_to_do[_ix])
            gamestate.rotate (rotations_to_do[_ix])
        elif _ix < moves_number and _ix >= rotations_number:  
            gamestate.move (moves_to_do[_ix])
        elif _ix >= moves_number and _ix < rotations_number:
            gamestate.rotate (rotations_to_do[_ix])         

    def Equal (self, tiles, extiles):
        for _y in range (0, 20):
            for _x in range (0,10):
                if extiles[_y][_x] != tiles[_y][_x]:
                    return False
        return True
