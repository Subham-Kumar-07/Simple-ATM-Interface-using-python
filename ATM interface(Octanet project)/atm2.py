import tkinter as tk
from tkinter import messagebox

# Simulated data store
accounts = {
    "savings": 1000,
    "current": 500
}

# Transaction history
transaction_history = []

# Dummy PIN for the example
correct_pin = "1234"

def login():
    pin = entry_pin.get()
    if pin == correct_pin:
        messagebox.showinfo("Login Success", "PIN accepted")
        login_window.destroy()
        open_atm_interface()
    else:
        messagebox.showerror("Login Failed", "Incorrect PIN")

def open_atm_interface():
    def handle_transaction(transaction):
        if transaction == "Withdraw Money":
            ask_pin_for_withdrawal()
        elif transaction == "Transaction History":
            display_transaction_history()
        else:
            open_transaction_window(transaction)

    def ask_pin_for_withdrawal():
        pin_window = tk.Toplevel(atm_window)
        pin_window.title("Enter PIN")
        pin_window.geometry("300x200")

        label = tk.Label(pin_window, text="Enter your PIN", font=("Arial", 12))
        label.pack(pady=10)

        entry_pin_withdraw = tk.Entry(pin_window, show="*", font=("Arial", 12))
        entry_pin_withdraw.pack(pady=5)

        def check_pin():
            pin = entry_pin_withdraw.get()
            if pin == correct_pin:
                messagebox.showinfo("PIN Accepted", "PIN accepted")
                pin_window.destroy()
                open_transaction_window("Withdraw Money")
            else:
                messagebox.showerror("Incorrect PIN", "Incorrect PIN")

        submit_button = tk.Button(pin_window, text="Submit", font=("Arial", 12), command=check_pin)
        submit_button.pack(pady=20)

    def open_transaction_window(transaction):
        transaction_window = tk.Toplevel(atm_window)
        transaction_window.title(transaction)
        transaction_window.geometry("300x300")

        if transaction == "Check Balance":
            label = tk.Label(transaction_window, text=f"Select Account to Check Balance", font=("Arial", 12))
            label.pack(pady=10)
        else:
            label = tk.Label(transaction_window, text=f"{transaction} Amount:", font=("Arial", 12))
            label.pack(pady=10)
            entry_amount = tk.Entry(transaction_window, font=("Arial", 12))
            entry_amount.pack(pady=5)

        account_var = tk.StringVar(value="savings")
        radio_savings = tk.Radiobutton(transaction_window, text="Savings", variable=account_var, value="savings", font=("Arial", 12))
        radio_savings.pack(pady=5)
        radio_checking = tk.Radiobutton(transaction_window, text="Current", variable=account_var, value="current", font=("Arial", 12))
        radio_checking.pack(pady=5)

        def submit():
            account_type = account_var.get()
            if transaction == "Check Balance":
                balance = accounts[account_type]
                messagebox.showinfo(transaction, f"Your {account_type} account balance is ${balance:.2f}")
                transaction_window.destroy()
                transaction_history.append(f"Checked balance of {account_type} account: ${balance:.2f}")
            else:
                amount = entry_amount.get()
                if amount:
                    amount = float(amount)
                    if transaction == "Withdraw Money":
                        if accounts[account_type] >= amount:
                            accounts[account_type] -= amount
                            messagebox.showinfo(transaction, f"${amount} withdrawn from your {account_type} account.")
                            transaction_history.append(f"Withdrew ${amount:.2f} from {account_type} account")
                        else:
                            messagebox.showerror(transaction, "Insufficient funds")
                    elif transaction == "Deposit Money":
                        accounts[account_type] += amount
                        messagebox.showinfo(transaction, f"${amount} deposited to your {account_type} account.")
                        transaction_history.append(f"Deposited ${amount:.2f} to {account_type} account")
                    transaction_window.destroy()
                else:
                    messagebox.showwarning(transaction, "Please enter an amount")

        submit_button = tk.Button(transaction_window, text="Submit", font=("Arial", 12), command=submit)
        submit_button.pack(pady=20)

    def display_transaction_history():
        history_window = tk.Toplevel(atm_window)
        history_window.title("Transaction History")
        history_window.geometry("400x300")

        if transaction_history:
            history_text = "\n".join(transaction_history)
        else:
            history_text = "No transactions yet."

        label = tk.Label(history_window, text=history_text, font=("Arial", 12), justify="left")
        label.pack(pady=10)

    def cancel_transaction():
        atm_window.destroy()

    atm_window = tk.Tk()
    atm_window.title("Bank of XYZ ATM")
    atm_window.geometry("400x500")

    label_title = tk.Label(atm_window, text="Available Transactions", font=("Arial", 18), fg="white", bg="red")
    label_title.pack(fill=tk.X)

    label_prompt = tk.Label(atm_window, text="Select your transaction.", font=("Arial", 14))
    label_prompt.pack(pady=20)

    buttons = [
        ("Withdraw Money", "blue"),
        ("Deposit Money", "gray"),
        ("Check Balance", "black"),
        ("Transaction History", "green"),
        ("Cancel", "red")
    ]

    for (text, color) in buttons:
        if text == "Cancel":
            button = tk.Button(atm_window, text=text, font=("Arial", 14), bg=color, fg="white", width=20, height=2, command=cancel_transaction)
        else:
            button = tk.Button(atm_window, text=text, font=("Arial", 14), bg=color, fg="white", width=20, height=2, command=lambda t=text: handle_transaction(t))
        button.pack(pady=5)

    atm_window.mainloop()

login_window = tk.Tk()
login_window.title("Bank of XYZ ATM Login")
login_window.geometry("400x300")

label_title = tk.Label(login_window, text="Bank of XYZ ATM Login", font=("Arial", 18), fg="white", bg="red")
label_title.pack(fill=tk.X)

label_card = tk.Label(login_window, text="Insert Card", font=("Arial", 14))
label_card.pack(pady=10)

# Simulate card insertion with a button
insert_card_button = tk.Button(login_window, text="Insert Card", font=("Arial", 12), command=lambda: messagebox.showinfo("Card Inserted", "Please enter your PIN"))
insert_card_button.pack(pady=5)

label_pin = tk.Label(login_window, text="Enter PIN", font=("Arial", 14))
label_pin.pack(pady=10)

entry_pin = tk.Entry(login_window, show="*", font=("Arial", 12))
entry_pin.pack(pady=5)

button_login = tk.Button(login_window, text="Login", font=("Arial", 14), bg="blue", fg="white", command=login)
button_login.pack(pady=20)

login_window.mainloop()
