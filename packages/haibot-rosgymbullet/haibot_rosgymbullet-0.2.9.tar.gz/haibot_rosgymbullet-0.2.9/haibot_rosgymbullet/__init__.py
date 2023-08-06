from gym.envs.registration import register
register(
    id='HaIBotEnv-v2.8', 
    entry_point='haibot_rosgymbullet.envs:DiffBotDrivingEnv'
)