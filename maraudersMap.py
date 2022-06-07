import numpy as np
from mandragore import readRLE
from matplotlib.pyplot import imshow, show
from lumos import lumos

# CECI EST UN COMENTAIRE


class Life:

    def __init__(self, shape=(1, 1), max_x_y=(-1, -1)):
        """
        :param shape: size of the required array (if the pattern is larger than the output, the output takes it's size)
        """
        self.count = 0
        self.restricted_shape = shape
        self.global_shape = shape
        self.global_current_life = np.zeros(shape)
        self.restricted_current_life = np.zeros(shape)
        self.bordure = [[0, 0], [0, 0]]
        self.max_x_y = max_x_y
        
        self.dictionaire = {
            'start_shape': shape,
            'max': self.max_x_y,
            'iport_patern': {
                'patern_1': {
                
                }
            }
        }
    
#   ################################################## getter ##########################################################
    
    def getlife(self):
        return self.restricted_current_life
    
    def getdepar(self):
        return
    
    def getcordonat(self):
        print(np.array(np.where(self.restricted_current_life == 1)), type(self.restricted_current_life))
        return np.array(np.where(self.restricted_current_life == 1)).tolist()
        
#   ################################################## edit ###########################################################
    def point_and_clic(self, cord):
        v = self.restricted_current_life[cord]
        self.restricted_current_life[cord] = self.global_current_life[self.bordure[0][0]+cord[0],
                                                                      self.bordure[1][0]+cord[1]] = 0 if v else 1

    def load(self, dictionaire):
        self.restricted_shape = self.global_shape = dictionaire['start_shape']
        self.global_current_life = self.restricted_current_life = np.zeros(self.restricted_shape)
        
        self.max_x_y = dictionaire['max']
        
        for looop in dictionaire['import_adapt']:
            for bloop in looop:
                self.draw_adapt(bloop['fill'], bloop[''], bloop[''])
                
    def draw_not_adapt(self, looper=True):
        return

    def draw_adapt(self, file, pattern_xy=(0, 0), mirror_x=1, mirror_y=1, rotation=0, padding=None):
        """
        :param file: Read the RLE file on the website 'https://conwaylife.com/wiki/Category:Patterns'
        :param pattern_xy: coordinates of the point (0;0) on the main array (default is (0,0))
        :param mirror_x: assign -1 if you want the pattern to be inverted horizontally (default is 1)
        :param mirror_y: assign -1 if you want the pattern to be inverted vertically (default is 1)
        :param rotation: nuber of time to  aray is 90° rotate
        :param padding: added pixels at the edge of the array ([[left,right],[up,down]])
        :return:
        """
        # definition des varibles :
        if padding is None:
            padding = [[0, 0], [0, 0]]
        padding = np.flip(padding, 0)
        rle = np.rot90(readRLE(file), 0-rotation)
        rlesize = rle.shape
        t_x = 1
        t_y = 1

        self.restricted_shape = (self.restricted_shape[0] if
                                 self.restricted_shape[0] >= rlesize[0] + pattern_xy[1] else rlesize[0] + pattern_xy[1],
                                 self.restricted_shape[1] if
                                 self.restricted_shape[1] >= rlesize[1] + pattern_xy[0] else rlesize[1] + pattern_xy[0])
        
        self.restricted_current_life = np.pad(self.restricted_current_life,
                                              [[0, self.restricted_shape[0] - self.restricted_current_life.shape[0]],
                                               [0, self.restricted_shape[1] - self.restricted_current_life.shape[1]]])

        bidul = (pattern_xy[1], pattern_xy[1] + rlesize[0],
                 pattern_xy[0], pattern_xy[0] + rlesize[1])

        self.restricted_current_life[bidul[0]:bidul[1], bidul[2]:bidul[3]] = rle[::mirror_y, ::mirror_x]
        self.restricted_current_life = np.pad(self.restricted_current_life, padding)
        
        self.restricted_shape = self.restricted_current_life.shape
        print(self.restricted_shape)
        self.global_current_life = np.zeros(self.restricted_shape)
        self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                 self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]] =\
            self.restricted_current_life
        
        self.global_shape = self.global_current_life.shape
        
    def draw_random(self):
        self.global_current_life = lumos(self.global_shape[0], self.global_shape[1])
        self.restricted_current_life =\
            self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                     self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]]

# ################################################# runing #########################################################
    
    def evolve(self, repet=1):
        
        self.count += 1
        
        sets = np.pad(self.global_current_life, np.ones((2, 2)).astype(int)*2)
        # sets = self.global_current_life
        evolve = np.pad(np.zeros(self.global_shape).astype(int), np.ones((2, 2)).astype(int))
        evolve[:, :] = (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
                        sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])
        evolve = np.logical_or(evolve == 3, np.logical_and(sets[1:-1, 1:-1] == 1, evolve == 2)).astype(int)

        self.bordure = (np.array(self.bordure)+1).tolist()
        
        if evolve[0].sum() == 0:
            evolve = evolve[1:]
            self.bordure[0][0] -= 1
        if evolve[-1].sum() == 0:
            evolve = evolve[:-1]
            self.bordure[0][1] -= 1
        if evolve[:, 0].sum() == 0:
            evolve = evolve[:, 1:]
            self.bordure[1][0] -= 1
        if evolve[:, -1].sum() == 0:
            evolve = evolve[:, :-1]
            self.bordure[1][1] -= 1
            
        self.global_current_life = evolve.astype(int)
        # print(evolve, "\n", self.bordure, "\n", self.restricted_shape)
        self.global_shape = self.global_current_life.shape
        self.restricted_current_life = self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                                                self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]]
    
    
if __name__ == '__main__':
    life = Life((0, 0))
    # life.starte_adapt('canadagoose', (20, 0))
    life.draw_adapt('canadagoose', (0, 0))
    print(life.restricted_current_life)
    
    for loop in range(0):
        life.evolve()
    imshow(life.restricted_current_life)
    show()
