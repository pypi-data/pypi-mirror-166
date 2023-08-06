import json
import os
import shutil
import typing
import atexit
import distutils.dir_util as dir_util

import ExtremePluginManager.constants as constants
import ExtremePluginManager.plugin.base_plugin as base_plugin
import ExtremePluginManager.plugin.directory_plugin as directory_plugin
import ExtremePluginManager.plugin.zip_file_plugin as zip_file_plugin
import ExtremePluginManager.strings as strings

PLUGIN_TYPES = [directory_plugin.DirectoryPlugin, zip_file_plugin.ZipFilePlugin]


class ExtremePluginManager:
    def __init__(
            self, plugin_directory: constants.PATH_TYPEHINT, create_dir: bool = False,
            plugin_register_filename: str = "plugins.json", start_event: str = "on_start", end_event: str = "on_stop",
            builtin_funcs: dict = None
    ):
        if not os.path.isdir(plugin_directory):
            if create_dir:
                os.makedirs(plugin_directory)

            else:
                raise ValueError("Plugin directory '{}' does not exist".format(
                    os.path.abspath(plugin_directory)
                ))

        self._plugin_directory = plugin_directory
        self._plugin_register_filename = plugin_register_filename
        self._start_event = start_event
        self._end_event = end_event
        self._builtin_funcs = {} if builtin_funcs is None else builtin_funcs

        self._plugins: typing.List[base_plugin.BasePlugin] = []
        self._plugin_register = {}

        self.reload_plugins()

        atexit.register(self.execute_end_event)

    @property
    def plugin_register(self) -> dict:
        return self._plugin_register

    def get_plugin_register(self) -> dict:
        return self._plugin_register

    def get_plugin_directory(self) -> constants.PATH_TYPEHINT:
        return self._plugin_directory

    @property
    def plugin_directory(self) -> constants.PATH_TYPEHINT:
        return self._plugin_directory

    def _get_register_path(self) -> str:
        return os.path.join(self._plugin_directory, self._plugin_register_filename)

    def reload_plugins(self):
        register_path = self._get_register_path()

        self.execute_end_event()

        self._plugins.clear()

        try:
            with open(register_path) as f:
                self._plugin_register = json.loads(f.read())

        except FileNotFoundError:
            with open(register_path, 'w') as f:
                f.write("{}")

            self._plugin_register = {}

        for plugin in self._get_raw_plugins():
            if self._plugin_register.get(plugin.plugin_id, False):
                plugin.reload()
                plugin.execute_event(self._start_event)
                self._plugins.append(plugin)

    def on_plugin_load(self, plugin: base_plugin.BasePlugin):
        pass

    def _get_raw_plugins(self) -> typing.List[base_plugin.BasePlugin]:
        result = []

        plugin_filename: str = os.path.normpath(self._plugin_register_filename).split(os.sep)[-1]

        for plugin_name in os.listdir(self._plugin_directory):
            if plugin_name == plugin_filename:
                continue

            full_path = os.path.join(self._plugin_directory, plugin_name)

            try:
                loaded = self._init_plugin(full_path)
            except Exception as e:
                print(e)
                loaded = None

            if loaded is not None:
                result.append(loaded)

        return result

    def _init_plugin(self, path: constants.PATH_TYPEHINT) -> base_plugin.BasePlugin:
        for plugin_type in PLUGIN_TYPES:
            if plugin_type.is_plugin_type(path):
                return plugin_type(self, path, self._builtin_funcs)

    def execute_event(self, event: str, *args, **kwargs):
        for plugin in self._plugins:
            plugin.execute_event(event, *args, **kwargs)

    def execute_end_event(self):
        self.execute_event(self._end_event)

    def execute_start_event(self):
        self.execute_event(self._start_event)

    def search_by_id(self, plugin_id: str) -> base_plugin.BasePlugin:
        for plugin in self._plugins:
            if plugin.plugin_id == plugin_id:
                return plugin

    def search_by_attribute(self, info_attribute: str, value, default=None) -> typing.List[base_plugin.BasePlugin]:
        return [p for p in self._plugins if getattr(p, info_attribute, default) == value]

    def install_plugin(
            self, path: constants.PATH_TYPEHINT, enable: bool = True, overwrite: bool = True, copy: bool = True
    ):
        if copy:
            dst_filename = os.path.join(self._plugin_directory, os.path.basename(path))

            if overwrite:
                if os.path.isdir(dst_filename):
                    shutil.rmtree(dst_filename)

                elif os.path.isfile(dst_filename):
                    os.remove(dst_filename)

            else:
                if os.path.exists(dst_filename):
                    raise ValueError('A plugin with the name {} already exists!'.format(os.path.basename(path)))

            if os.path.isdir(path):
                dir_util.copy_tree(path, dst_filename)

            elif os.path.isfile(path):
                shutil.copy2(path, dst_filename)

        else:
            dst_filename = path

        plugin = self._init_plugin(dst_filename)

        self._plugin_register[plugin.plugin_id] = enable

        with open(self._get_register_path(), 'w') as f:
            f.write(json.dumps(self._plugin_register))

        if enable:
            plugin.reload()
            plugin.execute_event(self._start_event)
            self._plugins.append(plugin)

    def uninstall_plugin(self, plugin_id: str, remove_files: bool = True):
        if plugin_id in self._plugin_register:
            if self._plugin_register[plugin_id]:
                self.search_by_id(plugin_id).execute_event(self._end_event)

            del self._plugin_register[plugin_id]

            with open(self._get_register_path(), 'w') as f:
                f.write(json.dumps(self._plugin_register))

        if remove_files:
            for plugin in self._get_raw_plugins():
                if plugin.plugin_id == plugin_id:
                    path = plugin.path

                    if os.path.isdir(path):
                        shutil.rmtree(path)

                    elif os.path.isfile(path):
                        os.remove(path)

    def create_template_plugin(self, plugin_id: str, enable: bool = True) -> str:
        path = os.path.join(self._plugin_directory, plugin_id)

        if os.path.isdir(path):
            shutil.rmtree(path)

        os.makedirs(path)

        with open(os.path.join(path, "info.json"), 'w') as f:
            f.write(strings.INFO.replace("{{id}}", plugin_id))

        with open(os.path.join(path, "main.py"), 'w') as f:
            f.write(
                strings.MAIN.replace("{{start_event}}", self._start_event).replace("{{end_event}}", self._end_event)
            )

        self.install_plugin(path, enable, copy=False)

        return path

    def enable_plugin(self, plugin_id: str):
        self.set_plugin_state(plugin_id, True)

    def disable_plugin(self, plugin_id: str):
        self.set_plugin_state(plugin_id, False)

    def set_plugin_state(self, plugin_id: str, state: bool):
        plugin = self.search_by_id(plugin_id)

        if state:
            plugin.execute_event(self._start_event)

        else:
            plugin.execute_event(self._end_event)

        self._plugin_register[plugin_id] = state

        with open(self._get_register_path(), 'w') as f:
            f.write(json.dumps(self._plugin_register))
