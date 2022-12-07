import numpy as np
from cellular_automaton.mandragore import readRLE, lumos
from matplotlib.pyplot import imshow, show

'''les calcule'''



class Life:

    def __init__(self, max_x_y=(400, 400), max_historic: int = 100):
        """
        :param max_x_y:
        :param max_historic:
        """
        self.count = 0
        self.shape = [0, 0]
        self.current_gen = np.zeros(self.shape)
        self.array_pos = [0, 0]  # ligne du haut, colonne de gauche
        self.max_x_y = max_x_y
        self.max_historic = max_historic
        self.run = False

        self.historic = [(self.current_gen, self.array_pos, self.shape, self.count)]

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
        cord = self.array_pos[0] + cord[1], self.array_pos[1] + cord[0]
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

    def nomalize_slices(self, rect):
        result = ()
        pading = [[0, 0], [0, 0]]
        for _ in range(2):
            if rect[_].start < self.array_pos[_]:
                pading[_][0] = self.array_pos[_] - rect[_].start
                self.shape[_] += self.array_pos[_] - rect[_].start
                self.array_pos[_] = rect[_].start

            if rect[_].stop > self.shape[_] - self.array_pos[_]:
                pading[_][1] = rect[_].stop - self.shape[_] - self.array_pos[_]
                self.shape[_] += rect[_].stop - self.shape[_]


            result += (slice(rect[_].start - self.array_pos[_], rect[_].stop - self.array_pos[_]),)
        print(pading)
        self.current_gen = np.pad(self.current_gen, pading)

        return result

    def draw_array(self, array, xy=(0, 0), mirror_x=1, mirror_y=1, rotation=0):
        array = np.rot90(array, 0 - rotation)

        bidul = (slice(xy[1], xy[1] + array.shape[0]),
                 slice(xy[0], xy[0] + array.shape[1]))

        self.nomalize_slices(bidul)

        self.current_gen[bidul] = array[::mirror_y, ::mirror_x]

        self.update_start_historic()

    def draw_adapt(self, file, pattern_xy=(0, 0), mirror_x=1, mirror_y=1, rotation=0):
        """
        :param file: Read the RLE file on the website 'https://conwaylife.com/wiki/Category:Patterns'
        :param pattern_xy: coordinates of the point (0;0) on the main array (default is (0,0))
        :param mirror_x: assign -1 if you want the pattern to be inverted horizontally (default is 1)
        :param mirror_y: assign -1 if you want the pattern to be inverted vertically (default is 1)
        :param rotation: nuber of time to  aray is 90° rotate
        :return:
        """
        # definition des varibles :
        
        rle = np.rot90(readRLE(file), 0-rotation)

        bidul = (slice(pattern_xy[1], pattern_xy[1] + rle.shape[0]),
                 slice(pattern_xy[0], pattern_xy[0] + rle.shape[1]))

        self.nomalize_slices(bidul)

        self.current_gen[bidul] = rle[::mirror_y, ::mirror_x]

        self.shape = self.current_gen.shape
        self.update_start_historic()

    def draw_random(self):
        self.current_gen = lumos(self.shape[0], self.shape[1])
        self.restricted_current_life = \
            self.current_gen[self.array_pos[0][0]:self.array_pos[0][0] + self.restricted_shape[0],
            self.array_pos[1][0]:self.array_pos[1][0] + self.restricted_shape[1]]
        self.update_start_historic()

    def update_start_historic(self):
        self.historic[0] = (self.current_gen, self.array_pos, self.shape, self.count)

    def load_historic(self, index: int):
        self.current_gen, self.array_pos, self.shape, self.count = self.historic[index]

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

            self.array_pos = (np.array(self.array_pos) + 1).tolist()  # rajoute 1 a toute la valeur de self.array_pos

            for to in 'ab':
                if evolve[0].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.array_pos[0][0] >= self.array_pos[0][1]):      # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[1:]       # retourne l'array substituer de la première lig1ne
                    self.array_pos[0][0] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[-1].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.array_pos[0][1] >= self.array_pos[0][0]):     # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[:-1]      # retourne l'array substituer de la première ligne
                    self.array_pos[0][1] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[:, 0].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.array_pos[1][0] >= self.array_pos[1][1]):   # test s'il y a une ou plusieurs cellules en vie sur la première ligne
                    evolve = evolve[:, 1:]    # retourne l'array substituer de la première ligne
                    self.array_pos[1][0] -= 1   # soustrait 1 a la valeur de la première ligne
                if evolve[:, -1].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.array_pos[1][1] >= self.array_pos[1][0]):  # test s'il y a une ou plusieurs cellules en vie sur dernière colonne
                    evolve = evolve[:, :-1]   # retourne l'array substituer de derni ère colonne
                    self.array_pos[1][1] -= 1   # soustrait 1 a la valeur de la dernière colonne


            self.current_gen = evolve.astype(int)
            # print(evolve, "\n", self.array_pos, "\n", self.restricted_shape)
            self.shape = self.current_gen.shape

            if len(self.historic) >= self.max_historic:
                del self.historic[1]
            self.historic.append((self.current_gen, self.array_pos, self.shape, self.count))

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
    life.draw_array(np.array([[1,1],[0,1]]))
    print(life.current_gen)
    
    for loop in range(0):
        life.evolve()
    imshow(life.current_gen)
    show()
