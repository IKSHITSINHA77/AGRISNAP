import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity, ScrollView, SafeAreaView, KeyboardAvoidingView, Platform } from 'react-native';

export default function Chatbot({ onClose }) {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I am AgriSnap AI assistant. How can I help you today?', sender: 'bot' }
  ]);
  const [inputText, setInputText] = useState('');

  const handleSend = () => {
    if (inputText.trim()) {
      const newMessage = {
        id: messages.length + 1,
        text: inputText,
        sender: 'user'
      };
      setMessages([...messages, newMessage]);
      setInputText('');

      // Simulate bot response
      setTimeout(() => {
        const botResponse = {
          id: messages.length + 2,
          text: getBotResponse(inputText),
          sender: 'bot'
        };
        setMessages(prev => [...prev, botResponse]);
      }, 1000);
    }
  };

  const getBotResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('disease') || lowerMessage.includes('sick')) {
      return 'I can help you identify crop diseases! Please upload a photo of your affected crop, and I will analyze it for you.';
    } else if (lowerMessage.includes('price') || lowerMessage.includes('market')) {
      return 'I can provide current market prices for various crops. Which crop are you interested in?';
    } else if (lowerMessage.includes('seed') || lowerMessage.includes('input')) {
      return 'We offer high-quality seeds and agricultural inputs. Would you like recommendations for your specific crop?';
    } else if (lowerMessage.includes('weather') || lowerMessage.includes('rain')) {
      return 'Weather information is crucial for farming. I can provide weather forecasts for your location. Please share your location.';
    } else if (lowerMessage.includes('soil') || lowerMessage.includes('test')) {
      return 'Soil testing is important for optimal crop growth. We can help you test your soil and provide fertilizer recommendations.';
    } else if (lowerMessage.includes('help') || lowerMessage.includes('support')) {
      return 'I can help you with: Disease detection, Market prices, Quality seeds, Weather updates, Soil testing, and Expert advice. What would you like to know?';
    } else {
      return 'Thank you for your message. Our team is here to help farmers with crop diseases, market prices, quality inputs, and expert advice. How can I assist you further?';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <View style={styles.header}>
          <Text style={styles.headerTitle}>AgriSnap AI Assistant</Text>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Text style={styles.closeButtonText}>✕</Text>
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.messagesContainer}>
          {messages.map((message) => (
            <View
              key={message.id}
              style={[
                styles.messageBubble,
                message.sender === 'user' ? styles.userMessage : styles.botMessage
              ]}
            >
              <Text style={[
                styles.messageText,
                message.sender === 'user' ? styles.userMessageText : styles.botMessageText
              ]}>
                {message.text}
              </Text>
            </View>
          ))}
        </ScrollView>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Type your message..."
            value={inputText}
            onChangeText={setInputText}
            multiline
          />
          <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
            <Text style={styles.sendButtonText}>Send</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f2f8f3',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#1f7a4d',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  closeButton: {
    padding: 10,
  },
  closeButtonText: {
    fontSize: 24,
    color: 'white',
    fontWeight: 'bold',
  },
  messagesContainer: {
    flex: 1,
    padding: 20,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 15,
    borderRadius: 20,
    marginBottom: 10,
  },
  userMessage: {
    backgroundColor: '#ff7a1a',
    alignSelf: 'flex-end',
    borderBottomRightRadius: 5,
  },
  botMessage: {
    backgroundColor: '#ffffff',
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 5,
    borderWidth: 1,
    borderColor: '#deeee4',
  },
  messageText: {
    fontSize: 14,
  },
  userMessageText: {
    color: 'white',
  },
  botMessageText: {
    color: '#333',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 20,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#d5e3db',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#c9d8cf',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    maxHeight: 100,
    backgroundColor: '#f8fcf9',
  },
  sendButton: {
    backgroundColor: '#ff7a1a',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  sendButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});
