from datetime import datetime

class Task:

    def __init__(self, project_name: str, title: str, priority: int, column_name: str, assignee_username: str,
                 date_due: int, comments: list =None):
        self.project_name = project_name
        self.title = title
        self.priority = priority
        self.column_name = column_name
        self.assignee_username = assignee_username
        self.date_due = date_due
        self.comments = comments

    def get_summary(self):

        data = list()
        data.append(self.project_name)
        data.append(self.title)
        data.append(self.priority)
        data.append(self.column_name)
        data.append(self.assignee_username)

        date_due = str()
        if self.date_due == '0':
            date_due = '-'
        else:
            date_due = datetime.fromtimestamp(float(self.date_due)).strftime("%A, %B %d, %Y %I:%M:%S")

        data.append(date_due)

        return data

    def __str__(self):
        return '[Task project_name={} title={} priority={} column_name={} assignee_username={} date_due={}]'.format(
            self.project_name, self.title, self.priority, self.column_name, self.assignee_username, self.date_due
        )


class Project:

    def __init__(self, project_id: int, project_name: str):
        self.project_id = project_id
        self.project_name = project_name


class Board:

    def __init__(self, project_name: str, board_name: str):
        self.project_name = project_name
        self.board_name = board_name
        self.data = dict()

    def add_column(self, column_name: str, tasks: list) -> None:
        self.data[column_name] = tasks



class KanboardException(Exception):
    def __init__(self, msg: str = ''):
        # Init the father class
        Exception.__init__(self, msg)
