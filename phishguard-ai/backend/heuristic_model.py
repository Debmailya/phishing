from __future__ import annotations


class HeuristicPhishingModel:
    """Fallback model used until a real sklearn/XGBoost model is trained."""

    @staticmethod
    def _row_score(row) -> float:
        score = 0.0
        score += 0.18 if row["num_dots"] >= 3 else 0.0
        score += 0.20 if row["has_at_symbol"] == 1 else 0.0
        score += 0.20 if row["has_ip_in_domain"] == 1 else 0.0
        score += 0.16 if row["url_length"] > 75 else 0.0
        score += 0.12 if row["num_digits"] > 8 else 0.0
        score += 0.10 if row["num_hyphens"] > 3 else 0.0
        score += 0.04 if row["uses_https"] == 0 else 0.0
        return min(max(score, 0.01), 0.99)

    def predict_proba(self, X):
        probs = []
        for _, row in X.iterrows():
            phishing_prob = self._row_score(row)
            probs.append([1.0 - phishing_prob, phishing_prob])
        return probs

    def predict(self, X):
        return [1 if row[1] >= 0.5 else 0 for row in self.predict_proba(X)]