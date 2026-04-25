import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import InsightCard from '../components/InsightCard';
import { appStyles } from '../theme/styles';

export default function CropHealthScreen({ reports }) {
  const latest = reports[0];

  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>Crop Health AI</Text>
      <View style={{ backgroundColor: 'rgba(255,255,255,0.07)', borderRadius: 12, borderColor: 'rgba(255,255,255,0.14)', borderWidth: 1, padding: 12 }}>
        <Text style={{ color: '#FFFFFF', fontWeight: '600', fontSize: 15 }}>Upload Crop Image</Text>
        <Text style={{ color: '#C8D8EC', marginTop: 6, marginBottom: 10 }}>AI flow: Upload -> Detect -> Severity -> Treatment</Text>
        <TouchableOpacity style={appStyles.accentButton}>
          <Text style={appStyles.accentButtonText}>Run AI Analysis</Text>
        </TouchableOpacity>
      </View>
      <InsightCard
        title="Latest Detection"
        body={
          latest
            ? `Disease: ${latest.prediction} | Severity: ${latest.severity} | Confidence: ${Math.round((latest.confidence || 0) * 100)}%`
            : 'No disease reports yet. Upload a crop image to begin AI diagnosis.'
        }
      />
    </View>
  );
}
