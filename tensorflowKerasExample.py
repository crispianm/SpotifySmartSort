"""
# import the library we will be using tensorflow
import tensorflow as tf

# TensorFlow constant (these are the weights)
w1 = tf.constant(0.5, name="w1")
w2 = tf.constant(-1.0, name="w2")
w3 = tf.constant(2.0, name="w3")
w4 = tf.constant(0.8, name="w4")
w5 = tf.constant(1.0, name="w5") #h1 weight
w6 = tf.constant(0.7, name="w6") #h2 weight
    
# TensorFlow variables (these are the input variables)
x1 = tf.Variable(5.0, name='x1')
x2 = tf.Variable(8.0, name='x2')
x3 = tf.Variable(4.0, name='x3')

# operations (this calculates the weighted sum)
h1 = tf.add(tf.multiply(w1, x1),tf.multiply(w2,x2), name='h1')
h2 = tf.add(tf.multiply(w3, x2),tf.multiply(w4,x3), name='h2')

y = tf.add(tf.multiply(w5,h1), tf.multiply(w6, h2)) # this adds up the two nodes

y.numpy() # the answer is numpy = ANSWER
"""

#########################

# Install TensorFlow
import tensorflow as tf

# Import the dataset (70000 images of handwritten letters)
mnist = tf.keras.datasets.mnist

"""The MNIST dataset is already split into test and train data, we can load these into variables with the following code:"""

# Split into test and train
(x_train, y_train), (x_test, y_test) = mnist.load_data()

"""For ANN, we often want to use normalised data (with values between 0 and 1). Greyscale images, like those in the MNIST dataset, can take values between 0 and 255 (which represent black and white respectively). Therefore, we can normalise the data by dividing by 255."""

# Normalise the data
x_train, x_test = x_train / 255.0, x_test / 255.0

"""
Use [Keras](https://keras.io/) within tensorflow

model = tf.keras.models.Sequential([
 [Sequential](https://www.tensorflow.org/api_docs/python/tf/keras/Sequential) 
 we are defining a feedforward ANN

tf.keras.layers.Flatten(input_shape=(28, 28)),
 defines the first layer of the ANN. 
 The input data is the handwriting images, which have 28x28 pixels with each pixel representing a data point. 
 Each image is fed into the ANN one at a time. 
 Flatten is used to flatten the 3D input without impacting the size.
  
tf.keras.layers.Dense(128, activation='relu'),
 defines another layer of the ANN. 
 [Dense](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense) 
 describes a standardly densely connected ANN layer. 
 The number is the units, or number of nodes in this layer. 
 This layer also has an activation function *relu* which performs the function *max(x, 0)*. 
 This is a *hidden* layer of the ANN.
  
tf.keras.layers.Dropout(0.2),
 specificing a dropout rate of 20%. 
 A dropout is when neurons in the ANN are randomly chosen to be excluded from the training of the ANN.
  
tf.keras.layers.Dense(10, activation='softmax')
 adding a final layer with 10 nodes 
 and a [softmax activation function](https://www.tensorflow.org/api_docs/python/tf/keras/activations/softmax).
"""

# Set out the architecture of the Neural Nework 
model = tf.keras.models.Sequential([ 
  tf.keras.layers.Flatten(input_shape=(28, 28)), 
  tf.keras.layers.Dense(128, activation='relu'), 
  tf.keras.layers.Dropout(0.2), 
  tf.keras.layers.Dense(10, activation='softmax')
])

"""
Compile the model

model.compile(optimizer='adam',
 The optimizer explains the formula for learning

loss='sparse_categorical_crossentropy',
  Loss defines the weights for the loss function. The loss function calculates the error in our ANN compared to the training data to be minimised. Sparse categorical crossentropy calculates the error between the labels and predictions.

metrics=['accuracy'])
  Metrics are what is tested throughout the learning process. These can be more complicated, but we will just be using accuracy which runs the model for test data and gives a percentage of how many datapoints were correctly classified. The closer to 100%, the better.
  Other arguments which can be used within the compile function can be found on (https://www.tensorflow.org/api_docs/python/tf/keras/Model), and scroll down to the compile section.
"""

# Create the model
model.compile(optimizer='adam', # optimizer explains the formula for learning
  loss='sparse_categorical_crossentropy', # loss defines the weights for the loss function
  metrics=['accuracy']) # metrics are what is tested throughout the learning process

"""The fit function can be used to train the model to our training data.
The epochs is how many times the data is run through the model. In this example, the model will be fit 5 times. 
However, it might be useful in real life to add some code to stop training the model if the metrics get worse.
"""

# Fit the model to the training data
model.fit(x_train, y_train, epochs=5)

"""In the above output, each epoch (out of 5) runs for each of the 1,875 training images.

The time is recorded, as is the loss (which we want to minimise) and the accuracy (which we want to maximise).
"""

# Compare the model to test data
model.evaluate(x_test,  y_test, verbose=1)

"""
After running the 313 test data images through the model, we get loss and accuracy numbers. These can be compared to the loss and accuracy numbers from the training data to check for overfitting to the training data. 

In the example, the test data has a higher accuracy than the training data, and a lower loss function.

Edit the Neural Network to see if you can improve the results: 

1. Change the number of nodes on the hidden layers 

2. Add additional layers (Hint: to add another standard layer, add a new line with [Dense](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense) as in the code above).

3. Change the [activation functions](https://www.tensorflow.org/api_docs/python/tf/keras/activations) 

4. Extra: change the [optimizer](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers), [loss](https://www.tensorflow.org/api_docs/python/tf/keras/losses) and [dropout](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout)
"""