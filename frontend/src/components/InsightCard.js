import React from 'react';
import { Text, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function InsightCard({ title, body }) {
  return (
    <View style={appStyles.insightCard}>
      <Text style={appStyles.insightTitle}>{title}</Text>
      <Text style={appStyles.insightBody}>{body}</Text>
    </View>
  );
}
