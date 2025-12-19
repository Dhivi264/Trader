from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChartUpload
from .chart_analyzer import ChartVisualAnalyzer
import logging
import os

logger = logging.getLogger(__name__)


def add_cors_headers(response):
    """Add CORS headers manually for PythonAnywhere compatibility"""
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def cors_response(data, status_code=200):
    """Create a Response with CORS headers"""
    response = Response(data, status=status_code)
    return add_cors_headers(response)


def index(request):
    """Main dashboard view - Chart Upload Interface"""
    return render(request, 'predictor/index.html')


@api_view(['POST'])
@csrf_exempt
def upload_chart_analysis(request):
    """
    📊 UPLOAD CHART FOR VISUAL ANALYSIS + REAL PRICE PREDICTION
    Combines visual chart analysis with real price data for accurate predictions
    REQUIRES chart image upload
    """
    try:
        symbol = request.data.get('symbol', 'UNKNOWN')
        timeframe = request.data.get('timeframe', '1h')
        
        # Validate symbol
        if not symbol or symbol == 'UNKNOWN' or symbol.strip() == '':
            return cors_response({'error': 'Please provide a valid trading symbol (e.g., EURUSD, GBPUSD)'}, 
                          status.HTTP_400_BAD_REQUEST)
        
        symbol = symbol.upper().strip()
        
        # REQUIRE chart image upload
        if 'chart_image' not in request.FILES or not request.FILES['chart_image']:
            return cors_response({
                'error': 'Chart image is required. Please upload a chart image to perform analysis.',
                'message': 'You must upload a trading chart image before analysis can be performed.'
            }, status.HTTP_400_BAD_REQUEST)
        
        chart_file = request.FILES['chart_image']
        
        # Validate file type
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        file_extension = os.path.splitext(chart_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return cors_response({'error': 'Invalid file type. Please upload JPG, PNG, or BMP images.'}, 
                          status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (max 10MB)
        if chart_file.size > 10 * 1024 * 1024:
            return cors_response({'error': 'File too large. Maximum size is 10MB.'}, 
                          status.HTTP_400_BAD_REQUEST)
        
        # Create ChartUpload instance
        chart_upload = ChartUpload.objects.create(
            chart_image=chart_file,
            symbol=symbol,
            timeframe=timeframe
        )
        
        # Analyze chart with real price data
        analyzer = ChartVisualAnalyzer()
        analysis_result = analyzer.analyze_chart_with_real_data(
            chart_upload.chart_image.path, 
            symbol,
            timeframe
        )
        
        # Update chart upload with analysis results
        chart_upload.chart_analysis = analysis_result.get('visual_analysis', {})
        chart_upload.market_structure = analysis_result.get('visual_analysis', {})
        chart_upload.real_price_prediction = analysis_result.get('real_price_prediction', {})
        chart_upload.analysis_completed = True
        chart_upload.save()
        
        return cors_response({
            'success': True,
            'chart_id': chart_upload.id,
            'symbol': chart_upload.symbol,
            'timeframe': chart_upload.timeframe,
            'analysis': analysis_result,
            'uploaded_at': chart_upload.uploaded_at.isoformat(),
            'message': 'Chart analyzed successfully with SMC analysis'
        })
        
    except Exception as e:
        logger.error(f"Chart upload analysis error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return cors_response({'error': f'Failed to analyze chart: {str(e)}'}, 
                       status.HTTP_500_INTERNAL_SERVER_ERROR)


# Removed perform_realtime_smc_analysis function - chart upload is now required


@api_view(['GET'])
def get_chart_analyses(request):
    """
    📋 GET CHART ANALYSIS HISTORY
    Retrieve list of uploaded charts with their analysis results
    """
    try:
        limit = int(request.GET.get('limit', 10))
        symbol = request.GET.get('symbol')
        
        uploads_query = ChartUpload.objects.all()
        
        if symbol:
            uploads_query = uploads_query.filter(symbol__icontains=symbol)
        
        uploads = uploads_query[:limit]
        
        data = []
        for upload in uploads:
            real_prediction = upload.real_price_prediction
            visual_analysis = upload.chart_analysis
            
            data.append({
                'id': upload.id,
                'symbol': upload.symbol,
                'timeframe': upload.timeframe,
                'uploaded_at': upload.uploaded_at.isoformat(),
                'analysis_completed': upload.analysis_completed,
                'chart_image_url': upload.chart_image.url if upload.chart_image else None,
                'real_price_prediction': {
                    'direction': real_prediction.get('direction', 'UNKNOWN'),
                    'confidence': real_prediction.get('confidence', 0),
                    'meets_threshold': real_prediction.get('meets_threshold', False),
                    'current_price': real_prediction.get('current_price', 0)
                },
                'visual_analysis': {
                    'trend_direction': visual_analysis.get('trend_direction', 'UNKNOWN'),
                    'pattern_type': visual_analysis.get('pattern_type', 'UNKNOWN'),
                    'chart_quality': visual_analysis.get('chart_quality', 'UNKNOWN')
                },
                'data_source': 'REAL_API_DATA'
            })
        
        return cors_response(data)
        
    except Exception as e:
        logger.error(f"Error fetching chart analyses: {e}")
        return cors_response({'error': 'Failed to fetch chart analyses'}, 
                       status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_chart_analysis_detail(request, chart_id):
    """
    🔍 GET DETAILED CHART ANALYSIS
    Get detailed analysis results for a specific uploaded chart
    """
    try:
        chart_upload = ChartUpload.objects.get(id=chart_id)
        
        return cors_response({
            'id': chart_upload.id,
            'symbol': chart_upload.symbol,
            'timeframe': chart_upload.timeframe,
            'uploaded_at': chart_upload.uploaded_at.isoformat(),
            'chart_image_url': chart_upload.chart_image.url if chart_upload.chart_image else None,
            'analysis_completed': chart_upload.analysis_completed,
            'visual_analysis': chart_upload.chart_analysis,
            'market_structure': chart_upload.market_structure,
            'real_price_prediction': chart_upload.real_price_prediction,
            'note': 'Analysis based on chart image and real price data'
        })
        
    except ChartUpload.DoesNotExist:
        return cors_response({'error': 'Chart analysis not found'}, 
                       status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching chart analysis detail: {e}")
        return cors_response({'error': 'Failed to fetch chart analysis detail'}, 
                       status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_chart_analysis(request, chart_id):
    """
    🗑️ DELETE UPLOADED CHART ANALYSIS
    Delete an uploaded chart and its analysis
    """
    try:
        chart_upload = ChartUpload.objects.get(id=chart_id)
        chart_upload.delete()  # This will also delete the image file
        
        return cors_response({'success': True, 'message': 'Chart analysis deleted successfully'})
        
    except ChartUpload.DoesNotExist:
        return cors_response({'error': 'Chart analysis not found'}, 
                       status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting chart analysis: {e}")
        return cors_response({'error': 'Failed to delete chart analysis'}, 
                       status.HTTP_500_INTERNAL_SERVER_ERROR)