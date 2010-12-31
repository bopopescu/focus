from django.test import TestCase
from models import *
from app.customers.models import *

class PermissionsTesting(TestCase):
    def setUp(self):
        self.user1 = User.objects.get_or_create(username="test")[0]
        self.user2 = User.objects.get_or_create(username="test2")[0]

        self.customer1 = Customer.objects.get_or_create(full_name="Customer1", cid=1)[0]
        self.customer2 = Customer.objects.get_or_create(full_name="Customer2", cid=2)[0]

        self.group1 = Group.objects.get_or_create(name="group1")[0]
        self.group2 = Group.objects.get_or_create(name="group2")[0]

        self.role1 = Role.objects.get_or_create(name="Leader")[0]
        self.role2 = Role.objects.get_or_create(name="Member")[0]

    def testUserPerm(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.user1.grant_role("Member", self.customer1)
        self.user1.grant_role("Leader", self.customer1)
        self.role2.grant_actions("DELETE")

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testGivePermToClasses(self):
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer)
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should now have this perm")

    def testTimeLimitedGrants(self):
        #First test
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Second test
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), False,
                         "The user should not have this perm")
        self.user2.grant_permissions("EDIT", self.customer1,
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), True, "The user should have this perm")

        #Third test
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("LIST", Customer,
                                     from_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm ")

        self.user2.grant_permissions("LIST", Customer,
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), True, "The user should have this perm")

    def testNegativeGrants(self):
        #First do normal test, and give valid permission
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Then create negative (delete) grants
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(), negative=True)

        #Now, the user should not have permission any longer
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")


    def testNegativeTimeLimitedGrants(self):
        #First, grants normally, then give negative time limited
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")

        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Then create negative (delete) grants, but from_date tomorrow
        self.user2.grant_permissions("CREATE", Customer, negative=True, from_date=datetime.today() + timedelta(1))

        #Then the user should still have permission
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should still have this perm")

        #But then we add negative permission, from today
        self.user2.grant_permissions("CREATE", Customer, negative=True,)

        #Now, the user should not have permission any longer
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm.")

        #Check if the user now has two negative permission
        self.assertEqual(Permission.objects.filter(user=self.user2, negative=True).count(), 2)

    def testUserInGroupPermissionByRoles(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group1.grant_role("Member", self.customer1)
        self.group1.grant_role("Leader", self.customer1)
        self.role2.grant_actions("DELETE")

        self.group1.addMember(self.user1)

        #Check if user is added properly
        self.assertEqual(self.group1.members.all()[0], self.user1)

        #Check if group has access
        self.assertEqual(self.group1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.group1.has_permission_to("DELETE", self.customer1), True)

        #Check if user gain access by group
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testUserInGroupPermissionByRolesInheritance(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group2.grant_role("Member", self.customer1)
        self.group2.grant_role("Leader", self.customer1)
        self.role2.grant_actions("DELETE")

        self.group1.addMember(self.user1)

        #Check if user is added properly
        self.assertEqual(self.group1.members.all()[0], self.user1)

        self.group1.parent = self.group2
        self.group1.save()

        #Check if group has access
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testUserInGroupPermissionClasses(self):
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.group1.grant_permissions("CREATE", Customer)
        self.group1.addMember(self.user2)
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should now have this perm")

    def testUserInGroupPermissionManuallyTimeLimited(self):

        self.group2.addMember(self.user2)

        #First test
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")

        self.group2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Second test
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), False,
                         "The user should not have this perm")

        self.group2.grant_permissions("EDIT", self.customer1,
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), True, "The user should have this perm")

        #Third test
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm")
        self.group2.grant_permissions("LIST", Customer,
                                     from_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm ")

        self.group2.grant_permissions("LIST", Customer,
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), True, "The user should have this perm")


    def testWhoHasPermissionToDoSomething(self):

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group2.grant_role("Member", self.customer1)
        self.group2.grant_role("Leader", self.customer1)

        self.group2.addMember(self.user1)
        self.group2.addMember(self.user2)

        self.assertEqual(self.user1 in self.customer1.whoHasPermissionTo("FAVORITE"), False)
        self.group2.grant_permissions("FAVORITE", self.customer1)
        self.assertEqual(self.user1 in self.customer1.whoHasPermissionTo("FAVORITE"), True)

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True, "The user should have this perm")
        self.assertEqual(self.user1.has_permission_to("VIEW", self.customer1), False, "The user should not have this perm")

        self.assertEqual(self.user1 in self.customer1.whoHasPermissionTo("EDIT"), True)
        self.assertEqual(self.user2 in self.customer1.whoHasPermissionTo("EDIT"), True)
        self.assertEqual(self.user2 in self.customer1.whoHasPermissionTo("VIEW"), False)