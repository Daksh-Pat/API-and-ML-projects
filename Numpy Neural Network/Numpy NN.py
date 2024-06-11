import numpy as np

#Eulers Activation function
def activate(z):
    activated = 1/(1+np.exp(z))
    return activated

#Forward propagation using input, weights, biases, and activation function
def forward(x,w,bias):
    #Forms predicted array to fillout and return
    y2=np.array([])
    #For each value in the input it will multiple it with the weights and add final value it to y2
    for y in range(len(x)):
        xw = 0
        for j in range(len(x)):
            xw+=w[y][j]*x[y]
        z=xw
        y2=np.append(y2,z)
    #Initial array is 1 by 3, this changes it so its transposed to 3 by 1
    y2=np.reshape(y2,(len(x),1))
    #Adds bias to the values of the predicted array
    y2=y2+bias
    #Applies Eulers activation function on predicted array and returns it
    y2=activate(y2)
    return y2

#Part of back propagation which re-adjusts the weights for each node based on output
def calculate_weight(y2,y1,x,w):
    #Calculates loss function of mean squared error to see how far off predicted is from actual
    MSE=(y1-y2)**2
    #Cost function calculates average loss across entire array
    C=np.sum(MSE)*(1/len(MSE))
    #Calcualtes rate of change with respect to the cost function vs predicted
    Cy2=np.sum(y1-y2)*(2/len(y1-y2))
    z=y2
    #Calculates rate of changge with respect to the predicted values vs the activated input array
    y2z=activate(z)*(1-activate(z))
    #Activated input is the same as input
    zw=x
    #Multiplies rate of change with gradient of cost vs predicted, predicted vs activated input, and activated input vs input
    Cw=Cy2*y2z*zw
    #Modifies weights based on learning rate of 0.5 and rate of change with respect to the cost function vs weights
    w=w-(0.5*Cw)
    return w

#Does the same thing as the first function but for the biases instead
def calculate_bias(y2,y1,bias):
    #Calculates loss function of mean squared error to see how far off predicted is from actual
    MSE=(y1-y2)**2
    #Cost function calculates average loss across entire array
    C=np.sum(MSE)*(1/len(MSE))
    #Calcualtes rate of change with respect to the cost function vs predicted
    Cy2=np.sum(y1-y2)*(2/len(y1-y2))
    z=y2
    #Calculates rate of changge with respect to the predicted values vs the activated input array
    y2z=activate(z)*(1-activate(z))
    #Multiplies rate of change with gradient of cost vs predicted and predicted vs activated input
    Cw=Cy2*y2z
    #Modifies biass based on learning rate of 0.5 and rate of change with respect to the cost function vs weights
    bias=bias-(0.5*Cw)
    return bias

#Forms random numpy array for input, output, and weights
x=np.random.rand(3,1)
y=np.random.rand(3,1)
w=np.random.rand(3,3)
#Bias is default set to 1.0
bias=1.0
#Forms first output from forward propagation to commence training loop
y2=forward(x,w,bias)

#Loop changes weights and biases until output predicted matches the actual output
while not (np.sum(y-y2))==0:
    #Forward propagation
    y2=forward(x,w,bias)
    print(np.sum(y-y2))
    #Back propagation
    w=calculate_weight(y2,y,x,w)
    bias=calculate_bias(y2,y,bias)

#Printing out final predicted values and the weights used to get them
y2=forward(x,w,bias)
print(y)
print(y2)
print(w)
