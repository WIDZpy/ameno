import numpy as np
from mandragore import readRLE, lumos
import json
from matplotlib.pyplot import imshow, show

'''les calcule'''


class Life:

    def __init__(self, shape=(1, 1), max_x_y=(400, 400), max_historic: int = 100):
        """
        param shape: size of the required array (if the pattern is larger than the output, the output takes it's size)
        :param max_x_y:
        :param max_historic:
        """
        self.count = 0
        self.restricted_shape = shape
        self.global_shape = shape
        self.global_current_life = np.zeros(shape)
        self.restricted_current_life = np.zeros(shape)
        self.bordure = [[0, 0], [0, 0]]  # ligne du haut, ligne du bas, colonne de gauche, colonne de droite
        self.max_x_y = max_x_y
        self.max_historic = max_historic
        self.run = False

        self.historic = [(self.global_current_life, self.bordure, self.global_shape, self.count)]

        self.dictionaire = {
            'start_shape': shape,
            'max': self.max_x_y,
            'iport_patern': {
                'patern_1': {
                
                }
            }
        }
    
#   ################################################## getter ##########################################################
    
    def get_life(self, evolve=False):

        if self.run and evolve:
            self.evolve()

        return self.global_current_life

    def get_coordinates(self):
        print(np.array(np.where(self.restricted_current_life == 1)), type(self.restricted_current_life))
        return np.array(np.where(self.restricted_current_life == 1)).tolist()
        
#   ################################################## edit ###########################################################
    
    def point_and_clic(self, cord):
        cord = cord[1], cord[0]
        v = self.restricted_current_life[cord]
        self.restricted_current_life[cord] = self.global_current_life[self.bordure[0][0]+cord[0],
                                                                      self.bordure[1][0]+cord[1]] = 0 if v else 1
        self.update_start_historic()

    def load(self, dictionary):
        pass
        # self.restricted_shape = self.global_shape = dictionary['start_shape']
        # self.global_current_life = self.restricted_current_life = np.zeros(self.restricted_shape)
        #
        # self.max_x_y = dictionary['max']
        #
        # for loop in dictionary['import_adapt']:
        #     for bloop in loop:
        #         self.draw_adapt(bloop['fill'], bloop['coordinate x y'], bloop['mirror x'], bloop['mirror Y'],
        #                         bloop['rotation'], bloop['padding'])
        self.update_start_historic()

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
        # t_x = 1
        # t_y = 1

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

        self.global_current_life = np.zeros(self.restricted_shape)
        self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                 self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]] =\
            self.restricted_current_life

        self.global_shape = self.global_current_life.shape
        self.update_start_historic()

    def draw_random(self):
        self.global_current_life = lumos(self.global_shape[0], self.global_shape[1])
        self.restricted_current_life =\
            self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                     self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]]
        self.update_start_historic()

    def update_start_historic(self):
        self.historic[0] = (self.global_current_life, self.bordure, self.global_shape, self.count)

    def load_historic(self, index: int):
        self.global_current_life, self.bordure, self.global_shape, self.count = self.historic[index]

# ################################################# running #########################################################

    def evolve(self):
        if self.global_current_life.sum():

            self.count += 1

            sets = np.pad(self.global_current_life, np.ones((2, 2)).astype(int)*2)
            # sets = self.global_current_life
            evolve = np.pad(np.zeros(self.global_shape).astype(int), np.ones((2, 2)).astype(int))
            evolve[:, :] = (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
                            sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])
            evolve = np.logical_or(evolve == 3, np.logical_and(sets[1:-1, 1:-1] == 1, evolve == 2)).astype(int)

            self.bordure = (np.array(self.bordure)+1).tolist()  # rajoute 1 a toute la valeur de self.bordure

            for to in 'ab':
                if evolve[0].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.bordure[0][0] >= self.bordure[0][1]):      # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[1:]       # retourne l'array substituer de la première lig1ne
                    self.bordure[0][0] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[-1].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.bordure[0][1] >= self.bordure[0][0]):     # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[:-1]      # retourne l'array substituer de la première ligne
                    self.bordure[0][1] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[:, 0].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.bordure[1][0] >= self.bordure[1][1]):   # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[:, 1:]    # retourne l'array substituer de la première ligne
                    self.bordure[1][0] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[:, -1].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.bordure[1][1] >= self.bordure[1][0]):  # test s'il y a une ou plusieurs cellules en vie sur dernière colonne
                    evolve = evolve[:, :-1]   # retourne l'array substituer de derni ère colonne
                    self.bordure[1][1] -= 1   # soustrait 1 a la valeur de la dernière colonne


            self.global_current_life = evolve.astype(int)
            # print(evolve, "\n", self.bordure, "\n", self.restricted_shape)
            self.global_shape = self.global_current_life.shape

            if len(self.historic) >= self.max_historic:
                del self.historic[1]
            self.historic.append((self.global_current_life, self.bordure, self.global_shape, self.count))

    def evolve_V1(self):
        
        self.count += 1
        
        sets = np.pad(self.global_current_life, np.ones((2, 2)).astype(int)*2)
        # sets = self.global_current_life
        evolve = np.pad(np.zeros(self.global_shape).astype(int), np.ones((2, 2)).astype(int))
        evolve[:, :] = (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
                        sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])
        evolve = np.logical_or(evolve == 3, np.logical_and(sets[1:-1, 1:-1] == 1, evolve == 2)).astype(int)

        self.bordure = (np.array(self.bordure)+1).tolist()  # rajoute 1 a toute la valeur de self.bordure
        
        if evolve[0].sum() == 0 or self.max_x_y[0] <= self.global_shape[0]:      # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[1:]       # retourne l'array substituer de la première ligne
            self.bordure[0][0] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[-1].sum() == 0 or self.max_x_y[0] <= self.global_shape[0]:     # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[:-1]      # retourne l'array substituer de la première ligne
            self.bordure[0][1] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[:, 0].sum() == 0 or self.max_x_y[1] <= self.global_shape[1]:   # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[:, 1:]    # retourne l'array substituer de la première ligne
            self.bordure[1][0] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[:, -1].sum() == 0 or self.max_x_y[1] <= self.global_shape[1]:  # test s'il y a une ou plusieurs cellules en vie sur dernière colonne
            evolve = evolve[:, :-1]   # retourne l'array substituer de derni ère colonne
            self.bordure[1][1] -= 1   # soustrait 1 a la valeur de la dernière colonne
            
        self.global_current_life = evolve.astype(int)
        # print(evolve, "\n", self.bordure, "\n", self.restricted_shape)
        self.global_shape = self.global_current_life.shape
        self.restricted_current_life\
            = self.global_current_life[self.bordure[0][0]:self.bordure[0][0]+self.restricted_shape[0],
                                       self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]]

    def play(self):
        self.run = True

    def pause(self):
        self.run = False

    def back(self):
        if len(self.historic) > 1:
            del self.historic[-1]
        self.load_historic(-1)



if __name__ == '__main__':
    life = Life()
    # life.starte_adapt('canadagoose', (20, 0))
    life.draw_adapt('canadagoose', (0, 0))
    print(life.restricted_current_life)
    
    for loop in range(0):
        life.evolve()
    imshow(life.restricted_current_life)
    show()
