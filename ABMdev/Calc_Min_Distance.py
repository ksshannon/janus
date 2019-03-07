#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:51:14 2019
Calculate distance to closest cell of a given land cover
@author: kek25
"""
import numpy as np

samp=np.random.randint(low = 2, size=(5,6))

city = np.array(np.nonzero(samp))
other = np.array(np.where(samp==0))

#x=other[1,:]
#y=other[0,:]

dist = np.empty(city.shape) #faster than zeros, but b careful!

for i in np.arange(other.shape[1]):
  #go through each non-city cell
   x=other[1,i]
   y=other[0,i]
   
   #calculate distance to each of the city cells 
   for j in np.arange(city.shape[1]):
       xc=city[1,j]
       yc=city[0,j]
       
       if (x == xc + 1 | x == xc -1 | x == xc) && (y == yc + 1 | y == yc -1 | y == yc)
   
   
        