"""Enhanced Entity Extraction with Management Intent Detection"""

import re
from typing import List, Set, Dict

class EntityExtractor:
    """Extracts financial entities and detects management intent"""
    
    # Financial keywords
    FINANCIAL_KEYWORDS = {
        'debt', 'loan', 'revenue', 'profit', 'loss', 'cash', 'equity',
        'liability', 'asset', 'earnings', 'ebitda', 'margin', 'growth',
        'decline', 'increase', 'decrease', 'capital', 'investment',
        'expenditure', 'income', 'dividend', 'share', 'stock'
    }
    
    # NEW: Strategic intent keywords (positive)
    STRATEGIC_POSITIVE = {
        'expansion', 'growth', 'diversification', 'acquisition',
        'innovation', 'investment', 'hiring', 'launching', 'developing',
        'strengthening', 'improving', 'scaling', 'entering', 'capturing'
    }
    
    # NEW: Operational reality keywords (negative)
    OPERATIONAL_NEGATIVE = {
        'closure', 'closing', 'layoff', 'downsizing', 'restructuring',
        'bankruptcy', 'liquidation', 'termination', 'suspension',
        'discontinuing', 'eliminating', 'reducing', 'cutting', 'divesting'
    }
    
    # NEW: Risk indicators
    RISK_KEYWORDS = {
        'risk', 'litigation', 'lawsuit', 'penalty', 'violation',
        'regulatory', 'investigation', 'dispute', 'contingent',
        'uncertainty', 'adverse', 'material', 'significant'
    }
    
    def extract_entities(self, text: str) -> Set[str]:
        """Extract financial entities from text"""
        text_lower = text.lower()
        found_entities = set()
        
        for keyword in self.FINANCIAL_KEYWORDS:
            if keyword in text_lower:
                found_entities.add(keyword)
        
        return found_entities
    
    def detect_intent(self, text: str) -> Dict[str, bool]:
        """
        NEW: Detect management intent vs operational reality
        
        Returns:
            {
                'strategic_positive': bool,  # Claims growth/expansion
                'operational_negative': bool, # Reality shows decline
                'risk_present': bool          # Risk factors mentioned
            }
        """
        text_lower = text.lower()
        
        has_positive = any(keyword in text_lower for keyword in self.STRATEGIC_POSITIVE)
        has_negative = any(keyword in text_lower for keyword in self.OPERATIONAL_NEGATIVE)
        has_risk = any(keyword in text_lower for keyword in self.RISK_KEYWORDS)
        
        return {
            'strategic_positive': has_positive,
            'operational_negative': has_negative,
            'risk_present': has_risk
        }
    
    def is_intent_contradiction(self, text1: str, text2: str) -> bool:
        """
        NEW: Check if two texts have contradictory intents
        
        Example:
            Text1: "We plan massive expansion" (positive)
            Text2: "Closing 5 factories next quarter" (negative)
            Returns: True (contradiction!)
        """
        intent1 = self.detect_intent(text1)
        intent2 = self.detect_intent(text2)
        
        # Case 1: Positive claims contradict negative operations
        if intent1['strategic_positive'] and intent2['operational_negative']:
            return True
        
        if intent2['strategic_positive'] and intent1['operational_negative']:
            return True
        
        # Case 2: Low risk claims contradict high risk disclosures
        if not intent1['risk_present'] and intent2['risk_present']:
            # One minimizes risk, other discloses it
            if any(word in text1.lower() for word in ['minimal', 'low', 'no', 'zero']):
                return True
        
        return False
    
    def has_entity_overlap(self, text1: str, text2: str) -> bool:
        """Check if two sentences mention same entities"""
        entities1 = self.extract_entities(text1)
        entities2 = self.extract_entities(text2)
        
        return len(entities1 & entities2) > 0


if __name__ == "__main__":
    # Test the enhancement
    extractor = EntityExtractor()
    
    test1 = "Company plans aggressive expansion into new markets"
    test2 = "Closing three factories due to financial constraints"
    
    print("🧪 Testing Management Intent Detection:")
    print(f"\nText 1: {test1}")
    print(f"Intent: {extractor.detect_intent(test1)}")
    
    print(f"\nText 2: {test2}")
    print(f"Intent: {extractor.detect_intent(test2)}")
    
    print(f"\nContradiction detected: {extractor.is_intent_contradiction(test1, test2)}")
    print("\n✅ Enhancement #1 complete!")