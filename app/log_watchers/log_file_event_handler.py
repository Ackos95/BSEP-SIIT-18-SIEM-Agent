from re import match
# from os.path import splitext, basename
from watchdog.events import FileSystemEventHandler
from SysLogParser.parser import SysLogParser
from app.siem_notifier.notifier import notify_siem_core


class LogFileEventHandler(FileSystemEventHandler):

    def __init__(self, config):
        """
        Class constructor, storing DI injected configuration

        :param config: Object containing all of the app configuration
        """

        self._config = config

    def _handle_file_change(self, file_path):
        """
        Handler function called for each file which changed (in watched directories)

        It reads through modified file, filters it by configuration regex filter,
        parses it (using SysLogParser), prepares it (extract data which should be sent TODO)
        and notifies SIEM-Core about new changes

        :param file_path: path to the modified file
        """

        try:
            with open(file_path, 'r') as modified_file:
                interesting_lines = list(filter(lambda line: match(self._config['filter'], line) is not None,
                                                modified_file.readlines()))

            # TODO: here should go some check for format (with exceptions)
            data = SysLogParser.parse_rfc5424(interesting_lines)
            # TODO: here should go some modification of data entries (customizations)

            notify_siem_core(self._config['siem-core-url'], data)
        except IOError:
            # silent error
            pass

    def on_modified(self, event):
        """
        Handler for an directory changed event (affecting both files in and watched directories)

        :param event: {(DirModifiedEvent or FileModifiedEvent)}
        """

        if not event.is_directory:  # and basename(splitext(event.src_path))[1] == 'log':
            self._handle_file_change(event.src_path)
