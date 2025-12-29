class EconomyMetrics:
    def __init__(self):
        self.history = []
        # Initialize with sensible defaults to avoid DivisionByZero in step 0
        self.current_metrics = {
            "gdp": 0.0,
            "avg_price": 1.0,
            "growth": 0.0,
            "inflation": 0.0
        }

    def update_metrics(self, total_production, current_market_price):
        prev_gdp = self.current_metrics["gdp"]
        prev_price = self.current_metrics["avg_price"]

        growth = (total_production - prev_gdp) / prev_gdp if prev_gdp > 0 else 0
        inflation = (current_market_price - prev_price) / prev_price if prev_price > 0 else 0

        self.current_metrics = {
            "gdp": round(total_production, 3),
            "avg_price": round(current_market_price, 3),
            "growth": round(growth, 3),
            "inflation": round(inflation, 3)
        }
        self.history.append(self.current_metrics.copy())

    def get_metric(self, metric_name):
        return self.current_metrics.get(metric_name, 0)
