import React from 'react';
import { Text, View } from 'react-native';
import InsightCard from '../components/InsightCard';
import MiniMetric from '../components/MiniMetric';
import { appStyles } from '../theme/styles';

export default function WeatherScreen({ weatherData }) {
  const item = weatherData[0] || {};
  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Weather & Climate Intelligence</Text>
      <View style={appStyles.metricGrid}>
        <MiniMetric label="Rainfall Forecast" value={`${item.rainfall_mm ?? '--'} mm`} />
        <MiniMetric label="Temperature" value={`${item.temperature ?? '--'} C`} />
        <MiniMetric label="Wind Speed" value={`${item.wind_speed_kmph ?? '--'} km/h`} />
        <MiniMetric label="Humidity" value={`${item.humidity ?? '--'}%`} />
      </View>
      <InsightCard title="AI Suggestion" body="Delay irrigation when rainfall forecast exceeds 10 mm in next cycle." />
    </View>
  );
}
