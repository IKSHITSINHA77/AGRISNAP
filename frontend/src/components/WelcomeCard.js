import React from 'react';
import { Text, TouchableOpacity, View } from 'react-native';
import { appStyles } from '../theme/styles';

export default function WelcomeCard({ loading, onRefresh }) {
  return (
    <View style={[appStyles.sectionCard, { backgroundColor: 'rgba(27,94,32,0.35)', borderColor: 'rgba(129,199,132,0.45)' }]}>
      <Text style={{ color: '#FFFFFF', fontSize: 20, fontWeight: '700' }}>Hello Farmer</Text>
      <Text style={{ color: '#C8D8EC', marginTop: 6 }}>
        Today's command center is {loading ? 'syncing live data...' : 'ready with real-time insights'}.
      </Text>
      <TouchableOpacity style={appStyles.accentButton} onPress={onRefresh}>
        <Text style={appStyles.accentButtonText}>{loading ? 'Refreshing...' : 'Refresh Live Data'}</Text>
      </TouchableOpacity>
    </View>
  );
}
