from library import KanboardLibrary

kb = KanboardLibrary("http://sdc-server/jsonrpc.php", "jsmoya", "0d7ca9fdcb78d238a862ee5fa69623898e9e5c5f3596ed4cf825708e3081")

my_dashboard = kb.get_my_dashboard()

overdue_tasks = kb.get_overdue_tasks()

projects = kb.get_project_list()

board = kb.get_board_stats('SKY', 'Dev')

# task = kb.get_task(10)

