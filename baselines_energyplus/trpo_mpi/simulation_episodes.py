import tensorflow as tf
import numpy as np
from baselines.common.policies import PolicyWithValue
from baselines.common import set_global_seeds
from gym_energyplus.envs import EnergyPlusEnv
from baselines.common.models import mlp
import os
from baselines.trpo_mpi.trpo_mpi import traj_segment_generator
from datetime import datetime
try:
    from mpi4py import MPI
except ImportError:
    MPI = None


def main():
    # 設置隨機種子以確保可重現性
    set_global_seeds(0)
    
    # 創建環境（這裡需要替換為您的 EnergyPlus 環境）
    energyplus_file = None
    model_file = os.path.expanduser("~/sim/test_sim/input/2ZoneDataCenterHVAC_wEconomizer_Temp.idf")
    weather_file = os.path.expanduser("~/sim/test_sim/input/USA_CA_San.Francisco.Intl.AP.724940_TMY3_2015_JuneFirst.epw")
    log_dir = None
    if log_dir is None:
        base_log_dir = os.path.expanduser("~/sim/sim_log/")
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(base_log_dir, current_time)
    env = EnergyPlusEnv(
                energyplus_file=energyplus_file,
                model_file=model_file,
                weather_file=weather_file,
                log_dir=log_dir,
                verbose=False,
                seed=None)
    
    # 載入訓練好的策略
    network=mlp(num_hidden=32, num_layers=2)
    pi_policy_network = network(env.observation_space.shape)
    pi_value_network = network(env.observation_space.shape)
    pi = PolicyWithValue(env.action_space, pi_policy_network, pi_value_network)
    pi.load(os.path.expanduser("~/sim/test_sim/nn"))

    # simulation specifical day config

    simulation_days = 1
    timestep_in_idf = 4 # 每 15 分鐘一步
    steps_per_day = timestep_in_idf*24  # 假設每 15 分鐘一步
    total_steps = simulation_days * steps_per_day
    # 進行一次完整的模擬
    seg_gen = traj_segment_generator(pi, env, total_steps, sim=True)

    result = seg_gen.__next__()
    total_reward = result["rew"].sum()

    print(f"The total reward is {total_reward}")

if __name__ == "__main__":
    main()
