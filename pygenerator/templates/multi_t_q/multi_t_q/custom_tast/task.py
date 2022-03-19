<<<<<<< HEAD:pygenerator/templates/multi_t_q/multi_t_q/custom_tast/task.py
=======
#!/usr/bin/env python


>>>>>>> 391530e3db66419902736c14babb0a6bcf179a51:pygenerator/templates/multi_t_q/lib/custom_tast/task.py
class Task(object):
    def __init__(self):
        """Custom task class to store the object to be processed"""
        # any object that you want to process
        self.process_target = None

    def __str__(self):
        return "Task<{}>".format(self.process_target)
