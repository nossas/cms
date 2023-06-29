from cms.api import add_plugin
from cms.models import Page

from contrib.frontend.landpage.models import Block


class BlockBuilderAPI:
    instance: Block
    
    inserts_db = []
    targets_db = []
    target = None

    def __init__(self, placeholder, language, **kwargs):

        self.placeholder = placeholder
        self.language = language
        self.instance = kwargs.get("instance", None)

        is_dirty = False
        if not self.instance:
            # Cria o bloco caso ele não seja passado na construção
            self.instance = add_plugin(
                plugin_type="BlockPlugin",
                placeholder=self.placeholder,
                language=self.language,
            )

        if not self.instance.title:
            is_dirty = True
            self.instance.title = f"Bloco {self.instance.position}"

        if not self.instance.slug:
            is_dirty = True
            self.instance.slug = f"bloco-{self.instance.position}"

        if is_dirty:
            self.instance.save()
        

        self.target = self.instance


    def add(self, plugin_type: str, is_target: bool = False, **data):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=plugin_type,
            language=self.instance.language,
            target=self.target,
            **data
        )

        if is_target:
            self.targets_db.append(self.target)
            self.target = plugin
        
        self.inserts_db.append(plugin)
        return self

    def previous(self):
        self.target = self.targets_db[-1]
        self.targets_db = self.targets_db[:-1]

        return self

    def get(self, index=-1):
        return self.inserts_db[index]
