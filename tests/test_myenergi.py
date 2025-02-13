from myenergi import myenergi


def test_var_input():
    s = myenergi.MyEnergi("abc", "123")
    assert s.__serial_number__ == "abc"
    assert s.__api_key__ == "xyz"
