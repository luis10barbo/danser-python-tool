import subprocess
import lib.yaml as yaml
from lib.pick import pick
import logging
import os
        

# Setup Logging
logging.basicConfig(filename='danser-python-tool.log', encoding='utf-8', level=logging.DEBUG, filemode="w", format="%(asctime)s %(levelname)-8s %(message)s")

def l_err(message):
    logging.error(message)

def l_debug(message):
    logging.debug(message)

def l_info(message):
    logging.info(message)

# Program

class replay():
    def __init__(self):
        self.skin = ""
        self.replay_name = ""
        self.replay_path = ""
        self.settings = ""
        self.start_time = ""
        
        self.current_error = ""
        
        self.cfg = config_file()
    
    def get_replay_info(self):
        return self.skin, self.replay_path, self.settings
    
    def sucess(self, sucess_message="No message"):
        l_info("Sucess! : " + sucess_message)
        if running_cli == 1:
            return self.replay_menu()
        else:
            return True, sucess_message
        
    
    def error(self, error_message):
        self.current_error = "\nError : " + error_message
        l_err(error_message)
        if running_cli == 1:
            return self.replay_menu(False)
        else:
            return False, error_message
        
    
    def set_skin(self):
        # Validate Path
        validation_result, err = self.cfg.validate_osu_path()
        if validation_result == False:
            self.error(err)
        
        # Get skins
        skins_path = os.path.join(self.cfg.config_file["OsuPath"], "Skins")
        skins = os.listdir(skins_path)
        
        # Select Skin
        selected_skin = selection_menu(skins, menu_title="skin", search="")
        self.skin = selected_skin
        self.sucess("Skin set")
        return self.skin
    
    def set_replay_path(self):
        # TBD
        validation_result, err = self.cfg.validate_replays_path()
        if validation_result == False:
            self.error(err)
        
        replays_path = self.cfg.config_file["ReplaysPath"]
        replays = [file_name for file_name in os.listdir(replays_path) if file_name.endswith(".osr") == True]

        # No replays at folder
        if len(replays) < 1:
            self.error("No replays at folder")
            
        # One replay at folder
        if len(replays) == 1:
            self.replay_path = os.path.join(replays_path, replays[0])
            self.sucess("Replay set to " + self.replay_path)
            
        # More than one replay at folder
        answer = selection_menu(replays, menu_title="replay", )
        
        self.replay_path = os.path.join(replays_path, answer)
        self.sucess("Replay set to " + self.replay_path)
        return self.replay_path

    def set_settings(self):
        # Validate Path
        validation_result, err = self.cfg.validate_danser_path()
        if validation_result == False:
            self.error(err)
            
        # Get settings files
        settings_path = os.path.join(self.cfg.config_file["DanserPath"], "settings")
        settings = os.listdir(settings_path)
        
        # Remove "".json" from settings
        for i in range(len(settings)):
            settings[i] = settings[i].replace(".json", "")
            

        settings.remove("api.txt")
        
        # Select settings file
        selected_settings = selection_menu(settings, menu_title="setting", search="")
        self.settings = selected_settings
        self.sucess("Settings set")
        return self.settings
        
    def set_start_time(self):
        response = "" 
        while response.isdigit() == False:
            response = input("Write, in seconds, when you want to start the replay : ")
        self.start_time = response
        self.sucess("Start time set")
    
    def record_replay(self, record_all=0):
        # Check if skin, path, settings is set
        if all([self.skin != "", self.replay_path != "", self.settings != ""]) != True:
            if record_all == 1:
                l_err("Skin, path and settings should be set to record replay!")
                return
            self.error("Skin, path and settings should be set to record replay!")
                
        
        
        start_time = ""
        if self.start_time != "":
            start_time = "-start=\"" + self.start_time + "\""
        recording_arguments = "danser.exe -skip -replay=\"" + self.replay_path + "\" -skin=\"" + self.skin + "\" -settings=\"" + self.settings + "\" -record -out=\"" + self.replay_name + "\" " + start_time 
        l_debug("Recording arguments > " + recording_arguments)

        # Create bat file
        danser_path = self.cfg.config_file["DanserPath"]
        executable_path = os.path.join(danser_path, "record_replay.bat")
        l_debug("Danser Path > " + (danser_path) + str(type(danser_path)))
        l_debug("Executable Path > " + str(executable_path))
        with open(executable_path, "w") as file:
            file.write(str(recording_arguments))
        subprocess.run(executable_path, cwd=danser_path)
        
        if record_all > 0:
            l_debug("Replay Recorded")
        else:   
            self.sucess("Replay recorded")
        
    def replay_menu(self, sucess=True):
        # Reset error if sucess
        if sucess == True:
            self.current_error = ""
        
        # Skin, Replay Path and Settings
        set_skin_entry = "Set Replay Skin"
        set_replay_path_entry = "Set Replay Path"
        set_settings_entry = "Set Replay Settings"
        set_start_time_entry = "Set Replay Start Time"
        exit_entry = "Return to main menu"
        
        menu_entries = [set_skin_entry, set_replay_path_entry, set_settings_entry, set_start_time_entry, exit_entry]
        exit_number = len(menu_entries)

        # Create menu
        _, entry_number = selection_menu(entries=menu_entries, menu_title="Action\n" + str(self.get_replay_info()) + self.current_error, return_number= 1)
        
        l_debug("entry number > " + str(entry_number))
        l_debug("exit number > " + str(exit_number))

        match entry_number:
            case 1:
                self.set_skin()
            case 2:
                self.set_replay_path()
            case 3:
                self.set_settings()
            case 4:
                self.set_start_time()
            case exit_number:
                return cli.main_menu()    
        
    
class config_file():
    def __init__(self) -> None:
        self.config_file = ""
        
        self.read_config()
        pass
    
    def validate_osu_path(self):
        return self.validate_path(config_entry="OsuPath", required_file="osu!.exe")
    
    def validate_danser_path(self):
        return self.validate_path(config_entry="DanserPath", required_file="danser.exe")
    
    def validate_replays_path(self):
        return self.validate_path(config_entry="ReplaysPath")
    
    def validate_path(self, config_entry="", required_file="", write_config=1):
        # Check if path in config is empty
        path = self.config_file[config_entry]
        if path == "":
            answer = ""
            if write_config > 0:
                while answer == "":
                    answer = input("Write an path to be set at key " + config_entry + " in config file : ")
                self.config_file[config_entry] = answer
                self.write_config()
                return True, None
            return False, "No path defined at " + config_entry
            
        # Check if directory exists
        if os.path.isdir(path) == False:
            return False, "\"" + path + "\" is not a directory!"
        
        # Check if "osu.exe" exists in osu path
        path_files = os.listdir(path)
        if required_file != "":
            if [result for result in path_files if required_file == result] != [required_file]:
                return False, "No " + required_file + " in folder"
        
        # Is valid path! 
        return True, None

    def write_config(self):
        with open("config.yml", "w") as file:
            yaml.safe_dump(self.config_file, file)
            
    def read_config(self):
        config_file_path = "config.yml"
        # Create config file if it doesn't exist
        if os.path.isfile(config_file_path) == False:
            with open(config_file_path, "w") as file:
                yaml.safe_dump({"OsuPath" : "", "DanserPath" : "", "ReplaysPath" : ""}, file)
        # Open file
        with open(config_file_path, "r+", encoding="utf-8") as file:
            self.config_file = yaml.safe_load(file.read().replace("\\", "\\\\"))
            return self.config_file


class command_line_interface(): 
    def __init__(self):
        self.selected_replay = None
        self.i_replay = 3
        self.replay_dict = {}
        self.current_error = ""
    
    def error(self, error):
        self.current_error = "\nError : " + error
        l_err(error)
        if running_cli == 1:
            return self.main_menu(False)
    
    def get_replay_info(self, replay_object):
        return replay_object.get_replay_info()
    
    def create_replay_object(self):
        self.replay_dict[self.i_replay] = replay()
        
        # Logging
        l_debug("New replay added to dict")
        l_debug("Replay Dict > " + str(self.replay_dict))
        
        self.i_replay += 1
        return self.main_menu()
    
    def delete_replay_object(self):
        if self.replay_dict == {}:
            self.error("No replays to be deleted")
        
        # Create menu entries 
        menu_entries = []
        for key in self.replay_dict:
            menu_entries.append(self.get_replay_info(self.replay_dict[key]))
            

        l_debug(menu_entries)
        # Create Menu
        _, entry_number = selection_menu(entries=menu_entries, menu_title="Object to delete", return_number=1)
        
        # Delete Replay Entry
        for i, key in zip(range(len(self.replay_dict)), self.replay_dict):
            if i == int(entry_number) - 1:
                
                # Logging
                l_debug("Replay deleted from dict")
                l_debug("Replay Dict > " + str(self.replay_dict))
                
                del self.replay_dict[key]
                break
            
        return self.main_menu()
            
    def modify_replay_object(self):
        if self.replay_dict == {}:
            self.error("No replays to be selected")
        
        # Create menu entries 
        menu_entries = []
        for key in self.replay_dict:
            menu_entries.append(self.get_replay_info(self.replay_dict[key]))
            
        l_debug(menu_entries)
        # Create Menu
        _, entry_number = selection_menu(entries=menu_entries, menu_title="Object to delete", return_number=1)
        
        # Select Replay Entry
        for i, key in zip(range(len(self.replay_dict)), self.replay_dict):
            if i == int(entry_number) - 1:
                
                # Logging
                l_debug("Replay deleted from dict")
                l_debug("Replay Dict > " + str(self.replay_dict))
                
                self.replay_dict[key].replay_menu()
                break
        
        pass
    
    def record_all_replays(self):
        if self.replay_dict == {}:
            self.error("No replays to be recorded")
            
        for replay in self.replay_dict:
            self.replay_dict[replay].record_replay(1)
        

    def main_menu(self, sucess=True):
        if sucess == True:
            self.current_error = ""
            
        # Menu entries
        create_replay_entry = "Create Replay Object"
        delete_replay_entry = "Delete Replay Object"
        modify_replay_entry = "Modify Replay Object"
        record_all_replays = "Record All Replays"
        exit_entry = "Exit Program"

        menu_entries = [create_replay_entry, delete_replay_entry, modify_replay_entry, record_all_replays, exit_entry]
        exit_number = len(menu_entries)

        # Create menu
        _, entry_number = selection_menu(entries=menu_entries, menu_title="Action" + self.current_error, return_number=1)

        match entry_number:
            case 1:
                return self.create_replay_object()
            case 2:
                return self.delete_replay_object()
            case 3:
                return self.modify_replay_object()
            case 4:
                return self.record_all_replays()
            case exit_number:
                exit()
            
            
def selection_menu( entries=[], menu_title="" , search="", return_number=0):
        search_button = "-- Search --"
        
        # Only entries that contains search string
        menu_entries = [str(entry_name) for entry_name in entries if search.lower() in str(entry_name).lower()]
        
        # Add indication number to entries
        for i in range(len(menu_entries)):
            menu_entries[i] = str(i + 1) + ". " + menu_entries[i]
            
        
        # Add search button to entries
        menu_entries.insert(0, search_button)

        # Add a "n" if menu_title Starts With Vowel
        n = ""
        if menu_title[:1].lower() in "a e i o u":
            n = "n"
        
        # Open select menu
        selected_entry, _ = pick(title="Select a" + n + " " + menu_title , options=menu_entries, indicator=">> ", default_index=1)
        # Selected entry is search
        if selected_entry == search_button:
            answer = input("Search for " + menu_title + " : ")
            return selection_menu(entries=entries , search=answer)

        # Get entry split 
        entry_split = selected_entry.split(". ", 1)
        number = entry_split[0]
        entry_name = entry_split[1]
        if return_number == 1:
            return entry_name, int(number) 
        return entry_name
running_cli = 0

if __name__ == "__main__":
    running_cli = 1
    cli = command_line_interface()
    cli.main_menu()