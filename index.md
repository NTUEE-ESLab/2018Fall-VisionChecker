# 2018Fall-VisionChecker

## Introduction

## Dependence

## Run

## Fearures



### Demo

## Implementation



## Develop Process 

### Motion Recognization Method

#### Using Neural Network
We refer the [websites](https://towardsdatascience.com/how-to-build-a-real-time-hand-detector-using-neural-networks-ssd-on-tensorflow-d6bac0e4b2ce) which build the network for hand tracking, and here you can find their [github page](https://github.com/victordibia/handtracking).

However, this solution is extremely slow which may delay for almost 5~10 sec on Rpi , and that means it is incapable for real-time usage.

#### Using traditional CV method

##### HSV for skin detection

You can refer to this [website](https://www.pyimagesearch.com/2014/08/18/skin-detection-step-step-example-using-python-opencv/) for  more information.

However, this solution need to know how far is the distance from the user to screen and where is the hand position at initial frame, or it can use the above neural network to find the hand position. It seems fine to use the neral network for only first frame. Nevertheless, eventually the result isn't accurate enough for testing which may delay for 2 sec.

##### Simple difference for two frame

We propose a very simple solution that just calculate the abs difference between two frame, and apply some filter to blur and threshold to let our  frame more clean.

