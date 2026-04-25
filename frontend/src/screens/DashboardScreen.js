import React from 'react';
import { Text, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function DashboardScreen({ dashboardSummary, weatherData, marketData }) {
  const topWeather = weatherData[0] || {};
  const topMarket = marketData[0] || {};

  const cards = [
    { label: 'Farm Health Score', value: dashboardSummary ? `${Math.min(99, Math.round((dashboardSummary.soil_health_index || 0) + 20))}` : '--', unit: '/100', trend: 'Live' },
    { label: 'Soil Quality Index', value: dashboardSummary ? `${Math.round(dashboardSummary.soil_health_index || 0)}` : '--', unit: '/100', trend: 'AI Rated' },
    { label: 'Water Signal', value: dashboardSummary?.water_usage_signal || '--', unit: '', trend: 'Hydration AI' },
    { label: 'Yield Forecast', value: dashboardSummary ? `${dashboardSummary.yield_forecast_tons || 0}` : '--', unit: ' tons', trend: 'Model' },
    { label: 'Weather', value: topWeather.condition || '--', unit: '', trend: `${topWeather.temperature || '--'} C` },
    { label: 'Market', value: topMarket.crop_name || '--', unit: '', trend: topMarket.price_per_quintal ? `INR ${topMarket.price_per_quintal}` : 'No feed' },
  ];

  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Dashboard</Text>
      <View style={appStyles.metricGrid}>
        {cards.map((card) => (
          <View key={card.label} style={appStyles.metricCard}>
            <Text style={appStyles.metricLabel}>{card.label}</Text>
            <Text style={appStyles.metricValue}>
              {card.value}
              {!!card.unit && <Text style={appStyles.metricUnit}> {card.unit}</Text>}
            </Text>
            <Text style={appStyles.metricTrend}>{card.trend}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}
