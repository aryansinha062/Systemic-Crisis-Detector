"""
REAL ML MODEL TRAINER - TRAINED ON ACTUAL CONTAGION DATA
"""

import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime

class RealContagionMLTrainer:
    """
    Train ML model on REAL historical contagion data
    Learn: Event severity + Company exposure → Actual risk outcome
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
        self.scaler = StandardScaler()
        self.trained = False
        self.training_data = []
    
    def load_real_contagion_data(self):
        """Load REAL collected contagion data from JSON"""
        try:
            with open('real_contagion_data.json', 'r') as f:
                data = json.load(f)
            
            print(f"\n✓ Loaded {len(data['events'])} REAL contagion events")
            return data['events']
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return []
    
    def extract_training_features(self, events):
        """
        Extract ML training features from REAL contagion events
        Features: [event_type_severity, max_peer_decline, weeks_to_max_decline, num_peers_affected]
        Target: peak_risk_score
        """
        
        X = []
        y = []
        
        event_type_severity = {
            'banking_crisis': 8.5,
            'liquidity_crisis': 7.5,
            'fraud_discovery': 8.0,
            'regulatory_violation': 6.5,
            'sector_stress': 6.0,
            'accounting_fraud': 9.0,
            'insolvency': 8.5
        }
        
        for event in events:
            event_name = event['event']
            event_type = event['event_type']
            peer_impacts = event['peer_impacts']
            
            if len(peer_impacts) == 0:
                continue
            
            # Calculate aggregate metrics
            all_max_declines = []
            all_peak_risks = []
            weeks_to_peak = []
            
            for peer_name, impacts in peer_impacts.items():
                impacts_dict = {imp['week']: imp for imp in impacts}
                
                max_decline = min([imp['return_pct'] for imp in impacts])
                peak_risk = max([imp['risk_score'] for imp in impacts])
                
                # Find week of peak risk
                peak_week = max([imp['week'] for imp in impacts if imp['risk_score'] == peak_risk])
                
                all_max_declines.append(max_decline)
                all_peak_risks.append(peak_risk)
                weeks_to_peak.append(peak_week)
            
            # Average metrics
            avg_max_decline = np.mean(all_max_declines)
            avg_peak_risk = np.mean(all_peak_risks)
            avg_weeks_to_peak = np.mean(weeks_to_peak)
            num_peers = len(peer_impacts)
            
            # Event severity
            severity = event_type_severity.get(event_type, 6.0)
            
            # Features: [severity, max_decline_magnitude, num_affected_peers, weeks_to_impact]
            features = [
                severity,
                abs(avg_max_decline),  # How much peers declined
                num_peers,  # How many peers affected
                avg_weeks_to_peak,  # How quickly impact happened
            ]
            
            X.append(features)
            y.append(avg_peak_risk)
            
            self.training_data.append({
                'event': event_name,
                'event_type': event_type,
                'features': features,
                'target': avg_peak_risk,
                'num_peers': num_peers,
                'max_peer_decline': avg_max_decline,
                'weeks_to_peak': avg_weeks_to_peak
            })
        
        return np.array(X), np.array(y)
    
    def train_model(self, X, y):
        """Train ML model on REAL data"""
        
        if len(X) < 2:
            print("✗ Not enough training data")
            return False
        
        print(f"\n{'='*100}")
        print(f"TRAINING ML MODEL ON REAL CONTAGION DATA")
        print(f"{'='*100}")
        print(f"Training samples: {len(X)}")
        print(f"Features: [event_severity, max_peer_decline, num_peers_affected, weeks_to_peak]")
        print(f"Target: peak_risk_score (1-10)")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Evaluate
        train_score = self.model.score(X_scaled, y)
        predictions = self.model.predict(X_scaled)
        rmse = np.sqrt(np.mean((predictions - y) ** 2))
        mae = np.mean(np.abs(predictions - y))
        
        print(f"\nModel Performance:")
        print(f"  R² Score: {train_score:.3f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  MAE: {mae:.2f}")
        
        print(f"\nFeature Importance:")
        features = ['Event Severity', 'Max Peer Decline %', 'Num Peers Affected', 'Weeks to Peak']
        for i, importance in enumerate(self.model.feature_importances_):
            print(f"  {features[i]}: {importance:.3f}")
        
        print(f"\nTraining Data Summary:")
        for i, data in enumerate(self.training_data, 1):
            print(f"  {i}. {data['event']}")
            print(f"     Type: {data['event_type']} | Peers: {data['num_peers']} | Max Decline: {data['max_peer_decline']:.2f}% | Peak Risk: {data['target']:.1f}")
        
        self.trained = True
        return True
    
    def predict_contagion_risk(self, event_severity, max_peer_decline, num_peers, weeks_to_peak):
        """
        Predict contagion risk using REAL trained model
        """
        if not self.trained:
            return None
        
        features = np.array([[event_severity, abs(max_peer_decline), num_peers, weeks_to_peak]])
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return min(10, max(1, prediction))
    
    def save_model(self):
        """Save trained model"""
        import pickle
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'trained': self.trained,
            'training_data': self.training_data
        }
        
        with open('real_contagion_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\n✓ Model saved: real_contagion_model.pkl")

if __name__ == "__main__":
    trainer = RealContagionMLTrainer()
    
    # Load REAL data
    events = trainer.load_real_contagion_data()
    
    if len(events) > 0:
        # Extract features
        X, y = trainer.extract_training_features(events)
        
        if len(X) > 0:
            # Train model
            trainer.train_model(X, y)
            
            # Save model
            trainer.save_model()
            
            print(f"\n{'='*100}")
            print("✓ REAL ML MODEL TRAINED AND SAVED")
            print("Ready for integration into main detector")
            print(f"{'='*100}\n")