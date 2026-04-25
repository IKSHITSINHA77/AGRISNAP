import React from 'react';
import { Text, View } from 'react-native';
import InsightCard from '../components/InsightCard';
import MiniMetric from '../components/MiniMetric';
import { appStyles } from '../theme/styles';

export default function SoilScreen() {
  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Soil Intelligence</Text>
      <View style={appStyles.metricGrid}>
        <MiniMetric label="Soil pH" value="6.7" />
        <MiniMetric label="Nitrogen" value="41 mg/kg" />
        <MiniMetric label="Phosphorus" value="19 mg/kg" />
        <MiniMetric label="Potassium" value="152 mg/kg" />
        <MiniMetric label="Moisture" value="34%" />
        <MiniMetric label="Temperature" value="26 C" />
      </View>
      <InsightCard title="AI Soil Recommendation" body="Best Crop: Wheat | Fertilizer: Split N+P application | Irrigation every 3 days." />
    </View>
  );
}
