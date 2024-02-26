import pytest
from unittest import mock

from libname.robot_serial import RobotSerial

def test_open_robot_serial():
    mock.patch('serial.Serial', autospec=True).start()

    # Create a robot serial object
    robot_serial = RobotSerial('/dev/ttyUSB0')

    assert True

def test_send_robot_serial():
    mock.patch('serial.Serial', autospec=True).start()

    # Create a robot serial object
    robot_serial = RobotSerial('/dev/ttyUSB0')

    with robot_serial:
        # Send a command
        robot_serial.send('GETCNTL')

    assert True

def test_send_and_wait_robot_serial():
    # Set the return value for the mock serial object
    mock_serial = mock.patch('serial.Serial', autospec=True).start()
    mock_instance = mock.Mock()
    mock_instance.readline.return_value = b'QoK\r'
    mock_serial.return_value = mock_instance

    # Create a robot serial object
    robot_serial = RobotSerial('/dev/ttyUSB0')

    with robot_serial:
        # Send a command and wait for a response
        response = robot_serial.sendAndWait('GETCNTL')

    print("ASFASFFFFFFFFFF", response)
    assert True

def test_execute_command_robot_serial():
    # Set the return value for the mock serial object
    mock_serial = mock.patch('serial.Serial', autospec=True).start()
    mock_instance = mock.Mock()
    mock_instance.readline.return_value = b'QoK\r'
    mock_serial.return_value = mock_instance

    # Create a robot serial object
    robot_serial = RobotSerial('/dev/ttyUSB0')

    with robot_serial:
        # Execute a command
        response = robot_serial.executeCommand('GETCNTL', wait=True)

    assert response == b'QoK\r'
