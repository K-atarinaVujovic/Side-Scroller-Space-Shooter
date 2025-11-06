# <p align=center>Side-Scroller Space Shooter</p>
A reinforcement learning project made in python for college class Basics of Computer Intelligence.

To run any available commands, run them inside the src folder.

- [About](#about)
    - [Game](#game)
    - [RL model](#rl-model)
- [Setup instructions](#setup-instructions)
- [Playing the game](#playing-the-game)
- [Training a model](#training-a-model)
    - [Additional training options](#additional-training-options)
- [Watching the model play](#watching-the-model-play)
- [Additional documentation](#additional-documentation)
- [TensorBoard report](#tensorboard-report)

## About
The project contains two segments: the game, and the RL model.

### Game
The game is made using pygame, and is based on side-scroller space shooting games like Gradius.

<p align="center">
  <img src=".github/assets/gameplay.gif" alt="Gameplay demo">
</p>

All pixel art assets were dowloaded from [Foozle](https://foozlecc.itch.io/) on [itch.io](https://itch.io): 
- [Void main ship](https://foozlecc.itch.io/void-main-ship)
- [Void fleet pack 1](https://foozlecc.itch.io/void-fleet-pack-1) 
- [Void environment pack](https://foozlecc.itch.io/void-environment-pack)

### RL model
The model uses the Proximal-Policy Optimization algorithm for training from the stable-baselines3 library.

For more details on the training process and existing models, go to [Additional documentation](#additional-documentation)

## Setup instructions
For the project to run, you need to have python installed. To install dependencies, run the following command:
```
pip install -r dependencies.txt
```

## Playing the game
To play the game yourself, run the following command:
```
python -m side-scroller-space-shooter.main
```
After running the command, a pygame window will open with the game ready to play.

## Training a model
To train a model with default options, run the following command:
```
python -m PPO.train -m <model-name>
```
All existing models are stored inside the PPO/models folder. If there is no existing model with <model-name>, a new one will be created, otherwise training will be done on the existing model.
The default number of timesteps is 25000.

### Additional training options
You can alter the training options by using any of the following arguments:
- `-t <num_timesteps>` - number of timesteps for training
- `-dd` - disable drawing the pygame window during training

 Example usage:
 ```
 pygame -m PPO.train -t 30000 -dd
```


## Watching the model play
To watch a trained model play the game, run the following command:
```
python -m PPO.play -m <model-name>
```
All existing models are stored inside the PPO/models folder

## Additional documentation
For more details on the project structure and training process, you can read the (project specification)["Specifikacija projekta.docx"]
The jupyter notebook used for project presentation is [Prezentacija.ipynb](src/Prezentacija.ipynb).

## TensorBoard report
To view the TensorBoard report for the models, run the following command:
```
tensorboard serve --logdir PPO/tensorboard
```
