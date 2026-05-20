# PongNeuralNetwork
Neural Network that learns how to play a simplified version of Pong.  

The only external library used for this project was pygame for the interface handling.  
```
pip install pygame-ce
```
Every other aspect for this project was made from scratch using plain python.  

In the current state of the project, running the main file will result in loading the neural network saved in the file ```saves/save_complete.json```. This neural network plays the game without making any mistakes.  
It is possible to change the save file in the ```parameters.py``` file, using the ```NETWORK_PATH``` parameter. The number displayed in the save file name indicates how many hits the pong paddle was able to make with that neural network.  

#### Training a new Neural Network  
To train a new neural network the following parameters in the ```parameters.py``` file showld be changed: 

* ```GENETIC_TRAIN``` must be True: This parameter allows the program to change the weights of the neural network in each iteration, it saves the configuration if it results in a higher number of hits than the previous one. If not, it loads the best configuration saved and tries again.
* ```LOAD_NETWORK``` should be False: This parameter will ignore all saved files and start the neural network with random values.

#### Changing Network Parameters  
To change the neural network parameters in the ```parameters.py``` the following values can be modified:  

* ```NUMBER_OF_NEURONS```: Indicates the number of neurons in each level of the Neural Network
* ```NUMBER_OF_LEVELS```: Indicates how many hidden layers the Neural Network has.
* ```MUTATE_AMOUNT```: Indicates the magnitude of the change every time the Neural Network mutates.  
  

<img width="620" height="537" alt="image" src="https://github.com/user-attachments/assets/c9af42b8-77ff-4714-8dea-adb4e88282a9" />


