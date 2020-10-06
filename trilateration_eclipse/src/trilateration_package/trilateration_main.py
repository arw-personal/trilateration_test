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
import numpy as np
import matplotlib.pyplot as plt

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
param x = x position of the result
param y1 = 1st possible y position of the result
param y2 = 2nd possible y position of the result
Purpose is to plot the input data and output results from the trilateration process
'''
def plotit(separation, distance1, distance2, x, y1, y2):
    #setup grid, title and axes labels
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Trilateration Result')    
    #plot input position 1 and 2
    plt.plot([0],[0],marker='.',markerfacecolor='green',markeredgecolor='green',markersize=13.0,label='Measurement Position 1')
    plt.plot([separation],[0],marker='.',markerfacecolor='orange',markeredgecolor='orange',markersize=13.0,label='Measurement Position 2')
    
    #plot distance circle
    circlexpos1=np.arange((-1*distance1),(distance1),0.001)
    circleypos1 = circlexpos1.copy()
    circleypos1neg = circlexpos1.copy()
    
    circlexpos2 = np.arange((separation-distance2),(separation+distance2),0.001)
    circleypos2 = circlexpos2.copy()
    circleypos2neg = circlexpos2.copy()
      
    circindex=0 
    for i in circlexpos1:
        ypos=(distance1**2 - circlexpos1[circindex]**2)**0.5
        circleypos1[circindex]=ypos
        circleypos1neg[circindex]=-1*ypos
        circindex = circindex + 1
    
    circindex=0
    for i in circlexpos2:
        ypos=(distance2**2 - (circlexpos2[circindex]-separation)**2)**0.5
        circleypos2[circindex]=ypos
        circleypos2neg[circindex]=-1*ypos
        circindex = circindex + 1

    plt.plot(circlexpos1,circleypos1,color='green',dashes=[1,1,1,1],label='Distance From Measurement Position 1')
    plt.plot(circlexpos1,circleypos1neg,color='green',dashes=[1,1,1,1])
    plt.plot(circlexpos2,circleypos2,color='orange',dashes=[1,1,1,1],label='Distance From Measurement Position 2')
    plt.plot(circlexpos2,circleypos2neg,color='orange',dashes=[1,1,1,1])
        
    #plot measured position
    plt.plot([x],[y1],marker='+',markeredgecolor='blue',markersize=13.0,label='Measured Object Positions')
    plt.plot([x],[y2],marker='+',markeredgecolor='blue',markersize=13.0)
    lg = plt.legend(bbox_to_anchor=(1.05, 1))
    plt.savefig('trilateration_result.png', dpi=300, format='png', bbox_extra_artists=(lg,), bbox_inches='tight')
    
    
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
    plotit(separation, distance1, distance2, x, y1, y2)

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

    # plt.plot([2,3,4,5],[3,8,10,12],'gs')
    # plt.axis([0,7,0,21])
    # 
    # 
    # t=np.arange(0,5,0.2)
    #plt.plot(t,t,'r--',t,t**3,'b^',t,t**2,'gs')
    #data={'a':np.arange(50),'c':np.random.randint(0,50,50),'d':np.random.randn(50)}
    #data['b']=data['a']+10*np.random.randn(50)
    #data['d']=np.abs(data['d'])*100
    #plt.scatter('a','b',c='c',s='d',data=data)
    #names=["Dingos","Wild Cats","Tigers"]
    #values=[1,11,111]
    #plt.figure(1,figsize=(9,3))
    #plt.subplot(131)
    #plt.bar(names,values)
    #plt.subplot(132)
    #plt.scatter(names,values)
    #plt.subplot(133)
    #plt.plot(names,values)
    #plt.suptitle('Varsity')
    #plt.show()
