#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, stat
from os.path import isdir, isfile, join
from watchdog.observers import Observer
from app.log_watchers.log_file_event_handler import LogFileEventHandler


class LogWatchers(object):
    """
    Class responsible for creating all of the necessary objects for watching changes in files in and
    watched directories, and handling those changes
    """

    def __init__(self, config):
        """
        Class constructor, stores DI injected configuration, and creates containers for
        `Observer` and `Handler` object (observers are separate threads)

        :param config: Object containing all app configuration
        """

        self._config = config
        self._observers = []
        self._handlers = []
        self._files = {}

    def _inspect_files(self, dir_name):
        for entry in listdir(dir_name):
            file_path = join(dir_name, entry)
            if isfile(file_path):
                self.update_read_file_size(file_path)

    def _create_handler(self):
        """
        Helper function for creating handlers for each watched directory

        :return: {LogFileEventHandler} instance
        """

        return LogFileEventHandler(self, self._config)

    def _create_observer(self, dir_path, handler):
        """
        Helper function for creating observers for each watched directory

        :param dir_path: {string}, path to watched directory
        :param handler: {LogFileEventHandler} handler for watched directory

        :return: {watchdog.observers.Observer} instance
        """

        observer = Observer()
        observer.schedule(handler, dir_path)

        return observer

    def start(self):
        """
        Function going through configuration, instantiating and storing observers and hanlders
        for each of the watched directories.

        It also starts each of the newly created `watchdog.observers.Observer` threads.
        """

        for dir_path in self._config['watch-directories']:
            if isdir(dir_path):
                # fetch initial size of all files in watched directories (for caching)
                self._inspect_files(dir_path)

                handler = self._create_handler()
                observer = self._create_observer(dir_path, handler)

                self._handlers.append(handler)
                self._observers.append(observer)

                observer.start()

    def stop(self):
        """
        Function for stopping watcher execution, it stops all of the `watchdog.observers.Observer` threads,
        and clears all of the stored objects for given config (to help garbage collector remove them)
        """

        for observer in self._observers:
            observer.stop()
            observer.join()

        # clear lists (loose references - help garbage collector)
        self._observers = []
        self._handlers = []

    def get_read_file_size(self, file_path):
        """
        Helper method for retrieving last read file size

        :param file_path: path to the file which should be read
        :return: size of the file on last read
        """

        if file_path not in self._files.keys() or stat(file_path).st_size < self._files[file_path]:
            self._files[file_path] = 0

        return self._files[file_path]

    def update_read_file_size(self, file_path):
        """
        Helper method for updating last read file size

        :param file_path: path to the file which was just read
        """

        self._files[file_path] = stat(file_path).st_size
