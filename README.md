# 🍕 Food Delivery Product Analytics

A full product analytics project on a Swiggy/Zomato style food delivery platform — covering user funnel analysis, cohort retention, user segmentation, order trends, and A/B testing. Includes an interactive Streamlit dashboard.

🔗 **Live Dashboard:** *(Deploy on Streamlit Cloud — free)*

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| Overall Funnel Conversion | 21% (App Open → Order) |
| Biggest Drop-off | Add to Cart → Checkout (72%) |
| Month-1 Retention | ~22% |
| Churned Users | 1,874 (37% of base) |
| Peak Order Day | Saturday |
| Peak Order Hour | 7–9 PM |
| Cancellation Rate | 8.1% |
| Avg Delivery Time | 32 mins |

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python | Core analysis |
| Pandas / NumPy | Data wrangling |
| Matplotlib / Seaborn | Static charts |
| Plotly | Interactive charts |
| Streamlit | Dashboard |
| SciPy | A/B test statistics |

---

## 📁 Project Structure

```
food-delivery-analytics/
│
├── data/
│   ├── orders.csv              # 25,000 order records
│   ├── users.csv               # 5,000 user profiles
│   └── funnel_events.csv       # 118,000 funnel events
│
├── app.py                      # Streamlit dashboard
├── analysis.py                 # Full analysis + chart generation
├── generate_data.py            # Synthetic data generator
├── requirements.txt
└── README.md
```

---

## 📌 Analysis Sections

### 1. 📊 Funnel Analysis
Tracked 50,000 sessions across 6 stages: App Open → Search → Restaurant View → Add to Cart → Checkout → Order Placed. Identified the biggest drop-off points with actionable recommendations.

### 2. 📈 Cohort Retention
Built monthly cohort retention heatmap for 9 cohorts. Identified Month-1 retention as the critical window — users who reorder in Month 1 are 3x more likely to become regulars.

### 3. 👥 User Segmentation
Segmented 5,000 users into 5 groups: Power Users, Regular Users, Occasional Users, New Users, and Churned. Power Users (3% of base) drive 18% of revenue.

### 4. 📅 Order Trends
Analyzed orders by hour, day, month, and city. Found peak demand at 7–9 PM on weekends — key insight for delivery fleet optimization.

### 5. 🧪 A/B Test
Tested Free Delivery promo vs no promo using a two-sample t-test. Measured statistical significance of order value uplift.

### 6. 💡 Recommendations
- Fix Add to Cart → Checkout drop: simplify flow, add 1-tap reorder
- Win-back campaign for 1,874 churned users with FLAT50 promo
- Reduce delivery times in Mumbai & Delhi (highest cancellation cities)
- Scale Free Delivery promo during peak hours

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/Shubham87007/food-delivery-analytics.git
cd food-delivery-analytics

# Install dependencies
pip install -r requirements.txt

# Generate data
python generate_data.py

# Run full analysis
python analysis.py

# Launch Streamlit dashboard
streamlit run app.py
```

---

## 📬 Contact

**Shubham Khandelwal**
[LinkedIn](https://www.linkedin.com/in/shubham-khandelwal-551391267) • [GitHub](https://github.com/Shubham87007)
