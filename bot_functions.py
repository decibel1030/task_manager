import datetime
import json
import os.path


def create_user_data_file(user_id):
    with open(f"data/{user_id}.json", 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("file created")


def refresh_data_in_user_file(user_id, issue_data):
    with open(f'data/{user_id}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(f'data/{user_id}.json', 'w', encoding='utf-8') as f:
        data.append([issue_data])
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('refreshed')


def get_date():
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    return f"Дата создания: {month}-{day} {hour}:{minute}"


def get_all_tasks_count(user_id):
    if os.path.exists(f"data/{user_id}.json"):
        with open(f'data/{user_id}.json', 'r', encoding='utf-8') as f:
            issues_list = json.load(f)
            issues_count = len(issues_list)
            if issues_count == 0:
                return False
        return f"У вас {issues_count} запланированных задач. Показать их ?"
    else:
        return False


def get_count_for_kb(user_id):
    if os.path.exists(f"data/{user_id}.json"):
        with open(f'data/{user_id}.json', 'r', encoding='utf-8') as f:
            issues_list = json.load(f)
            issues_count = len(issues_list)
            if issues_count == 0:
                return False
        return f"{issues_count}"
    else:
        return False


def get_all_task_list(user_id):
    if get_all_tasks_count(user_id) is not False:
        with open(f"data/{user_id}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        text = ''
        issue_id = 0
        for issue in data:
            hr = "------------\n"
            for datas in issue:
                print(datas)
                issue_id += 1
                text += f"<b>🔊 {issue_id}.{datas['title']}</b>\n" \
                        f"📄 {datas['description']}\n" \
                        f"⏰ {datas['created_at']}\n{hr}"

        return text
