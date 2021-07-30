import json
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from django.conf import settings
from .models import Restaurantdata
from userauthen.models import CustomUser
from django.db import connection
from django.core.paginator import Paginator
from django.db.models import Q
from userauthen.models import history
from django.db import connection
from django.http import JsonResponse
import json
# Create your views here.


def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


def browseRest(request):
    user = CustomUser.objects.get(username=request.user.username)
    localities = Restaurantdata.objects.values(
        'city', 'cluster_label').distinct()
    print(len(localities))
    cluster = 0
    for local in localities:
        if(user.locality == local['city']):
            cluster = local['cluster_label']
            break
    print(cluster)
    qs = Restaurantdata.objects.filter(cluster_label=cluster)
    filtered_name_query = request.GET.get('name')
    print(filtered_name_query)
    if filtered_name_query != '' and filtered_name_query is not None:

        qs = qs.filter(Q(name__icontains=filtered_name_query) |
                       Q(cuisines__icontains=filtered_name_query))
    sortmethod = request.GET.get('sortmethod')
    if sortmethod == 'cost':
        qs = qs.order_by('-cost')
    elif sortmethod == 'rate':
        qs = qs.order_by('-rate')
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'restdata': page_obj}
    return render(request, 'browse.html', context)


def recommender_page(request):
    # Receive data from clien
    user = CustomUser.objects.get(username=request.user.username)
    histlist = history.objects.filter(customer_id=user.id).order_by('-id')[0]
    print(histlist)
    name = Restaurantdata.objects.get(id=histlist.restname_id).name
    # dataset_path = os.path.join(settings.STATIC_ROOT, 'zomato_final.csv')
    db_query = str(Restaurantdata.objects.all().query)
    zomato = pd.read_sql_query(db_query, connection)
    df_percent = zomato.sample(frac=0.5)
    df_percent.set_index('name', inplace=True)
    indices = pd.Series(df_percent.index)
   # cos_path = os.path.join(settings.STATIC_ROOT, 'cosine_similarities.pickle')
    cosine_similarities = pd.read_pickle(
        "D:/minor project/django_restaurant/restaurant/restrecommender/static/restrecommender/cosine_similarities.pickle")
    recommend_restaurant = []
    idx = indices[indices == name].index[0]
    score_series = pd.Series(
        cosine_similarities[idx]).sort_values(ascending=False)
    top30_indexes = list(score_series.iloc[0:31].index)
    print(len(top30_indexes))
    localities = Restaurantdata.objects.values(
        'city', 'cluster_label').distinct()
    print(len(localities))
    cluster = 0
    for local in localities:
        if(user.locality == local['city']):
            cluster = local['cluster_label']
            break
    print(cluster)
    for each in top30_indexes:
        recommend_restaurant.append(list(df_percent.index)[each])

    df_new = pd.DataFrame(
        columns=['cuisines', 'Mean Rating', 'cost', 'Cluster Label', 'city'])

    for each in recommend_restaurant:
        df_new = df_new.append(pd.DataFrame(df_percent[[
                               'cuisines', 'Mean Rating', 'cost', 'Cluster Label', 'city']][df_percent.index == each].sample()))

    df_new = df_new.drop_duplicates(
        subset=['cuisines', 'Mean Rating', 'cost', 'Cluster Label', 'city'], keep=False)
    df_new = df_new.sort_values(by='Mean Rating', ascending=False).head(30)
    print(user.locality)
    df_new = df_new[df_new['Cluster Label'] == cluster]
    print(df_new)
    df_new['name'] = df_new.index
    df_new.rename(columns={"Mean Rating": "rating"}, inplace=True)
    cont = df_new.to_dict('records')
    context = {'restdata': cont, 'lastvisited': name}
    return render(request, 'recommender_page.html', context)


def profile(request):
    username = CustomUser.objects.get(username=request.user.username)
    hist = history.objects.filter(customer=username)
    print(hist.values())
    restlist = []
    for x in hist:
        restlist.append(x.restname_id)
    print(restlist)
    restdata = Restaurantdata.objects.filter(id__in=restlist)
    print(restdata.values())
    context = {'list': hist, 'restdata': restdata}
    return render(request, 'profile.html', context)


def updateItem(request):
    data = json.loads(request.body)
    restid = data['restid']
    action = data['action']
    print('Action:', action)
    print('Restaurant ID:', restid)
    customer = request.user.id
    order, created = history.objects.get_or_create(
        customer_id=customer, restname_id=restid)
    order.save()
    if(created):
        return JsonResponse('Succesfully Marked as Visited', safe=False)
    else:
        return JsonResponse('Restaurant Already Visited', safe=False)
