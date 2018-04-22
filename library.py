from model import KanboardException, Task, Project, Board
from util import create_tasks_from_dict
from kanboard import Kanboard
from terminaltables import AsciiTable


class KanboardLibrary:

    def __init__(self, url: str, user: str, token: str):
        self.kb = Kanboard(url, user, token)

    def get_version(self) -> str:
        return self.kb.execute("getVersion")

    def get_prioritys(self) -> list:
        pass

    def find_task_date_due(self, tasks: list, date_due: str) -> Task:
        for task in tasks:
            if task.date_due == date_due:
                return task
        return None

    def get_summary_tasks(self, tasks: list) -> str:
        table_list = list()
        headers = ['Project name', 'Title', 'Priority', 'Status', 'Assignee', 'Due date']
        table_list.append(headers)

        for task in tasks:
            data = task.get_summary()
            table_list.append(data)

        table = AsciiTable(table_list)
        return table.table

    def get_my_dashboard(self, printable: bool =True) -> Task:
        my_dashboard = self.kb.execute('getMyDashboard')

        tasks = list()
        for project in my_dashboard:
            task = Task(project['project_name'], project['title'], project['priority'], project['column_name'],
                        project['assignee_username'], project['date_due'])
            tasks.append(task)

        if printable:
            table = self.get_summary_tasks(tasks)
            print(table)

        return tasks

    def get_overdue_tasks(self, printable: bool =True) -> Task:
        overdue_tasks = self.kb.execute('getMyOverdueTasks')
        my_dashboard = self.get_my_dashboard(printable=False)

        tasks = list()
        for overdue_task in overdue_tasks:

            t = self.find_task_date_due(my_dashboard, overdue_task['date_due'])

            task = Task(overdue_task['project_name'], overdue_task['title'], t.priority,
                        t.column_name, overdue_task['assignee_username'], overdue_task['date_due'])
            tasks.append(task)

        if printable:
            table = self.get_summary_tasks(tasks)
            print(table)

        return tasks

    def get_project_list(self, printable=True) -> Project:
        # Get dict of projects
        projects = self.kb.execute('getMyProjectsList')

        if printable:
            table_list = list()
            headers = ['Project id', 'Project name', 'Boards']
            table_list.append(headers)

            for id in projects:
                boards = self.kb.execute('getBoard', project_id=id)
                boards_list = list()
                for item in boards:
                    boards_list.append(item['name'])

                data = [id, projects[id], ','.join(boards_list)]
                table_list.append(data)

            table = AsciiTable(table_list)
            print(table.table)

        return projects

    def get_project_id(self, project_name: str, printable=True) -> int:

        # Get dict of projects
        projects = self.get_project_list(printable=False)


        for id in projects:
            if projects[id] == project_name:
                return id

        raise KanboardException('Project not found')

    def _get_board(self, project_name: str, board_name: str) -> dict:
        project_id = self.get_project_id(project_name, printable=False)
        boards = self.kb.execute('getBoard', project_id=project_id)
        for board in boards:
            if board['name'] == board_name:
                return board

        raise KanboardException('Project or board does not exist')

    def get_board_stats(self, project_name: str, board_name: str) -> Task:

        board_data = self._get_board(project_name, board_name)

        board = Board(project_name, board_name)

        for column in board.columns:
            tasks = create_tasks_from_dict(column.tasks)
            board.add_column(column['title'], tasks)


        # tasks = list()
        # for project in my_dashboard:
        #     task = Task(project['project_name'], project['title'], project['priority'], project['column_name'],
        #                 project['assignee_username'], project['date_due'])
        #     tasks.append(task)
        #
        # if printable:
        #     table = self.get_summary_tasks(tasks)
        #     print(table)
        #
        # return tasks

        pass