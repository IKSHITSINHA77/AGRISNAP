import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function ModuleSelector({ modules, activeModule, onChangeModule }) {
  return (
    <View style={appStyles.sectionCard}>
      <Text style={{ color: '#9FB7D3', fontSize: 12, marginBottom: 8 }}>Main Modules</Text>
      <View style={appStyles.chipRow}>
        {modules.map((module) => (
          <TouchableOpacity
            key={module}
            style={[appStyles.chip, activeModule === module && { backgroundColor: '#1B5E20' }]}
            onPress={() => onChangeModule(module)}
          >
            <Text style={[appStyles.chipText, activeModule === module && { color: '#FFFFFF', fontWeight: '600' }]}>
              {module}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}
