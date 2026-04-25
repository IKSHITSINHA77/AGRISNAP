import React from 'react';
import { Text, View } from 'react-native';
import InsightCard from '../components/InsightCard';
import MiniMetric from '../components/MiniMetric';
import { appStyles } from '../theme/styles';

export default function MarketScreen({ marketData }) {
  const item = marketData[0] || {};
  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Market Intelligence</Text>
      <View style={appStyles.metricGrid}>
        <MiniMetric label="Crop" value={item.crop_name || '--'} />
        <MiniMetric label="Mandi" value={item.mandi_name || '--'} />
        <MiniMetric label="Location" value={item.location || '--'} />
        <MiniMetric label="Price" value={item.price_per_quintal ? `INR ${item.price_per_quintal}` : '--'} />
      </View>
      <InsightCard title="AI Market Insight" body="Best selling window predicted when demand trend and price momentum align." />
    </View>
  );
}
