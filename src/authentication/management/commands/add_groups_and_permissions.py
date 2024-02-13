from clients.models import Client, ClientIssue
from projects.models import Project,Issue,TimeLog,BillableHours
from employes.models import Employee,DocumentTraining,AllocatedAsset
from assigned_employes.models import AssignedEmploye
from authentication.models import Account
from employee_skill.models import EmployeeSkills,Skill
from timesheet.models import TimeSheet,ActualTimeLog

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

class GroupName:
    SUPERADMIN = "Super Admin"
    ADMIN = "Admin"
    PROJECTMANAGER = "Project Manager"
    EMPLOYEE = "Employee"
    CLIENT = "Client"
    HR = "Human Resources"

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.add_groups()

    def add_groups(self):
        print("----------------------------------")
        print("Creating/Checking Django Groups...")
        try:
            client_content_type = ContentType.objects.get_for_model(Client)
            client_issue_content_type = ContentType.objects.get_for_model(ClientIssue)
            project_content_type = ContentType.objects.get_for_model(Project)
            issue_content_type = ContentType.objects.get_for_model(Issue)
            timelog_content_type = ContentType.objects.get_for_model(TimeLog)
            billablehours_content_type = ContentType.objects.get_for_model(BillableHours)
            employee_content_type = ContentType.objects.get_for_model(Employee)
            document_content_type = ContentType.objects.get_for_model(DocumentTraining)
            allocations_content_type = ContentType.objects.get_for_model(AssignedEmploye)
            account_content_type = ContentType.objects.get_for_model(Account)
            skill_content_type = ContentType.objects.get_for_model(Skill)
            employee_skill_content_type = ContentType.objects.get_for_model(EmployeeSkills)
            timesheet_content_type = ContentType.objects.get_for_model(TimeSheet)
            actual_timelog_content_type = ContentType.objects.get_for_model(ActualTimeLog)
            allocated_asset_content_type = ContentType.objects.get_for_model(AllocatedAsset)
            GROUPS = [
                [
                    GroupName.SUPERADMIN,
                    [

                    ]
                ],
                [
                    GroupName.ADMIN,
                    [
                        ('add_account' , account_content_type),
                        ('change_account' , account_content_type),
                        ('view_account' , account_content_type),
                        ('delete_account' , account_content_type),
                        ('add_employee' , employee_content_type),
                        ('view_employee' , employee_content_type),
                        ('change_employee' , employee_content_type),
                        ('delete_employee' , employee_content_type),
                        ('view_documenttraining' , document_content_type),
                        ('add_documenttraining' , document_content_type),
                        ('change_documenttraining' , document_content_type),
                        ('delete_documenttraining' , document_content_type),
                        ('add_client' , client_content_type),
                        ('view_client' , client_content_type),
                        ('change_client' , client_content_type),
                        ('delete_client' , client_content_type),
                        ('add_project' , project_content_type),
                        ('view_project' , project_content_type),
                        ('change_project' , project_content_type),
                        ('delete_project' , project_content_type),
                        ('add_issue' , issue_content_type),
                        ('view_issue' , issue_content_type),
                        ('change_issue' , issue_content_type),
                        ('delete_issue' , issue_content_type),
                        ('add_timelog' , timelog_content_type),
                        ('view_timelog' , timelog_content_type),
                        ('change_timelog' , timelog_content_type),
                        ('delete_timelog' , timelog_content_type),
                        ('add_billablehours' , billablehours_content_type),
                        ('view_billablehours' , billablehours_content_type),
                        ('change_billablehours' , billablehours_content_type),
                        ('delete_billablehours' , billablehours_content_type),
                        ('add_assignedemploye' , allocations_content_type),
                        ('view_assignedemploye' , allocations_content_type),
                        ('change_assignedemploye' , allocations_content_type),
                        ('delete_assignedemploye' , allocations_content_type),
                        ('view_clientissue' , client_issue_content_type),
                        ('add_clientissue' , client_issue_content_type),
                        ('change_clientissue' , client_issue_content_type),
                        ('delete_clientissue' , client_issue_content_type),
                        ('add_actualtimelog' , actual_timelog_content_type),
                        ('view_actualtimelog' , actual_timelog_content_type),
                        ('change_actualtimelog' , actual_timelog_content_type),
                        ('delete_actualtimelog' , actual_timelog_content_type),
                        ('add_timesheet' , timesheet_content_type),
                        ('view_timesheet' , timesheet_content_type),
                        ('change_timesheet' , timesheet_content_type),
                        ('delete_timesheet' , timesheet_content_type),
                        ('add_employeeskills' , employee_skill_content_type),
                        ('change_employeeskills' , employee_skill_content_type),
                        ('view_employeeskills' , employee_skill_content_type),
                        ('delete_employeeskills' , employee_skill_content_type),
                        ('add_allocatedasset' , allocated_asset_content_type),
                        ('view_allocatedasset' , allocated_asset_content_type),
                        ('change_allocatedasset' , allocated_asset_content_type),
                        ('delete_allocatedasset' , allocated_asset_content_type),
                    ]
                ],
                [
                    GroupName.PROJECTMANAGER,
                    [
                        ('add_account' , account_content_type),
                        ('change_account' , account_content_type),
                        ('view_account' , account_content_type),
                        ('delete_account' , account_content_type),
                        ('view_client' , client_content_type),
                        ('view_project' , project_content_type),
                        ('view_employee' , employee_content_type),
                        ('view_documenttraining' , document_content_type),
                        ('add_documenttraining' , document_content_type),
                        ('change_documenttraining' , document_content_type),
                        ('delete_documenttraining' , document_content_type),
                        ('add_assignedemploye' , allocations_content_type),
                        ('view_assignedemploye' , allocations_content_type),
                        ('change_assignedemploye' , allocations_content_type),
                        ('delete_assignedemploye' , allocations_content_type),
                        ('add_issue' , issue_content_type),
                        ('view_issue' , issue_content_type),
                        ('change_issue' , issue_content_type),
                        ('delete_issue' , issue_content_type),
                        ('add_timelog' , timelog_content_type),
                        ('view_timelog' , timelog_content_type),
                        ('change_timelog' , timelog_content_type),
                        ('delete_timelog' , timelog_content_type),
                        ('add_billablehours' , billablehours_content_type),
                        ('view_billablehours' , billablehours_content_type),
                        ('change_billablehours' , billablehours_content_type),
                        ('delete_billablehours' , billablehours_content_type),
                    ]
                ],
                [
                    GroupName.EMPLOYEE,
                    [
                        ('add_account' , account_content_type),
                        ('change_account' , account_content_type),
                        ('view_account' , account_content_type),
                        ('delete_account' , account_content_type),
                        ('add_skill' , skill_content_type),
                        ('change_skill' , skill_content_type),
                        ('view_skill' , skill_content_type),
                        ('delete_skill' , skill_content_type),
                        ('add_employeeskills' , employee_skill_content_type),
                        ('change_employeeskills' , employee_skill_content_type),
                        ('view_employeeskills' , employee_skill_content_type),
                        ('delete_employeeskills' , employee_skill_content_type),
                        ('view_assignedemploye' , allocations_content_type),
                        ('view_employee' , employee_content_type),
                        ('change_employee' , employee_content_type),
                        ('delete_employee' , employee_content_type),
                        ('add_actualtimelog' , actual_timelog_content_type),
                        ('view_actualtimelog' , actual_timelog_content_type),
                        ('change_actualtimelog' , actual_timelog_content_type),
                        ('delete_actualtimelog' , actual_timelog_content_type),
                        ('add_timesheet' , timesheet_content_type),
                        ('view_timesheet' , timesheet_content_type),
                        ('change_timesheet' , timesheet_content_type),
                        ('delete_timesheet' , timesheet_content_type),
                    ]
                ],
                [
                    GroupName.CLIENT,
                    [
                        ('add_account' , account_content_type),
                        ('change_account' , account_content_type),
                        ('view_account' , account_content_type),
                        ('delete_account' , account_content_type),
                        ('view_client' , client_content_type),
                        ('change_client' , client_content_type),
                        ('delete_client' , client_content_type),
                        ('add_client' , client_content_type),
                        ('view_clientissue' , client_issue_content_type),
                        ('add_clientissue' , client_issue_content_type),
                        ('change_clientissue' , client_issue_content_type),
                        ('delete_clientissue' , client_issue_content_type),
                    ]
                ],
                [
                    GroupName.HR,
                    [
                        ('view_documenttraining' , document_content_type),
                        ('view_employee' , employee_content_type),
                    ]
                ],
            ]
            for group_data in GROUPS:
                group, created = Group.objects.get_or_create(name=group_data[0])
                group.permissions.clear()
                group_action = "Created" if created else "Already Exists"
                print(f"{group_action} group: {group_data[0]}")
                for perm in group_data[1]:
                    content_type = perm[1]
                    codename = perm[0]
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    group.permissions.add(permission)
                    print(f"Added permission '{permission}' to group '{group.name}'")
        except Exception as ex:
            print(ex)
