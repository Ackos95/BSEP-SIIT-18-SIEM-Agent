import re
from watchdog.events import FileSystemEventHandler
from app.siem_notifier.notifier import notify_siem_core


class LogFileEventHandler(FileSystemEventHandler):
    """
    Handler class for watched directories change signals,

    It is derived from `watchdog.events.FileSystemEventHandler` class, and overrides only
    `on_modified` event handler. Ensures caching of all files from watched directories,
    and also handling each file change with reading (only new) data, filtering it, and possibly
    notifying SIEM-Core
    """

    def __init__(self, context, config, dir_config):
        """
        Class constructor, storing DI injected configuration

        :param context: {LogWatchers} instance (under which handler is instantiated)
        :param config: Object containing all of the app configuration
        """

        self._context = context
        self._config = config
        self._dir_config = dir_config

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
                modified_file.seek(self._context.get_read_file_size(file_path))
                interesting_lines = list(filter(lambda line: re.search(self._dir_config['filterRegex'], line) is not None,
                                                modified_file.readlines()))
                self._context.update_read_file_size(file_path)

            if interesting_lines:
                # TODO: Handle log entries (transform maybe?), for now just pass logs as they are read

                # TODO: here should go some check for format (with exceptions)
                # data = SysLogParser.parse_rfc5424(interesting_lines)
                # TODO: here should go some modification of data entries (customizations)

                notify_siem_core(self._config['agent']['logDestinationIp'], interesting_lines)
        except IOError:
            # silent error (mostly for tmp files which get created and deleted instantly)
            pass

    def on_modified(self, event):
        """
        Handler for an directory changed event (affecting both files in and watched directories)

        :param event: {(DirModifiedEvent or FileModifiedEvent)}
        """

        if not event.is_directory:
            self._handle_file_change(event.src_path)
