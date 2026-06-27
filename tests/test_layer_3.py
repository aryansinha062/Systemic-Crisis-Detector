"""
Tests for Layer 3: Network Mapping & Cascade Modeling
"""

import pytest
from src.layer_3_network_cascade import NetworkCascadeDetector

def test_network_detector_initializes():
    detector = NetworkCascadeDetector()
    assert detector is not None
    assert detector.network is not None

def test_network_structure_analysis():
    detector = NetworkCascadeDetector()
    result = detector.analyze_network_structure('TSLA')
    assert result['company'] == 'TSLA'
    assert 'network_risk_score' in result
    assert result['alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_critical_nodes_calculation():
    detector = NetworkCascadeDetector()
    result = detector.calculate_critical_nodes()
    assert 'critical_nodes' in result
    assert len(result['critical_nodes']) > 0
    assert 'centrality_scores' in result

def test_cascade_path_modeling():
    detector = NetworkCascadeDetector()
    result = detector.model_cascade_path('TSLA', 30)
    assert result['trigger_company'] == 'TSLA'
    assert 'cascade_timeline' in result
    assert len(result['cascade_timeline']) > 0
    assert result['cascade_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

def test_cascade_spreads_over_time():
    detector = NetworkCascadeDetector()
    result = detector.model_cascade_path('JPMorgan', 30)
    timeline = result['cascade_timeline']
    # Cascade should spread (number of affected companies should increase)
    assert timeline[-1]['total_affected'] >= timeline[0]['total_affected']

def test_contagion_probability():
    detector = NetworkCascadeDetector()
    result = detector.estimate_contagion_probability('TSLA', 'Panasonic')
    assert 'contagion_probability' in result
    assert 0.0 <= result['contagion_probability'] <= 1.0
    assert result['connection_type'] in ['DIRECT', 'INDIRECT']

def test_contagion_direct_connection():
    detector = NetworkCascadeDetector()
    result = detector.estimate_contagion_probability('TSLA', 'Panasonic')
    # Direct supplier relationship
    assert result['connection_type'] == 'DIRECT'
    assert result['contagion_probability'] > 0.5

def test_contagion_no_connection():
    detector = NetworkCascadeDetector()
    result = detector.estimate_contagion_probability('UNKNOWN1', 'UNKNOWN2')
    # No connection
    assert result['contagion_probability'] == 0.0

def test_generate_comprehensive_alert():
    detector = NetworkCascadeDetector()
    result = detector.generate_network_alert()
    assert 'critical_nodes' in result
    assert 'cascade' in result
    assert 'contagion' in result
    assert result['network_alert'] in ['CRITICAL', 'WARNING', 'NORMAL']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])