import numpy as np

class LineN:

    def __init__(self):
        self.bdsize = 3 # board size
        self.state = np.zeros((self.bdsize,self.bdsize,self.bdsize), dtype = int)
        self.turn = 1
        self.n_stone = 0
        self.disp()
        print("Player " + str(self.turn) + "'s turn.")

    def put_stone(self, put_place):
        '''
        Judge if the stone can be put at the "put_place",
        and replace "state" if it can be done.
        "success" which indicates the replacement was done
        is also returned
        [input]
        put_place (array 4x4, integer):
            the place (x, y) where the player is trying
            to put the stone
        [output]
        success (True or False):
            the stone was put (or not)
        put_z (integer):
            z element of the place where the stone was put
        '''

        put_place = np.array(put_place)
        tower = self.state[put_place[0], put_place[1], :]
        if ( np.prod(tower != 0) ):
            success = False
            iz = -100
        else:
            success = True
            for iz in range(self.bdsize):
                if tower[iz] == 0:
                    tower[iz] = self.turn
                    break
            self.state[put_place[0], put_place[1], :] = tower[:]
        return success, iz

    def lined(self,put_place3D):
        '''
        Judge if a line is formed
        [input]
        put_place3D (array NxNxN, integer):
            the place (x, y, z) where the stone was put
            in the previous step
        [output]
        formed (True or False):
            a line is formed or not
        '''
        put_place3D = np.array(put_place3D)
        # turn = self.state[put_place3D[0], put_place3D[1], put_place3D[2]]

        tower = self.state[put_place3D[0], put_place3D[1],:]
        formed = np.prod(tower == self.turn)

        if (not formed):
            tower = self.state[put_place3D[0], :, put_place3D[2]]
            formed = np.prod(tower == self.turn)

        if (not formed):
            tower = self.state[:, put_place3D[1], put_place3D[2]]
            formed = np.prod(tower == self.turn)

        edge = put_place3D % 3

        if (not formed):
            if (edge[0] != 0 and edge[1] != 0):
                if (put_place3D[0] == put_place3D[1]):
                    tower = np.array(
                        [self.state[i,i,put_place3D[2]] for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)
                else:
                    tower = np.array(
                        [self.state[i,self.bdsize-1-i,put_place3D[2]]
                         for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)

        if (not formed):
            if (edge[0] != 0 and edge[2] != 0):
                if (put_place3D[0] == put_place3D[2]):
                    tower = np.array(
                        [self.state[i,put_place3D[1],i] for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)
                else:
                    tower = np.array(
                        [self.state[i,put_place3D[1],self.bdsize-1-i]
                         for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)

        if (not formed):
            if (edge[1] != 0 and edge[2] != 0):
                if (put_place3D[1] == put_place3D[2]):
                    tower = np.array(
                        [self.state[put_place3D[0],i,i] for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)
                else:
                    tower = np.array(
                        [self.state[put_place3D[0],i,self.bdsize-1-i]
                         for i in range(self.bdsize)] )
                    formed = np.prod(tower == self.turn)

        if (not formed):
            if str(put_place3D) in {'[1 1 1]', '[2 2 2]'}:
                tower = np.array([self.state[i,i,i] for i in range(self.bdsize)])
                formed = np.prod(tower == self.turn)
            elif str(put_place3D) in {'[2 1 1]', '[1 2 2]'}:
                tower = np.array([self.state[self.bdsize-1-i,i,i] for i in range(self.bdsize)])
                formed = np.prod(tower == self.turn)
            elif str(put_place3D) in {'[1 2 1]', '[2 1 2]'}:
                tower = np.array([self.state[i,self.bdsize-1-i,i] for i in range(self.bdsize)])
                formed = np.prod(tower == self.turn)
            elif str(put_place3D) in {'[1 1 2]', '[2 2 1]'}:
                tower = np.array([self.state[i,i,self.bdsize-1-i] for i in range(self.bdsize)])
                formed = np.prod(tower == self.turn)

        return formed != 0

    def disp(self):
        for i in range(self.bdsize):
            print(self.state[:,:,i])
            print()

    def step(self,put_place):
        if (self.n_stone == self.bdsize**3):
            self.disp()
            print("Draw.")

        success, iz = self.put_stone(put_place)
        if (not success):
            print("Put the stone elsewhere.")
        else:
            self.n_stone += 1
            self.disp()
            formed = self.lined([put_place[0], put_place[1], iz])
            if (formed):
                print("Player " + str(self.turn) + " won!")
            else:
                if (self.n_stone == self.bdsize**3):
                    print("Draw.")
                else:
                    self.turn *= -1
                    print("Player " + str(self.turn) + "'s turn.")

if __name__ == '__main__':
    a = LineN()
