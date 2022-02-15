# danser-python-tool
Basic python tool to help me recording videos at danser-go

# Documentation
This tool requires you to fill the "config.yml" properly and to set at least the skin of the replay, path of the replay and settings of the replay.

Create a replay object:
```
import main as python-tool

replay_object = python-tool.replay()
```
Replay object methods:

Set skin of replay:
  Opens a menu to select the skin of the replay
```
replay_object.set_skin()
```

Set path of replay:
  Automatically gets one osr file from main folder (To be improved)
```
replay_object.set_replay_path()
```

Set settings of replay:
  Opens a menu to select the settings of the replay
```
replay_object.set_settings()
```

Set start time of replay:
  Sets start time of replay by x seconds
```
replay_object.set_settings()
```

To make this tool work, your python file should be looking like this:
```
import main as python-tool

replay_object = python-tool.replay()

replay_object.set_skin()
replay_object.set_settings()
replay_object.set_replay_path()

replay_object.record_replay()
```

# Useful Links

[danser-go](https://github.com/Wieku/danser-go)
