import tkinter as tk
from tkinter import messagebox

class AmortizationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Amortization Calculator")

        # Define variables
        self.pv = tk.DoubleVar()
        self.r = tk.DoubleVar()
        self.n = tk.IntVar()
        self.p = tk.DoubleVar()
        self.home_insurance = tk.DoubleVar(value=0.00)
        self.mortgage_insurance = tk.DoubleVar(value=0.00)
        self.property_tax = tk.DoubleVar(value=0.00)
        self.extra_towards_principal = tk.DoubleVar(value=0.00)
        self.known_payment = tk.StringVar(value="no")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Current Loan Amount:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.pv).grid(row=0, column=1)

        tk.Label(self.root, text="Annual Interest Rate (%):").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.r).grid(row=1, column=1)

        tk.Label(self.root, text="Number of Years:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.n).grid(row=2, column=1)

        tk.Label(self.root, text="Do you know your monthly loan payment? (yes/no)").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.known_payment).grid(row=3, column=1)

        tk.Button(self.root, text="Next", command=self.user_prompt).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Reset", command=self.reset_fields).grid(row=5, column=0, columnspan=2)

    def reset_fields(self):
        self.pv.set(0.00)
        self.r.set(0.00)
        self.n.set(0)
        self.p.set(0.00)
        self.home_insurance.set(0.00)
        self.mortgage_insurance.set(0.00)
        self.property_tax.set(0.00)
        self.extra_towards_principal.set(0.00)
        self.known_payment.set("no")

        for widget in self.root.winfo_children():
            try:
                if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
                elif isinstance(widget, tk.Entry) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
                elif isinstance(widget, tk.Button) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
            except KeyError:
                continue

        tk.Button(self.root, text="Next", command=self.user_prompt).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Reset", command=self.reset_fields).grid(row=5, column=0, columnspan=2)

    def user_prompt(self):
        pv = self.pv.get()
        r = (self.r.get() / 100) / 12
        n = self.n.get() * 12
        known_payment = self.known_payment.get().lower()

        for widget in self.root.winfo_children():
            try:
                if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
                elif isinstance(widget, tk.Entry) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
                elif isinstance(widget, tk.Button) and widget.grid_info()['row'] > 5:
                    widget.grid_forget()
            except KeyError:
                continue

        if known_payment == 'yes':
            self.create_known_payment_ui()
        else:
            self.create_unknown_payment_ui()

    def create_known_payment_ui(self):
        tk.Label(self.root, text="Total Monthly Payment:").grid(row=6, column=0)
        tk.Entry(self.root, textvariable=self.p).grid(row=6, column=1)

        tk.Label(self.root, text="Home Insurance (monthly):").grid(row=7, column=0)
        tk.Entry(self.root, textvariable=self.home_insurance).grid(row=7, column=1)

        tk.Label(self.root, text="Mortgage Insurance (monthly):").grid(row=8, column=0)
        tk.Entry(self.root, textvariable=self.mortgage_insurance).grid(row=8, column=1)

        tk.Label(self.root, text="Property Tax (monthly):").grid(row=9, column=0)
        tk.Entry(self.root, textvariable=self.property_tax).grid(row=9, column=1)

        tk.Label(self.root, text="Extra Payment Towards Principal (monthly):").grid(row=10, column=0)
        tk.Entry(self.root, textvariable=self.extra_towards_principal).grid(row=10, column=1)

        tk.Button(self.root, text="Calculate", command=self.calculate_known_payment).grid(row=11, column=0, columnspan=2)

    def create_unknown_payment_ui(self):
        tk.Label(self.root, text="Approximate Home Insurance (monthly):").grid(row=6, column=0)
        tk.Entry(self.root, textvariable=self.home_insurance).grid(row=6, column=1)

        tk.Label(self.root, text="Approximate Mortgage Insurance (monthly):").grid(row=7, column=0)
        tk.Entry(self.root, textvariable=self.mortgage_insurance).grid(row=7, column=1)

        tk.Label(self.root, text="Approximate Property Tax (monthly):").grid(row=8, column=0)
        tk.Entry(self.root, textvariable=self.property_tax).grid(row=8, column=1)

        tk.Label(self.root, text="Extra Payment Towards Principal (monthly):").grid(row=9, column=0)
        tk.Entry(self.root, textvariable=self.extra_towards_principal).grid(row=9, column=1)

        tk.Button(self.root, text="Calculate", command=self.calculate_unknown_payment).grid(row=10, column=0, columnspan=2)

    def calculate_known_payment(self):
        pv = self.pv.get()
        r = (self.r.get() / 100) / 12
        n = self.n.get() * 12
        p = self.p.get()
        home_insurance = self.home_insurance.get()
        mortgage_insurance = self.mortgage_insurance.get()
        property_tax = self.property_tax.get()
        total_additional_costs = home_insurance + mortgage_insurance + property_tax

        self.calculate_amortization_schedule(pv, r, n, p, total_additional_costs, known_payment=True)

    def calculate_unknown_payment(self):
        pv = self.pv.get()
        r = (self.r.get() / 100) / 12
        n = self.n.get() * 12
        home_insurance = self.home_insurance.get()
        mortgage_insurance = self.mortgage_insurance.get()
        property_tax = self.property_tax.get()
        total_additional_costs = home_insurance + mortgage_insurance + property_tax

        p = (r * pv) / (1 - (1 + r) ** -n)
        total_payment = p + total_additional_costs
        self.p.set(total_payment)
        self.calculate_amortization_schedule(pv, r, n, total_payment, total_additional_costs, known_payment=False)

    def calculate_amortization_schedule(self, pv, r, n, p, total_additional_costs, known_payment):
        extra_towards_principal = self.extra_towards_principal.get()
        if known_payment:
            interest_payment = pv * r
            principal_payment = p - interest_payment - total_additional_costs + extra_towards_principal
            new_balance = pv - principal_payment        
            
        else:
            interest_payment = pv * r
            principal_payment = p - interest_payment - total_additional_costs + extra_towards_principal
            new_balance = pv - principal_payment
            
        result = (
            f"Interest Payment: {interest_payment:.2f}\n"
            f"Principal Payment: {principal_payment:.2f}\n"
            f"Additional Costs: {total_additional_costs:.2f}\n"
            f"Total monthly Payment: {p:.2f} + {extra_towards_principal:.2f} (Extra Towards principal)\n"
            f"New Balance after Payment: {new_balance:.2f}"
        )

        messagebox.showinfo("Amortization Result", result)
        self.show_amortization_schedule(pv, r, p, total_additional_costs, n, extra_towards_principal)

    def show_amortization_schedule(self, pv, r, p, total_additional_costs, n, extra_towards_principal):
        if messagebox.askyesno("Amortization Schedule", "Do you want to see your amortization schedule?"):
            month = 1
            current_balance = pv
            schedule = ""
            total_cost = 0.0
            total_interest_paid = 0.0
            total_principal_paid = 0.0
            original_interest_paid = 0.0

            temp_balance = pv
            for _ in range(n):
                interest_payment = temp_balance * r
                principal_payment = p - interest_payment - total_additional_costs
                if temp_balance <= 0:
                    break
                temp_balance -= principal_payment
                original_interest_paid += interest_payment

            while current_balance > 0:
                interest_payment = current_balance * r
                principal_payment = p - interest_payment - total_additional_costs + extra_towards_principal
                total_payment = interest_payment + principal_payment + total_additional_costs  # Total monthly payment

                if principal_payment >= current_balance:
                    principal_payment = current_balance
                    current_balance = 0
                else:
                    current_balance -= principal_payment

                total_cost += total_payment
                total_interest_paid += interest_payment
                total_principal_paid += principal_payment

                if extra_towards_principal == 0:
                    original_interest_paid += interest_payment

                interest_ratio = (interest_payment / total_payment) * 100 #interest to payment ratio
                
                schedule += (
                    f"Month {month}:\n"
                    f"Interest Payment: {interest_payment:.2f} ({interest_ratio:.2f}% of payment)\n"
                    f"Principal Payment: {principal_payment:.2f} (includes any extra payment)\n"
                    f"Total Payment: {total_payment:.2f}\n"
                    f"Remaining Balance: {current_balance:.2f}\n\n"
                )

                month += 1
                if current_balance == 0:
                    schedule += "*****Loan Summary*****\n"
                    years_to_payoff = month / 12
                    schedule += f"\n^^Years to pay off loan: {years_to_payoff:.2f}^^"
                    break
                elif month > n:
                    schedule += "Error: Loan term exceeded without full payoff.\n"
                    break

            if extra_towards_principal > 0:
                interest_saved = original_interest_paid - total_interest_paid
                months_saved = n - month
                schedule += f"\n^^Extra Payments Reduced Loan Term by {months_saved} Months^^"
                schedule += f"\n^^Total Interest Saved: {interest_saved:.2f}^^"

            schedule += f"\n^^Total Interest Paid: {total_interest_paid:.2f}^^"
            schedule += f"\n^^Total Principal Paid: {total_principal_paid:.2f}^^\n"
            schedule += f"\n^^Total Cost of the Loan: {total_cost:.2f}^^\n"


            self.show_schedule_window(schedule)

    def show_schedule_window(self, schedule):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Amortization Schedule")

        text_widget = tk.Text(schedule_window, wrap='word')
        text_widget.insert('1.0', schedule)
        text_widget.config(state='disabled')

        scrollbar = tk.Scrollbar(schedule_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

def main():
    root = tk.Tk()
    app = AmortizationCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
