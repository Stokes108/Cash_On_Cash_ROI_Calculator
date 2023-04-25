
#Created the mortgage parent class because I could then use this for other functions in a program 
# This is a simple mortgage calculator and the more complex ROI calculator inherits all of this data
#IT is not essential to have this class but it allows me to more eaisly expand my code in the future

#Example: I could add features like a total investment calcualtor for properties stocks etc 
# which will take a mortgage, but doesn't want or need the the rental income information

class Mortagage():
    base_interest_rate = 0.07153
    #I use a base_interest rate for houses in a similar neighborhood

    def __init__(self, price, down_payment, time_frame):
        self.price = price
        self.down_payment = down_payment
        self.time_frame = time_frame

    

    #Calculates the mortage rate based on time-frame of mortgage
    def mortgage_rate(self):
        if self.time_frame >= 20:
            return self.base_interest_rate
        elif self.time_frame < 20:
            return self.base_interest_rate - 0.01

    def loan_amount(self):
        return self.price - self.down_payment

    def find_mortage(self):
        total_payments = self.time_frame * 12
        loan = self.loan_amount()
        interest_rate = self.mortgage_rate() / 12

        payment_numerator = loan * (interest_rate * (interest_rate + 1) ** total_payments)
        payment_denominator = ((1 + interest_rate) ** total_payments) - 1 

        return payment_numerator // payment_denominator


class Rental_Property(Mortagage):
    tax_rate = 0.0253
    vacancy_rate = 0.05
    property_mangager_rate = 0.05
    capital_ex_rate = 0.03
    closing_percentage = 0.03
    insurance_percentage = 0.01
    utility_fees = 0.001
    repair_rate = 0.01


    def __init__(self, price, down_payment, time_frame, rental_income, rehab_budget, utility = False, lawn_care = 0, HOA = 0):
        super().__init__(price, down_payment, time_frame)
        self.rental_income = rental_income
        self.rehab_budget = rehab_budget
        self.utility = utility 
        self.lawn_care = lawn_care
        self.HOA = HOA

    def expenses(self):

        # Taxes and insurance are based on total price so have to divide it by 12 to get monthly 
        taxes = (self.tax_rate * self.price) / 12
        insurance = (self.insurance_percentage * self.price)/  12

        # Calculates the cost per month based on percentages for the neighborhood
        vacancy = self.vacancy_rate * self.rental_income 
        cap_ex = self.capital_ex_rate * self.rental_income
        repair_rate = self.repair_rate * self.rental_income
        property_mangager = self.property_mangager_rate * self.rental_income
        utility_cost = 0

        #Checks to see if we are paying utilities or renters
        if self.utility:
            utility_cost = self.utility_fees * self.rental_income
        
        #add all expenses together 
        total_expenses = (taxes + insurance + vacancy + cap_ex + repair_rate + property_mangager +
        utility_cost + self.HOA + self.lawn_care)

        return round(total_expenses)

    def cash_flow(self):
        return self.rental_income - self.expenses()

    def investment_cost(self):
        closing_cost = self.closing_percentage * self.loan_amount()
        total_investment = closing_cost + self.down_payment + self.rehab_budget
        return total_investment

    def cash_ROI(self):
        annual_cash_flow = self.cash_flow() * 12
        investment = self.investment_cost()
        cash_ROI = round(annual_cash_flow / self.investment_cost(), 4) * 100

        return cash_ROI


  
    #This class_method create object is used to create an instance of the class from a collection 
    #of data in a list or string or dictionary. It allows an object to be created from a dictionary 


    @classmethod
    def create_object(cls, dic):
        house_price = dic['house price']
        down_pay= dic['down payement'] 
        mortgage_time = dic['mortgage time(years)']
        rental_in = dic['rental income']
        rehab = dic['rehab budget']
        utilities = dic['utility']
        lawn = dic['lawn care']
        HOA = dic['HOA fees']

        rental = cls(house_price, down_pay, mortgage_time, rental_in, rehab, utilities, lawn, HOA)
        
        return rental


def find_input():
    user_flag = True
    input_dict = {'house price' : 0, 
                'down payement': 0, 
                'mortgage time(years)' : 0,
                'rental income' : 0,
                'rehab budget' : 0,
                'utility' : False,
                'lawn care' : 0, 
                'HOA fees' : 0,}

    while user_flag:
        print('\nWelcome to the Cash on Cash ROI calculator\nBefore you begin to invest we need to collect some information\n')

        for x in input_dict:
            if user_flag:
                if x != 'utility':

                    input_value = input(f'Please enter your {x}: ')
                    user_flag = verify_quit(input_value)
                    if input_value != 'quit':
                        input_value = verify_digit_input(input_value)
                        input_dict[x] = input_value

                else:
                    input_value = input("Will your renters pay the utilities (y/n): ")
                    input_value = verify_bool(input_value)
                    input_dict[x] = input_value

            
            
        if user_flag:
            current_rental = Rental_Property.create_object(input_dict)
            print(f'This is your calculated cash on cash ROI for the current property: {current_rental.cash_ROI()}')
            user_flag = verify_bool(input('Would you like to calculate another ROI? (y/n): '))

    if not user_flag:
        print('\nThank you for assessing with us! It was a pleasure I hope you make lots of money soon\n')


def verify_digit_input(value):
    value_flag = True
    while value_flag:
        if value.isdigit():
            value_flag = False
        else:
            value = input("You did not enter a digit please enter a number: ")
    return int(value)

def verify_bool(value):
    value_flag = True
    while value_flag:
        if value in 'yn':
            value_flag = False
        else:
            value = input("You did not enter y or n. Please choose again: ")
    return True if value == 'y' else False

def verify_quit(value):
    if value.lower().strip() == 'quit':
        return False
    else:
        return True



find_input()

rental_1 = Rental_Property(500000, 50000, 30, 2000, 30000 )
print(f'This is a test case for the default values in Rental_Property class Here is the ROI: {rental_1.cash_ROI()}')