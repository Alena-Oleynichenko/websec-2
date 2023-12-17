from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from json import load
import get_schedule

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
@app.get("/faculties")
def post_faculties(request: Request):
    with open("data/groups.json", encoding="utf-8") as f:
        data = load(f)

    faculties = {}
    for faculty, groups in data.items():
        faculties[faculty] = groups["id"]

    return templates.TemplateResponse("faculties.html", {"request": request, "faculties": faculties})


@app.get("/search")
def post_search(request: Request, searchText: str):
    with open("data/groups_tmp.json", encoding="utf-8") as f:
        data1 = load(f)
    with open("data/staff.json", encoding="utf-8") as f:
        data2 = load(f)

    searchGroups = {}
    for group, id in data1.items():
        if searchText in group:
            searchGroups[group] = id

    staff = {}
    for teacher, id in data2.items():
        if searchText in teacher:
            staff[teacher] = id

    return templates.TemplateResponse("search.html", {"request": request, "staff": staff, "groups": searchGroups, "searchText": searchText})


@app.get("/staff")
def post_staff(request: Request):
    with open("data/staff.json", encoding="utf-8") as f:
        data = load(f)

    staff = {}
    for teacher, id in data.items():
        staff[teacher] = id

    return templates.TemplateResponse("staff.html", {"request": request, "staff": staff})


@app.get("/faculties/{facultyId}/groups")
def post_groups(request: Request, facultyId: int):
    with open("data/groups.json", encoding="utf-8") as f:
        data = load(f)

    for faculty, grouplist in data.items():
        if int(grouplist["id"]) == facultyId:
            return templates.TemplateResponse("groups.html", {"request": request, "groups": grouplist["groups"]})

    return {"detail": "Faculty not found"}


@app.get("/schedule/groups")
def post_schedule(groupId: str, week: int = None):
    if week is None:
        url = f"https://ssau.ru/rasp?groupId={groupId}"
    else:
        url = f"https://ssau.ru/rasp?groupId={groupId}&selectedWeek={str(week)}&selectedWeekday=1"

    get_schedule.parser(url)
    with open("data/schedule.json", encoding="utf-8") as f:
        schedule = load(f)

    return {"groupId": groupId, "title": schedule["title"], "weeks": schedule["weeks"], "dates": schedule["dates"], "rows": schedule["rows"]}


@app.get("/schedule/staff")
def post_staff_schedule(staffId: str, week: int = None):
    if week is None:
        url = f"https://ssau.ru/rasp?staffId={staffId}"
    else:
        url = f"https://ssau.ru/rasp?staffId={staffId}&selectedWeek={str(week)}&selectedWeekday=1"

    get_schedule.parser(url)
    with open("data/schedule.json", encoding="utf-8") as f:
        schedule = load(f)

    return {"staffId": staffId, "title": schedule["title"], "weeks": schedule["weeks"], "dates": schedule["dates"], "rows": schedule["rows"]}
