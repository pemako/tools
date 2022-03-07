#!/usr/bin/env python


class Task(object):
    def __init__(self):
        """Custom task class to store the object to be processed"""
        # any object that you want to process
        self.process_target = None

    def __str__(self):
        return "Task<{}>".format(self.process_target)
