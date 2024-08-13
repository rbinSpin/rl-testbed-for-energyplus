#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
import sys
from mpi4py import MPI
from common.energyplus_util import (
    energyplus_arg_parser,
    energyplus_logbase_dir
)
from baselines.common.models import mlp
from baselines.trpo_mpi import trpo_mpi
import os
import datetime
from baselines import logger
from baselines_energyplus.bench import Monitor
import gym
import tensorflow as tf
import time

class ModelSaver:
    def __init__(self, save_path, save_frequency=10):
        self.save_path = save_path
        self.save_frequency = save_frequency
        self.iteration = 0
        self.start_time = time.time()

    def __call__(self, locals, globals):
        self.iteration += 1
        if self.iteration % self.save_frequency == 0:
            model = locals.get('pi')
            if model and hasattr(model, 'save'):
                save_path = os.path.join(self.save_path, f'model_iter_{self.iteration}')
                model.save(save_path)
                print(f"Model saved at iteration {self.iteration} in path: {save_path}")

        # 每小時打印一次進度
        if time.time() - self.start_time > 3600:
            self.start_time = time.time()
            print(f"Training progress: iteration {self.iteration}")

def make_energyplus_env(env_id, seed):
    """
    Create a wrapped, monitored gym.Env for EnergyEnv
    """
    env = gym.make(env_id)
    env = Monitor(env, logger.get_dir())
    env.seed(seed)
    return env

def train(env_id, num_timesteps, seed):
    workerseed = seed + 10000 * MPI.COMM_WORLD.Get_rank()
    
    # Create a new base directory like /tmp/openai-2018-05-21-12-27-22-552435
    log_dir = os.path.join(energyplus_logbase_dir(), datetime.datetime.now().strftime("openai-%Y-%m-%d-%H-%M-%S-%f"))
    if not os.path.exists(log_dir + '/output'):
        os.makedirs(log_dir + '/output')
    os.environ["ENERGYPLUS_LOG"] = log_dir

    model = os.getenv('ENERGYPLUS_MODEL')
    if model is None:
        print('Environment variable ENERGYPLUS_MODEL is not defined')
        sys.exit(1)
    weather = os.getenv('ENERGYPLUS_WEATHER')
    if weather is None:
        print('Environment variable ENERGYPLUS_WEATHER is not defined')
        sys.exit(1)

    rank = MPI.COMM_WORLD.Get_rank()
    if rank == 0:
        print('train: init logger with dir={}'.format(log_dir)) #XXX
        logger.configure(log_dir)
    else:
        logger.configure(format_strs=[])
        logger.set_level(logger.DISABLED)

    env = make_energyplus_env(env_id, workerseed)

    # 創建保存模型的目錄
    models_dir = os.path.join(log_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    # 創建 ModelSaver 實例
    model_saver = ModelSaver(save_path=models_dir, save_frequency=1)
    
    def combined_callback(locals, globals):
        model_saver(locals, globals)
        # 在這裡可以添加其他回調函數

    pi = trpo_mpi.learn(env=env,
                        network=mlp(num_hidden=32, num_layers=2),
                        total_timesteps=num_timesteps,
                        timesteps_per_batch=16*1024,
                        max_kl=0.01,
                        cg_iters=10,
                        cg_damping=0.1,
                        gamma=0.99,
                        lam=0.98,
                        vf_iters=5,
                        vf_stepsize=1e-3,
                        callback=combined_callback)
    
    pi.save(f"{models_dir}/final")



    env.close()

def main():
    args = energyplus_arg_parser().parse_args()
    train(args.env, num_timesteps=35040*100, seed=args.seed)
    # a day 96 steps, a year 35040 
    #train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)

if __name__ == '__main__':
    main()
