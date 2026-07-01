"""
PROPRIETARY & CONFIDENTIAL
HISTORICAL CORRELATION TRAINER - ML MODEL FOR CONTAGION PREDICTION
Patent Pending: "12-Layer Algorithmic Fraud Detection System"
© 2026 Aryan Sinha. All Rights Reserved.

TRAINS: ML model on historical fraud/distress cases
LEARNS: Time-lag correlations between events and outcomes
PREDICTS: "If event X, company Y has Z% risk in N weeks"
"""

import json
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle

class HistoricalCorrelationTrainer:
    """
    Train ML model on historical contagion cases
    Learn: which events predict which company failures
    """
    
    def __init__(self):
        self.name = "CorrelationTrainer_ML"
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False
        
        # Historical cases: (event, affected_company, time_lag_weeks, outcome_risk_score)
        self.training_data = [
            # Format: (event_type, event_severity, company_exposure, time_lag_weeks, actual_risk_outcome)
            
            # CASE 1: Satyam Computers Fraud (2009)
            ('accounting_fraud_sebi', 9.0, 0.80, 0, 9.5),  # Direct: immediate risk
            ('accounting_fraud_sebi', 9.0, 0.60, 4, 8.0),  # Peers: 4 weeks later
            ('accounting_fraud_sebi', 9.0, 0.40, 8, 6.5),  # Sector: 8 weeks
            ('accounting_fraud_sebi', 9.0, 0.20, 12, 4.5),  # Weak link: 12 weeks
            
            # CASE 2: Bhushan Steel Insolvency (2017)
            ('supplier_stress', 8.5, 0.70, 0, 8.0),  # Suppliers: immediate
            ('supplier_stress', 8.5, 0.50, 6, 6.5),  # Customers: 6 weeks
            ('supplier_stress', 8.5, 0.35, 12, 5.0),  # Competitors: 12 weeks
            ('supplier_stress', 8.5, 0.15, 20, 3.0),  # Weak exposure: 20 weeks
            
            # CASE 3: YES Bank Crisis (2020)
            ('liquidity_crisis', 8.0, 0.75, 0, 8.5),  # Banking peers: immediate
            ('liquidity_crisis', 8.0, 0.55, 2, 7.0),  # Credit dependent: 2 weeks
            ('liquidity_crisis', 8.0, 0.40, 4, 5.5),  # Sector: 4 weeks
            ('liquidity_crisis', 8.0, 0.25, 8, 4.0),  # Weak link: 8 weeks
            
            # CASE 4: IndusInd Bank Fraud (2020)
            ('management_fraud', 8.5, 0.80, 0, 9.0),  # Banking system: immediate
            ('management_fraud', 8.5, 0.60, 3, 7.5),  # Peer banks: 3 weeks
            ('management_fraud', 8.5, 0.40, 6, 6.0),  # Business partners: 6 weeks
            ('management_fraud', 8.5, 0.20, 10, 4.0),  # Weak exposure: 10 weeks
            
            # CASE 5: Suzlon Energy SEBI Penalty (2012)
            ('regulatory_violation', 7.5, 0.65, 0, 7.5),  # Sector: immediate
            ('regulatory_violation', 7.5, 0.45, 5, 6.0),  # Competitors: 5 weeks
            ('regulatory_violation', 7.5, 0.30, 10, 4.5),  # Weak link: 10 weeks
            
            # CASE 6: IL&FS Crisis (2018)
            ('company_collapse', 9.0, 0.85, 0, 9.5),  # Financial system: immediate
            ('company_collapse', 9.0, 0.70, 2, 8.5),  # Exposure: 2 weeks
            ('company_collapse', 9.0, 0.50, 6, 7.0),  # Sector: 6 weeks
            ('company_collapse', 9.0, 0.30, 12, 5.0),  # Weak: 12 weeks
            
            # CASE 7: Customer Bankruptcy (Auto supplier example)
            ('customer_bankruptcy', 7.0, 0.60, 2, 7.5),  # Dependent suppliers: 2 weeks
            ('customer_bankruptcy', 7.0, 0.40, 8, 5.5),  # Peers: 8 weeks
            ('customer_bankruptcy', 7.0, 0.20, 16, 3.0),  # Weak: 16 weeks
            
            # CASE 8: Supply Chain Disruption (COVID-like)
            ('supply_disruption', 6.5, 0.70, 2, 6.5),  # Direct dependent: 2 weeks
            ('supply_disruption', 6.5, 0.45, 6, 5.0),  # Sector: 6 weeks
            ('supply_disruption', 6.5, 0.25, 12, 3.5),  # Weak: 12 weeks
            
            # CASE 9: Competitor Gets SEBI Enforcement (Sector sweep)
            ('competitor_sebi', 7.0, 0.50, 4, 6.0),  # Peers in sector: 4 weeks
            ('competitor_sebi', 7.0, 0.35, 8, 4.5),  # Related sector: 8 weeks
            ('competitor_sebi', 7.0, 0.15, 16, 2.5),  # Weak link: 16 weeks
            
            # CASE 10: Geopolitical Crisis (Supply chain impact)
            ('geopolitical_event', 6.0, 0.65, 4, 5.5),  # Supply dependent: 4 weeks
            ('geopolitical_event', 6.0, 0.40, 8, 4.0),  # Sector: 8 weeks
            ('geopolitical_event', 6.0, 0.20, 16, 2.5),  # Weak: 16 weeks
        ]
    
    def prepare_training_data(self):
        """
        Convert training cases into ML format
        Features: [event_severity, company_exposure, time_lag_weeks]
        Target: actual_risk_outcome
        """
        X = []
        y = []
        
        for case in self.training_data:
            event_type, event_severity, exposure, time_lag, outcome = case
            
            # Feature vector
            features = [
                event_severity,      # How severe is the event? (1-9)
                exposure,            # How exposed is this company? (0-1)
                time_lag,            # How many weeks after event? (0-20)
                1.0 / (1.0 + time_lag),  # Time decay function (closer = more impact)
            ]
            
            X.append(features)
            y.append(outcome)
        
        return np.array(X), np.array(y)
    
    def train_model(self):
        """
        Train ML model on historical contagion data
        Learn: event severity + exposure + time_lag → risk prediction
        """
        print("\n" + "="*100)
        print("TRAINING CORRELATION MODEL ON HISTORICAL DATA")
        print("="*100)
        
        X, y = self.prepare_training_data()
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Model performance
        train_score = self.model.score(X_scaled, y)
        predictions = self.model.predict(X_scaled)
        rmse = np.sqrt(np.mean((predictions - y) ** 2))
        
        print(f"\nModel Training Complete:")
        print(f"  Training R² Score: {train_score:.3f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  Training Cases: {len(self.training_data)}")
        
        # Feature importance
        print(f"\nFeature Importance:")
        feature_names = ['Event Severity', 'Company Exposure', 'Time Lag (weeks)', 'Time Decay']
        for i, importance in enumerate(self.model.feature_importances_):
            print(f"  {feature_names[i]}: {importance:.3f}")
        
        self.trained = True
        return train_score, rmse
    
    def predict_contagion_risk(self, event_severity, company_exposure, time_lag_weeks):
        """
        Predict risk for a company given:
        - event_severity: How severe is the triggering event? (1-9)
        - company_exposure: How exposed is this company? (0-1)
        - time_lag_weeks: How many weeks after event? (0-20)
        
        Returns: Predicted risk score (1-10)
        """
        if not self.trained:
            return 5.0
        
        # Prepare features
        features = np.array([[
            event_severity,
            company_exposure,
            time_lag_weeks,
            1.0 / (1.0 + time_lag_weeks),
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return min(10, max(1, prediction))
    
    def predict_time_series_risk(self, event_severity, company_exposure):
        """
        Predict risk trajectory over time
        Shows how risk decays as weeks pass
        """
        time_lags = list(range(0, 25, 2))  # 0, 2, 4, ..., 24 weeks
        risks = []
        
        for lag in time_lags:
            risk = self.predict_contagion_risk(event_severity, company_exposure, lag)
            risks.append(risk)
        
        return time_lags, risks
    
    def analyze_contagion_scenario(self, event_type, event_severity, company_exposure):
        """
        Analyze complete contagion scenario
        """
        
        time_lags, risks = self.predict_time_series_risk(event_severity, company_exposure)
        
        # Peak risk
        peak_risk = max(risks)
        peak_week = time_lags[risks.index(peak_risk)]
        
        # Risk stabilization (when drops below 5.0)
        stabilization_week = None
        for lag, risk in zip(time_lags, risks):
            if risk < 5.0:
                stabilization_week = lag
                break
        
        return {
            'event_type': event_type,
            'event_severity': event_severity,
            'company_exposure': company_exposure,
            'peak_risk': peak_risk,
            'peak_week': peak_week,
            'stabilization_week': stabilization_week,
            'risk_trajectory': dict(zip(time_lags, [round(r, 2) for r in risks]))
        }

if __name__ == "__main__":
    trainer = HistoricalCorrelationTrainer()
    
    # Train model
    train_score, rmse = trainer.train_model()
    
    # Test predictions
    print("\n" + "="*100)
    print("CONTAGION PREDICTIONS - TESTING ON HISTORICAL SCENARIOS")
    print("="*100)
    
    test_scenarios = [
        ('Satyam-like fraud', 9.0, 0.70),  # High severity, high exposure
        ('Bhushan-like supplier stress', 8.5, 0.50),  # High severity, medium exposure
        ('YES Bank-like liquidity', 8.0, 0.40),  # High severity, lower exposure
        ('Mild regulatory issue', 5.0, 0.30),  # Low severity, low exposure
    ]
    
    for scenario_name, severity, exposure in test_scenarios:
        result = trainer.analyze_contagion_scenario(scenario_name, severity, exposure)
        
        print(f"\n{scenario_name}:")
        print(f"  Severity: {severity}/10 | Exposure: {exposure:.0%}")
        print(f"  Peak Risk: {result['peak_risk']:.2f}/10 at Week {result['peak_week']}")
        print(f"  Stabilizes below 5.0: Week {result['stabilization_week']}")
        print(f"  Risk Timeline:")
        for week, risk in list(result['risk_trajectory'].items())[:6]:
            print(f"    Week {week:2d}: {risk:.2f}/10")