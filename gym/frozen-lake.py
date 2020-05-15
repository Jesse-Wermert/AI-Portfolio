import gym
import numpy as np


MAX_ITERATIONS = 100
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

MAPS = {"4x4": ["SFFF", "FHFH", "FFFH", "HFFG"],
        "8x8": ["SFFFFFFF", "FFFFFFFF", "FFFHFFFF", "FFFFFHFF", "FFFHFFFF", "FHHFFFHF", "FHFHFHFH", "FFFHFFFG"]}


class FrozenLakeState(ProblemState):


    # gym.envs.register(id='FrozenLakeNotSlippery-v0',
    #                  entry_point='gym.envs.toy_text:FrozenLakeEnv',
    #                  kwargs={'map_name': '4x4', 'is_slippery': False},
    #                  max_episode_steps=100,
    #                  reward_threshold=0.78
    #                  )

    env = gym.make('FrozenLakeNotSlippery-v0')
    # above is for the environment to be based on deterministic policy
    observation_space = env.observation_space
    state_space = env.observation_space.n
    # Sampling State Space:
    for i in range(MAX_ITERATIONS):
        print(env.observation_space.sample())
    action_space = env.action_space



    """env = gym.make("FrozenLake-v0")
    env.reset()

    print("Action space: ", env.action_space)
    print("Observation space: ", env.observation_space)

    for i in range(MAX_ITERATIONS):
        random_action = env.action_space.sample()
        new_state, reward, done, info = env.step(
           random_action)
        env.render()
        if done:
            break
    env.close()
    """
