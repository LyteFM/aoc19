# -*- coding: utf-8 -*-
import numpy as np
import unittest


class Test(unittest.TestCase):
    
    def test_1(self):
        s = list('123456789012')
        self.assertEqual(compute_best_layer(s, 6), 1)
        
    def test_2(self):
        s = list('0222112222120000')
        img = read_img(s, 4)
        r = render_img(img, 2)
        self.assertEqual(r[0,0], 0)
        self.assertEqual(r[0,1], 1)
        self.assertEqual(r[1,0], 1)
        self.assertEqual(r[1,1], 0)
        
        
def render_img(img, px):
    # no masks needed... simply use advanced indexing...
    row_indices = np.argmax(img!=2, axis=0)
    r = img[row_indices, np.arange(img.shape[1])]
    return r.reshape(-1, px)
       
        
def render_img_1(img, px): # first approach
    # 0 is black, 1 is white, and 2 is transparent (i.e. next one is seen)
    # rendered: first layer in front, last in back
    row_indices = np.argmax(img!=2, axis=0) # list of indices, argmax stops at first True
    r =  np.fromiter((img[row_indices[i], i] for i in range(len(row_indices))), dtype=np.int32)
    return r.reshape(-1, px)


def render_img_2(img, px):
    row_indices = np.argmax(img!=2, axis=0)
    mask = np.arange(img.shape[0])[:,None] == row_indices
     # weird.. this is different than with the other approach...
    # r = img[mask]
    # img[mask][6] is 0 when it should be 1...
    # img[row_indices[6], 6] is 1 (and same as img[56, 6] and img[:, 6][56])
    # img[:,6][mask[:,6]] -> 1
    # BUT: img[6][mask[6]] -> 0 that's what happens...
    # I had 100 rows, 150 columns in img and mask, respectively. Calling img[mask] caused r to be populated BY THE ROWS 
    # of mask, i.e. np.where(mask[0]) would select thnp.arange(img.shape[1])e respective elements from img[0] and so on.
    # Since the mask was meant to be applied BY COLUMN, transposing both img and mask gives the desired result
    # remember: an index mask is always applied by row!
    r = img.T[mask.T]
    return r.reshape(-1, px)

   
def read_img(s, pxrow):
    d = np.array(s, dtype=np.int8)
    return d.reshape(-1, pxrow) # one flattened image per row


def compute_best_layer(s: list, pxrow: int):
    d = read_img(s, pxrow)
    idx = np.argmin(np.sum(d==0, axis=1)) # axis=1 -> sum column wise, i.e. sum of each row
    return np.sum(d[idx]==1)*np.sum(d[idx]==2)


def minimal():
    f = list(open('day_8_input.csv').read())[:-1] # newline at end
    img = np.array(f, dtype=np.int8).reshape(-1, 25*6)
    best_idx = np.argmin(np.sum(img==0, axis=1))
    print(np.sum(img[best_idx]==1)*np.sum(img[best_idx]==2))
    r = img[np.argmax(img!=2, axis=0), np.arange(img.shape[1])].reshape(-1,25)
    print(str(r).replace('0', ' '))


if __name__ == '__main__':
    unittest.main()
    f = list(open('day_8_input.csv').read())[:-1]
    print('1)', compute_best_layer(f, 25*6))
    img = read_img(f, 25*6)
    r = render_img(img, 25)
    print(str(r).replace('0', ' '))