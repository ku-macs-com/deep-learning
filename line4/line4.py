import numpy as np

def put_stone(state, put_place, turn):
    '''
    Judge if the stone can be put at the "put_place",
    and replace "state" if it can be done.
    "success" which indicates the replacement was done
    is also returned
    [input]
    state (array 4x4x4, integer):
        state of the board
        values are 0 (vacant) or 1 (black) or -1 (white)
        at each place (x, y, z)
    put_place (array 4x4, integer):
        the place (x, y) where the player is trying 
        to put the stone
    turn (integer):
        color of the stone put(1 (black) or -1 (white))
    [output]
    success (True or False):
        the stone was put (or not)
    put_z (integer):
        z element of the place where the stone was put
    
    '''
    put_place = np.array(put_place)
    tower = state[put_place[0], put_place[1], :]
    if ( np.prod(tower != 0) ):
        success = False
        iz = -100
    else:
        success = True
        for iz in range(4):
            if tower[iz] == 0:
                tower[iz] = turn
                break
    state[put_place[0], put_place[1], :] = tower[:]
    return success, iz
    
def lined(state, put_place3D):
    '''
    Judge if a line is formed
    [input]
    state (array 4x4x4, integer):
        state of the board
        values are 0 (vacant) or 1 (black) or -1 (white)
        at each place (x, y, z)
    put_place3D (array 4x4x4, integer):
        the place (x, y, z) where the stone was put
        in the previous step
    [output]
    formed (True or False):
        a line is formed or not
    '''
    put_place3D = np.array(put_place3D)
    turn = state[put_place3D[0], put_place3D[1], put_place3D[2]]
    
    tower = state[put_place3D[0], put_place3D[1],:]
    formed = np.prod(tower == turn)

    if (not formed):
        tower = state[put_place3D[0], :, put_place3D[2]]
        formed = np.prod(tower == turn)

    if (not formed):
        tower = state[:, put_place3D[1], put_place3D[2]]
        formed = np.prod(tower == turn)

    edge = put_place3D % 3
    
    if (not formed):
        if (edge[0] != 0 and edge[1] != 0):
            if (put_place3D[0] == put_place3D[1]):
                tower = np.array(
                    [state[i,i,put_place3D[2]] for i in range(4)] )
                formed = np.prod(tower == turn)
            else:
                tower = np.array(
                    [state[i,3-i,put_place3D[2]] for i in range(4)] )
                formed = np.prod(tower == turn)
        
    if (not formed):
        if (edge[0] != 0 and edge[2] != 0):
            if (put_place3D[0] == put_place3D[2]):
                tower = np.array(
                    [state[i,put_place3D[1],i] for i in range(4)] )
                formed = np.prod(tower == turn)
            else:
                tower = np.array(
                    [state[i,put_place3D[1],3-i] for i in range(4)] )
                formed = np.prod(tower == turn)

    if (not formed):
        if (edge[1] != 0 and edge[2] != 0):
            if (put_place3D[1] == put_place3D[2]):
                tower = np.array(
                    [state[put_place3D[0],i,i] for i in range(4)] )
                formed = np.prod(tower == turn)
            else:
                tower = np.array(
                    [state[put_place3D[0],i,3-i] for i in range(4)] )
                formed = np.prod(tower == turn)

    if (not formed):
        if str(put_place3D) in {'[1 1 1]', '[2 2 2]'}:
            tower = np.array([state[i,i,i] for i in range(4)])
            formed = np.prod(tower == turn)
        elif str(put_place3D) in {'[2 1 1]', '[1 2 2]'}:
            tower = np.array([state[3-i,i,i] for i in range(4)])
            formed = np.prod(tower == turn)
        elif str(put_place3D) in {'[1 2 1]', '[2 1 2]'}:
            tower = np.array([state[i,3-i,i] for i in range(4)])
            formed = np.prod(tower == turn)
        elif str(put_place3D) in {'[1 1 2]', '[2 2 1]'}:
            tower = np.array([state[i,i,3-i] for i in range(4)])
            formed = np.prod(tower == turn)

    return formed != 0

def disp(state):
    for i in range(4):
        print(state[:,:,i])
        print()

def step(state, put_place, turn, N_stone):
    if (N_stone == 64):
        disp(state)
        print("Draw.")
    
    success, iz = put_stone(state, put_place, turn)
    if (not success):
        print("Put the stone elsewhere.")
    else:
        N_stone += 1
        disp(state)
        formed = lined(state, [put_place[0], put_place[1], iz])
        if (formed):
            print("Player " + str(turn) + " won!")
        else:
            if (N_stone == 64):
                print("Draw.")
            else:
                turn *= -1
                print("Player " + str(turn) + "'s turn.")
    return turn, N_stone
        
state = np.zeros((4,4,4), dtype = int)
turn = 1
print("Player 1's turn")
N_stone = 0
