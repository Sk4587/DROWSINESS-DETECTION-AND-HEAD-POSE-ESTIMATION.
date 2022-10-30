# DROWSINESS-DETECTION-AND-HEAD-POSE-ESTIMATION.

## Abstract
The webcam gets the image of the driver and by using Dlib and opencv , facial landmarks can be recognized. By using the location of points around the eye , the Eye Aspect Ratio can be calculated. From this ratio, drowsy state can be detected. By using the pygame library, alert music is played to warn the driver.

The next goal is to find the pose of an object when we have a calibrated camera, and we know the locations of n 3D points on the object and the corresponding 2D projections in the image and this can be achieved by the Perspective n Point method.

## NEED FOR DROWSINESS DETECTION
In the busy moving world , safety is of very high priority. In 2018, drowsiness or sleepiness was a factor for 2.5 percent of drivers and motorcycle operators involved in fatal crashes. The main aim of this project is to monitor the driver . The project is about detecting the drowsy state and alerting the driver.

## EXPERIMENTAL DETAILS:

### HARDWARE AND SOFTWARE USED:

#### Accessories used:
* Webcam
* Laptop
* Earphones

#### Language used:
* Python

#### Libraries used:
* Dlib
* Numpy
* Opencv
* Pygame

### CALCULATING EAR

![image](https://user-images.githubusercontent.com/46374770/198864699-789c495f-bb0f-4045-b4fb-16ce1422cabe.png) ![image](https://user-images.githubusercontent.com/46374770/198864727-f65d68d9-2d58-48da-b351-833df7d1c0c5.png)

While blinking , EAR reaches a very small value for a shorter duration (in order of milliseconds). When EAR is low for a longer duration, drowsy state (which is also known as microsleep) is reached.

![image](https://user-images.githubusercontent.com/46374770/198864741-f8390fc4-6998-41a5-bf6c-a96530588a77.png)

### ALGORITHM FOR DROWSINESS DETECTION:

![image](https://user-images.githubusercontent.com/46374770/198864752-cc38b7e4-03e5-44cd-9ddc-0a444f40e52d.png)

### BLINK RATE:

Blink rate is also closely related to drowsiness. A normal human blinks 12-19 times each minute while driving. If the rate goes beyond the threshold blink rate(21 blinks per minute) ,drowsy state is reached and alert music is played.

### HEAD POSE ESTIMATION:

In computer vision the pose of an object refers to its relative orientation and position with respect to a camera. You can change the pose by either moving the object with respect to the camera, or the camera with respect to the object.
The pose estimation problem described in this tutorial is often referred to as Perspective-n-Point problem or PNP in computer vision jargon. As we shall see in the following sections in more detail, in this problem the goal is to find the pose of an object when we have a calibrated camera, and we know the locations of n 3D points on the object and the corresponding 2D projections in the image.

### HOW DOES POSE ESTIMATION ALGORITHM WORK?

There are three coordinate systems in play here. The 3D coordinates of the various facial features shown above are in world coordinates. If we knew the rotation and translation ( i.e. pose ), we could transform the 3D points in world coordinates to 3D points in camera coordinates. The 3D points in camera coordinates can be projected onto the image plane ( i.e. image coordinate system ) using the intrinsic parameters of the camera ( focal length, optical center etc. ).

### EYE GAZE DETECTION:

By using dlib , facial landmarks can be recognised and by using facial points around the eye ,rectangles around the eye can be made using opencv.Then the rectangle part is cropped and processed using opencv to detect the eyeball. By using the function “HoughCircles” in opencv , circular eyeballs are detected. It first applied an edge detector in the image, from which it make contours and from the contours made it tried to calculate a “circularity ratio”, i.e., how much that contour looks like a circle.



