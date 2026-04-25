import React, { useEffect, useMemo, useState } from 'react';
import { Modal, SafeAreaView, ScrollView, TextInput, TouchableOpacity, View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Chatbot from './Chatbot';
import ErrorCard from './src/components/ErrorCard';
import ModuleSelector from './src/components/ModuleSelector';
import TopBar from './src/components/TopBar';
import WelcomeCard from './src/components/WelcomeCard';
import { API_BASE } from './src/config';
import AssistantScreen from './src/screens/AssistantScreen';
import CropHealthScreen from './src/screens/CropHealthScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import FarmMapScreen from './src/screens/FarmMapScreen';
import MarketScreen from './src/screens/MarketScreen';
import SoilScreen from './src/screens/SoilScreen';
import WeatherScreen from './src/screens/WeatherScreen';
import { appStyles } from './src/theme/styles';

const Tab = createBottomTabNavigator();
const MODULES = ['Dashboard', 'Farm Map', 'Soil Intelligence', 'Crop Health AI', 'Weather & Climate', 'Market Intelligence', 'AI Assistant'];

export default function App() {
  const [showChatbot, setShowChatbot] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dashboardSummary, setDashboardSummary] = useState(null);
  const [weatherData, setWeatherData] = useState([]);
  const [marketData, setMarketData] = useState([]);
  const [reports, setReports] = useState([]);
  const [selectedModule, setSelectedModule] = useState('Dashboard');

  const filteredModules = useMemo(
    () => MODULES.filter((item) => item.toLowerCase().includes(searchText.toLowerCase())),
    [searchText]
  );

  useEffect(() => {
    loadCommandCenterData();
  }, []);

  const requestJson = async (path) => {
    const response = await fetch(`${API_BASE}${path}`);
    if (!response.ok) throw new Error(`API ${path} failed (${response.status})`);
    return response.json();
  };

  const loadCommandCenterData = async () => {
    setLoading(true);
    setError('');
    try {
      const [summary, weather, market, diseaseReports] = await Promise.all([
        requestJson('/dashboard/summary/'),
        requestJson('/weather/'),
        requestJson('/market-prices/'),
        requestJson('/reports/'),
      ]);
      setDashboardSummary(summary);
      setWeatherData(Array.isArray(weather) ? weather : [weather]);
      setMarketData(Array.isArray(market) ? market : normalizeLegacyMarket(market));
      setReports(Array.isArray(diseaseReports) ? diseaseReports : []);
    } catch (err) {
      setError(err.message || 'Unable to load live intelligence data.');
    } finally {
      setLoading(false);
    }
  };

  const HomeTab = () => (
    <SafeAreaView style={appStyles.container}>
      <TopBar />
      <View style={appStyles.searchWrap}>
        <TextInput
          style={appStyles.searchInput}
          placeholder="Search modules, insights, alerts..."
          placeholderTextColor="#93A4BB"
          value={searchText}
          onChangeText={setSearchText}
        />
      </View>
      <ScrollView contentContainerStyle={appStyles.scrollContent}>
        <WelcomeCard loading={loading} onRefresh={loadCommandCenterData} />
        <ErrorCard message={error} />
        <ModuleSelector modules={filteredModules} activeModule={selectedModule} onChangeModule={setSelectedModule} />
        <RoutedModule
          selectedModule={selectedModule}
          dashboardSummary={dashboardSummary}
          weatherData={weatherData}
          marketData={marketData}
          reports={reports}
          onOpenAssistant={() => setShowChatbot(true)}
        />
      </ScrollView>
      <FloatingAIButton onPress={() => setShowChatbot(true)} />
    </SafeAreaView>
  );

  return (
    <>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={{
            headerShown: false,
            tabBarStyle: { backgroundColor: '#0A1020', borderTopColor: 'rgba(255,255,255,0.12)' },
            tabBarActiveTintColor: '#81C784',
            tabBarInactiveTintColor: '#9FB7D3',
          }}
        >
          <Tab.Screen name="Home" component={HomeTab} />
          <Tab.Screen name="Map" component={() => <ScreenContainer><FarmMapScreen /></ScreenContainer>} />
          <Tab.Screen name="AI" component={() => <ScreenContainer><AssistantScreen onOpenAssistant={() => setShowChatbot(true)} /></ScreenContainer>} />
          <Tab.Screen name="Market" component={() => <ScreenContainer><MarketScreen marketData={marketData} /></ScreenContainer>} />
          <Tab.Screen name="Profile" component={ProfileScreen} />
        </Tab.Navigator>
      </NavigationContainer>

      <Modal visible={showChatbot} animationType="slide" onRequestClose={() => setShowChatbot(false)}>
        <Chatbot onClose={() => setShowChatbot(false)} />
      </Modal>
    </>
  );
}

function RoutedModule({ selectedModule, dashboardSummary, weatherData, marketData, reports, onOpenAssistant }) {
  switch (selectedModule) {
    case 'Farm Map':
      return <FarmMapScreen />;
    case 'Soil Intelligence':
      return <SoilScreen />;
    case 'Crop Health AI':
      return <CropHealthScreen reports={reports} />;
    case 'Weather & Climate':
      return <WeatherScreen weatherData={weatherData} />;
    case 'Market Intelligence':
      return <MarketScreen marketData={marketData} />;
    case 'AI Assistant':
      return <AssistantScreen onOpenAssistant={onOpenAssistant} />;
    default:
      return <DashboardScreen dashboardSummary={dashboardSummary} weatherData={weatherData} marketData={marketData} />;
  }
}

function ScreenContainer({ children }) {
  return (
    <SafeAreaView style={appStyles.container}>
      <TopBar />
      <ScrollView contentContainerStyle={appStyles.scrollContent}>{children}</ScrollView>
    </SafeAreaView>
  );
}

function FloatingAIButton({ onPress }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        position: 'absolute',
        right: 16,
        bottom: 16,
        width: 54,
        height: 54,
        borderRadius: 27,
        backgroundColor: '#1B5E20',
        borderWidth: 2,
        borderColor: '#81C784',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Text style={{ color: '#FFFFFF', fontWeight: '700', fontSize: 13 }}>AI</Text>
    </TouchableOpacity>
  );
}

function ProfileScreen() {
  return (
    <ScreenContainer>
      <View style={appStyles.sectionCard}>
        <Text style={appStyles.sectionTitle}>Profile & Reports</Text>
        <Text style={{ color: '#C8D8EC', lineHeight: 20 }}>
          Profile settings, report exports, and personalization controls can be managed here.
        </Text>
      </View>
    </ScreenContainer>
  );
}

function normalizeLegacyMarket(payload) {
  if (!payload || Array.isArray(payload)) return [];
  return Object.keys(payload).map((cropName) => ({
    crop_name: cropName,
    mandi_name: payload[cropName].location || 'Unknown',
    location: payload[cropName].location || 'Unknown',
    price_per_quintal: payload[cropName].price || 0,
  }));
}
