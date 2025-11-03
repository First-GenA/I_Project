from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.urls import resolve
from .models import BankInfo, Transactions, UserInfo
from .forms import Profile
import lichess.api
from lichess.format import JSON, PGN
import json
from .models import BankInfo, Transactions, UserInfo
from .forms import Profile
import lichess.api


# Create your views here.
class Default:
    @staticmethod
    def home(request): # type: ignore
        """
        This is the default home function.
        Leads to the home/index page
        """
        context = {}
        if request.method == 'POST':
            if 0 == 0:
                address = request.POST.get('email')
                subject = request.POST.get('username')
                message = request.POST.get('message')
                print(f'address:=>{address} subject:=>{subject} message:=>{message} name:=>{request.POST.get("name")}')
                subject = request.POST.get('usename')
                message = request.POST.get('message')
                print(f"address:=>{address} subject:=>{subject} message:=>{message} name:=>{request.POST.get('name')}")
                # validate user input
                if address and subject and message:
                    try:
                        # send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                        send_mail(subject, message, address, [
                            settings.EMAIL_HOST_USER])  # note: django uses the set email backend as user does not
                        # give auth details
                        send_mail("Email received",
                                  "Your feedback was received and will be acted upon within 48hrs. Thankyou for your "
                                  "feedback.",
                                  settings.EMAIL_HOST_USER, [address])
                        send_mail(subject, message, address, [
                            settings.EMAIL_HOST_USER])
                        # note: django uses the set email backend as user does not give auth details
                        send_mail(
                            "Email received", "Your feedback was received and will be acted upon within 48hrs."
                                              " Thankyou for your feedback.", settings.EMAIL_HOST_USER, [address])
                        context['result'] = 'Email sent successfully'
                    except Exception as e:
                        context['result'] = f'Error sending email:=> {e}'
                else:
                    context['result'] = 'All fields are required'

        return render(request, 'index.html', context)

    @staticmethod
    def lichess(request):
        try:
            context = {}
            result = {}

            if request.method == 'POST':
                username = request.POST.get('username')
                format = request.POST.get('gameType')
                # test above values for correct entry
                print(f'username:=> {username} format:=> {format}')
                results = LichessScraper.fetch_recent_games(username, format),
                """try:
                    result = LichessScraper.fetch_recent_games(username, format)
                except Exception as e:
                    print(f'Error lichess:=>{e}')"""

                context.update({'username': username, 'format': format})
                return render(request, 'commercial/scraper.html', {'context': context,
                                                                   'results': results, })
            else:
                return render(request, 'commercial/scraper.html', {})
        except Exception as e:
            print(f"Error:=> {e}")
        return render(request, 'index.html', {})


class Commerce:
    @staticmethod
    def default(request):
        return render(request, 'commercial/commerce.html', {})


def deposit_withdrawal(request):
    """
    Call the deposit function
    """
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
                    print('Select an info type.')
            else:
                messages.error(request, 'Login please.')
                return redirect('/login')
        else:
            # Show the page
            return render(request, 'finances/deposit.html')
    except Exception as e:
        print(f'Information error: -> {e}')
    return render(request, 'finances/deposit.html')


def generic(request):
    """
    The generic function redirect
    Handles user finances options
    """
    return render(request, 'generic.html')


def elements(request):
    """
    The elements
    """
    return render(request, 'elements.html')


class UserInformation:
    """
    Handles user authentication and registration
    Handles storage of user info
    """

    @staticmethod
    def login_user(request):
        """
        The login function. Called on user login
        Can redirect to register
        """

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            # authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None and User.objects.exists():
                login(request, user)
                # redirect to the home page
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'errors/404.html', {})

        return render(request, 'login.html')

    @staticmethod
    def register(request):
        """
        The register function. Called on register.
        """
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
                print(f'Verification error: -> {e}')
                messages.error(request, 'Username already exists')
                return redirect('/registration')
        else:
            return render(request, 'registration.html')

    @staticmethod
    def profile(request):
        """
        Allow user to edit their details and also display them
        """
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
                        User.objects.filter(id=request.user.id).update(
                            username=name)  # update username in user data table
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
                try:
                    image = UserInfo.objects.get(user=user)
                except Exception as e:
                    print(f'Image retrieval error:=> {e}')
                    image = None
                return render(request, 'profile.html', {'form': form, 'image': image})
        else:
            messages.error(request, 'You are not logged in')
            return redirect('/login')

    @staticmethod
    def user_logout(request):
        """
        Logout the user
        """
        logout(request)
        return redirect('/')


class Finance:
    """
    Finance operations of the user
    Bank transactions and history
    """

    @staticmethod
    def finances(request):
        """
        load the default finances web template
        show finance overview
        """
        if request.user.is_authenticated:
            transactionInfo = None
            bankBal = None
            try:
                # get current user
                user = User.objects.get(id=request.user.id)
                userinfo = UserInfo.objects.get(user=user)
                # get user bank information
                bankBal = BankInfo.objects.values().filter(b_user=user)
                # get all transactions by the user ordered from the latest
                transactionInfo = Transactions.objects.all().filter(t_owner=userinfo).order_by('-t_creation')
            except Exception as e:
                print(f'Banking detail error: -> {e}')

            return render(request, 'finances/finances.html', {'finances': transactionInfo, 'balance': bankBal})

        else:
            messages.error(request, 'You are not logged in')
            return redirect('/login')

    @staticmethod
    def deposit(request, amount, bank):
        """
        tracks bank deposits or withdrawals
        opens a gui window to collect necessary data from user
        """
        # get user account and info
        try:
            user = User.objects.get(id=request.user.id)  # current user
            bankinfo = BankInfo.objects.filter(b_name=bank).get(b_user=user)
            userinfo = UserInfo.objects.get(user=user)
            transactionAmount = amount
            print(f'user: {user}\n bankinfo: {bankinfo}\n userinfo: {userinfo}\n')
            # update the bank balance
            try:
                if float(amount) >= 0:
                    amount = float(amount) + bankinfo.b_balance
                    print(f'Amount:= {amount}')
                    BankInfo.objects.filter(b_user=user, b_name=bank).update(b_balance=amount)
                    print(f'bank updated')
                    Transactions.objects.update_or_create(t_amount=transactionAmount, t_type='deposit', t_bank=bankinfo,
                                                          t_owner=userinfo)
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

    @staticmethod
    def withdrawal(request, amount, bank):
        """
        Withdraw money
        """
        # get user account and info
        try:
            user = User.objects.get(id=request.user.id)  # current user
            bankinfo = BankInfo.objects.filter(b_name=bank).get(b_user=user)
            userinfo = UserInfo.objects.get(user=user)
            transactionAmount = amount
            print(f'user: {user}\n bankinfo: {bankinfo}\n userinfo: {userinfo}\n')
            # update the bank balance
            try:
                if bankinfo.b_balance >= 0 and float(amount) <= bankinfo.b_balance:
                    amount = bankinfo.b_balance - float(amount)
                    print(f'Amount:= {amount}')
                    BankInfo.objects.filter(b_user=user, b_name=bank).update(b_balance=amount)
                    print(f'bank updated')
                    Transactions.objects.update_or_create(t_amount=transactionAmount, t_type='withdrawal',
                                                          t_bank=bankinfo, t_owner=userinfo)
                    print(f'Transactions updated')
                    messages.success(request, 'withdrawal has been made')
                else:
                    messages.error(request, 'Your bank balance is below the requested amount.')
            except Exception as e:
                print(f'Bank update error: -> {e}')
                # messages.error(request, 'Withdrawal denied. Check your banking information.')
        except Exception as e:
            print(f'User info error:=> {e}')
            messages.error(request, 'Withdrawal denied! Check your banking information.')

    @staticmethod
    def bank_registration(request):
        """
        Register a new bank
        A deposit must be made
        """
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            bankName = request.POST['bank']
            bankBalance = request.POST['amount']
            banks = BankInfo.objects.filter(b_name=bankName, b_user=user).values()
            print(f'User->{user}\nBank=>{bankName}\nBalance->{bankBalance}\nBanks=>{banks}')
            if banks:
                messages.info(request, 'Bank already exists')
            else:
                # create a new bank account
                try:
                    BankInfo.objects.create(b_name=bankName, b_balance=bankBalance, b_user=user)
                    print(f'Bank account created')
                    messages.success(request, 'Bank registered')
                except Exception as e:
                    print(f'Bank update error: -> {e}')
            return redirect('/finances')
        else:
            return render(request, 'finances/bankreg.html', {})

    @staticmethod
    def history(request):
        """
        Plots a graph of the users spending habits
        """
        return render(request, 'Finances/finances.html')


class LichessScraper:
    """
    Scrapes Lichess.org for user data and information
    """

    def __init__(self):
        pass
        # Steps:-
        # generate form, get username
        #  game history from lichess
        # return data as dictionary


    def fetch_recent_games(username, format):
        """
        get the user's most recent games from lichess
        """
        games = []
        try:
            raw_games_data = lichess.api.user_games(username, max=20, perftype=format, as_format=JSON)
            for data in raw_games_data:
                games.append(data)
            return games
        except Exception as e:
            print(f"Error fetching games:=> {e}")
            return []


class Gambling(View):
    """
    The gambling function class
    Handles all the gambling functions
    """

    @staticmethod
    def get(request):
        # get the link url
        resolver_match = request.resolver_match
        # set the link url to a variable
        current_url = resolver_match.url_name
        # check the url names
        if current_url == 'slips':
            return render(request, 'commercial/betslips.html', {})
        elif current_url == 'bets':
            return render(request, 'commercial/betsl.html', {})
        else:
            return render(request, 'commercial/commerce.html', {})

    @staticmethod
    def post(request):
        selection = request.POST.get('team')  # get the selected team prediction
        context = {
            'selection': selection
        }
        match selection:
            case 'Home':
                print(f'Selected {selection}')
            case 'Draw':
                print(f'Selected {selection}')
            case 'Away':
                print(f'Selected {selection}')
            case _:  # default case
                print(f'Enter a valid value {selection}')
        return render(request, 'commercial/betslips.html', context=context)
