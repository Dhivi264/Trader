from django.contrib import admin
from .models import ChartUpload


@admin.register(ChartUpload)
class ChartUploadAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'timeframe', 'uploaded_at', 'analysis_completed', 'get_real_prediction', 'get_visual_trend']
    list_filter = ['timeframe', 'analysis_completed', 'uploaded_at', 'symbol']
    readonly_fields = ['uploaded_at', 'chart_analysis', 'market_structure', 'real_price_prediction']
    search_fields = ['symbol']
    
    def get_real_prediction(self, obj):
        if obj.real_price_prediction:
            direction = obj.real_price_prediction.get('direction', 'N/A')
            confidence = obj.real_price_prediction.get('confidence', 0)
            return f"{direction} ({confidence:.1f}%)"
        return 'N/A'
    get_real_prediction.short_description = 'Real Price Prediction'
    
    def get_visual_trend(self, obj):
        if obj.chart_analysis:
            return obj.chart_analysis.get('trend_direction', 'N/A')
        return 'N/A'
    get_visual_trend.short_description = 'Visual Trend'
    
    fieldsets = (
        ('Chart Information', {
            'fields': ('chart_image', 'symbol', 'timeframe', 'uploaded_at')
        }),
        ('Analysis Status', {
            'fields': ('analysis_completed',)
        }),
        ('Real Price Analysis (Primary)', {
            'fields': ('real_price_prediction',),
            'description': 'Predictions based on real API price data - THIS IS THE PRIMARY SOURCE'
        }),
        ('Visual Analysis (Context Only)', {
            'fields': ('chart_analysis', 'market_structure'),
            'classes': ('collapse',),
            'description': 'Visual patterns from chart image - FOR CONTEXT ONLY, NOT USED FOR PREDICTIONS'
        }),
    )