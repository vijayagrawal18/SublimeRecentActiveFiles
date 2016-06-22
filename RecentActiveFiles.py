import sublime, sublime_plugin
import os

class RecentActiveFilesEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.file_name():
            view.window().run_command("recent_active_files", { "file_name": view.file_name() })

class RecentActiveFilesCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        File.project_folder = self.window.folders()[0]

    def run(self, file_name=None):
        if file_name:
            File.add(file_name)
        else:
            items = [[f.name(), f.path_from_project()] for f in File.all_recents]
            def on_done(index):
                if index < 0:
                    self.window.open_file(File.current_file.path)

            def on_highlight(index):
                if index >= 0:
                    self.window.open_file(File.all_recents[index].path, sublime.TRANSIENT)
                return True

            self.window.show_quick_panel(items, on_done, 0, -1, on_highlight)

class File(object):
    all_recents = []
    current_file = None
    project_folder = None

    def __init__(self, path):
        super(File, self).__init__()
        self.path = path

    def __eq__(self, other):
        return isinstance(other, File) and self.path == other.path

    @classmethod
    def add(cls, path):
        if cls.current_file is not None:
            cls.all_recents.insert(0, cls.current_file)
        cls.current_file = cls(path)
        if cls.current_file in cls.all_recents:
            cls.all_recents.remove(cls.current_file)

    def name(self):
        return os.path.basename(self.path)

    def path_from_project(self):
        return self.path.replace(self.project_folder + '/', '', 1)
