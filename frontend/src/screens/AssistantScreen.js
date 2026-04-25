import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function AssistantScreen({ onOpenAssistant }) {
  return (
    <View style={appStyles.sectionCard}>
      <Text style={appStyles.sectionTitle}>AI Assistant</Text>
      <View style={{ backgroundColor: 'rgba(255,255,255,0.07)', borderRadius: 12, borderWidth: 1, borderColor: 'rgba(255,255,255,0.14)', padding: 12 }}>
        <Text style={{ color: '#D8E6F7', marginBottom: 10, lineHeight: 18 }}>
          Ask crop, weather, soil, disease, and market strategy questions in one place.
        </Text>
        <TouchableOpacity style={appStyles.primaryButton} onPress={onOpenAssistant}>
          <Text style={appStyles.primaryButtonText}>Open AI Assistant</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
