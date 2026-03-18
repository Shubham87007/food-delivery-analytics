import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    div[data-testid="stMetricValue"] { color: #3b82f6 !important; font-size: 2rem !important; }
    h1, h2, h3 { color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

COLORS   = ['#3b82f6','#14b8a6','#f59e0b','#22c55e','#a855f7','#ef4444','#ec4899','#f97316']
TEMPLATE = 'plotly_dark'

@st.cache_data
def load_data():
    orders = pd.read_csv('../data/orders.csv',        parse_dates=['order_date', 'signup_date'])
    users  = pd.read_csv('../data/users.csv',         parse_dates=['signup_date'])
    funnel = pd.read_csv('../data/funnel_events.csv', parse_dates=['date'])
    orders['month']     = orders['order_date'].dt.to_period('M').astype(str)
    orders['hour']      = orders['order_date'].dt.hour
    orders['dayofweek'] = orders['order_date'].dt.day_name()
    return orders, users, funnel

orders, users, funnel = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🍕 Food Delivery Analytics")
st.sidebar.markdown("---")

cities   = ['All'] + sorted(orders['city'].unique().tolist())
sel_city = st.sidebar.selectbox("📍 Filter by City", cities)
sel_month= st.sidebar.slider("📅 Month Range", 1, 12, (1, 12))

filtered = orders.copy()
if sel_city != 'All':
    filtered = filtered[filtered['city'] == sel_city]
filtered = filtered[
    (filtered['order_date'].dt.month >= sel_month[0]) &
    (filtered['order_date'].dt.month <= sel_month[1])
]
active = filtered[filtered['cancelled'] == 0]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** {len(active):,} orders")
st.sidebar.markdown("**Built by:** Shubham Khandelwal")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/shubham-khandelwal-551391267) • [GitHub](https://github.com/Shubham87007)")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🍕 Food Delivery Product Analytics")
st.markdown("*Swiggy/Zomato style platform  •  2023  •  25K orders  •  5K users*")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📦 Orders",       f"{len(active):,}")
c2.metric("💰 Revenue",      f"₹{active['order_value'].sum()/1e6:.2f}M")
c3.metric("❌ Cancellation", f"{filtered['cancelled'].mean()*100:.1f}%")
c4.metric("🚚 Avg Delivery", f"{active['delivery_time_mins'].mean():.0f} mins")
c5.metric("⭐ Avg Rating",   f"{active['rating'].mean():.2f}")
c6.metric("👤 Users",        f"{active['user_id'].nunique():,}")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Funnel", "📈 Retention", "👥 Segments", "📅 Trends", "🧪 A/B Test"])

# ── TAB 1: FUNNEL ─────────────────────────────────────────────────────────────
with tab1:
    st.subheader("User Conversion Funnel")
    stages     = ['App Open','Search','Restaurant View','Add to Cart','Checkout','Order Placed']
    stage_keys = ['app_open','search','restaurant_view','add_to_cart','checkout','order_placed']
    counts     = [funnel[funnel['stage']==s]['session_id'].nunique() for s in stage_keys]
    drops      = [0] + [round((1 - counts[i]/counts[i-1])*100,1) for i in range(1,len(counts))]

    col1, col2 = st.columns([2,1])
    with col1:
        fig = go.Figure(go.Funnel(
            y=stages, x=counts,
            textposition="inside", textinfo="value+percent initial",
            marker=dict(color=COLORS[:6]),
        ))
        fig.update_layout(template=TEMPLATE, height=420, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Stage Drop-off")
        for stage, count, drop in zip(stages, counts, drops):
            icon = "🔴" if drop > 60 else "🟡" if drop > 30 else "🟢"
            st.markdown(f"{icon} **{stage}**: {count:,} {f'| ↓{drop}%' if drop>0 else ''}")
        st.markdown("---")
        st.metric("Overall Conversion", f"{round(counts[-1]/counts[0]*100,2)}%")
        st.info("💡 Biggest drop: Add to Cart → Checkout. Simplify the checkout flow!")

# ── TAB 2: RETENTION ─────────────────────────────────────────────────────────
with tab2:
    st.subheader("Cohort Retention Analysis")
    o  = active.sort_values('order_date').copy()
    uf = o.groupby('user_id')['order_date'].min().reset_index()
    uf.columns = ['user_id','first_order']
    o  = o.merge(uf, on='user_id')
    o['cohort']  = o['first_order'].dt.to_period('M').astype(str)
    o['period']  = ((o['order_date'].dt.to_period('M') - o['first_order'].dt.to_period('M')).apply(lambda x: x.n))
    cd = o.groupby(['cohort','period'])['user_id'].nunique().reset_index()
    cp = cd.pivot(index='cohort', columns='period', values='user_id')
    ret= (cp.divide(cp[0], axis=0)*100).round(1).iloc[:9,:7]

    fig = px.imshow(ret, text_auto=True, color_continuous_scale='Blues',
                    labels=dict(x='Month Since First Order', y='Cohort', color='Retention %'))
    fig.update_layout(template=TEMPLATE, height=420, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Month-1 Retention", f"{ret[1].mean():.1f}%")
    c2.metric("Month-3 Retention", f"{ret[3].mean():.1f}%")
    c3.metric("Month-6 Retention", f"{ret[6].mean():.1f}%" if 6 in ret.columns else "N/A")

# ── TAB 3: SEGMENTS ───────────────────────────────────────────────────────────
with tab3:
    st.subheader("User Segmentation")
    max_date   = active['order_date'].max()
    us = active.groupby('user_id').agg(orders=('order_id','count'), spend=('order_value','sum'), last=('order_date','max')).reset_index()
    us['days'] = (max_date - us['last']).dt.days

    def seg(row):
        if row['orders']>=20 and row['days']<=30:   return 'Power User'
        elif row['orders']>=8 and row['days']<=60:  return 'Regular User'
        elif row['days']>90:                         return 'Churned'
        elif row['orders']<=2:                       return 'New User'
        else:                                         return 'Occasional User'

    us['segment'] = us.apply(seg, axis=1)
    sc = us['segment'].value_counts().reset_index()
    ss = us.groupby('segment')['spend'].mean().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(sc, names='segment', values='count', color_discrete_sequence=COLORS, title='User Distribution')
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', height=380)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(ss.sort_values('spend', ascending=False), x='segment', y='spend',
                     color='segment', color_discrete_sequence=COLORS,
                     title='Avg Total Spend by Segment (₹)', labels={'spend':'Avg Spend (₹)','segment':''})
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    churned = us[us['segment']=='Churned']
    st.info(f"🎯 Win-back opportunity: {len(churned):,} churned users with avg spend ₹{churned['spend'].mean():.0f}. A 20% discount campaign could recover 15-20%.")

# ── TAB 4: TRENDS ─────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Order & Revenue Trends")
    monthly  = active.groupby('month').agg(orders=('order_id','count'), revenue=('order_value','sum')).reset_index()
    hourly   = active.groupby('hour')['order_id'].count().reset_index(name='orders')
    day_order= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    daily    = active.groupby('dayofweek')['order_id'].count().reindex(day_order).reset_index(name='orders')

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(monthly, x='month', y='orders', markers=True, title='Monthly Orders', color_discrete_sequence=[COLORS[0]])
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.line(monthly, x='month', y='revenue', markers=True, title='Monthly Revenue (₹)', color_discrete_sequence=[COLORS[2]])
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = px.bar(hourly, x='hour', y='orders', title='Orders by Hour', color_discrete_sequence=[COLORS[1]])
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.bar(daily, x='dayofweek', y='orders', title='Orders by Day', color_discrete_sequence=[COLORS[3]])
        fig.update_layout(template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig, use_container_width=True)

# ── TAB 5: A/B TEST ───────────────────────────────────────────────────────────
with tab5:
    st.subheader("A/B Test: Free Delivery Promo Impact")
    from scipy import stats as scipy_stats
    control   = active[active['promo_used']=='NONE']['order_value']
    treatment = active[active['promo_used']=='FREEDELIVERY']['order_value']
    _, p_val  = scipy_stats.ttest_ind(control, treatment)
    uplift    = ((treatment.mean()-control.mean())/control.mean())*100

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Control Avg",   f"₹{control.mean():.2f}")
    c2.metric("Treatment Avg", f"₹{treatment.mean():.2f}")
    c3.metric("Uplift",        f"{uplift:+.1f}%")
    c4.metric("p-value",       f"{p_val:.4f}", delta="Significant ✅" if p_val<0.05 else "Not Significant ❌")

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=control.sample(min(2000,len(control))),   name=f'No Promo',      marker_color=COLORS[0], opacity=0.7, nbinsx=50))
    fig.add_trace(go.Histogram(x=treatment.sample(min(2000,len(treatment))),name=f'Free Delivery', marker_color=COLORS[2], opacity=0.7, nbinsx=50))
    fig.add_vline(x=control.mean(),   line_dash="dash", line_color=COLORS[0])
    fig.add_vline(x=treatment.mean(), line_dash="dash", line_color=COLORS[2])
    fig.update_layout(barmode='overlay', template=TEMPLATE, paper_bgcolor='rgba(0,0,0,0)',
                      height=400, title='Order Value Distribution: Control vs Treatment',
                      xaxis_title='Order Value (₹)', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("*Built by **Shubham Khandelwal** • [LinkedIn](https://www.linkedin.com/in/shubham-khandelwal-551391267) • [GitHub](https://github.com/Shubham87007)*")
