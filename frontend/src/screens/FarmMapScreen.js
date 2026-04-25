import React from 'react';
import { Text, View } from 'react-native';
import { MAP_LAYERS } from '../config';
import { appStyles } from '../theme/styles';

export default function FarmMapScreen() {
  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Farm Map Intelligence</Text>
      <View style={appStyles.mapPlaceholder}>
        <Text style={appStyles.mapText}>Satellite Farm View</Text>
        <Text style={appStyles.mapSubtext}>Mapbox/Leaflet-ready layer architecture for crop zones and risk overlays.</Text>
      </View>
      <Text style={{ color: '#9FB7D3', fontSize: 12, marginBottom: 8 }}>Layers Toggle</Text>
      <View style={appStyles.chipRow}>
        {MAP_LAYERS.map((layer) => (
          <View key={layer} style={appStyles.chip}>
            <Text style={appStyles.chipText}>{layer}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}
