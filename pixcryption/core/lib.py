from uuid import uuid4
from math import sqrt
from PIL import Image
import numpy as np
import itertools
import random
# import time --> There is not use of time module :/

def create_user_key(uuid):

  #  Creating random varibles:
  print('Preparing To Generate User Key (This may take a while but will only run once!)')
  allc = [i for i in itertools.product(range(256), repeat=3)]  # WORK here it take tooooooo long!
  # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
  print('Complete...')
  print('Randomizing Base Key...')
  random.seed(uuid)  # seed here is a kind of remember random with value uuid
  random.shuffle(allc)  # randomised the allc value
  print('Randomized...')

  #  Creating pixel positions: <-- WORK HERE
  max_it = 1114112
  w = int( 1114112 / sqrt(1114112)) + 1
  pixels = []
  key_list = [None] * 1114112
  fresh = [None] * w
  count = 0
  total = 0
  print('Generating User Key...')
  for i in allc:
    if total == max_it:
      break
    if count == w:
      pixels.append(fresh)  # <-- Appends 'fresh'
      fresh = [None] * w  # <-- Rests
      count = 0  # <-- Rests
    fresh[count] = i # <-- appends 'i'
    key_list[total] = i
    count += 1
    total += 1

  #  Creating Image:
  array = np.array(pixels, dtype=np.uint8)
  new_image = Image.fromarray(array)
  new_image.save('user_key.png')
  print('Finished....')
  return pixels, key_list

def get_list_from_key(imdata):
  im = Image.open(imdata)
  pixels = list(im.getdata())
  return pixels

def encrypt_w_user_key(key_list, string):  # <-- WORK HERE
  try:
    w = int(len(string) / sqrt(len(string))) + 1
    pixels = []
    fresh = []
    for i in string:
        if len(fresh) == w:
            pixels.append(fresh)
            fresh = []
        fresh.append(key_list[ord(i)])
    pixels.append(fresh)

    if len(pixels[-1]) != w:
        num_left = int(w - len(pixels[-1]))
        count = 0
        while count < num_left:
            pixels[-1].append((0, 0, 0))
            count += 1

    array = np.array(pixels, dtype=np.uint8)
    uid = str(uuid4()).split('-')[0]
    new_image = Image.fromarray(array)
    new_image.save('enc_msg_{}.png'.format(uid))
    return True, 'enc_msg_{}.png'.format(uid)
  except Exception as e:
    return False, e
  
def decrypt_with_user_key(user_key, image_path): # <-- WORK HERE
  try:
    # get image pixels
    str_image = Image.open(image_path)
    str_pixels = list(str_image.getdata())
    # get user pixels
    user_key_im = Image.open(user_key)
    user_key_pixels = list(user_key_im.getdata())
    count = 0
    user_map = [None] * len(user_key_pixels)
    for i in user_key_pixels:
      user_map[count] = i
      count += 1
    string = ""
    for i in str_pixels:
      if i == (0,0,0):
        string += ""
      else:
        string += chr(user_map.index(i))
    print(string)
    
  except Exception as e:
    print(e)