def test_environment_init():
    from ai_ops_env.environment import OpsEnv

    env = OpsEnv()
    state = env.reset()

    assert state is not None
