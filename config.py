import json
import os


class JsonTools:
    def __init__(self, filename : str = "settings.json"):
        self.filename: str = filename
        self.__filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        self.__data: dict
        self.__setup()


    def __setup(self) -> None:
        if os.path.exists(self.__filepath):
            with open(self.__filepath, "r", encoding="UTF-8") as file:
                loaded = json.load(file)
                self.__data = loaded if isinstance(loaded, dict) else {} 
        else:
            self.__data = {}   
    

    def __setitem__(self, key: str, value: str) -> None:        
        self.__data[key] = value
        

    def __getitem__(self, key) -> str:
        return self.__data[key]


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.save()
        return False


    def save(self) -> None:
        with open(self.__filepath, "w", encoding="UTF-8") as file:
            json.dump(self.__data, file, indent=4, ensure_ascii=False)
    
    def __len__(self) -> int:
        return len(self.__data)


