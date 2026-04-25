import React from 'react';
import { Text, View } from 'react-native';

export default function ErrorCard({ message }) {
  if (!message) return null;
  return (
    <View
      style={{
        backgroundColor: 'rgba(220,38,38,0.22)',
        borderWidth: 1,
        borderColor: 'rgba(248,113,113,0.55)',
        borderRadius: 14,
        padding: 12,
      }}
    >
      <Text style={{ color: '#FECACA', fontWeight: '700', marginBottom: 4 }}>Live API Warning</Text>
      <Text style={{ color: '#FEE2E2', fontSize: 12, lineHeight: 18 }}>{message}</Text>
      <Text style={{ color: '#FEE2E2', fontSize: 12, lineHeight: 18 }}>
        Set `EXPO_PUBLIC_API_URL` to your backend URL.
      </Text>
    </View>
  );
}
