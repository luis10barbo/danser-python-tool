import subprocess
from turtle import title
import lib.yaml as yaml
from lib.pick import pick
import logging
import os
        
def run():
    class replay():
        def __init__(self):
            self.skin = ""
            self.replay_name = ""
            self.replay_path = ""
            self.settings = ""
            self.start_time = ""
            
        def set_skin(self):
            # Validate Path
            validation_result, err = cfg.validate_osu_path()
            if validation_result == False:
                print(err)
                exit()
            
            # Get skins
            skins_path = os.path.join(cfg.config_file["OsuPath"], "Skins")
            skins = os.listdir(skins_path)
            
            # Select Skin
            selected_skin = self.selection_menu(skins, menu_title="skin", search="")
            self.skin = selected_skin
            return self.skin
        
        def set_replay_path(self):
            current_directory = os.listdir(".")

            self.replay_name = [file_name for file_name in current_directory if file_name.endswith(".osr") == True][0]
            self.replay_path = os.path.join(os.getcwd(), self.replay_name)
            return self.replay_path

        def set_settings(self):
            # Validate Path
            validation_result, err = cfg.validate_danser_path()
            if validation_result == False:
                print(err)
                exit()
                
            # Get settings files
            settings_path = os.path.join(cfg.config_file["DanserPath"], "settings")
            settings = os.listdir(settings_path)
            settings.remove("api.txt")
            
            # Select settings file
            selected_settings = self.selection_menu(settings, menu_title="setting", search="")
            self.settings = selected_settings.replace(".json", "")
            return self.settings
            
        def set_start_time(self):
            response = "" 
            while response.isdigit() == False:
                response = input("Write, in seconds, when you want to start the replay : ")
            self.start_time = response
                
            
        def selection_menu(self, entries=[], menu_title="" ,search=""):
            search_button = "-- Search --"
            
            # Only entries that contains search string
            menu_entries = [entry_name for entry_name in entries if search.lower() in entry_name.lower()]
            
            # Add indication number to entries
            for i in range(len(menu_entries)):
                menu_entries[i] = str(i + 1) + ". " + menu_entries[i]
                
            
            # Add search button to entries
            menu_entries.insert(0, search_button)
            
            # Open select menu
            selected_entry, _ = pick(title="Select a " + menu_title , options=menu_entries)
            # Selected entry is search
            if selected_entry == search_button:
                response = input("Search for " + menu_title + " : ")
                return self.selection_menu(entries=entries , search=response)
            return selected_entry.split(". ", 1)[1]
        
        def record_replay(self):
            start_time = ""
            if self.start_time != "":
                start_time = "-start=\"" + self.start_time + "\""
            recording_arguments = "danser.exe -skip -replay=\"" + self.replay_path + "\" -skin=\"" + self.skin + "\" -settings=\"" + self.settings + "\" -record -out=\"" + self.replay_name + "\" " + start_time 
            print(recording_arguments)

            # Create bat file
            danser_path = cfg.config_file["DanserPath"]
            executable_path = os.path.join(danser_path, "record_replay.bat")
            print("danser", danser_path, type(danser_path))
            print("executable", executable_path)
            with open(executable_path, "w") as file:
                file.write(str(recording_arguments))
            subprocess.run(executable_path, cwd=danser_path)
        
    class config_file():
        def __init__(self) -> None:
            self.config_file = ""
            
            self.read_config()
            pass
        
        def validate_osu_path(self):
            return self.validate_path(config_entry="OsuPath", required_file="osu!.exe")
        
        def validate_danser_path(self):
            return self.validate_path(config_entry="DanserPath", required_file="danser.exe")
        
        def validate_path(self, config_entry="", required_file=""):
            # Check if path in config is empty
            path = self.config_file[config_entry]
            if path == "":
                return False, "No path defined at " + config_entry
                
            # Check if directory exists
            if os.path.isdir(path) == False:
                return False, "Directory \"" + path + "\" doesn't exist"
            
            # Check if "osu.exe" exists in osu path
            path_files = os.listdir(path)
            if required_file != "":
                if [result for result in path_files if required_file == result] != [required_file]:
                    return False, "No " + required_file + " in folder"
            
            # Is valid path! 
            return True, None
                    
        def read_config(self):
            config_file_path = "config.yml"
            # Create config file if it doesn't exist
            if os.path.isfile(config_file_path) == False:
                with open(config_file_path, "w") as file:
                    yaml.safe_dump({"OsuPath" : "", "DanserPath" : ""}, file)
            # Open file
            with open(config_file_path, "r", encoding="utf-8") as file:
                self.config_file = yaml.safe_load(file.read().replace("\\", "\\\\"))
                return self.config_file
    
    def record_replay():
        replay_skin = replay_object.skin
        replay_path = replay_object.path
        replay_config = replay_object.config
        execution_arguments = None

    
    # Get os path Separator
    os_sep = os.path.sep

    cfg = config_file()
    
    # Create Replay Object
    replay_object = replay()
    replay_object.set_skin()
    replay_object.set_settings()
    replay_object.set_replay_path()
    # replay_object.set_start_time()
    
    print(replay_object.skin)
    print(replay_object.settings)
    print(replay_object.replay_path)
    print(replay_object.start_time)
    
    replay_object.record_replay()
    
    



if __name__ == "__main__":
    run()
