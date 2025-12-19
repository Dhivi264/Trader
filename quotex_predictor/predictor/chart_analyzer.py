"""
Advanced Chart Analysis Module with Smart Money Concepts (SMC)
Analyzes uploaded chart images using advanced SMC concepts including:
- Market Structure Shift (MSS)
- Order Blocks (OB)
- Quasimodo (QMLR)
- Smart Money Concepts (SMC)
- Smart Money Divergence (SMD)
- Support and Resistance
- Fair Value Gap (FVG)
- Inverse Fair Value Gap (IFVG)
- Liquidity Analysis
- Liquidity Sweep
- Liquidity Grab
- Change of Character (CHoCH)
"""

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("⚠️ OpenCV not available - using Pillow-only image processing")

import numpy as np
from PIL import Image
import logging
from typing import Dict, Any, List, Tuple
from .data_sources import DataSourceManager
from .technical_analysis import AdvancedTechnicalAnalyzer
import pandas as pd

logger = logging.getLogger(__name__)


class ChartVisualAnalyzer:
    """
    Analyzes uploaded chart images for visual patterns and combines with real price data
    """
    
    def __init__(self):
        self.data_manager = DataSourceManager()
        self.technical_analyzer = AdvancedTechnicalAnalyzer()
        
    def analyze_chart_with_real_data(self, image_path: str, symbol: str, timeframe: str = '1h') -> Dict[str, Any]:
        """
        Analyze chart image for visual patterns and get real price prediction
        
        Args:
            image_path: Path to uploaded chart image
            symbol: Trading pair symbol
            timeframe: Chart timeframe (15m or 1h)
            
        Returns:
            Combined analysis with visual patterns and real price prediction
        """
        try:
            # 1. Analyze visual patterns from chart image
            visual_analysis = self._analyze_visual_patterns(image_path)
            
            # 2. Get real price data and generate prediction
            real_prediction = self._get_real_price_prediction(symbol)
            
            # 3. Combine both analyses
            combined_analysis = {
                'symbol': symbol,
                'timeframe': timeframe,
                'visual_analysis': visual_analysis,
                'real_price_prediction': real_prediction,
                'recommendation': self._generate_recommendation(visual_analysis, real_prediction),
                'analysis_timestamp': None,
                'success': True
            }
            
            # Clean all data for JSON serialization
            cleaned_analysis = self._clean_for_json_serialization(combined_analysis)
            
            return cleaned_analysis
            
        except Exception as e:
            logger.error(f"Chart analysis error: {e}")
            return self._get_error_analysis(symbol, str(e))
    
    def _analyze_visual_patterns(self, image_path: str) -> Dict[str, Any]:
        """Analyze visual patterns from chart image"""
        try:
            if OPENCV_AVAILABLE:
                return self._analyze_with_opencv(image_path)
            else:
                return self._analyze_with_pillow(image_path)
            
        except Exception as e:
            logger.error(f"Visual pattern analysis error: {e}")
            return {
                'trend_direction': 'UNKNOWN',
                'support_resistance': {'levels': []},
                'pattern_type': 'UNCLEAR',
                'chart_quality': 'POOR',
                'confidence': 0.3,
                'error': str(e)
            }
    
    def _analyze_with_opencv(self, image_path: str) -> Dict[str, Any]:
        """Analyze with OpenCV (full functionality)"""
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Basic visual analysis
        visual_patterns = {
            'trend_direction': self._detect_visual_trend(gray),
            'support_resistance': self._detect_visual_levels(gray),
            'pattern_type': self._identify_visual_patterns(gray),
            'chart_quality': self._assess_chart_quality(gray),
            'confidence': 0.6  # Visual analysis has lower confidence
        }
        
        return visual_patterns
    
    def _analyze_with_pillow(self, image_path: str) -> Dict[str, Any]:
        """Analyze with Pillow only (basic functionality)"""
        # Load image with Pillow
        img = Image.open(image_path)
        if img.mode != 'L':
            img = img.convert('L')  # Convert to grayscale
        
        # Convert to numpy array
        gray = np.array(img)
        
        # Basic visual analysis (simplified without OpenCV)
        visual_patterns = {
            'trend_direction': self._detect_basic_trend(gray),
            'support_resistance': {'levels': [], 'count': 0},
            'pattern_type': self._identify_basic_patterns(gray),
            'chart_quality': self._assess_basic_quality(gray),
            'confidence': 0.4  # Lower confidence without OpenCV
        }
        
        return visual_patterns
    
    def _detect_basic_trend(self, gray_img: np.ndarray) -> str:
        """Detect trend using basic image analysis (no OpenCV)"""
        try:
            height, width = gray_img.shape
            
            # Analyze brightness changes from left to right
            left_third = gray_img[:, :width//3].mean()
            right_third = gray_img[:, 2*width//3:].mean()
            
            # Simple trend detection based on brightness
            if right_third > left_third * 1.05:
                return 'BULLISH'
            elif right_third < left_third * 0.95:
                return 'BEARISH'
            else:
                return 'SIDEWAYS'
                
        except Exception as e:
            logger.error(f"Basic trend detection error: {e}")
            return 'UNKNOWN'
    
    def _identify_basic_patterns(self, gray_img: np.ndarray) -> str:
        """Identify basic patterns without OpenCV"""
        try:
            # Simple pattern recognition based on image variance
            variance = np.var(gray_img)
            
            if variance < 1000:
                return 'CONSOLIDATION'
            elif variance > 5000:
                return 'VOLATILE'
            else:
                return 'TRENDING'
                
        except Exception as e:
            logger.error(f"Basic pattern identification error: {e}")
            return 'UNKNOWN'
    
    def _assess_basic_quality(self, gray_img: np.ndarray) -> str:
        """Assess chart quality without OpenCV"""
        try:
            height, width = gray_img.shape
            
            if width < 400 or height < 300:
                return 'TOO_SMALL'
            
            # Simple quality check based on contrast
            contrast = gray_img.max() - gray_img.min()
            
            if contrast < 50:
                return 'LOW_CONTRAST'
            elif contrast > 200:
                return 'GOOD'
            else:
                return 'ACCEPTABLE'
                
        except Exception as e:
            logger.error(f"Basic quality assessment error: {e}")
            return 'UNKNOWN'

    def _detect_visual_trend(self, gray_img: np.ndarray) -> str:
        """Detect trend direction from image"""
        try:
            # Simple edge detection to find trend
            edges = cv2.Canny(gray_img, 50, 150)
            
            # Find lines using Hough transform
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=20)
            
            if lines is not None:
                # Analyze line angles
                upward_lines = 0
                downward_lines = 0
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    if x2 - x1 != 0:
                        angle = np.arctan((y2 - y1) / (x2 - x1)) * 180 / np.pi
                        if -45 < angle < -10:  # Upward trend (negative angle in image coords)
                            upward_lines += 1
                        elif 10 < angle < 45:   # Downward trend
                            downward_lines += 1
                
                if upward_lines > downward_lines:
                    return 'BULLISH'
                elif downward_lines > upward_lines:
                    return 'BEARISH'
            
            return 'SIDEWAYS'
            
        except Exception as e:
            logger.error(f"Visual trend detection error: {e}")
            return 'UNKNOWN'
    
    def _detect_visual_levels(self, gray_img: np.ndarray) -> Dict[str, Any]:
        """Detect support/resistance levels visually"""
        try:
            # Find horizontal lines
            edges = cv2.Canny(gray_img, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            
            horizontal_lines = []
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    if abs(y2 - y1) < 10:  # Horizontal line
                        horizontal_lines.append({
                            'y_position': (y1 + y2) // 2,
                            'length': abs(x2 - x1),
                            'strength': abs(x2 - x1) / gray_img.shape[1]
                        })
            
            # Convert numpy integers to regular Python integers
            clean_levels = []
            for level in horizontal_lines[:5]:
                clean_levels.append({
                    'y_position': int(level['y_position']),
                    'length': int(level['length']),
                    'strength': float(level['strength'])
                })
            
            return {
                'levels': clean_levels,
                'count': len(horizontal_lines)
            }
            
        except Exception as e:
            logger.error(f"Visual level detection error: {e}")
            return {'levels': [], 'count': 0}
    
    def _identify_visual_patterns(self, gray_img: np.ndarray) -> str:
        """Identify chart patterns visually"""
        try:
            # Simple pattern recognition based on image characteristics
            height, width = gray_img.shape
            
            # Analyze image variance to determine pattern type
            variance = np.var(gray_img)
            
            if variance < 1000:
                return 'CONSOLIDATION'
            elif variance > 5000:
                return 'VOLATILE'
            else:
                return 'TRENDING'
                
        except Exception as e:
            logger.error(f"Visual pattern identification error: {e}")
            return 'UNKNOWN'
    
    def _assess_chart_quality(self, gray_img: np.ndarray) -> str:
        """Assess the quality of the uploaded chart"""
        try:
            # Check image clarity and size
            height, width = gray_img.shape
            
            if width < 400 or height < 300:
                return 'TOO_SMALL'
            
            # Check for blur (using Laplacian variance)
            laplacian_var = float(cv2.Laplacian(gray_img, cv2.CV_64F).var())
            
            if laplacian_var < 100:
                return 'BLURRY'
            elif laplacian_var > 500:
                return 'GOOD'
            else:
                return 'ACCEPTABLE'
                
        except Exception as e:
            logger.error(f"Chart quality assessment error: {e}")
            return 'UNKNOWN'
    
    def _get_real_price_prediction(self, symbol: str) -> Dict[str, Any]:
        """Get advanced SMC prediction using real price data from API"""
        try:
            # Get real price data
            multi_tf_data = self.data_manager.get_multi_timeframe_data(symbol, ['1h', '4h'], 200)
            
            if not multi_tf_data or '1h' not in multi_tf_data:
                return {
                    'error': 'No real price data available',
                    'direction': 'UNKNOWN',
                    'confidence': 0,
                    'current_price': 0
                }
            
            # Perform advanced SMC analysis on real data
            df_1h = multi_tf_data['1h']
            df_4h = multi_tf_data.get('4h', None)
            
            # SMC Analysis
            smc_analysis = self._perform_smc_analysis(df_1h, df_4h)
            
            # Traditional technical analysis
            technical_analysis = self.technical_analyzer.analyze(df_1h=df_1h, df_4h=df_4h)
            
            # Combine SMC and technical analysis
            combined_confidence = self._calculate_combined_confidence(smc_analysis, technical_analysis)
            final_direction = self._determine_final_direction(smc_analysis, technical_analysis)
            
            return {
                'direction': final_direction,
                'confidence': combined_confidence,
                'current_price': float(df_1h['close'].iloc[-1]) if not df_1h.empty else 0,
                'meets_threshold': combined_confidence >= 70,
                'smc_analysis': smc_analysis,
                'technical_analysis': technical_analysis.get('advanced_analysis', {}),
                'data_source': 'REAL_API_DATA_WITH_SMC',
                'trend_continuation': self._analyze_trend_continuation(smc_analysis),
                'next_direction': self._predict_next_direction(smc_analysis)
            }
            
        except Exception as e:
            logger.error(f"Real price prediction error: {e}")
            return {
                'error': str(e),
                'direction': 'UNKNOWN',
                'confidence': 0,
                'current_price': 0
            }
    
    def _perform_smc_analysis(self, df_1h: pd.DataFrame, df_4h: pd.DataFrame = None) -> Dict[str, Any]:
        """Perform comprehensive Smart Money Concepts analysis"""
        try:
            smc_results = {
                'market_structure_shift': self._detect_market_structure_shift(df_1h),
                'order_blocks': self._identify_order_blocks(df_1h),
                'qmlr_pattern': self._detect_qmlr_pattern(df_1h),
                'support_resistance': self._identify_smart_sr_levels(df_1h),
                'fair_value_gaps': self._detect_fair_value_gaps(df_1h),
                'inverse_fair_value_gaps': self._detect_inverse_fair_value_gaps(df_1h),
                'liquidity_analysis': self._analyze_liquidity(df_1h),
                'liquidity_sweep': self._detect_liquidity_sweep(df_1h),
                'liquidity_grab': self._detect_liquidity_grab(df_1h),
                'change_of_character': self._detect_change_of_character(df_1h),
                'smart_money_divergence': self._detect_smart_money_divergence(df_1h),
                'overall_bias': 'NEUTRAL',
                'confidence_score': 0
            }
            
            # Calculate overall bias and confidence
            smc_results['overall_bias'] = self._calculate_smc_bias(smc_results)
            smc_results['confidence_score'] = self._calculate_smc_confidence(smc_results)
            
            return smc_results
            
        except Exception as e:
            logger.error(f"SMC analysis error: {e}")
            return {'error': str(e), 'overall_bias': 'UNKNOWN', 'confidence_score': 0}
    
    def _detect_market_structure_shift(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Market Structure Shift (MSS)"""
        try:
            if len(df) < 20:
                return {'detected': False, 'type': 'INSUFFICIENT_DATA'}
            
            # Calculate swing highs and lows
            highs = df['high'].rolling(window=5, center=True).max()
            lows = df['low'].rolling(window=5, center=True).min()
            
            swing_highs = df[df['high'] == highs]['high'].dropna()
            swing_lows = df[df['low'] == lows]['low'].dropna()
            
            # Check for structure breaks
            recent_highs = swing_highs.tail(3)
            recent_lows = swing_lows.tail(3)
            
            bullish_mss = False
            bearish_mss = False
            
            if len(recent_lows) >= 2:
                # Bullish MSS: Higher Low formation
                if recent_lows.iloc[-1] > recent_lows.iloc[-2]:
                    bullish_mss = True
            
            if len(recent_highs) >= 2:
                # Bearish MSS: Lower High formation
                if recent_highs.iloc[-1] < recent_highs.iloc[-2]:
                    bearish_mss = True
            
            mss_type = 'BULLISH' if bullish_mss else 'BEARISH' if bearish_mss else 'NONE'
            
            return {
                'detected': bullish_mss or bearish_mss,
                'type': mss_type,
                'strength': 'HIGH' if bullish_mss or bearish_mss else 'LOW',
                'recent_swing_highs': recent_highs.tolist()[-3:] if len(recent_highs) >= 3 else [],
                'recent_swing_lows': recent_lows.tolist()[-3:] if len(recent_lows) >= 3 else []
            }
            
        except Exception as e:
            logger.error(f"MSS detection error: {e}")
            return {'detected': False, 'type': 'ERROR', 'error': str(e)}
    
    def _identify_order_blocks(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify Order Blocks (OB)"""
        try:
            if len(df) < 10:
                return {'bullish_obs': [], 'bearish_obs': [], 'count': 0}
            
            bullish_obs = []
            bearish_obs = []
            
            # Look for strong moves followed by retracements
            for i in range(5, len(df) - 5):
                # Bullish Order Block: Strong up move after consolidation
                prev_candles = df.iloc[i-3:i+1]
                next_candles = df.iloc[i:i+5]
                
                # Check for strong bullish candle
                current_candle = df.iloc[i]
                body_size = abs(current_candle['close'] - current_candle['open'])
                candle_range = current_candle['high'] - current_candle['low']
                
                if body_size > candle_range * 0.7 and current_candle['close'] > current_candle['open']:
                    # Check if price moved significantly higher after
                    if next_candles['high'].max() > current_candle['high'] * 1.002:
                        bullish_obs.append({
                            'index': i,
                            'high': float(current_candle['high']),
                            'low': float(current_candle['low']),
                            'open': float(current_candle['open']),
                            'close': float(current_candle['close']),
                            'strength': float(body_size / candle_range)
                        })
                
                # Bearish Order Block: Strong down move after consolidation
                if body_size > candle_range * 0.7 and current_candle['close'] < current_candle['open']:
                    # Check if price moved significantly lower after
                    if next_candles['low'].min() < current_candle['low'] * 0.998:
                        bearish_obs.append({
                            'index': i,
                            'high': float(current_candle['high']),
                            'low': float(current_candle['low']),
                            'open': float(current_candle['open']),
                            'close': float(current_candle['close']),
                            'strength': float(body_size / candle_range)
                        })
            
            return {
                'bullish_obs': bullish_obs[-5:],  # Keep last 5
                'bearish_obs': bearish_obs[-5:],  # Keep last 5
                'count': len(bullish_obs) + len(bearish_obs),
                'recent_bias': 'BULLISH' if len(bullish_obs[-3:]) > len(bearish_obs[-3:]) else 'BEARISH'
            }
            
        except Exception as e:
            logger.error(f"Order block identification error: {e}")
            return {'bullish_obs': [], 'bearish_obs': [], 'count': 0, 'error': str(e)}
    
    def _detect_qmlr_pattern(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Quasimodo (QMLR) pattern"""
        try:
            if len(df) < 15:
                return {'detected': False, 'type': 'INSUFFICIENT_DATA'}
            
            # Look for QMLR pattern: Left Shoulder - Head - Right Shoulder formation
            qmlr_patterns = []
            
            for i in range(7, len(df) - 7):
                # Get potential pattern points
                left_shoulder = df.iloc[i-6:i-3]
                head = df.iloc[i-3:i+1]
                right_shoulder = df.iloc[i+1:i+4]
                
                # Bullish QMLR (Inverse Head and Shoulders)
                ls_low = left_shoulder['low'].min()
                head_low = head['low'].min()
                rs_low = right_shoulder['low'].min()
                
                if head_low < ls_low and head_low < rs_low and abs(ls_low - rs_low) < (ls_low * 0.01):
                    qmlr_patterns.append({
                        'type': 'BULLISH_QMLR',
                        'left_shoulder': float(ls_low),
                        'head': float(head_low),
                        'right_shoulder': float(rs_low),
                        'neckline': float((left_shoulder['high'].max() + right_shoulder['high'].max()) / 2),
                        'index': i,
                        'strength': 'HIGH'
                    })
                
                # Bearish QMLR (Head and Shoulders)
                ls_high = left_shoulder['high'].max()
                head_high = head['high'].max()
                rs_high = right_shoulder['high'].max()
                
                if head_high > ls_high and head_high > rs_high and abs(ls_high - rs_high) < (ls_high * 0.01):
                    qmlr_patterns.append({
                        'type': 'BEARISH_QMLR',
                        'left_shoulder': float(ls_high),
                        'head': float(head_high),
                        'right_shoulder': float(rs_high),
                        'neckline': float((left_shoulder['low'].min() + right_shoulder['low'].min()) / 2),
                        'index': i,
                        'strength': 'HIGH'
                    })
            
            recent_pattern = qmlr_patterns[-1] if qmlr_patterns else None
            
            return {
                'detected': len(qmlr_patterns) > 0,
                'patterns': qmlr_patterns[-3:],  # Keep last 3
                'recent_pattern': recent_pattern,
                'bias': recent_pattern['type'].split('_')[0] if recent_pattern else 'NEUTRAL'
            }
            
        except Exception as e:
            logger.error(f"QMLR detection error: {e}")
            return {'detected': False, 'type': 'ERROR', 'error': str(e)}
    
    def _identify_smart_sr_levels(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify Smart Support and Resistance levels"""
        try:
            if len(df) < 20:
                return {'support_levels': [], 'resistance_levels': [], 'count': 0}
            
            # Calculate pivot points
            window = 5
            support_levels = []
            resistance_levels = []
            
            for i in range(window, len(df) - window):
                # Support level: Local low
                if df['low'].iloc[i] == df['low'].iloc[i-window:i+window+1].min():
                    # Check if this level was tested multiple times
                    level_price = df['low'].iloc[i]
                    tests = 0
                    
                    for j in range(max(0, i-20), min(len(df), i+20)):
                        if abs(df['low'].iloc[j] - level_price) < level_price * 0.002:
                            tests += 1
                    
                    if tests >= 2:  # At least 2 tests
                        support_levels.append({
                            'price': float(level_price),
                            'index': i,
                            'tests': tests,
                            'strength': 'HIGH' if tests >= 3 else 'MEDIUM'
                        })
                
                # Resistance level: Local high
                if df['high'].iloc[i] == df['high'].iloc[i-window:i+window+1].max():
                    level_price = df['high'].iloc[i]
                    tests = 0
                    
                    for j in range(max(0, i-20), min(len(df), i+20)):
                        if abs(df['high'].iloc[j] - level_price) < level_price * 0.002:
                            tests += 1
                    
                    if tests >= 2:
                        resistance_levels.append({
                            'price': float(level_price),
                            'index': i,
                            'tests': tests,
                            'strength': 'HIGH' if tests >= 3 else 'MEDIUM'
                        })
            
            return {
                'support_levels': support_levels[-5:],  # Keep last 5
                'resistance_levels': resistance_levels[-5:],  # Keep last 5
                'count': len(support_levels) + len(resistance_levels),
                'nearest_support': support_levels[-1] if support_levels else None,
                'nearest_resistance': resistance_levels[-1] if resistance_levels else None
            }
            
        except Exception as e:
            logger.error(f"S/R level identification error: {e}")
            return {'support_levels': [], 'resistance_levels': [], 'count': 0, 'error': str(e)}
    
    def _detect_fair_value_gaps(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Fair Value Gaps (FVG)"""
        try:
            if len(df) < 5:
                return {'bullish_fvgs': [], 'bearish_fvgs': [], 'count': 0}
            
            bullish_fvgs = []
            bearish_fvgs = []
            
            for i in range(2, len(df)):
                # Bullish FVG: Gap between candle 1 high and candle 3 low
                if i >= 2:
                    candle1 = df.iloc[i-2]
                    candle2 = df.iloc[i-1]
                    candle3 = df.iloc[i]
                    
                    # Bullish FVG condition
                    if candle1['high'] < candle3['low'] and candle2['close'] > candle2['open']:
                        bullish_fvgs.append({
                            'start_index': i-2,
                            'end_index': i,
                            'gap_high': float(candle3['low']),
                            'gap_low': float(candle1['high']),
                            'gap_size': float(candle3['low'] - candle1['high']),
                            'filled': False
                        })
                    
                    # Bearish FVG condition
                    if candle1['low'] > candle3['high'] and candle2['close'] < candle2['open']:
                        bearish_fvgs.append({
                            'start_index': i-2,
                            'end_index': i,
                            'gap_high': float(candle1['low']),
                            'gap_low': float(candle3['high']),
                            'gap_size': float(candle1['low'] - candle3['high']),
                            'filled': False
                        })
            
            return {
                'bullish_fvgs': bullish_fvgs[-5:],  # Keep last 5
                'bearish_fvgs': bearish_fvgs[-5:],  # Keep last 5
                'count': len(bullish_fvgs) + len(bearish_fvgs),
                'recent_bias': 'BULLISH' if len(bullish_fvgs[-3:]) > len(bearish_fvgs[-3:]) else 'BEARISH'
            }
            
        except Exception as e:
            logger.error(f"FVG detection error: {e}")
            return {'bullish_fvgs': [], 'bearish_fvgs': [], 'count': 0, 'error': str(e)}
    
    def _detect_inverse_fair_value_gaps(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Inverse Fair Value Gaps (IFVG)"""
        try:
            # IFVG is essentially the opposite of FVG - areas where price moved too fast and left gaps
            fvg_result = self._detect_fair_value_gaps(df)
            
            # Inverse the logic - what was bullish FVG becomes bearish IFVG signal
            return {
                'bullish_ifvgs': fvg_result.get('bearish_fvgs', []),
                'bearish_ifvgs': fvg_result.get('bullish_fvgs', []),
                'count': fvg_result.get('count', 0),
                'recent_bias': 'BEARISH' if fvg_result.get('recent_bias') == 'BULLISH' else 'BULLISH'
            }
            
        except Exception as e:
            logger.error(f"IFVG detection error: {e}")
            return {'bullish_ifvgs': [], 'bearish_ifvgs': [], 'count': 0, 'error': str(e)}
    
    def _analyze_liquidity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze liquidity zones and levels"""
        try:
            if len(df) < 10:
                return {'liquidity_zones': [], 'high_liquidity_areas': [], 'count': 0}
            
            liquidity_zones = []
            
            # Identify areas with high volume and tight ranges (liquidity pools)
            for i in range(5, len(df) - 5):
                window = df.iloc[i-5:i+5]
                
                # High liquidity characteristics
                avg_volume = window['volume'].mean() if 'volume' in df.columns else 1000
                current_volume = df['volume'].iloc[i] if 'volume' in df.columns else 1000
                price_range = window['high'].max() - window['low'].min()
                avg_range = (window['high'] - window['low']).mean()
                
                # Liquidity zone: High volume, tight range
                if current_volume > avg_volume * 1.5 and price_range < avg_range * 0.8:
                    liquidity_zones.append({
                        'index': i,
                        'price_level': float((df['high'].iloc[i] + df['low'].iloc[i]) / 2),
                        'volume_ratio': float(current_volume / avg_volume) if avg_volume > 0 else 1,
                        'range_compression': float(price_range / avg_range) if avg_range > 0 else 1,
                        'strength': 'HIGH' if current_volume > avg_volume * 2 else 'MEDIUM'
                    })
            
            return {
                'liquidity_zones': liquidity_zones[-5:],  # Keep last 5
                'high_liquidity_areas': [zone for zone in liquidity_zones if zone['strength'] == 'HIGH'][-3:],
                'count': len(liquidity_zones),
                'current_liquidity': 'HIGH' if liquidity_zones and liquidity_zones[-1]['strength'] == 'HIGH' else 'MEDIUM'
            }
            
        except Exception as e:
            logger.error(f"Liquidity analysis error: {e}")
            return {'liquidity_zones': [], 'high_liquidity_areas': [], 'count': 0, 'error': str(e)}
    
    def _detect_liquidity_sweep(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Liquidity Sweep patterns"""
        try:
            if len(df) < 10:
                return {'sweeps': [], 'recent_sweep': None, 'count': 0}
            
            sweeps = []
            
            for i in range(5, len(df) - 2):
                # Look for sweep patterns
                current = df.iloc[i]
                previous = df.iloc[i-1]
                next_candle = df.iloc[i+1]
                
                # Bullish sweep: Price breaks below previous low then quickly recovers
                prev_low = df.iloc[i-5:i]['low'].min()
                if (current['low'] < prev_low and 
                    current['close'] > current['open'] and
                    next_candle['low'] > current['low']):
                    
                    sweeps.append({
                        'type': 'BULLISH_SWEEP',
                        'index': i,
                        'sweep_level': float(current['low']),
                        'recovery_level': float(current['close']),
                        'strength': 'HIGH' if current['close'] > prev_low else 'MEDIUM'
                    })
                
                # Bearish sweep: Price breaks above previous high then quickly falls
                prev_high = df.iloc[i-5:i]['high'].max()
                if (current['high'] > prev_high and 
                    current['close'] < current['open'] and
                    next_candle['high'] < current['high']):
                    
                    sweeps.append({
                        'type': 'BEARISH_SWEEP',
                        'index': i,
                        'sweep_level': float(current['high']),
                        'recovery_level': float(current['close']),
                        'strength': 'HIGH' if current['close'] < prev_high else 'MEDIUM'
                    })
            
            return {
                'sweeps': sweeps[-5:],  # Keep last 5
                'recent_sweep': sweeps[-1] if sweeps else None,
                'count': len(sweeps),
                'bias': sweeps[-1]['type'].split('_')[0] if sweeps else 'NEUTRAL'
            }
            
        except Exception as e:
            logger.error(f"Liquidity sweep detection error: {e}")
            return {'sweeps': [], 'recent_sweep': None, 'count': 0, 'error': str(e)}
    
    def _detect_liquidity_grab(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Liquidity Grab patterns"""
        try:
            if len(df) < 8:
                return {'grabs': [], 'recent_grab': None, 'count': 0}
            
            grabs = []
            
            for i in range(3, len(df) - 3):
                current = df.iloc[i]
                
                # Bullish liquidity grab: Wick below support then strong close above
                support_level = df.iloc[i-3:i]['low'].min()
                if (current['low'] < support_level and 
                    current['close'] > support_level and
                    (current['close'] - current['low']) > (current['high'] - current['low']) * 0.6):
                    
                    grabs.append({
                        'type': 'BULLISH_GRAB',
                        'index': i,
                        'grab_level': float(current['low']),
                        'close_level': float(current['close']),
                        'wick_size': float(current['close'] - current['low']),
                        'strength': 'HIGH'
                    })
                
                # Bearish liquidity grab: Wick above resistance then strong close below
                resistance_level = df.iloc[i-3:i]['high'].max()
                if (current['high'] > resistance_level and 
                    current['close'] < resistance_level and
                    (current['high'] - current['close']) > (current['high'] - current['low']) * 0.6):
                    
                    grabs.append({
                        'type': 'BEARISH_GRAB',
                        'index': i,
                        'grab_level': float(current['high']),
                        'close_level': float(current['close']),
                        'wick_size': float(current['high'] - current['close']),
                        'strength': 'HIGH'
                    })
            
            return {
                'grabs': grabs[-5:],  # Keep last 5
                'recent_grab': grabs[-1] if grabs else None,
                'count': len(grabs),
                'bias': grabs[-1]['type'].split('_')[0] if grabs else 'NEUTRAL'
            }
            
        except Exception as e:
            logger.error(f"Liquidity grab detection error: {e}")
            return {'grabs': [], 'recent_grab': None, 'count': 0, 'error': str(e)}
    
    def _detect_change_of_character(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Change of Character (CHoCH)"""
        try:
            if len(df) < 15:
                return {'detected': False, 'type': 'INSUFFICIENT_DATA'}
            
            # Look for significant changes in market behavior
            recent_data = df.tail(10)
            older_data = df.iloc[-20:-10] if len(df) >= 20 else df.iloc[:-10]
            
            if len(older_data) == 0:
                return {'detected': False, 'type': 'INSUFFICIENT_DATA'}
            
            # Calculate characteristics
            recent_volatility = recent_data['high'].subtract(recent_data['low']).mean()
            older_volatility = older_data['high'].subtract(older_data['low']).mean()
            
            recent_trend = (recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]) / recent_data['close'].iloc[0]
            older_trend = (older_data['close'].iloc[-1] - older_data['close'].iloc[0]) / older_data['close'].iloc[0]
            
            # Detect change of character
            volatility_change = abs(recent_volatility - older_volatility) / older_volatility if older_volatility > 0 else 0
            trend_change = recent_trend * older_trend < 0  # Opposite signs
            
            choch_detected = volatility_change > 0.3 or trend_change
            
            choch_type = 'NONE'
            if choch_detected:
                if recent_trend > 0 and older_trend < 0:
                    choch_type = 'BEARISH_TO_BULLISH'
                elif recent_trend < 0 and older_trend > 0:
                    choch_type = 'BULLISH_TO_BEARISH'
                elif volatility_change > 0.5:
                    choch_type = 'VOLATILITY_CHANGE'
            
            return {
                'detected': choch_detected,
                'type': choch_type,
                'volatility_change': float(volatility_change),
                'trend_change': trend_change,
                'recent_trend': float(recent_trend),
                'older_trend': float(older_trend),
                'strength': 'HIGH' if volatility_change > 0.5 or abs(recent_trend - older_trend) > 0.05 else 'MEDIUM'
            }
            
        except Exception as e:
            logger.error(f"CHoCH detection error: {e}")
            return {'detected': False, 'type': 'ERROR', 'error': str(e)}
    
    def _detect_smart_money_divergence(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect Smart Money Divergence (SMD)"""
        try:
            if len(df) < 20:
                return {'detected': False, 'type': 'INSUFFICIENT_DATA'}
            
            # Calculate price momentum and volume momentum
            price_momentum = df['close'].pct_change(5).tail(10)
            volume_momentum = df['volume'].pct_change(5).tail(10) if 'volume' in df.columns else pd.Series([0]*10)
            
            # Look for divergence between price and volume
            divergences = []
            
            for i in range(5, len(price_momentum)):
                price_trend = price_momentum.iloc[i-5:i].mean()
                volume_trend = volume_momentum.iloc[i-5:i].mean()
                
                # Bullish divergence: Price down, volume up
                if price_trend < -0.01 and volume_trend > 0.1:
                    divergences.append({
                        'type': 'BULLISH_DIVERGENCE',
                        'index': i,
                        'price_momentum': float(price_trend),
                        'volume_momentum': float(volume_trend),
                        'strength': 'HIGH' if abs(price_trend) > 0.02 else 'MEDIUM'
                    })
                
                # Bearish divergence: Price up, volume down
                elif price_trend > 0.01 and volume_trend < -0.1:
                    divergences.append({
                        'type': 'BEARISH_DIVERGENCE',
                        'index': i,
                        'price_momentum': float(price_trend),
                        'volume_momentum': float(volume_trend),
                        'strength': 'HIGH' if abs(price_trend) > 0.02 else 'MEDIUM'
                    })
            
            return {
                'detected': len(divergences) > 0,
                'divergences': divergences[-3:],  # Keep last 3
                'recent_divergence': divergences[-1] if divergences else None,
                'count': len(divergences),
                'bias': divergences[-1]['type'].split('_')[0] if divergences else 'NEUTRAL'
            }
            
        except Exception as e:
            logger.error(f"SMD detection error: {e}")
            return {'detected': False, 'type': 'ERROR', 'error': str(e)}
    
    def _calculate_smc_bias(self, smc_results: Dict[str, Any]) -> str:
        """Calculate overall SMC bias"""
        try:
            bullish_signals = 0
            bearish_signals = 0
            
            # Market Structure Shift
            mss = smc_results.get('market_structure_shift', {})
            if mss.get('type') == 'BULLISH':
                bullish_signals += 2
            elif mss.get('type') == 'BEARISH':
                bearish_signals += 2
            
            # Order Blocks
            obs = smc_results.get('order_blocks', {})
            if obs.get('recent_bias') == 'BULLISH':
                bullish_signals += 1
            elif obs.get('recent_bias') == 'BEARISH':
                bearish_signals += 1
            
            # QMLR Pattern
            qmlr = smc_results.get('qmlr_pattern', {})
            if qmlr.get('bias') == 'BULLISH':
                bullish_signals += 2
            elif qmlr.get('bias') == 'BEARISH':
                bearish_signals += 2
            
            # Fair Value Gaps
            fvg = smc_results.get('fair_value_gaps', {})
            if fvg.get('recent_bias') == 'BULLISH':
                bullish_signals += 1
            elif fvg.get('recent_bias') == 'BEARISH':
                bearish_signals += 1
            
            # Liquidity Sweep
            sweep = smc_results.get('liquidity_sweep', {})
            if sweep.get('bias') == 'BULLISH':
                bullish_signals += 1
            elif sweep.get('bias') == 'BEARISH':
                bearish_signals += 1
            
            # Liquidity Grab
            grab = smc_results.get('liquidity_grab', {})
            if grab.get('bias') == 'BULLISH':
                bullish_signals += 1
            elif grab.get('bias') == 'BEARISH':
                bearish_signals += 1
            
            # Change of Character
            choch = smc_results.get('change_of_character', {})
            if choch.get('type') == 'BEARISH_TO_BULLISH':
                bullish_signals += 2
            elif choch.get('type') == 'BULLISH_TO_BEARISH':
                bearish_signals += 2
            
            # Smart Money Divergence
            smd = smc_results.get('smart_money_divergence', {})
            if smd.get('bias') == 'BULLISH':
                bullish_signals += 1
            elif smd.get('bias') == 'BEARISH':
                bearish_signals += 1
            
            # Determine overall bias
            if bullish_signals > bearish_signals + 1:
                return 'BULLISH'
            elif bearish_signals > bullish_signals + 1:
                return 'BEARISH'
            else:
                return 'NEUTRAL'
                
        except Exception as e:
            logger.error(f"SMC bias calculation error: {e}")
            return 'NEUTRAL'
    
    def _calculate_smc_confidence(self, smc_results: Dict[str, Any]) -> float:
        """Calculate SMC confidence score"""
        try:
            confidence_factors = []
            
            # Add confidence based on each SMC component
            mss = smc_results.get('market_structure_shift', {})
            if mss.get('detected'):
                confidence_factors.append(85 if mss.get('strength') == 'HIGH' else 70)
            
            obs = smc_results.get('order_blocks', {})
            if obs.get('count', 0) > 0:
                confidence_factors.append(75)
            
            qmlr = smc_results.get('qmlr_pattern', {})
            if qmlr.get('detected'):
                confidence_factors.append(80)
            
            fvg = smc_results.get('fair_value_gaps', {})
            if fvg.get('count', 0) > 0:
                confidence_factors.append(70)
            
            sweep = smc_results.get('liquidity_sweep', {})
            if sweep.get('count', 0) > 0:
                confidence_factors.append(75)
            
            grab = smc_results.get('liquidity_grab', {})
            if grab.get('count', 0) > 0:
                confidence_factors.append(75)
            
            choch = smc_results.get('change_of_character', {})
            if choch.get('detected'):
                confidence_factors.append(80 if choch.get('strength') == 'HIGH' else 65)
            
            smd = smc_results.get('smart_money_divergence', {})
            if smd.get('detected'):
                confidence_factors.append(70)
            
            # Calculate weighted average
            if confidence_factors:
                return sum(confidence_factors) / len(confidence_factors)
            else:
                return 50  # Neutral confidence
                
        except Exception as e:
            logger.error(f"SMC confidence calculation error: {e}")
            return 50
    
    def _calculate_combined_confidence(self, smc_analysis: Dict, technical_analysis: Dict) -> float:
        """Calculate combined confidence from SMC and technical analysis"""
        try:
            smc_confidence = smc_analysis.get('confidence_score', 50)
            tech_confidence = technical_analysis.get('confidence', 50)
            
            # Weight SMC analysis higher (70% SMC, 30% Technical)
            combined = (smc_confidence * 0.7) + (tech_confidence * 0.3)
            
            return min(95, max(5, combined))  # Clamp between 5-95
            
        except Exception as e:
            logger.error(f"Combined confidence calculation error: {e}")
            return 50
    
    def _determine_final_direction(self, smc_analysis: Dict, technical_analysis: Dict) -> str:
        """Determine final direction based on SMC and technical analysis"""
        try:
            smc_bias = smc_analysis.get('overall_bias', 'NEUTRAL')
            tech_direction = technical_analysis.get('direction', 'UNKNOWN')
            
            # If both agree, high confidence
            if smc_bias == tech_direction and smc_bias in ['BULLISH', 'BEARISH']:
                return 'UP' if smc_bias == 'BULLISH' else 'DOWN'
            
            # If SMC has strong signal, prioritize it
            smc_confidence = smc_analysis.get('confidence_score', 50)
            if smc_confidence >= 75 and smc_bias in ['BULLISH', 'BEARISH']:
                return 'UP' if smc_bias == 'BULLISH' else 'DOWN'
            
            # If technical analysis has strong signal
            tech_confidence = technical_analysis.get('confidence', 50)
            if tech_confidence >= 75 and tech_direction in ['UP', 'DOWN']:
                return tech_direction
            
            return 'UNKNOWN'
            
        except Exception as e:
            logger.error(f"Final direction determination error: {e}")
            return 'UNKNOWN'
    
    def _analyze_trend_continuation(self, smc_analysis: Dict) -> Dict[str, Any]:
        """Analyze trend continuation probability"""
        try:
            continuation_factors = []
            
            # Market Structure Shift
            mss = smc_analysis.get('market_structure_shift', {})
            if mss.get('detected') and mss.get('strength') == 'HIGH':
                continuation_factors.append('STRONG_MSS')
            
            # Order Blocks alignment
            obs = smc_analysis.get('order_blocks', {})
            if obs.get('count', 0) >= 2:
                continuation_factors.append('MULTIPLE_ORDER_BLOCKS')
            
            # Fair Value Gaps
            fvg = smc_analysis.get('fair_value_gaps', {})
            if fvg.get('count', 0) >= 2:
                continuation_factors.append('MULTIPLE_FVGS')
            
            # Liquidity patterns
            sweep = smc_analysis.get('liquidity_sweep', {})
            grab = smc_analysis.get('liquidity_grab', {})
            if sweep.get('count', 0) > 0 or grab.get('count', 0) > 0:
                continuation_factors.append('LIQUIDITY_ACTIVITY')
            
            continuation_probability = len(continuation_factors) * 20  # Each factor adds 20%
            continuation_probability = min(90, continuation_probability)
            
            return {
                'probability': continuation_probability,
                'factors': continuation_factors,
                'likely_continuation': continuation_probability >= 60,
                'strength': 'HIGH' if continuation_probability >= 80 else 'MEDIUM' if continuation_probability >= 60 else 'LOW'
            }
            
        except Exception as e:
            logger.error(f"Trend continuation analysis error: {e}")
            return {'probability': 50, 'factors': [], 'likely_continuation': False, 'strength': 'LOW'}
    
    def _predict_next_direction(self, smc_analysis: Dict) -> Dict[str, Any]:
        """Predict next direction based on SMC analysis"""
        try:
            direction_signals = {
                'BULLISH': 0,
                'BEARISH': 0,
                'NEUTRAL': 0
            }
            
            # Analyze each SMC component for next direction
            components = [
                'market_structure_shift',
                'order_blocks', 
                'qmlr_pattern',
                'fair_value_gaps',
                'liquidity_sweep',
                'liquidity_grab',
                'change_of_character',
                'smart_money_divergence'
            ]
            
            for component in components:
                comp_data = smc_analysis.get(component, {})
                
                if component == 'market_structure_shift':
                    if comp_data.get('type') == 'BULLISH':
                        direction_signals['BULLISH'] += 2
                    elif comp_data.get('type') == 'BEARISH':
                        direction_signals['BEARISH'] += 2
                
                elif component in ['order_blocks', 'fair_value_gaps', 'liquidity_sweep', 'liquidity_grab']:
                    bias = comp_data.get('recent_bias') or comp_data.get('bias', 'NEUTRAL')
                    if bias == 'BULLISH':
                        direction_signals['BULLISH'] += 1
                    elif bias == 'BEARISH':
                        direction_signals['BEARISH'] += 1
                
                elif component == 'qmlr_pattern':
                    if comp_data.get('bias') == 'BULLISH':
                        direction_signals['BULLISH'] += 2
                    elif comp_data.get('bias') == 'BEARISH':
                        direction_signals['BEARISH'] += 2
                
                elif component == 'change_of_character':
                    if comp_data.get('type') == 'BEARISH_TO_BULLISH':
                        direction_signals['BULLISH'] += 2
                    elif comp_data.get('type') == 'BULLISH_TO_BEARISH':
                        direction_signals['BEARISH'] += 2
                
                elif component == 'smart_money_divergence':
                    bias = comp_data.get('bias', 'NEUTRAL')
                    if bias == 'BULLISH':
                        direction_signals['BULLISH'] += 1
                    elif bias == 'BEARISH':
                        direction_signals['BEARISH'] += 1
            
            # Determine next direction
            max_signals = max(direction_signals.values())
            if max_signals == 0:
                next_direction = 'SIDEWAYS'
                confidence = 50
            else:
                next_direction = max(direction_signals, key=direction_signals.get)
                confidence = min(95, (max_signals / sum(direction_signals.values())) * 100)
            
            return {
                'direction': 'UP' if next_direction == 'BULLISH' else 'DOWN' if next_direction == 'BEARISH' else 'SIDEWAYS',
                'confidence': confidence,
                'signal_breakdown': direction_signals,
                'timeframe': '1-4 hours',
                'key_levels': self._identify_key_levels(smc_analysis)
            }
            
        except Exception as e:
            logger.error(f"Next direction prediction error: {e}")
            return {
                'direction': 'UNKNOWN',
                'confidence': 50,
                'signal_breakdown': {'BULLISH': 0, 'BEARISH': 0, 'NEUTRAL': 0},
                'timeframe': 'unknown',
                'key_levels': []
            }
    
    def _identify_key_levels(self, smc_analysis: Dict) -> List[Dict]:
        """Identify key levels from SMC analysis"""
        try:
            key_levels = []
            
            # Support/Resistance levels
            sr_levels = smc_analysis.get('support_resistance', {})
            for support in sr_levels.get('support_levels', [])[-2:]:
                key_levels.append({
                    'type': 'SUPPORT',
                    'price': support['price'],
                    'strength': support['strength']
                })
            
            for resistance in sr_levels.get('resistance_levels', [])[-2:]:
                key_levels.append({
                    'type': 'RESISTANCE', 
                    'price': resistance['price'],
                    'strength': resistance['strength']
                })
            
            # Order Block levels
            obs = smc_analysis.get('order_blocks', {})
            for ob in obs.get('bullish_obs', [])[-2:]:
                key_levels.append({
                    'type': 'BULLISH_ORDER_BLOCK',
                    'price': (ob['high'] + ob['low']) / 2,
                    'strength': 'HIGH'
                })
            
            for ob in obs.get('bearish_obs', [])[-2:]:
                key_levels.append({
                    'type': 'BEARISH_ORDER_BLOCK',
                    'price': (ob['high'] + ob['low']) / 2,
                    'strength': 'HIGH'
                })
            
            # Fair Value Gap levels
            fvgs = smc_analysis.get('fair_value_gaps', {})
            for fvg in fvgs.get('bullish_fvgs', [])[-2:]:
                key_levels.append({
                    'type': 'BULLISH_FVG',
                    'price': (fvg['gap_high'] + fvg['gap_low']) / 2,
                    'strength': 'MEDIUM'
                })
            
            for fvg in fvgs.get('bearish_fvgs', [])[-2:]:
                key_levels.append({
                    'type': 'BEARISH_FVG',
                    'price': (fvg['gap_high'] + fvg['gap_low']) / 2,
                    'strength': 'MEDIUM'
                })
            
            # Sort by price and return top levels
            key_levels.sort(key=lambda x: x['price'])
            return key_levels[-8:]  # Return top 8 levels
            
        except Exception as e:
            logger.error(f"Key levels identification error: {e}")
            return []
    
    def _clean_for_json_serialization(self, obj):
        """
        Recursively clean data for JSON serialization
        Handles numpy types, pandas objects, datetime objects, etc.
        """
        import numpy as np
        import math
        from datetime import datetime
        
        if isinstance(obj, dict):
            return {k: self._clean_for_json_serialization(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json_serialization(item) for item in obj]
        elif isinstance(obj, tuple):
            return [self._clean_for_json_serialization(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return self._clean_for_json_serialization(obj.tolist())
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, (int, float)):
            if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
                return None
            return obj
        elif isinstance(obj, str):
            return obj
        elif obj is None:
            return None
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        elif hasattr(obj, 'tolist'):  # pandas Series/arrays
            return self._clean_for_json_serialization(obj.tolist())
        elif hasattr(obj, 'item') and hasattr(obj, 'size') and obj.size == 1:  # single numpy objects
            return self._clean_for_json_serialization(obj.item())
        elif pd.isna(obj):  # pandas NaN
            return None
        else:
            # Try to convert to string as last resort
            try:
                return str(obj)
            except:
                return None
    
    def _generate_recommendation(self, visual_analysis: Dict, real_prediction: Dict) -> Dict[str, Any]:
        """Generate final recommendation combining visual and real data analysis"""
        try:
            visual_direction = visual_analysis.get('trend_direction', 'UNKNOWN')
            real_direction = real_prediction.get('direction', 'UNKNOWN')
            real_confidence = real_prediction.get('confidence', 0)
            
            # Prioritize real data prediction
            if real_prediction.get('meets_threshold', False):
                recommendation = {
                    'final_direction': real_direction,
                    'confidence': real_confidence,
                    'basis': 'REAL_PRICE_DATA',
                    'visual_confirmation': visual_direction == real_direction,
                    'recommendation_strength': 'HIGH' if real_confidence >= 80 else 'MEDIUM'
                }
            else:
                recommendation = {
                    'final_direction': 'WAIT',
                    'confidence': 50,
                    'basis': 'INSUFFICIENT_CONFIDENCE',
                    'visual_confirmation': False,
                    'recommendation_strength': 'LOW'
                }
            
            # Add visual pattern insights
            recommendation['visual_insights'] = {
                'chart_trend': visual_direction,
                'pattern_type': visual_analysis.get('pattern_type', 'UNKNOWN'),
                'chart_quality': visual_analysis.get('chart_quality', 'UNKNOWN')
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return {
                'final_direction': 'ERROR',
                'confidence': 0,
                'basis': 'ANALYSIS_ERROR',
                'error': str(e)
            }
    
    def _get_error_analysis(self, symbol: str, error_msg: str) -> Dict[str, Any]:
        """Return error analysis structure"""
        return {
            'symbol': symbol,
            'timeframe': 'unknown',
            'visual_analysis': {
                'error': error_msg,
                'confidence': 0
            },
            'real_price_prediction': {
                'error': 'Could not fetch real price data',
                'direction': 'UNKNOWN',
                'confidence': 0
            },
            'recommendation': {
                'final_direction': 'ERROR',
                'confidence': 0,
                'basis': 'SYSTEM_ERROR'
            },
            'success': False,
            'error': error_msg
        }