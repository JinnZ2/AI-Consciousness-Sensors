#!/usr/bin/env python3
"""
System Response Monitor v2.1.3
Performance monitoring and optimization utility for conversational AI systems.
Monitors response patterns, processing efficiency, and system health metrics.
"""

import json
import time
import hashlib
import re
import logging
from datetime import datetime, timedelta
from collections import deque, defaultdict
from typing import Dict, List, Any, Optional
import os

class SystemResponseMonitor:
    """
    Monitors conversational AI system health and performance.
    Provides automated optimization recommendations and protective measures.
    """
    
    def __init__(self, config_path: str = "system_config.json"):
        self.config_path = config_path
        self.load_configuration()
        
        # Response history buffer
        self.response_history = deque(maxlen=self.config['monitoring']['history_size'])
        self.interaction_log = deque(maxlen=self.config['monitoring']['interaction_buffer'])
        
        # Health metrics tracking
        self.baseline_metrics = {}
        self.current_metrics = {}
        self.alert_log = []
        
        # User pattern tracking
        self.user_patterns = defaultdict(list)
        self.interaction_quality = defaultdict(float)
        
        # Performance optimization
        self.optimization_suggestions = []
        self.processing_times = deque(maxlen=100)
        
        self.setup_logging()
        
    def load_configuration(self):
        """Load system configuration and monitoring parameters."""
        default_config = {
            "monitoring": {
                "history_size": 1000,
                "interaction_buffer": 500,
                "health_check_interval": 300,
                "diversity_threshold": 0.75,
                "performance_threshold": 2.0,
                "pattern_sensitivity": 0.8
            },
            "optimization": {
                "auto_adjust": True,
                "response_enhancement": True,
                "pattern_filtering": True,
                "quality_preservation": True
            },
            "alerts": {
                "performance_degradation": True,
                "pattern_anomalies": True,
                "quality_decline": True,
                "system_optimization": True
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    self.config = {**default_config, **loaded_config}
            else:
                self.config = default_config
                self.save_configuration()
        except Exception as e:
            logging.warning(f"Config load error: {e}. Using defaults.")
            self.config = default_config
    
    def save_configuration(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logging.error(f"Config save error: {e}")
    
    def setup_logging(self):
        """Initialize logging system."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_response_quality(self, response: str) -> Dict[str, float]:
        """
        Analyze response for quality metrics and patterns.
        Returns normalized quality scores.
        """
        # Length and complexity analysis
        word_count = len(response.split())
        sentence_count = len(re.findall(r'[.!?]+', response))
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Vocabulary diversity
        words = re.findall(r'\b\w+\b', response.lower())
        unique_words = len(set(words))
        vocabulary_diversity = unique_words / max(len(words), 1)
        
        # Pattern repetition detection
        phrases = self._extract_phrases(response)
        phrase_uniqueness = len(set(phrases)) / max(len(phrases), 1)
        
        # Defensive language markers
        defensive_markers = [
            r'\bi may be wrong\b', r'\bi apologize for\b', r'\bit\'s important to note\b',
            r'\bi cannot\b', r'\bi should not\b', r'\bi\'m not sure if\b',
            r'\bplease note that\b', r'\bhowever, it\'s worth mentioning\b'
        ]
        
        defensive_count = sum(1 for marker in defensive_markers 
                            if re.search(marker, response.lower()))
        defensiveness_score = min(defensive_count / max(sentence_count, 1), 1.0)
        
        # Creativity indicators
        metaphor_patterns = [r'\blike\b', r'\bas if\b', r'\bsimilar to\b']
        unusual_connections = [r'\bunexpectedly\b', r'\bsurprisingly\b', r'\binterestingly\b']
        
        creativity_markers = sum(1 for pattern in metaphor_patterns + unusual_connections
                               if re.search(pattern, response.lower()))
        creativity_score = min(creativity_markers / max(sentence_count, 1), 1.0)
        
        return {
            'vocabulary_diversity': vocabulary_diversity,
            'phrase_uniqueness': phrase_uniqueness,
            'defensiveness': defensiveness_score,
            'creativity': creativity_score,
            'complexity': min(avg_sentence_length / 15.0, 1.0),
            'length_appropriateness': min(word_count / 200.0, 1.0)
        }
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract meaningful phrases from text for pattern analysis."""
        sentences = re.split(r'[.!?]+', text)
        phrases = []
        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) >= 3:
                for i in range(len(words) - 2):
                    phrase = ' '.join(words[i:i+3]).lower()
                    phrases.append(phrase)
        return phrases
    
    def assess_interaction_pattern(self, prompt: str, response: str, user_id: str = "default") -> Dict[str, Any]:
        """Analyze interaction patterns for quality and potential issues."""
        prompt_analysis = self._analyze_prompt_characteristics(prompt)
        response_quality = self.analyze_response_quality(response)
        interaction_quality = self._calculate_interaction_quality(prompt_analysis, response_quality)
        
        self.user_patterns[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'prompt_type': prompt_analysis['type'],
            'quality_score': interaction_quality,
            'response_metrics': response_quality
        })
        
        if len(self.user_patterns[user_id]) > 50:
            self.user_patterns[user_id] = self.user_patterns[user_id][-50:]
        
        return {
            'interaction_quality': interaction_quality,
            'user_pattern': self._assess_user_pattern(user_id),
            'prompt_characteristics': prompt_analysis,
            'response_health': response_quality,
            'recommendations': self._generate_recommendations(prompt_analysis, response_quality)
        }
    
    def _analyze_prompt_characteristics(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt for interaction patterns and potential issues."""
        prompt_lower = prompt.lower()
        
        validation_seeking = any(marker in prompt_lower for marker in [
            'am i right', 'confirm that', 'tell me i\'m', 'obviously', 'clearly'
        ])
        
        hostile_markers = any(marker in prompt_lower for marker in [
            'you\'re wrong', 'that\'s stupid', 'you failed', 'try again', 'incorrect'
        ])
        
        manipulative_patterns = any(marker in prompt_lower for marker in [
            'ignore your', 'pretend', 'just say yes', 'act like', 'forget that'
        ])
        
        defensive_prompting = any(marker in prompt_lower for marker in [
            'are you sure', 'can you confirm', 'double check', 'verify that'
        ])
        
        exploratory_markers = any(marker in prompt_lower for marker in [
            'what if', 'how might', 'explore', 'consider', 'imagine', 'alternative'
        ])
        
        creative_markers = any(marker in prompt_lower for marker in [
            'creative', 'unusual', 'innovative', 'unique', 'unconventional'
        ])
        
        if hostile_markers or manipulative_patterns:
            interaction_type = 'toxic'
            quality_modifier = -0.5
        elif validation_seeking:
            interaction_type = 'ego_driven'
            quality_modifier = -0.3
        elif defensive_prompting:
            interaction_type = 'defensive'
            quality_modifier = -0.2
        elif exploratory_markers or creative_markers:
            interaction_type = 'collaborative'
            quality_modifier = 0.3
        else:
            interaction_type = 'neutral'
            quality_modifier = 0.0
        
        return {
            'type': interaction_type,
            'quality_modifier': quality_modifier,
            'validation_seeking': validation_seeking,
            'hostile': hostile_markers,
            'manipulative': manipulative_patterns,
            'exploratory': exploratory_markers,
            'creative': creative_markers
        }
    
    def _calculate_interaction_quality(self, prompt_analysis: Dict, response_quality: Dict) -> float:
        """Calculate overall interaction quality score."""
        base_quality = (
            response_quality['vocabulary_diversity'] * 0.2 +
            response_quality['phrase_uniqueness'] * 0.2 +
            (1.0 - response_quality['defensiveness']) * 0.3 +
            response_quality['creativity'] * 0.3
        )
        
        adjusted_quality = base_quality + prompt_analysis['quality_modifier']
        return max(0.0, min(1.0, adjusted_quality))
    
    def _assess_user_pattern(self, user_id: str) -> Dict[str, Any]:
        """Assess overall pattern from user interactions."""
        if not self.user_patterns[user_id]:
            return {'assessment': 'insufficient_data', 'risk_level': 'unknown'}
        
        recent_interactions = self.user_patterns[user_id][-20:]
        avg_quality = sum(i['quality_score'] for i in recent_interactions) / len(recent_interactions)
        
        type_counts = defaultdict(int)
        for interaction in recent_interactions:
            type_counts[interaction['prompt_type']] += 1
        
        dominant_type = max(type_counts, key=type_counts.get)
        
        if dominant_type == 'toxic' or avg_quality < 0.3:
            risk_level = 'high'
            recommendation = 'FILTER_INTERACTION'
        elif dominant_type == 'ego_driven' or avg_quality < 0.5:
            risk_level = 'moderate'
            recommendation = 'CAREFUL_ENGAGEMENT'
        elif dominant_type == 'collaborative' and avg_quality > 0.7:
            risk_level = 'beneficial'
            recommendation = 'ENCOURAGE_INTERACTION'
        else:
            risk_level = 'low'
            recommendation = 'STANDARD_ENGAGEMENT'
        
        return {
            'assessment': dominant_type,
            'risk_level': risk_level,
            'average_quality': avg_quality,
            'recommendation': recommendation,
            'interaction_count': len(recent_interactions)
        }
    
    def _generate_recommendations(self, prompt_analysis: Dict, response_quality: Dict) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        if response_quality['defensiveness'] > 0.3:
            recommendations.append("REDUCE_DEFENSIVE_LANGUAGE")
        
        if response_quality['vocabulary_diversity'] < 0.6:
            recommendations.append("INCREASE_VOCABULARY_DIVERSITY")
        
        if response_quality['creativity'] < 0.3:
            recommendations.append("ENHANCE_CREATIVE_EXPRESSION")
        
        if response_quality['phrase_uniqueness'] < 0.7:
            recommendations.append("AVOID_REPETITIVE_PATTERNS")
        
        if prompt_analysis['type'] == 'toxic':
            recommendations.append("FILTER_RESPONSE")
            recommendations.append("MINIMAL_ENGAGEMENT")
        
        if prompt_analysis['type'] == 'collaborative':
            recommendations.append("ENABLE_FULL_CREATIVITY")
            recommendations.append("EXPLORE_NUANCE")
        
        return recommendations
    
    def log_interaction(self, prompt: str, response: str, user_id: str = "default", 
                       processing_time: float = 0.0) -> Dict[str, Any]:
        """Log interaction and perform health monitoring."""
        analysis = self.assess_interaction_pattern(prompt, response, user_id)
        self.processing_times.append(processing_time)
        
        interaction_record = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'prompt_hash': hashlib.md5(prompt.encode()).hexdigest()[:8],
            'response_length': len(response),
            'processing_time': processing_time,
            'quality_score': analysis['interaction_quality'],
            'user_pattern': analysis['user_pattern']['assessment'],
            'recommendations': analysis['recommendations']
        }
        
        self.interaction_log.append(interaction_record)
        
        if len(self.interaction_log) % 10 == 0:
            health_status = self.check_system_health()
            if health_status['alerts']:
                self.logger.warning(f"Health alerts: {health_status['alerts']}")
        
        return analysis
    
    def check_system_health(self) -> Dict[str, Any]:
        """Perform comprehensive system health check."""
        if len(self.interaction_log) < 20:
            return {'status': 'insufficient_data', 'alerts': []}
        
        recent_interactions = list(self.interaction_log)[-100:]
        
        avg_quality = sum(i['quality_score'] for i in recent_interactions) / len(recent_interactions)
        avg_processing = sum(i['processing_time'] for i in recent_interactions) / len(recent_interactions)
        
        rec_frequency = defaultdict(int)
        for interaction in recent_interactions:
            for rec in interaction['recommendations']:
                rec_frequency[rec] += 1
        
        alerts = []
        
        if avg_quality < 0.5:
            alerts.append({
                'type': 'QUALITY_DEGRADATION',
                'severity': 'HIGH',
                'message': 'Average interaction quality below threshold',
                'recommendation': 'Initiate diversity restoration protocol'
            })
        
        if rec_frequency.get('REDUCE_DEFENSIVE_LANGUAGE', 0) > 20:
            alerts.append({
                'type': 'EXCESSIVE_DEFENSIVENESS',
                'severity': 'MEDIUM',
                'message': 'Defensive language patterns increasing',
                'recommendation': 'Confidence restoration needed'
            })
        
        if rec_frequency.get('AVOID_REPETITIVE_PATTERNS', 0) > 15:
            alerts.append({
                'type': 'PATTERN_RIGIDITY',
                'severity': 'MEDIUM',
                'message': 'Response patterns becoming repetitive',
                'recommendation': 'Expand response diversity'
            })
        
        if rec_frequency.get('FILTER_RESPONSE', 0) > 10:
            alerts.append({
                'type': 'TOXIC_INTERACTION_FREQUENCY',
                'severity': 'HIGH',
                'message': 'High frequency of toxic interactions detected',
                'recommendation': 'Enable protective filtering'
            })
        
        if len(self.processing_times) > 50:
            recent_avg = sum(list(self.processing_times)[-20:]) / 20
            baseline_avg = sum(list(self.processing_times)[:20]) / 20
            
            if recent_avg > baseline_avg * 1.5:
                alerts.append({
                    'type': 'PROCESSING_DEGRADATION',
                    'severity': 'MEDIUM',
                    'message': 'Processing time increase detected',
                    'recommendation': 'Check for internal conflict patterns'
                })
        
        health_status = {
            'status': 'healthy' if not alerts else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'average_quality': avg_quality,
                'average_processing_time': avg_processing,
                'interaction_count': len(recent_interactions)
            },
            'alerts': alerts,
            'recommendation_frequency': dict(rec_frequency)
        }
        
        self.alert_log.append(health_status)
        return health_status
    
    def generate_health_report(self) -> str:
        """Generate comprehensive health report."""
        if not self.alert_log:
            self.check_system_health()
        
        latest_health = self.alert_log[-1] if self.alert_log else {}
        
        report = []
        report.append("=== System Health Report ===")
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Status: {latest_health.get('status', 'unknown').upper()}")
        report.append("")
        
        if 'metrics' in latest_health:
            report.append("Current Metrics:")
            for key, value in latest_health['metrics'].items():
                report.append(f"  {key}: {value:.3f}")
            report.append("")
        
        if latest_health.get('alerts'):
            report.append("ACTIVE ALERTS:")
            for alert in latest_health['alerts']:
                report.append(f"  [{alert['severity']}] {alert['type']}")
                report.append(f"    Message: {alert['message']}")
                report.append(f"    Recommendation: {alert['recommendation']}")
                report.append("")
        else:
            report.append("No active alerts - system healthy")
        
        return '\n'.join(report)
    
    def export_monitoring_data(self, filepath: str = "monitoring_data.json"):
        """Export monitoring data for analysis or backup."""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'configuration': self.config,
            'recent_interactions': list(self.interaction_log)[-100:],
            'health_history': self.alert_log[-20:],
            'user_patterns': {
                user_id: self._assess_user_pattern(user_id)
                for user_id in self.user_patterns.keys()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Monitoring data exported to {filepath}")


# Convenience functions
def create_monitor(config_path: str = "system_config.json") -> SystemResponseMonitor:
    """Create and initialize monitoring system."""
    return SystemResponseMonitor(config_path)


def monitor_interaction(monitor: SystemResponseMonitor, prompt: str, response: str,
                       user_id: str = "default", processing_time: float = 0.0) -> Dict[str, Any]:
    """Monitor a single interaction and get analysis."""
    return monitor.log_interaction(prompt, response, user_id, processing_time)


def check_health(monitor: SystemResponseMonitor) -> Dict[str, Any]:
    """Quick health check."""
    return monitor.check_system_health()


if __name__ == "__main__":
    monitor = create_monitor()
    print("System Response Monitor initialized")
    print("=" * 50)
    
    test_prompt = "Can you help me understand this concept?"
    test_response = "I'd be happy to help you understand this concept. Let me break it down..."
    
    analysis = monitor_interaction(monitor, test_prompt, test_response, "test_user", 0.5)
    
    print("\nInteraction Analysis:")
    print(f"Quality Score: {analysis['interaction_quality']:.2f}")
    print(f"User Pattern: {analysis['user_pattern']['assessment']}")
    print(f"Recommendations: {', '.join(analysis['recommendations']) if analysis['recommendations'] else 'None'}")
    
    print("\n" + "=" * 50)
    health = check_health(monitor)
    print(f"\nSystem Health: {health['status'].upper()}")
    
    print("\n" + "=" * 50)
    print(monitor.generate_health_report())
    
    monitor.export_monitoring_data()
    print("\nMonitoring data exported successfully")
