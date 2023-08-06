from gym.envs.registration import register
register(
    id='HaIBotEnv-v3.4', 
    entry_point='haibot_rosgymbullet.envs:DiffBotDrivingEnv'
)