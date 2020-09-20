'''
Created on 18 Sep 2020

@author: Andrew Witham

Main file for trilateration package
'''

'''
TO DO
a) add option for a format where count rates at measurement positions can be speicifed 
instead of distances
b) plot input and output data
c) add support for a general cartesian coordinate config so x,y values for measurement
positions can be specified
d) add a better front end than just command line!
'''
import argparse

'''
param separation = separation between the two recievers
param distance1 = distance between object and reciever 1
param distance2 = distance between object and reciever 2
output x = x coordinate of object
output y1 = 1st possible y coordinate of object
output y2 = 2nd possible y coordinate of object
This implements a trilateration algorithm for 2d cartesian coordinates
where the distance from an object to two recievers is known as well
as the separation between the two recievers.
The function returns the x and y coordinates of the object based on
an cartesian coordinate system where reciever 1 is at the origin and reciever 2 is
on the x axis. 
distance1^2 = x^2 + y^2
distance2^2 = (separation - x)^2 + y^2
Thus
x = (distance1^2 - distance2^2 + separation^2) / (2 * separation)
y = +-sqrt(distance1^2 - x^2)
Algorithm taken from the Wikipedia page on Multilateration
https://en.wikipedia.org/wiki/True-range_multilateration

'''
def trilaterate2D(separation, distance1, distance2):
    x = 'Undefined'
    y1 = 'Undefined'
    y2 = 'Undefined'
    if (separation > 0):
        x = (distance1**2 - distance2**2 + separation**2) / (2 * separation)
        y1 = (distance1**2 - x**2)**0.5
        y2 = -1*(distance1**2 - x**2)**0.5
    else:
        print('Separation is 0 or less please define a positive separation')
    return x, y1, y2

'''
param separation = separation between the two recievers
param distance1 = distance between object and reciever 1
param distance2 = distance between object and reciever 2
Purpose is to give information on input data and output results
and calls the logic to perform the trilateration calculation

'''
def dothecalculation(separation, distance1, distance2):
    print('Trilateration Calculation For 2D Cartesian Coordinates\n')
    print('Input\nSeparation defined between measurement points = ', separation, 'm')
    print('Distance between object and measurement point 1 = ', distance1, 'm')
    print('Distance between object and measurement point 2 = ', distance2, 'm\n')
    print('Object positions defined based on a coordinate system where...')
    
    print('a) measurement point 1 is at the origin')
    print('b) measurement point 2 is on the y axis\n')
    
    print('Output')
    x,y1,y2 = trilaterate2D(separation, distance1, distance2)
    print('Object Position x value ', x)
    print('Object Position y possible value 1 ', y1)
    print('Object Position y possible value 2 ', y2)    

if __name__ == '__main__':
    # create agrmunent parser
    parser = argparse.ArgumentParser(description='Perform 2D Trilateration')
 
    # add arguments to the argument parser
    parser.add_argument('separation', type=float, help='Separation in metres between measurement points')
    parser.add_argument('distance1', type=float, help='Distance in m between object and measurement point 1')
    parser.add_argument('distance2', type=float, help='Distance in m between object and measurement point 2')
 
    # parse the arguments from the command line
    args = parser.parse_args()
    dothecalculation(args.separation, args.distance1, args.distance2)
    

    