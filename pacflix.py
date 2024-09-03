from tabulate import tabulate
import secrets


class MyError(Exception):
    def __init__(self, error, value):
        self.error = error
        self.value = value


class User:
    def __init__(self, username = "", duration_plan = 0, current_plan = "None",):
        self.username = username
        self.current_plan = current_plan
        self.duration_plan = duration_plan
        self.referral_code = "None"

        self.user_data = [self.current_plan,
                          self.duration_plan,
                          self.referral_code]

        self.user_database = {"Shandy": ["Basic Plan", 12, "shandy-2134"],
                          "Cahya": ["Standard Plan", 24, "cahya-abcd"],
                          "Ana": ["Premium Plan", 5, "ana-2f9g"],
                          "Bagus": ["Basic Plan", 11, "bagus-9f92"]
                          }
        
        self.user_database[self.username] = self.user_data

        # -------PacFlix Plan List Variable-----------
        self.first_row = ['Basic Plan', 'Standard Plan', 'Premium Plan', 'Services']

        self.can_stream = [True , True, True, 'Bisa Stream']
        self.can_download = [True, True, True, 'Bisa Download']
        self.has_SD = [True, True, True, 'Kualitas SD']
        self.has_HD = [False, True, True, 'Kualitas HD']
        self.has_UHD = [False, False, True, 'Kualitas UHD']
        self.num_of_device = [1, 2, 4, 'Number of devices']
        self.content = ['3rd party Movie only', 'Basic Plan Content + Sports', 'Basic Plan + Standrad Plan + PacFlix Original Series', 'Jenis Konten']
        self.price = [120_000, 160_000, 200_000, 'harga']

        self.all_plan = [self.can_stream,
                      self.can_download,
                      self.has_SD,
                      self.has_HD,
                      self.has_UHD,
                      self.num_of_device,
                      self.content,
                      self.price
                      ]

    def check_benefit(self):
        #Show all benefit
        all_data = tabulate(self.all_plan, headers = self.first_row)
        print("PacFlix Plan List \n")
        print(all_data, "\n")

    def check_plan(self, username):
        user_plan = []
        user_service = []
        self.user_data = self.user_database.get(username)

        if self.user_data[0] in self.first_row[:3]:
            print(f"{username} menggunakan {self.user_data[0]}")
            print(f"Sejak {self.user_data[1]} bulan yang lalu \n")
            print(f"{self.user_data[0]} PacFlix Benefit List")

            idx = self.first_row.index(self.user_data[0])
            first_row = [self.user_data[0], self.first_row[3]]

            for i in self.all_plan:
                user_plan.append(i[idx])
                user_service.append(i[3])

            self.plan_service = [user_plan, user_service]
            self.plan_service = list(map(list, zip(*self.plan_service)))
            self.plan_service = tabulate(self.plan_service, headers=first_row)

            print(self.plan_service)
        
        else:
            print("Please pick your plan to enjoy our service")

    def upgrade_plan(self, username, current_plan, new_plan):
        self.user_data = self.user_database.get(username)
        self.duration_plan = self.user_data[1]

        try:
            #Check if the plan is exist
            if current_plan not in self.first_row[:3]:
                raise MyError(error = "plan_not_exist", value = current_plan)
            
            #Check if the new_plan is exist
            if new_plan not in self.first_row[:3]:
                raise MyError(error = "plan_not_exist", value = new_plan)

            #Check if the user plan is correct
            if current_plan != self.user_data[0]:
                raise MyError(error = "plan_isn't", value = current_plan)

            #Check if it is downgrade
            if self.first_row.index(new_plan) < self.first_row.index(new_plan):
                raise MyError(error = "downgrade", value = current_plan)

            #Check the plan duration
            if self.duration_plan > 12:
                discount = 5/100
            else:
                discount = 0

            #Get the index of the plan
            idx = self.first_row.index(new_plan)

            #Get the price from index of plan
            plan_price = self.price[idx]

            #Count the price
            final_price = plan_price - (plan_price * discount)

            #Update the new data to user_database
            self.current_plan = new_plan
            self.user_data = [self.current_plan, self.duration_plan, self.referral_code]
            self.user_database[self.username] = self.user_data

            #Show the price
            print(final_price)

        except MyError as my:
            if my.error == "plan_not_exist":
                print(f"{my.error}. {my.value} is not in PacFlix plan list")
            elif my.error == "plan_isn't":
                print(f"Your {my.error} {my.value}. Your current plane is {self.user_data[0]}")
            elif my.error == "downgrade":
                print(f"Can't {my.error}. Your current plan is {my.value}")


class NewUser(User):
    def __init__(self, username):
        self.username = username
        super().__init__(username)
    
    def check_benefit(self):
        super().check_benefit()

    def pick_plan(self, new_plan, referral_code = ""):
        self.data_referral = [value[2] for username, value in self.user_database.items()]

        try:
            self.current_plan = new_plan

            #Check if the plan is correct
            if self.current_plan not in self.first_row[:3]:
                raise MyError(error = "new_plan", value = new_plan)
            
            #Check the existence of the referral code
            if referral_code not in self.data_referral:
                print(f"{referral_code} Referral code is not exist")
                discount = 0
            else:
                print(f"{referral_code} Referral code is exist")
                discount = 4/100
            
            #Get the index of the plan
            idx = self.first_row.index(new_plan)

            #Get the price from index of plan
            plan_price = self.price[idx]
            final_price = plan_price - (plan_price * discount)

            #Create referral code for new user
            token = secrets.token_hex(2)
            self.referral_code = self.username.lower() + "-" + token

            #Show the price
            print(final_price)
            print(f"This is your referral code = {self.referral_code}")

            #Update the duration of new user
            self.duration_plan += 1

            #Update the data of new user
            self.user_data = [self.current_plan, self.duration_plan, self.referral_code]
            self.user_database[self.username] = self.user_data

        except MyError as my:
            if my.error == "new_plan":
                print(f"{my.value} is not in PacFlix plan list")