#! /usr/bin/env python
import os
import imp
from threading import Thread
from ui import Term

PLUGINS_DIR = './plugins'

def run_plugin(name, func, args, out):
    try:
        res = func(*args)
    except Exception as err:
        Term.print_error('{0}: {1}'.format(name, err))
    else:
        out.append(res)

class Loader:
    def __init__(self, plugins_dir = PLUGINS_DIR):
        self._plugins_dir = plugins_dir
        self._plugins = []
        self.add_plugins_from(plugins_dir)

    def add_plugins_from(self, directory):
        content = os.listdir(directory)
        for filename in content:
            location = os.path.join(directory, filename)
            if not os.path.isdir(location):
                if filename.endswith('.py'):
                    self.load_plugin(location)
            elif '__init__.py' in os.listdir(location):
                self.load_plugin(os.path.join(location, '__init__.py'))

    def load_plugin(self, location):
        directory, filename = os.path.split(location)
        filename = os.path.splitext(filename)[0]
        try:
            module_desc = imp.find_module(filename, [directory])
            module = imp.load_module(filename, *module_desc)
            # print('* Loading plugin {0}{1}{2}'.format(Term.BGREEN, filename, Term.END))
            self._plugins.append({
                'name': filename,
                'dir': dir(module),
                'module': module
            })
        except Exception as e:
            print(e)

    def get_names(self):
        return [p['name'] for p in self._plugins]

    def exec_command(self, command, *args):
        funcs = [getattr(p['module'], command)
                 for p in self._plugins
                 if command in p['dir']]
        pool = []
        out = []
        for plugin in self._plugins:
            if command in plugin['dir']:
                func = getattr(plugin['module'], command)
                th = Thread(target=run_plugin, args=[plugin['name'], func, args, out])
                th.start()
                pool.append(th)
        for th in pool:
            th.join()
        return out
