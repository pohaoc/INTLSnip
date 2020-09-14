# INTLSnip
A snipping tool that resizes the image intelligently using content aware scaling

# Why
The inspiration came when I was cropping some images for training data. I wanted a way to avoid squishing image and still preserve the features.

The tool is implemented with the algorithm described in this [paper](https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf)

GUI built with PyQt5
# How does it work?

The application allows users to crop image and decide what percentage of size they want to reduce it to while still preserving the prominent features

The algorithm creates a mapping of weights on each pixel by summing the absolute value of the partial derivative of the images in x-axis and y-axis.
It is done by convoling against the image with a 3x3 [sobel filter](https://en.wikipedia.org/wiki/Sobel_operator)

The formula to calculate the weight is 
<img src="https://render.githubusercontent.com/render/math?math=e1(I) = \lvert\frac{\partial}{\partial x} I\rvert + \lvert\frac{\partial}{\partial xy} I\rvert ">

After obtaining the weight mapping, the algorithm finds the minimum path from top to bottom.
Remove said path and repeating the same process will result in an image that preserves all the prominent features.

For more information please see this [blog](https://karthikkaranth.me/blog/implementing-seam-carving-with-python/).

Example (50% reduction):

![Original](https://github.com/du00d/INTLSnip/blob/master/src/cropped/054057.jpg)
![Processed at 50% size](https://github.com/du00d/INTLSnip/blob/master/src/cropped/carved.jpg)

# Potential Uses / Issues
Because the algorithm looks for prominent features in the image, if you were to crop an image of a face and reduce it by 50%. If it thinks the eyes and mouth are more outlined than the shape of face. The resulting picture may make you look like an alien. This may be not be a good thing if you are trying to make an instagram post. However, this could be potentially used in data augmentation for neural networks.

