from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from volunteers.models import v_user, advertisement
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout


def homepage(request):
    context = {}
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
    return render(request, "homepage.html", context)


def about(request):
    return render(request, "about.html", {})


def ads(request):
    queryset = advertisement.objects.all()
    # todo: sorting...
    context = {'ads': queryset}
    return render(request, "ads.html", context)


def leaderboard(request):
    context = {'users': v_user.objects.order_by("-score")}
    return render(request, "leaderboard.html", context)


def validate_user_creation(request):
    return True, User(username=request.POST['username'], email=request.POST['email'],
                      password=request.POST['password'], manager=('volunteer-manager' in request.POST))


def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            context['error'] = 'error'  # todo: handle errors
    return render(request, "login.html", context)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = v_user(username=request.POST['username'], score=0)
            user.save()
            return redirect('home')
    return render(request, 'register.html', {'form': form})
    # if request.method == 'POST':
    #     valid, user = validate_user_creation(request)
    #     if valid:
    #         user.save()
    #         return redirect('login')
    # return render(request, "register.html", {})


def validate_ad_creation(request):
    rp = request.POST
    all_day = ('allday' in request.POST)
    is_license = ('license_s' in request.POST)
    is_food = ('food' in request.POST)
    is_physical = ('physical_work' in request.POST)
    print(rp)
    if all_day:
        return True, advertisement(title=rp['title'], all_day=all_day, start_date=rp['w_start_s'],
                                   end_date=rp['w_end_s'], number_of_hours=rp['work_per_day_s'],
                                   is_license=is_license, is_food=is_food, is_physical=is_physical,
                                   location_street=rp['street'], location_number=rp['street_number'],
                                   location_city=rp['city'], description=rp['description'], author=request.user)
    else:
        return True, advertisement(title=rp['title'], all_day=all_day, one_day_date=rp['d_start_s'],
                                   start_time=rp['d_from_s'], end_time=rp['d_to_s'], is_license=is_license,
                                   is_food=is_food, is_physical=is_physical, location_street=rp['street'],
                                   location_number=rp['street_number'], location_city=rp['city'],
                                   description=rp['description'], author=request.user)


def new_ad(request):
    if request.method == 'POST':
        valid, ad = validate_ad_creation(request)
        if valid:
            ad.save()
            print("saved")
            return redirect('home')
    return render(request, "new_ad.html", {})


def calculate_points_complicated(total_hours, distance, periphery, prior_knowledge, is_license, language, food, group,
                                 physical):
    return (
                   50 * total_hours + 10 * distance + 30 * periphery + 30 * prior_knowledge + 30 * is_license + 30 * language + 30 * food + 30 * group) * (
                   1 + physical)


def calculate_points(total_hours, physical, is_license):
    return 30 * (1 + physical + is_license + total_hours)


def update_score(user, ad, hours):
    score = calculate_points(hours, 2, 3)  # ad.physical, ad.is_license)
    user.score += score
    user.save()


def submit_score(request):
    context = {}
    if request.user.is_authenticated:
        context['ads'] = advertisement.objects.all().filter(author=request.user)
    if request.method == 'POST':
        if v_user.objects.filter(username=request.POST['username']).exists():
            user = v_user.objects.get(username=request.POST['username'])
            ad = advertisement.objects.get(title=request.POST['ad'])
            hours = int(request.POST['hours'])
            update_score(user, ad, hours)
            return redirect('home')
    return render(request, "submit_score.html", context)
