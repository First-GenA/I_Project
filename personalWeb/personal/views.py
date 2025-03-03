from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BankInfo, Transactions, UserInfo
from .forms import Profile

# Create your views here.
def home(request):
    '''
    This is the default home function.
    Leads to the home/index page
    '''
    return render(request, 'index.html')

def deposit_withdrawal(request):
    '''
    Call the deposit function
    '''
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                ttype = request.POST['transaction']
                amount = request.POST['amount']
                bank = request.POST['bank']
                # convert to desired type
                ttype = str(ttype)
                amount = float(amount)
                bank = str(bank)
                print(f'amount: {amount} type: {ttype} bank: {bank}')
                if ttype == 'deposit':
                    print('deposit')
                    try:
                        Finance.deposit(request, amount, bank)
                        return redirect('/finances')
                    except Exception as e:
                        print(f'Function call error(deposit):=> {e}\n')
                    print('Function called')
                elif ttype == 'withdraw':
                    print('withdrawal')
                    try:
                        Finance.withdrawal(request, amount, bank)
                        return redirect('/finances')
                    except Exception as e:
                        print(f'Function call error(deposit):=> {e}\n')
                    print('Function called')
                else:
                    print('Select an info type brah.')
            else:
                messages.error(request, 'Login please.')
                return redirect('/login')
        else:
            # Show the page
            return render(request, 'finances/deposit.html')
    except Exception as e:
        print(f'Information error:-> {e}')
    return render(request, 'finances/deposit.html')

def generic(request):
    '''
    The generic function reirect
    Handles user finances options
    '''
    return render(request, 'generic.html')

def elements(request):
    '''
    The elements
    '''
    return render(request, 'elements.html')

class UserInformation:
    '''
    Handles user authentication and registration
    Handles storage of user info
    '''

    def login_user(request):
        '''
        The login function. Called on user login
        Can redirects to register
        '''
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            #authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to the home page
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('/login')
            
        return render(request, 'login.html')
    
    def register(request):
        '''
        The register function. Called on register.
        '''
        if request.method == 'POST':
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            # TODO: validate user input
            # create the user
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, 'User created successfully')
                # update the profile
                UserInfo.objects.filter(user=user).update_or_create(user=user, u_name=username)
                print('Profile updated')
                return redirect('/login')
            except Exception as e:
                print(f'Verification error:-> {e}')
                messages.error(request, 'Username already exists')
                return redirect('/registration')
        else:
            return render(request, 'registration.html')
    
    def profile(request):
        '''
        Allow user to edit their details and also display them
        '''
        if request.user.is_authenticated:
            # get current user
            user = User.objects.get(id=request.user.id)
            user_info = UserInfo.objects.get(user=user)
            if request.method == 'POST':
                # update the profile database(userinfo)
                form = Profile(request.POST, request.FILES, instance=user_info)
                if form.is_valid():
                    form.save()
                    try:
                        name = form['u_name'].value()  # get form username
                        User.objects.filter(id=request.user.id).update(username=name)  # update username in user data table
                    except Exception as e:
                        print(f'Username update error:=> {e}')

                    messages.success(request, 'Profile updated successfully')
                    return redirect('/profile')
                else:
                    messages.error(request, 'Form submission Error')
                    # reload the form
                    return redirect('/profile')
            else:
                # display the available user details
                form = Profile(instance=user_info)
                image = UserInfo.objects.get(user=user)
                return render(request, 'profile.html', {'form': form, 'image': image})
        else:
            messages.error(request, 'You are not logged in')
            return redirect('/login')
         
    def user_logout(request):
        '''
        Logout the user
        '''
        logout(request)
        return redirect('/')
    
class Finance:
    '''
    Finance operations of the user
    Bank transactions and history
    '''
    def finances(request):
        '''
        load the default finaces web template'
        show finance overview
        '''
        if request.user.is_authenticated:
            try:
                # get current user
                user = User.objects.get(id=request.user.id)
                userinfo = UserInfo.objects.get(user=user)
                # get user bank information
                bankbal = BankInfo.objects.values().filter(b_user=user)
                # get all transactions by the user ordered from the latest
                transactioninfo = Transactions.objects.all().filter(t_owner=userinfo).order_by('-t_creation')
            except Exception as e:
                print(f'Banking detail error:-> {e}')
            
            return render(request, 'finances/finances.html', {'finances': transactioninfo, 'balance': bankbal})
        
        else:
            messages.error(request, 'You are not logged in')
            return redirect('/login')
    
    def deposit(request, amount, bank):
        '''
        tracks bank deposits or withdrawals
        opens a gui window to collect necessary data from user
        '''
        # get user account and info
        try:
            user = User.objects.get(id=request.user.id)  # current user
            bankinfo = BankInfo.objects.filter(b_name=bank).get(b_user=user)
            userinfo = UserInfo.objects.get(user=user)
            transactionamount = amount
            print(f'user: {user}\n bankinfo: {bankinfo}\n userinfo: {userinfo}\n')
            # update the bank balance
            try:
                if float(amount) >= 0:
                    amount = float(amount) + bankinfo.b_balance
                    print(f'Amount:= {amount}')
                    BankInfo.objects.filter(b_user=user, b_name=bank).update(b_balance=amount)
                    print(f'bank updated')
                    Transactions.objects.update_or_create(t_amount=transactionamount, t_type='deposit', t_bank=bankinfo, t_owner=userinfo)
                    print(f'Transactions updated')
                    messages.success(request, 'deposit has been made')
                else:
                    messages.error(request, 'Your deposit amount is below the minimum amount.(0)')
            except Exception as e:
                print(f'Banking error:= {e}')
                # messages.error(request, 'Deposit denied. Check your banking information.')
        except Exception as e:
            messages.success(request, 'deposit has not been made. Check your banking information.')
            print(f'User info error:=> {e}')
        
    def withdrawal(request, amount, bank):
        '''
        Withdraw money
        '''
        # get user account and info
        try:
            user = User.objects.get(id=request.user.id)  # current user
            bankinfo = BankInfo.objects.filter(b_name=bank).get(b_user=user)
            userinfo = UserInfo.objects.get(user=user)
            transactionamount = amount
            print(f'user: {user}\n bankinfo: {bankinfo}\n userinfo: {userinfo}\n')
            # update the bank balance
            try:
                if bankinfo.b_balance >= 0 and float(amount) <= bankinfo.b_balance:
                    amount = bankinfo.b_balance - float(amount)
                    print(f'Amount:= {amount}')
                    BankInfo.objects.filter(b_user=user, b_name=bank).update(b_balance=amount)
                    print(f'bank updated')
                    Transactions.objects.update_or_create(t_amount=transactionamount, t_type='withdrawal', t_bank=bankinfo, t_owner=userinfo)
                    print(f'Transactions updated')
                    messages.success(request, 'withdrawal has been made')
                else:
                    messages.error(request, 'Your bank balance is below the requested amount.')
            except Exception as e:
                print(f'Bank update error')
                # messages.error(request, 'Withdrawal denied. Check your banking information.')
        except Exception as e:
            print(f'User info error:=> {e}')
            messages.error(request, 'Withdrawal denied! Check your banking information.')

    def bank_registration(request):
        '''
        Register a new bank
        A deposit must be made
        '''
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            bankname = request.POST['bank']
            bankbalance = request.POST['amount']
            banks = BankInfo.objects.filter(b_name=bankname, b_user=user).values()
            print(f'User->{user}\nBank=>{bankname}\nBalance->{bankbalance}\nBanks=>{banks}')
            if banks:
                messages.info(request, 'Bank already exists') 
            else:
                # create a new bank account
                try:
                    BankInfo.objects.create(b_name=bankname, b_balance=bankbalance, b_user=user)
                    print(f'Bank account created')
                    messages.success(request, 'Bank registered')
                except Exception as e:
                    print(f'Bank update error:-> {e}')
            return redirect('/finances')
        else:
            return render(request, 'finances/bankreg.html', {})
    
    def history(request):
        '''
        Plots a graph of the users spending habits
        '''
        return render(request, 'Finances/finances.html')
        