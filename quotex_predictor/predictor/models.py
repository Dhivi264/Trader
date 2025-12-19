from django.db import models
import os


class ChartUpload(models.Model):
    """Model for storing uploaded chart images and their analysis"""
    TIMEFRAME_CHOICES = [
        ('15m', '15 Minutes'),
        ('1h', '1 Hour'),
    ]
    
    chart_image = models.ImageField(upload_to='charts/', help_text="Upload 15-minute or 1-hour chart image")
    symbol = models.CharField(max_length=20, help_text="Trading pair symbol (e.g., EURUSD)")
    timeframe = models.CharField(max_length=3, choices=TIMEFRAME_CHOICES, default='1h')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_completed = models.BooleanField(default=False)
    
    # Chart Analysis Results (visual analysis only)
    chart_analysis = models.JSONField(default=dict, blank=True, help_text="Visual chart pattern analysis")
    market_structure = models.JSONField(default=dict, blank=True, help_text="Market structure from chart")
    
    # Real Price Prediction (using API data)
    real_price_prediction = models.JSONField(default=dict, blank=True, help_text="Prediction using real price data")
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.symbol} - {self.timeframe} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def delete(self, *args, **kwargs):
        # Delete the image file when the model instance is deleted
        if self.chart_image:
            if os.path.isfile(self.chart_image.path):
                os.remove(self.chart_image.path)
        super().delete(*args, **kwargs)