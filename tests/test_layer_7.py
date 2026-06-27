"""
Tests for Layer 7: Market Structure Analysis
"""

import pytest
from src.layer_7_market_structure import MarketStructureAnalyzer

def test_analyzer_initializes():
    analyzer = MarketStructureAnalyzer()
    assert analyzer is not None

def test_short_constraints_analysis():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.analyze_short_constraints()
    assert 'constraints' in result
    assert result['max_short_hold_years'] <= 3
    assert result['total_cost_percent'] > 0

def test_long_advantages_analysis():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.analyze_long_advantages()
    assert 'advantages' in result
    assert result['cost'] == 0
    assert result['hold_duration'] == 'indefinite'

def test_paradox_calculation():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.calculate_paradox()
    assert result['cascade_inevitable'] == True
    assert result['market_self_corrects'] == False

def test_market_reform_proposal():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.propose_market_reform()
    assert 'reforms' in result
    assert 'naked_shorting' in result['reforms']
    assert result['necessity'] == 'CRITICAL'

def test_intervention_roi():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.estimate_intervention_roi()
    assert 'scenarios' in result
    assert result['average_roi'] > 1.0

def test_policy_recommendation():
    analyzer = MarketStructureAnalyzer()
    result = analyzer.generate_policy_recommendation()
    assert 'market_structure_problem' in result
    assert 'proposed_solution' in result
    assert result['urgency'] == 'CRITICAL'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])