from qLearningAgent import QLearningAgent
import coffeegame
import gym


def main():
    lake_env = gym.make('FrozenLake-v0', is_slippery=False)
    coffee_env = coffeegame.CoffeeEnv()
    taxi_env = gym.make('Taxi-v3').env
    lake_agent = QLearningAgent(lake_env, 100, 20000, decay_rate=0.001, alpha=0.1, gamma=0.6, epsilon=1,
                                rendering_enabled=False)
    coffee_agent = QLearningAgent(coffee_env, 100, 20000, decay_rate=0.01, alpha=0.1, gamma=0.6, epsilon=1,
                                  rendering_enabled=False)
    taxi_agent = QLearningAgent(taxi_env, 150, 100000, decay_rate=0.01, alpha=0.1, gamma=0.6, epsilon=1,
                                rendering_enabled=False)

    lake_agent.learn("FrozenLake-v0 (non-slippery)")
    # coffee_agent.learn("John's CoffeeGame")
    # taxi_agent.learn("Taxi-v3")


main()
