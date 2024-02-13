from datetime import datetime, timedelta
from operator import itemgetter

import requests
import json

team_id = "6934779"
assignee_data = "88845470,88845337,88845310,88842188,88842187,88841286,72728170,88840042,50345350,66845174,66815616,66815615,61774361,61764234,61740310,66783615,66766986,66762034,61702180,66756833,66753586,66742864,66701306,66630083,66653850,63074158,63066221,66630095,66630092,66630101,66630091,66630096,66630093,66630094,66630098,66630099,66630089,66630078,66630097,66630085,66630088,66630086,66630082,66630079,66630087,66630081,63012130,63012127,63012128,63012129,60997570,60992706,60992713,60982172,60980113,60980111,60977812,54661029,60932916,55035416,2805628,49122692,48815816,48804064,48781184,48667000,48639348,48638123,48628402,48622064,48622065,48610201,24632290,2833039,2824675,2802907,2798401,2795098,2789132,2784829,2784828,2780093,2777652,2779367,2779366,2776070,2776611,2776610,2776608,2776572,2776570,"
headers = {
    "Content-Type": "application/json",
    "Authorization": "2833039_f33ffdf19a4b8bc0a70418becc928e33cb6db790047b01d1391d65af93c6c926"
}


def hours_logged_this_month():
    url = f"https://api.clickup.com/api/v2/team/{team_id}/time_entries"

    query = {
        "start_date": int((datetime.strptime(f'01.{datetime.now().month}.{datetime.now().year} 00:0:00',
                                             '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),
        "end_date": int((datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 00:0:00',
                                           '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),
        "assignee": assignee_data,
    }

    response = requests.get(url, headers=headers, params=query)
    total_duration_this_month = 0
    for data in response.json()['data']:
        total_duration_this_month += round(int(data['duration']) / 3600000, 2)

    print(total_duration_this_month)
    return {"hours_logged_this_month": total_duration_this_month}


def closed_tickets_last_day():
    url = f"https://api.clickup.com/api/v2/team/{team_id}/task"

    query = {
        "start_date": int(
            (datetime.strptime(f'{int(datetime.now().day) - 1}.{datetime.now().month}.{datetime.now().year} 00:0:00',
                               '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),
        "end_date": int((datetime.strptime(f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year} 00:0:00',
                                           '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),

        "include_closed": "true",
    }

    response = requests.get(url, headers=headers, params=query)
    closed_count = 0
    for data in response.json()['tasks']:
        if "Closed" == data['status']['status']:
            closed_count += 1
    print(closed_count)
    return {"closed_tickets_last_day": closed_count}


def head_count():
    url = "https://api.clickup.com/api/v2/team"

    response = requests.get(url, headers=headers)

    data = response.json()
    head_count_data = len(data["teams"][0]["members"])
    return {"head_count_data": head_count_data}


def employee_hours_ratio():
    team_id = "6934779"
    url = "https://api.clickup.com/api/v2/team/" + team_id + "/time_entries"

    query = {
        "start_date": int((datetime.strptime(f'01.{datetime.now().month}.{datetime.now().year} 00:0:00',
                                             '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),
        "end_date": int(datetime.now().timestamp() * 1000),
        "assignee": assignee_data,
    }

    response = requests.get(url, headers=headers, params=query)

    time_track_list = []
    for data in response.json()['data']:
        time_update_status = True
        for time_track_obj in time_track_list:
            if time_track_obj['id'] == data['user']['id']:
                time_track_obj['time_locked'] += round(int(data['duration']) / 3600000, 2)
                time_update_status = False
                break

        if time_update_status:
            user_data = data['user'].copy()
            user_data['time_locked'] = round(int(data['duration']) / 3600000, 2)
            user_data.pop('profilePicture')
            time_track_list.append(user_data)

    # custom functions to get employee info
    def get_name(employee):
        return employee.get('time_locked')

    time_track_list.sort(key=get_name, reverse=True)

    return {
        "highest_hour_employees": [{"username": t['username'], "time_locked": t['time_locked']} for t in
                                   time_track_list[:10]],
        "lowest_hour_employees": [{"username": t['username'], "time_locked": t['time_locked']} for t in
                                  time_track_list[-10:]]
    }


def top_project_projection():
    url = "https://api.clickup.com/api/v2/team/" + team_id + "/time_entries"

    query = {
        "assignee": assignee_data,
        "include_location_names": "true",
    }

    response = requests.get(url, headers=headers, params=query)

    project_lists = []

    for data in response.json()["data"]:
        time_update_status = True
        project_data = {}
        for time_track_obj in project_lists:
            if time_track_obj["folder_id"] == data.get("task_location", {}).get("folder_id"):
                time_track_obj["project_time_duration"] += round(int(data["duration"]) / 3600000, 2)
                time_track_obj["project_folder_name"] = data.get("task_location", {}).get("folder_name")
                time_update_status = False
                break

        if time_update_status:
            project_data = {
                "folder_id": data.get("task_location", {}).get("folder_id"),
                "project_time_duration": round(int(data["duration"]) / 3600000, 2),
                "project_folder_name": data.get("task_location", {}).get("folder_name")
            }
            project_lists.append(project_data)

    # custom functions to get employee info
    def get_name(projects):
        return projects.get('project_time_duration')

    project_lists.sort(key=get_name, reverse=True)

    for project in project_lists[:10]:
        print(project)

    return project_lists


def current_month_projection():
    url = "https://api.clickup.com/api/v2/team/" + team_id + "/time_entries"
    query = {
        "start_date": int((datetime.strptime(f'01.{datetime.now().month}.{datetime.now().year} 00:0:00',
                                             '%d.%m.%Y %H:%M:%S')).timestamp() * 1000),
        "end_date": int((datetime.now().timestamp() * 1000)),
        "include_location_names": "true",
        "assignee": "88845470,88845337,88845310,88842188,88842187,88841286,72728170,88840042,50345350,66845174,66815616,66815615,61774361,61764234,61740310,66783615,66766986,66762034,61702180,66756833,66753586,66742864,66701306,66630083,66653850,63074158,63066221,66630095,66630092,66630101,66630091,66630096,66630093,66630094,66630098,66630099,66630089,66630078,66630097,66630085,66630088,66630086,66630082,66630079,66630087,66630081,63012130,63012127,63012128,63012129,60997570,60992706,60992713,60982172,60980113,60980111,60977812,54661029,60932916,55035416,2805628,49122692,48815816,48804064,48781184,48667000,48639348,48638123,48628402,48622064,48622065,48610201,24632290,2833039,2824675,2802907,2798401,2795098,2789132,2784829,2784828,2780093,2777652,2779367,2779366,2776070,2776611,2776610,2776608,2776572,2776570,",
        "team_id": team_id
    }

    response = requests.get(url, headers=headers, params=query)

    projected_list = []
    for data in response.json()["data"]:
        time_update_status = True
        proj_time = datetime.fromtimestamp(int(data['start']) / 1000)
        for time_track_obj in projected_list:
            if time_track_obj["day"] == proj_time.day:
                # and time_track_obj["month"] == proj_time.month and \
                # time_track_obj["year"] == proj_time.year:
                time_track_obj["total_time_duration"] += round(int(data["duration"]) / 3600000, 2)
                time_update_status = False
                break

        if time_update_status:
            project_data = {
                "day": proj_time.day,
                # "month": proj_time.month,
                # "year": proj_time.year,
                "total_time_duration": round(int(data["duration"]) / 3600000, 2),
            }
            projected_list.append(project_data)

    # projected_list = sorted(projected_list, key=itemgetter('year', 'month', 'day'))
    projected_list = sorted(projected_list, key=itemgetter('day'))
    return projected_list
