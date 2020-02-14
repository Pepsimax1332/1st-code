# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 18:38:02 2020

@author: Max
"""

import Digit_Recogniser, Grid_Reader, LightningSudoku, cv2, easygui, time, sys
import numpy as np


if __name__ == '__main__':

    # loads neaural network
    mlp = Digit_Recogniser.mlp
    # loads dataset
    digits = Digit_Recogniser.digits
    
    # opens image file
    img = easygui.fileopenbox()

    start = time.time()
    # loads image into grid  
    grid = Grid_Reader.Grid(img)
    
    # predicts cells in grid
    input_string = ''
    for square in grid.digits:
        
        v = mlp.predict(square.reshape(1, -1))
        input_string += str(v[0]) if v[0] != 0 else '.'
        
    # loads image to be displayed in -s show flag
    image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    
    if len(sys.argv) > 1 and sys.argv[1] == '-s':
    
        cv2.imshow('image', image)  # Display the image
        cv2.waitKey(0)    # Wait for any key to be pressed (with the image window active)
        cv2.destroyAllWindows()
        
        cv2.imshow('image', grid.cropped2)  # Display the image
        cv2.waitKey(0)    # Wait for any key to be pressed (with the image window active)
        cv2.destroyAllWindows()
    
    # solves sudoku using lighnting sudoku algorithm
    print(input_string)
    sudoku = LightningSudoku.Sudoku(input_string)
    print()
    
    # assemples a new grid based on the input and output. All chars in input that where .
    # are assigned a corresponding value from the solution
    solved_grid = []
    blank_grid = []
    c = 0
    for i in sudoku.solution:
        if input_string[c] == '.':
            solved_grid.append(digits['target_imgs'][int(i)])
        else:
            solved_grid.append(digits['target_imgs'][0])
            
        blank_grid.append(digits['target_imgs'][0])
        
        c += 1
    
    # assembles solution image and a blank image for removing grid lines
    img = grid.show_digits(solved_grid)
    blank_img = grid.show_digits(blank_grid)
    
    # adds alpha values to solved image for later merging
    crop = grid.cropped2.copy()
    crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
    b, g, r = cv2.split(crop)
    alpha = np.ones(b.shape, dtype=b.dtype) * 100
    crop = cv2.merge((b, g, r, alpha))
    
    new_image = np.zeros(np.shape(blank_img))
    
    # removes grid lines from solution image based on blank image
    for i in range(len(blank_img[0])):
        for j in range(len(blank_img)):
            if blank_img[i][j] == 255:
                img[i][j] = 0
    
    # converts image back to color and adds aplha values for superimposing
    img = cv2.bitwise_not(img, img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    b, g, r = cv2.split(img)
    alpha = np.ones(b.shape, dtype=b.dtype) * 100
    img = cv2.merge((b, g, r, alpha))
    
    # changes digits to red and makes all other pixles transparent
    for i in range(len(blank_img[0])):
        for j in range(len(blank_img)):
            if img[i][j][0] == 0:
                img[i][j] = [0, 0, 255, 1]
            else:
                img[i][j] = [255,255,255,0]
                
    # resizes image
    h, v = grid.cropped2.shape[0], grid.cropped2.shape[1]
    img = cv2.resize(img, (h, v))            
    
    # overlays solutions on real image
    a = 1
    fin = cv2.addWeighted(crop, 0.5 , img, 0.3, 0)
    
    lab = cv2.cvtColor(fin, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    limg = cv2.merge((cl,a,b))
    fin = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    end = time.time()
    print('Total execution time: %s' % (end - start))

    cv2.imshow('image', fin)  # Display the image
    cv2.waitKey(0)    # Wait for any key to be pressed (with the image window active)
    cv2.destroyAllWindows()
    


