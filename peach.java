import java.util.Scanner;
import java.util.ArrayList;

abstract class Account {
    protected String accountNumber;
    protected double balance;
    protected String accountType;

    public Account(String accountNumber, double balance, String accountType) {
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.accountType = accountType;
    }

    public abstract void displayInfo();
    public abstract void deposit(double amount);
    public abstract void withdraw(double amount);
}

class SavingsAccount extends Account {
    private static final double minBalance = 500.0;

    public SavingsAccount(String accountNumber, double balance) {
        super(accountNumber, balance, "Savings");
    }

    public void displayInfo() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Balance: " + balance);
        System.out.println("Account Type: " + accountType);
    }

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposited: " + amount);
    }

    public void withdraw(double amount) {
        if (balance - amount >= minBalance) {
            balance -= amount;
            System.out.println("Withdrawn: " + amount);
        } else {
            System.out.println("Insufficient balance. Minimum balance should be maintained.");
        }
    }
}

class CheckingAccount extends Account {
    private static final double overdraftLimit = 1000.0;
    private static final double fine = 100.0;
    private static final int finePeriodMonths = 4;
    private int monthsOverDrawn = 0;

    public CheckingAccount(String accountNumber, double balance) {
        super(accountNumber, balance, "Checking");
    }

    public void withdraw(double amount) {
        if (balance - amount >= -overdraftLimit) {
            balance -= amount;
            System.out.println("Withdrew: " + amount);
        } else {
            System.out.println("Amount exceeded overdraft limit.");
        }
    }

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposited " + amount + " in your bank account");
    }

    public void displayInfo() {
        System.out.println("Account number: " + accountNumber);
        System.out.println("Account Type: " + accountType);
        System.out.println("Account Balance: " + balance);
    }

    public void calculateFine() {
        monthsOverDrawn++;
        if (monthsOverDrawn % finePeriodMonths == 0) {
            balance -= fine;
            System.out.println("Fine of rupees " + fine + " has been applied");
        }
    }
}

class DepositAccount extends Account {
    private boolean internet;

    public DepositAccount(double balance, String accountNumber) {
        super(accountNumber, balance, "Deposit");
        internet = false;
    }

    public void displayInfo() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Balance: " + balance);
        System.out.println("Account Type: " + accountType);
        System.out.println("Internet Enabled: " + internet);
    }

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposited: " + amount);
    }

    public void withdraw(double amount) {
        System.out.println("Withdrawals are not allowed in deposit accounts.");
    }

    public void applyInternet() {
        this.internet = true;
        System.out.println("Internet banking enabled for Deposit Account");
    }
}

public class peach {
    static ArrayList<Account> accounts = new ArrayList<>();

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int choice = 0;
        boolean continueProgram = true;

        while (continueProgram) {
            System.out.println("Enter ");
            System.out.println("1 to create an account");
            System.out.println("2 to Display account info");
            System.out.println("3 to Deposit into account");
            System.out.println("4 to Withdraw from account");
            System.out.println("5 to Apply internet banking to deposit account");
            System.out.println("6 to calculate fine");
            System.out.println("Any other number to exit");
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    createAccount();
                    break;
                case 2:
                    displayInfo();
                    break;
                case 3:
                    deposit();
                    break;
                case 4:
                    withdraw();
                    break;
                case 5:
                    internetBanking();
                    break;
                case 6:
                    simulateCalculation();
                    break;
                default:
                    continueProgram = false; // Exit the loop
                    break;
            }
        }
    }

    public static void createAccount() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter account type (Savings, Deposit, Checking):");
        String choice = sc.next();
        System.out.println("Enter account Number:");
        String accountNumber = sc.next();
        System.out.println("Enter initial deposit:");
        double balance = sc.nextDouble();

        if (choice.equalsIgnoreCase("savings")) {
            accounts.add(new SavingsAccount(accountNumber, balance));
            System.out.println("Account created successfully");
        } else if (choice.equalsIgnoreCase("checking")) {
            accounts.add(new CheckingAccount(accountNumber, balance));
            System.out.println("Account created successfully");
        } else if (choice.equalsIgnoreCase("deposit")) {
            accounts.add(new DepositAccount(balance, accountNumber));
            System.out.println("Account created successfully");
        } else {
            System.out.println("Invalid input");
        }
    }

    public static void displayInfo() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter account number:");
        String accountNum = sc.next();

        for (Account ac : accounts) {
            if (ac.accountNumber.equals(accountNum)) {
                ac.displayInfo();
                return;
            }
        }
        System.out.println("No such account exists");
    }

    public static void deposit() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter Account Number: ");
        String number = sc.next();
        System.out.println("Enter Deposit Amount: ");
        double amount = sc.nextDouble();

        for (Account account : accounts) {
            if (account.accountNumber.equals(number)) {
                account.deposit(amount);
                return;
            }
        }
        System.out.println("Account not found.");
    }

    public static void withdraw() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter account number:");
        String accountNumber = sc.next();
        System.out.println("Enter the amount to withdraw:");
        double amount = sc.nextDouble();

        for (Account ac : accounts) {
            if (ac.accountNumber.equals(accountNumber)) {
                ac.withdraw(amount);
                return;
            }
        }
        System.out.println("Invalid account number entered");
    }

    public static void internetBanking() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter Account Number: ");
        String number = sc.next();
        for (Account ac : accounts) {
            if (ac.accountNumber.equals(number) && ac.accountType.equals("Deposit")) {
                ((DepositAccount) ac).applyInternet();
                return;
            }
        }
        System.out.println("Deposit Account not found.");
    }

    public static void simulateCalculation() {
        System.out.println("incoming");
        for (Account ac : accounts) {
            if (ac.accountType.equals("Checking")) {
                ((CheckingAccount) ac).calculateFine();
            }
        }
    }
}
