import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.api_sound import StartPlayTTS
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode

# Set logging level
MiniSdk.set_log_level(logging.INFO)
# Set robot type
MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)


async def test_get_device_by_name():
    """Search for a device by its name."""
    result: WiFiDevice = await MiniSdk.get_device_by_name("00081", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


async def test_connect(dev: WiFiDevice) -> bool:
    """Connect to a device."""
    return await MiniSdk.connect(dev)


async def test_start_run_program():
    """Enter programming mode."""
    await MiniSdk.enter_program()


async def shutdown():
    """Disconnect and release resources."""
    await MiniSdk.quit_program()
    await MiniSdk.release()
    print("Program done. Exiting...")
    asyncio.get_event_loop().stop()


async def test_play_action():
    """Execute a demo action."""
    block = PlayAction(action_name='012')
    result_type, response = await block.execute()
    print(f'test_play_action result: {response}')
    assert result_type == MiniSdk.MiniApiResultType.Success, 'test_play_action timeout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'


async def test_move_robot():
    """Control the robot to move."""
    block = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    result_type, response = await block.execute()
    print(f'test_move_robot result: {response}')
    assert result_type == MiniSdk.MiniApiResultType.Success, 'test_move_robot timeout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


async def test_get_action_list():
    """Retrieve the list of supported actions."""
    block = GetActionList(action_type=RobotActionType.INNER)
    result_type, response = await block.execute()
    print(f'test_get_action_list result: {response}')
    assert result_type == MiniSdk.MiniApiResultType.Success, 'test_get_action_list timeout'
    assert response is not None and isinstance(response, GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


async def test_feel():
    test_feel = f"I feel good today, thank you!"
    tts_action = StartPlayTTS(text=test_feel)
    await tts_action.execute()

async def test_play_expression():
    block: PlayExpression = PlayExpression(express_name="codemao9")
    await block.execute() 

async def test_sneeze(): # sneeze
    """Execute a sneeze action."""
    block = PlayExpression(express_name='codemao9')
    await block.execute()

async def main():
    device = await test_get_device_by_name()
    if device:
        await test_connect(device)
        await test_start_run_program()
        await test_feel()
        await test_play_expression()
        await test_sneeze()
        await test_play_action()
        # await test_move_robot()
        await test_get_action_list()
        await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
        
         

