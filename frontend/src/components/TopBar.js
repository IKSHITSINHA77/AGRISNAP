import React from 'react';
import { Text, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function TopBar() {
  return (
    <View style={appStyles.topBar}>
      <View>
        <Text style={appStyles.brand}>AgriSnap AI</Text>
        <Text style={appStyles.brandSub}>Smart Farming Command Center</Text>
      </View>
      <View style={appStyles.topActions}>
        <Text style={appStyles.topIcon}>AI</Text>
        <Text style={appStyles.topIcon}>Profile</Text>
      </View>
    </View>
  );
}
