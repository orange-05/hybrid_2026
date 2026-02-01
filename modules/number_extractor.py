"""Financial Number Extraction and Validation"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class FinancialFigure:
    """Represents an extracted financial number"""
    value: float
    unit: str  # million, billion, thousand, crore, lakh
    context: str  # What it's about (revenue, debt, etc.)
    sentence: str  # Full sentence
    page: int


class NumberExtractor:
    """Extracts and validates financial numbers"""
    
    # Patterns for financial numbers
    PATTERNS = {
        'currency': r'\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|thousand|M|B|K))?',
        'percentage': r'\d+(?:\.\d+)?%',
        'indian': r'₹?[\d,]+(?:\.\d+)?(?:\s*(?:crore|lakh|million|billion))?'
    }
    
    # Financial contexts
    FINANCIAL_CONTEXTS = [
        'revenue', 'income', 'profit', 'loss', 'debt', 'loan',
        'asset', 'liability', 'equity', 'cash', 'ebitda',
        'earnings', 'dividend', 'capital', 'expenditure', 'sales'
    ]
    
    def extract_numbers(self, text: str, page_num: int = 0) -> List[FinancialFigure]:
        """Extract all financial numbers from text"""
        figures = []
        
        # Extract USD currency
        for match in re.finditer(self.PATTERNS['currency'], text):
            figure = self._parse_currency(match.group(), text, page_num)
            if figure:
                figures.append(figure)
        
        # Extract Indian currency
        for match in re.finditer(self.PATTERNS['indian'], text):
            if '₹' in match.group() or 'crore' in match.group().lower() or 'lakh' in match.group().lower():
                figure = self._parse_indian_currency(match.group(), text, page_num)
                if figure:
                    figures.append(figure)
        
        return figures
    
    def _parse_currency(self, value_str: str, sentence: str, page: int) -> Optional[FinancialFigure]:
        """Parse USD currency string"""
        clean = value_str.replace('$', '').replace(',', '').strip()
        
        # Extract unit
        unit = 'dollars'
        if 'billion' in clean.lower() or 'B' in clean:
            unit = 'billion'
            clean = re.sub(r'[^\d.]', '', clean.split('billion')[0].split('B')[0])
        elif 'million' in clean.lower() or 'M' in clean:
            unit = 'million'
            clean = re.sub(r'[^\d.]', '', clean.split('million')[0].split('M')[0])
        elif 'thousand' in clean.lower() or 'K' in clean:
            unit = 'thousand'
            clean = re.sub(r'[^\d.]', '', clean.split('thousand')[0].split('K')[0])
        
        try:
            value = float(clean)
        except:
            return None
        
        context = self._detect_context(sentence)
        
        return FinancialFigure(
            value=value,
            unit=unit,
            context=context,
            sentence=sentence[:100],  # Truncate long sentences
            page=page
        )
    
    def _parse_indian_currency(self, value_str: str, sentence: str, page: int) -> Optional[FinancialFigure]:
        """Parse Indian currency (₹, crore, lakh)"""
        clean = value_str.replace('₹', '').replace(',', '').strip()
        
        unit = 'rupees'
        if 'crore' in clean.lower():
            unit = 'crore'
            clean = re.sub(r'[^\d.]', '', clean.split('crore')[0])
        elif 'lakh' in clean.lower():
            unit = 'lakh'
            clean = re.sub(r'[^\d.]', '', clean.split('lakh')[0])
        
        try:
            value = float(clean)
        except:
            return None
        
        context = self._detect_context(sentence)
        
        return FinancialFigure(
            value=value,
            unit=unit,
            context=context,
            sentence=sentence[:100],
            page=page
        )
    
    def _detect_context(self, sentence: str) -> str:
        """Detect what the number is about"""
        sentence_lower = sentence.lower()
        
        for context in self.FINANCIAL_CONTEXTS:
            if context in sentence_lower:
                return context
        
        return 'unknown'
    
    def find_contradictions(self, figures: List[FinancialFigure]) -> List[Tuple[FinancialFigure, FinancialFigure, float]]:
        """
        Find contradictory financial numbers
        
        Returns:
            List of (figure1, figure2, difference_percent) tuples
        """
        contradictions = []
        
        # Group by context
        by_context = {}
        for fig in figures:
            if fig.context == 'unknown':
                continue
            if fig.context not in by_context:
                by_context[fig.context] = []
            by_context[fig.context].append(fig)
        
        # Find mismatches within same context
        for context, figs in by_context.items():
            if len(figs) < 2:
                continue
            
            # Compare all pairs
            for i, fig1 in enumerate(figs):
                for fig2 in figs[i+1:]:
                    # Skip if same page (likely same statement)
                    if fig1.page == fig2.page:
                        continue
                    
                    # Normalize to same unit
                    val1_normalized = self._normalize_value(fig1.value, fig1.unit)
                    val2_normalized = self._normalize_value(fig2.value, fig2.unit)
                    
                    # Calculate difference percentage
                    if val1_normalized > 0:
                        diff_percent = abs(val1_normalized - val2_normalized) / val1_normalized
                        
                        # Flag if differs by more than 20%
                        if diff_percent > 0.20:
                            contradictions.append((fig1, fig2, diff_percent))
        
        return contradictions
    
    def _normalize_value(self, value: float, unit: str) -> float:
        """Convert all values to base units for comparison"""
        multipliers = {
            'billion': 1_000_000_000,
            'million': 1_000_000,
            'thousand': 1_000,
            'crore': 10_000_000,
            'lakh': 100_000,
            'K': 1_000,
            'M': 1_000_000,
            'B': 1_000_000_000,
            'dollars': 1,
            'rupees': 1
        }
        
        return value * multipliers.get(unit, 1)


if __name__ == "__main__":
    # Test
    extractor = NumberExtractor()
    
    test1 = "Company revenue reached $500 million in Q3 2024"
    test2 = "Total annual revenue was $300 million for the year"
    test3 = "Revenue of ₹2000 crore reported in financial statements"
    
    figures1 = extractor.extract_numbers(test1, page_num=10)
    figures2 = extractor.extract_numbers(test2, page_num=150)
    figures3 = extractor.extract_numbers(test3, page_num=200)
    
    all_figures = figures1 + figures2 + figures3
    
    print("🧪 Testing Number Extraction:")
    print(f"\n📊 Extracted {len(all_figures)} financial figures:")
    for fig in all_figures:
        print(f"   Page {fig.page}: {fig.value} {fig.unit} ({fig.context})")
    
    contradictions = extractor.find_contradictions(all_figures)
    
    print(f"\n❌ Found {len(contradictions)} contradictions:")
    for f1, f2, diff in contradictions:
        print(f"\n  Contradiction in '{f1.context}':")
        print(f"    Page {f1.page}: {f1.value} {f1.unit}")
        print(f"    Page {f2.page}: {f2.value} {f2.unit}")
        print(f"    Difference: {diff*100:.1f}%")
    
    print("\n✅ Enhancement #2 complete!")