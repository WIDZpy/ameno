import numpy as np
from cellular_automaton.mandragore import readRLE, lumos
from matplotlib.pyplot import imshow, show

'''les calcule'''


class Life:

    def __init__(self, max_x_y=(400, 400), max_historic: int = 100):
        """
        param shape: size of the required array (if the pattern is larger than the output, the output takes it's size)
        :param max_x_y:
        :param max_historic:
        """
        self.count = 0
        self.shape = 1, 1
        self.current_gen = np.zeros(self.shape)
        self.bordure = [[0, 0], [0, 0]]  # ligne du haut, ligne du bas, colonne de gauche, colonne de droite
        self.max_x_y = max_x_y
        self.max_historic = max_historic
        self.run = False

        self.historic = [(self.current_gen, self.bordure, self.shape, self.count)]

        self.dictionaire = {
            'start_shape': self.shape,
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

        return self.current_gen
        
#   ################################################## edit ###########################################################
    
    def point_and_clic(self, cord):
        cord = self.bordure[0][0] + cord[1], self.bordure[1][0] + cord[0]
        v = self.current_gen[cord]
        self.current_gen[cord] = v ^ 1
        self.update_start_historic()

    def load(self, dictionary):
        pass
        # self.restricted_shape = self.shape = dictionary['start_shape']
        # self.current_gen = self.restricted_current_life = np.zeros(self.restricted_shape)
        #
        # self.max_x_y = dictionary['max']
        #
        # for loop in dictionary['import_adapt']:
        #     for bloop in loop:
        #         self.draw_adapt(bloop['fill'], bloop['coordinate x y'], bloop['mirror x'], bloop['mirror Y'],
        #                         bloop['rotation'], bloop['padding'])
        self.update_start_historic()

    def draw_adapt(self, file, pattern_xy=(0, 0), mirror_x=1, mirror_y=1, rotation=0):
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
        
        rle = np.rot90(readRLE(file), 0-rotation)

        bidul = (slice(pattern_xy[1], pattern_xy[1] + rle.shape[0]),
                 slice(pattern_xy[0], pattern_xy[0] + rle.shape[1]))

        self.current_gen[bidul] = rle[::mirror_y, ::mirror_x]

        self.shape = self.current_gen.shape
        self.update_start_historic()

    def draw_random(self):
        self.current_gen = lumos(self.shape[0], self.shape[1])
        self.restricted_current_life = \
            self.current_gen[self.bordure[0][0]:self.bordure[0][0] + self.restricted_shape[0],
                                     self.bordure[1][0]:self.bordure[1][0]+self.restricted_shape[1]]
        self.update_start_historic()

    def update_start_historic(self):
        self.historic[0] = (self.current_gen, self.bordure, self.shape, self.count)

    def load_historic(self, index: int):
        self.current_gen, self.bordure, self.shape, self.count = self.historic[index]

# ################################################# running #########################################################

    def evolve(self):
        if self.current_gen.sum():

            self.count += 1

            sets = np.pad(self.current_gen, np.ones((2, 2)).astype(int) * 2)
            # sets = self.current_gen
            evolve = np.pad(np.zeros(self.shape).astype(int), np.ones((2, 2)).astype(int))
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


            self.current_gen = evolve.astype(int)
            # print(evolve, "\n", self.bordure, "\n", self.restricted_shape)
            self.shape = self.current_gen.shape

            if len(self.historic) >= self.max_historic:
                del self.historic[1]
            self.historic.append((self.current_gen, self.bordure, self.shape, self.count))

    def evolve_V1(self):
        
        self.count += 1
        
        sets = np.pad(self.current_gen, np.ones((2, 2)).astype(int) * 2)
        # sets = self.current_gen
        evolve = np.pad(np.zeros(self.shape).astype(int), np.ones((2, 2)).astype(int))
        evolve[:, :] = (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
                        sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])
        evolve = np.logical_or(evolve == 3, np.logical_and(sets[1:-1, 1:-1] == 1, evolve == 2)).astype(int)

        self.bordure = (np.array(self.bordure)+1).tolist()  # rajoute 1 a toute la valeur de self.bordure
        
        if evolve[0].sum() == 0 or self.max_x_y[0] <= self.shape[0]:      # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[1:]       # retourne l'array substituer de la première ligne
            self.bordure[0][0] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[-1].sum() == 0 or self.max_x_y[0] <= self.shape[0]:     # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[:-1]      # retourne l'array substituer de la première ligne
            self.bordure[0][1] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[:, 0].sum() == 0 or self.max_x_y[1] <= self.shape[1]:   # test s'il y a une ou plusieurs cellules en vie sur la première ligne
            evolve = evolve[:, 1:]    # retourne l'array substituer de la première ligne
            self.bordure[1][0] -= 1   # soustrait 1 a la valeur de la première ligne
        if evolve[:, -1].sum() == 0 or self.max_x_y[1] <= self.shape[1]:  # test s'il y a une ou plusieurs cellules en vie sur dernière colonne
            evolve = evolve[:, :-1]   # retourne l'array substituer de derni ère colonne
            self.bordure[1][1] -= 1   # soustrait 1 a la valeur de la dernière colonne
            
        self.current_gen = evolve.astype(int)
        # print(evolve, "\n", self.bordure, "\n", self.restricted_shape)
        self.shape = self.current_gen.shape
        self.restricted_current_life\
            = self.current_gen[self.bordure[0][0]:self.bordure[0][0] + self.restricted_shape[0],
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
