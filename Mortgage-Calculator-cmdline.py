print("\n**** Welcome to the Amortization Calculator ****")

def amort_equation():
    pv = float(input('Enter the current loan amount: '))
    r = float(input('Enter the annual interest rate on the loan: '))
    n = int(input("Enter the number of years on the loan: "))
    r = (r / 100) / 12  # Convert annual interest rate to a monthly rate
    n = n * 12  # Convert loan duration in years to months
    return pv, r, n

def user_prompt(pv, r, n):
    home_insurance = 0.0
    mortgage_insurance = 0.0
    property_tax = 0.0
    known_payment = input('Do you know your monthly loan payment? (yes/no): ').lower()

    if known_payment == 'yes':
        p = float(input('Enter your total monthly payment (including taxes and insurance if applicable): '))
        if input('Do you pay home insurance? (yes/no): ').lower() == 'yes':
            home_insurance = float(input('Enter your monthly home insurance payment: '))
        if input('Do you pay mortgage insurance? (yes/no): ').lower() == 'yes':
            mortgage_insurance = float(input("Enter your monthly mortgage insurance payment: "))
        if input('Do you pay property taxes? (yes/no): ').lower() == 'yes':
            property_tax = float(input("Enter your monthly property tax payment: "))
        total_additional_costs = home_insurance + mortgage_insurance + property_tax
        
    else:
        if input('Do you know the approximate amount you will pay for home insurance? (yes/no): ').lower() == 'yes':
            home_insurance = float(input('Enter the approximate monthly payment for home insurance: '))
        if input('Will you be paying mortgage insurance? (yes/no): ').lower() == 'yes':
            mortgage_insurance = float(input("Enter the approximate monthly payment for mortgage insurance: "))
        if input('Do you know approximately how much your monthly property tax will be? (yes/no): ').lower() == 'yes':
            property_tax = float(input("Enter the approximate monthly payment for property tax: "))
        p = (r * pv) / (1 - (1 + r) ** -n)
        total_additional_costs = home_insurance + mortgage_insurance + property_tax
        p += total_additional_costs

    return p, total_additional_costs, known_payment

def known_or_unknown(known_payment, pv, r, p, total_additional_costs):
    if known_payment == "yes".lower():
        interest_payment = pv * r
        principal_payment = p - interest_payment - total_additional_costs
        new_balance = pv - principal_payment
        total_payment = p
        print(f"\tInterest Payment: {interest_payment:.2f}")
        print(f"\tPrincipal Payment: {principal_payment:.2f}")
        print(f"\tAdditional Costs: {total_additional_costs}")
        print(f"\tTotal monthly Payment: {total_payment:.2f}")
        print(f"\tNew Balance after Payment: {new_balance:.2f}")
    else:
        interest_payment = pv * r
        principal_payment = p - interest_payment - total_additional_costs
        new_balance = pv - principal_payment
        total_payment = interest_payment + principal_payment + total_additional_costs
        print(f"\tInterest Payment: {interest_payment:.2f}")
        print(f"\tPrincipal Payment: {principal_payment:.2f}")
        print(f"\tAdditional Costs: {total_additional_costs}")
        print(f"\tTotal monthly Payment: {total_payment:.2f}")
        print(f"\tNew Balance after Payment: {new_balance:.2f}")

def print_schedule(pv, r, p, total_additional_costs, n):
    table_activate = input("\nDo you want to see your amortization schedule for the loan? (yes/no): ").lower()
    if table_activate == "yes":
        extra_towards_principal = 0.0  # Initialize to zero for cases where no extra payment is made
        if input("Do you want to make an extra payment towards principal to see how early you can pay your loan off? (yes/no): ").lower() == "yes":
            extra_towards_principal = float(input("How much extra would you like to pay towards the principal each month? "))
        month = 1
        current_balance = pv
        while current_balance > 0:
            interest_payment = current_balance * r
            principal_payment = p - interest_payment - total_additional_costs + extra_towards_principal
            if principal_payment >= current_balance:
                principal_payment = current_balance
                current_balance = 0
            else:
                current_balance -= principal_payment
            print(f"Month {month}:")
            print(f"\tInterest Payment: {interest_payment:.2f}")
            print(f"\tPrincipal Payment: {principal_payment:.2f} (includes any extra payment)")
            print(f"\tRemaining Balance: {current_balance:.2f}")
            month += 1
            if current_balance == 0:
                print("Loan paid in full")
                years_to_payoff = month / 12
                print(f"# years to pay loan: {years_to_payoff:.2f}")
                break
            elif month > n:
                print("Error: Loan term exceeded without full payoff.")
                break

def main():
    pv, r, n = amort_equation()
    p, total_additional_costs, known_payment = user_prompt(pv, r, n)
    known_or_unknown(known_payment, pv, r, p, total_additional_costs)  # Corrected argument list
    print_schedule(pv, r, p, total_additional_costs, n)

main()
