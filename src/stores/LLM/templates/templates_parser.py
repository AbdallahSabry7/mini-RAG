import os

class template_parser:
    def __init__(self,language : str = "en"):
        self.language = language
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.set_language_path(language = self.language)


    def set_language_path(self, language : str):
        language_path = os.path.join(self.current_path,"locales", language)
        if not os.path.exists(language_path):
            self.language = "en"

    def get(self,group : str , key : str , vars : dict = {}):
        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path,"locales", self.language, f"{group}.py")
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path,"locales", "en", f"{group}.py")
            self.language = "en"
        if not os.path.exists(group_path):
            return None
        
        module = __import__(f"stores.LLM.templates.locales.{self.language}.{group}", fromlist=[group])

        if not module:
            return None
        key_attribute = getattr(module, key)
        return key_attribute.substitute(vars) if vars else key_attribute
        
        
        


