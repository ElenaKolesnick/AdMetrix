import io
import json
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db.models import Sum, F, Avg, Max, Min, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

from .models import GameMarketingData, UserProfile
from .forms import ProfileUpdateForm, CSVImportForm

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def get_quarter_label(date_obj):
    if not date_obj: return "N/A"
    quarter = (date_obj.month - 1) // 3 + 1
    return f"Q{quarter} {date_obj.year}"

def predict_future_revenue(queryset, total_spend, total_installs):
    """
    Гибридный движок прогнозирования. 
    1. Пробует LinearRegression.
    2. Если данных мало/они плохие — использует средний LTV.
    """
    try:
        # Принудительно приводим к float для расчетов
        ts = float(total_spend or 0)
        ti = float(total_installs or 0)
        
        if ts <= 0: 
            print(">>> ML Debug: Траты равны 0, прогноз невозможен")
            return 0.0
            
        data = list(queryset.values('spend', 'installs', 'iap_revenue', 'ad_revenue'))
        X, y = [], []
        
        for d in data:
            s = float(d['spend'] or 0)
            i = float(d['installs'] or 0)
            r = float(d['iap_revenue'] or 0) + float(d['ad_revenue'] or 0)
            X.append([s, i])
            y.append(r)

        # МЕТОД 1: Линейная регрессия (если данных много и они разные)
        if len(X) > 10:
            try:
                model = LinearRegression().fit(np.array(X), np.array(y))
                prediction = model.predict(np.array([[ts * 1.1, ti * 1.1]]))
                res = float(prediction[0])
                if res > 0: 
                    print(f">>> ML Debug: Прогноз по регрессии: {res}")
                    return round(res, 2)
            except:
                pass

        # МЕТОД 2: Финансовый (Средний ROAS + 10%)
        total_rev = sum(y)
        if ts > 0:
            current_roas = total_rev / ts
            # Прогнозируем доход, если бюджет вырастет на 10%
            prediction = (ts * 1.1) * current_roas
            print(f">>> ML Debug: Прогноз по ROAS: {prediction}")
            return round(prediction, 2)
            
        return 0.0
    except Exception as e:
        print(f">>> ML Debug: Критическая ошибка прогноза: {e}")
        return 0.0

# --- АВТОРИЗАЦИЯ ---

def home_page(request):
    if request.user.is_authenticated: return redirect('dashboard_index')
    return render(request, 'homepage.html')

def login_page(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard_index')
    return render(request, 'login.html', {'form': form})

def register_page(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if not hasattr(user, 'profile'): UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('dashboard_index')
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request); return redirect('homepage')

# --- ИМПОРТ ---

@login_required
def import_page(request):
    form = CSVImportForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        uploaded_file = request.FILES['csv_file']
        try:
            if uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                content = uploaded_file.read().decode('utf-8-sig', errors='ignore')
                df = pd.read_csv(io.StringIO(content), sep=None, engine='python')

            df.columns = [str(c).strip().lower() for c in df.columns]

            maps = {
                'date': ['date', 'дата', 'day'],
                'spend': ['spend', 'cost', 'затраты'],
                'iap': ['iap_revenue', 'revenue', 'выручка'],
                'ad': ['ad_revenue', 'ad', 'ads'],
                'inst': ['installs', 'установки', 'inst'],
                'geo': ['country', 'страна', 'geo'],
                'ch': ['channel', 'канал', 'source'],
                'os': ['platform', 'os']
            }

            def get_c(key):
                for name in maps[key]:
                    if name in df.columns: return name
                return None

            c_date, c_spend = get_c('date'), get_c('spend')
            c_iap, c_inst = get_c('iap'), get_c('inst')
            c_ad, c_geo, c_ch, c_os = get_c('ad'), get_c('geo'), get_c('ch'), get_c('os')

            if not all([c_date, c_spend, c_iap, c_inst]):
                messages.error(request, "Колонки не найдены.")
                return render(request, 'import.html', {'form': form})

            GameMarketingData.objects.filter(user=request.user).delete()
            
            new_objs = []
            for _, row in df.iterrows():
                try:
                    def clean_f(val):
                        v = str(val).replace(',', '.').replace('$', '').replace(' ', '').strip()
                        return float(v) if v and v != 'nan' else 0.0
                    
                    s = clean_f(row[c_spend])
                    iap = clean_f(row[c_iap])
                    ad = clean_f(row[c_ad]) if c_ad else 0.0
                    ins = int(float(str(row[c_inst]).strip() or 0))
                    
                    if ins <= 0 and s <= 0: continue

                    new_objs.append(GameMarketingData(
                        user=request.user,
                        date=pd.to_datetime(row[c_date]).date(),
                        spend=s, iap_revenue=iap, ad_revenue=ad, installs=ins,
                        channel=str(row.get(c_ch, 'Organic')),
                        country=str(row.get(c_geo, 'US')).upper()[:3],
                        os=str(row.get(c_os, 'All')),
                        cpi=s/ins if ins > 0 else 0,
                        ltv=(iap+ad)/ins if ins > 0 else 0,
                        roas=(iap+ad)/s if s > 0 else 0
                    ))
                except: continue

            if new_objs:
                GameMarketingData.objects.bulk_create(new_objs)
                messages.success(request, f"Загружено {len(new_objs)} записей.")
                return redirect('report')

        except Exception as e:
            messages.error(request, f"Ошибка: {e}")

    return render(request, 'import.html', {'form': form})

# --- ОТЧЕТЫ (REPORT) ---

@login_required
@never_cache
def report_page(request):
    total_stats = {'t_spend': 0, 't_installs': 0, 't_rev': 0, 'avg_cpi': 0, 'avg_ltv': 0, 'max_date': None}
    predicted_rev, roi_trend, cpi_trend, ltv_trend = 0.0, [], [], []
    map_json, line_json = '{}', '{}'
    
    qs = GameMarketingData.objects.filter(user=request.user).order_by('date')
    
    # Фильтрация
    ch_filter = request.GET.get('channel')
    if ch_filter: 
        qs = qs.filter(channel=ch_filter)

    if qs.exists():
        res = qs.aggregate(
            t_spend=Sum('spend'), 
            t_installs=Sum('installs'),
            t_rev=Sum(F('iap_revenue') + Coalesce(F('ad_revenue'), Value(0.0))),
            max_d=Max('date'), a_cpi=Avg('cpi'), a_ltv=Avg('ltv')
        )
        total_stats = {
            't_spend': float(res['t_spend'] or 0), 
            't_installs': float(res['t_installs'] or 0),
            't_rev': float(res['t_rev'] or 0), 
            'avg_cpi': float(res['a_cpi'] or 0),
            'avg_ltv': float(res['a_ltv'] or 0), 
            'max_date': res['max_d']
        }
        
        # Тренды для графиков
        daily = qs.values('date').annotate(
            s=Sum('spend'), 
            r=Sum(F('iap_revenue') + Coalesce(F('ad_revenue'), Value(0.0))), 
            i=Sum('installs')
        ).order_by('date')
        
        roi_trend = [round((d['r']/d['s']*100),1) if d['s'] > 0 else 0 for d in daily][-14:]
        cpi_trend = [round(d['s']/d['i'],2) if d['i'] > 0 else 0 for d in daily][-14:]
        ltv_trend = [round(d['r']/d['i'],2) if d['i'] > 0 else 0 for d in daily][-14:]
        
        # --- ВЫЗОВ ML ---
        predicted_rev = predict_future_revenue(qs, total_stats['t_spend'], total_stats['t_installs'])
        
        # Plotly
        df = pd.DataFrame(list(qs.values('date', 'country', 'spend', 'installs', 'iap_revenue', 'ad_revenue')))
        if not df.empty:
            df['rev'] = df['iap_revenue'].fillna(0) + df['ad_revenue'].fillna(0)
            fig_map = px.choropleth(df.groupby('country')['installs'].sum().reset_index(), locations="country", color="installs", template="plotly_white")
            map_json = fig_map.to_json()
            daily_df = df.groupby('date')[['spend', 'rev']].sum().reset_index()
            fig_line = px.line(daily_df, x='date', y=['spend', 'rev'], template="plotly_white")
            line_json = fig_line.to_json()

    paginator = Paginator(qs.order_by('-date'), 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'channels': GameMarketingData.objects.filter(user=request.user).values_list('channel', flat=True).distinct(),
        'map_json': map_json, 'line_json': line_json, 
        'predicted_rev': predicted_rev,
        'current_period': get_quarter_label(total_stats['max_date']),
        'total_stats': total_stats, 
        'roi_trend': roi_trend, 'cpi_trend': cpi_trend, 'ltv_trend': ltv_trend,
    }
    return render(request, 'report.html', context)

@login_required
def index_page(request):
    qs = GameMarketingData.objects.filter(user=request.user)
    stats = qs.aggregate(
        ti=Coalesce(Sum('installs'), Value(0)),
        ts=Coalesce(Sum('spend'), Value(0.0)),
        tr=Coalesce(Sum(F('iap_revenue') + Coalesce(F('ad_revenue'), Value(0.0))), Value(0.0))
    )
    context = {
        'total_installs': stats['ti'],
        'total_spend': round(stats['ts'], 2),
        'roas': round((stats['tr']/stats['ts']*100), 1) if stats['ts'] > 0 else 0,
        'recent_data': qs.order_by('-date')[:10]
    }
    return render(request, 'index.html', context)

def learning_page(request): return render(request, 'learning.html')

@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, "Обновлено!"); return redirect('profile')
    return render(request, 'profile.html', {'form': form})