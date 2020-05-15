import numpy as np
import gym
import coffeegame
import random
import matplotlib.pyplot as plt


class QLearningAgent:

    def __init__(self, environment, max_steps_per_episode, max_eps, decay_rate=0.01,
                 alpha=0.1, gamma=0.6, epsilon=0.5, rendering_enabled=True):
        self.env = environment
        self.action_space_size = self.env.action_space.n
        self.state_space_size = self.env.observation_space.n
        self.table = np.zeros((self.state_space_size, self.action_space_size))
        self.max_steps = max_steps_per_episode
        self.max_episodes = max_eps
        self.learning_rate = alpha
        self.discount_rate = gamma
        self.exploration_rate = epsilon
        self.rendering_enabled = rendering_enabled
        self.decay_rate = decay_rate

    def learn(self, experiment_name):
        """
        Perform q-learning in the given environment.
        """
        ep_rewards = []
        aggr_ep_rewards = {'ep': [], 'avg': []}
        for _ in range(self.max_episodes):
            state = self.env.reset()
            episode_reward = 0
            for t in range(self.max_steps):
                if self.rendering_enabled:
                    self.env.render()
                if random.uniform(0, 1) < self.exploration_rate:
                    action = self.env.action_space.sample()  # explore action space
                else:
                    action = np.argmax(self.table[state])  # exploit learned values
                new_state, reward, done, info = self.env.step(action)
                self.table[state, action] = self.table[state, action] * (1-self.learning_rate) + \
                    self.learning_rate * (reward + self.discount_rate * np.max(self.table[new_state, :]))
                episode_reward += reward
                if done:
                    self.exploration_rate *= (1-self.decay_rate)
                    print("Episode finished after {} timesteps".format(t+1))
                    break
                else:
                    state = new_state
            ep_rewards.append(episode_reward)
            if not _ % self.max_steps:
                average_reward = sum(ep_rewards[-1000:])/1000
                aggr_ep_rewards['ep'].append(_)
                aggr_ep_rewards['avg'].append(average_reward)
        self.env.close()
        fig = plt.figure()
        # fig.suptitle('Average reward per 1000 episodes', fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_title(experiment_name)
        ax.set_xlabel('Episode idx')
        ax.set_ylabel('Avg. Reward/1000 episodes')
        # fig.plot()
        # plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
        plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='average rewards')
        fig.legend(loc=4)
        plt.show()
        # plt.set_xlabel('Episode idx')
        # plt.set_ylabel('Avg reward/1000 episodes')
        # plt.legend(loc=4)
        # plt.show()

    def test_game(self):
        reward_games = []
        for _ in range(1000):
            state = self.env.reset()
            rewards = 0
            while True:
                action = np.argmax(self.table[state])
                next_state, reward, done, info = self.env.step(action)
                state = next_state
                rewards += reward
                if done:
                    reward_games.append(rewards)
                    break
        return np.mean(reward_games)

    def behave(self):
        """
        This fcn should test if the q-learning algorithm has been
        successful. It should choose actions from start state to finish
        state that maximize reward (presuming q-learning has worked).
        """
        state = self.env.reset()
        for _ in range(self.max_steps):
            action = np.max(self.table[state])
            next_state, reward, done, info = self.env.step(action)
            if done:
                return reward
            else:
                state = next_state


# coffee_env = coffeegame.CoffeeEnv()
# coffee_agent = QLearningAgent(coffee_env, 100, 4000, rendering_enabled=False)
# coffee_agent.learn("coffee")

# Frozen Lake Environment
# lake_env = gym.make('FrozenLake-v0', is_slippery=False)
# lake_agent = QLearningAgent(lake_env, 100, 1000, rendering_enabled=False)
# lake_agent.learn("frozen lake")
