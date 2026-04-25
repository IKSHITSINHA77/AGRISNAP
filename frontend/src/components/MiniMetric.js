import React from 'react';
import { Text, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function MiniMetric({ label, value }) {
  return (
    <View style={appStyles.miniMetric}>
      <Text style={appStyles.miniMetricLabel}>{label}</Text>
      <Text style={appStyles.miniMetricValue}>{value}</Text>
    </View>
  );
}
