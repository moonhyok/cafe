from opinion.settings import *

# Store landmarks as an array of arrays, each containing
# a name, description, photo_url, and an array of their ratings. 
# Index landmarks in the dictionary under opinion_space_id.

LANDMARKS = {}

# Sarah Palin
# Gas: 10
# Truth: 0
# Obama: 2
# Health: 0
# Torture: 10
# => (10, 0, 2, 0, 10)
# => (1.0, 0.0, 0.2, 0.0, 1.0)
# Woman: 9

# Ralph Nader
# Gas: 0
# Truth: 10
# Obama: 9
# Health: 10
# Torture: 0
# => (0, 10, 9, 10, 0)
# => (0.0, 1.0, 0.9, 1.0, 0.0)
# Woman: 8

# Rush Limbaugh
# Gas: 10
# Truth: 0
# Obama: 0
# Health: 0
# Torture: 10
# => (10, 0, 0, 0, 10)
# => (1.0, 0.0, 0.0, 0.0, 1.0)
# Woman: 2

# Arnold Schwarzenegger
# Gas: 4
# Truth: 3
# Obama: 5
# Health: 9
# Torture: 2
# => (4, 3, 5, 9, 2)
# => (0.4, 0.3, 0.5, 0.9, 0.2)
# Woman: 5

# Nancy Pelosi
# Gas: 4
# Truth: 10
# Obama: 9
# Health: 9
# Torture: 0
# => (4, 10, 9, 9, 0)
# => (0.4, 1.0, 0.9, 0.9, 0.0)
# Woman: 3

IMG_URL_PREFIX = 'images/'
           
__nader = ('Ralph Nader',
           'Ralph Nader was an independent candidate for President of the United States in 2004 and 2008, and a Green Party candidate in 1996 and 2000.',
           IMG_URL_PREFIX + 'nader.jpg',
           (0.0, 1.0, 0.9, 1.0, 0.0))
          
__limbaugh = ('Rush Limbaugh',
              'Rush Limbaugh is an American radio host and conservative political commentator.',
              IMG_URL_PREFIX + 'limbaugh.jpg',
              (1.0, 0.0, 0.0, 0.0, 1.0))

__schwarzenegger = ('Arnold Schwarzenegger',
                    'Arnold Schwarzenegger is the current Governor of the U.S. state of California. He is a Republican.',
                    IMG_URL_PREFIX + 'schwarzenegger.jpg',
                    (0.4, 0.3, 0.5, 0.9, 0.2))

__pelosi = ('Nancy Pelosi',
            'Nancy Pelosi is the current Speaker of the United States House of Representatives. She is a Democrat.',
            IMG_URL_PREFIX + 'pelosi.jpg',
            (0.4, 1.0, 0.9, 0.9, 0.0))

LANDMARKS[1] = (__nader, __limbaugh, __schwarzenegger, __pelosi)