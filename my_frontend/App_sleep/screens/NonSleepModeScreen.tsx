import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Animated } from 'react-native';

const API_URL = 'http://localhost:8000';

interface Props {
  onBack: () => void;
}

export default function NonSleepModeScreen({ onBack }: Props) {
  const [drowsyStatus, setDrowsyStatus] = useState({
    level: 0,
    state: 'NORMAL',
    timestamp: ''
  });
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [pulseAnim] = useState(new Animated.Value(1));

  // 펄스 애니메이션
  useEffect(() => {
    if (isMonitoring) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.1,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      ).start();
    }
  }, [isMonitoring]);

  const sendDrowsyData = async (level: number, state: string) => {
    try {
      const response = await fetch(`${API_URL}/drowsy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          drowsy_level: level,
          state: state,
          user_id: 'user123',
          mode: 'nonsleep'
        })
      });
      const data = await response.json();
      console.log('✅ 백엔드 응답:', data);
    } catch (error) {
      console.error('❌ 전송 실패:', error);
    }
  };

  const simulateDrowsyDetection = () => {
    const randomLevel = Math.random();
    let state = 'NORMAL';
    
    if (randomLevel > 0.7) {
      state = 'DROWSY';
    } else if (randomLevel > 0.4) {
      state = 'WARNING';
    }
    
    setDrowsyStatus({
      level: randomLevel,
      state: state,
      timestamp: new Date().toLocaleTimeString('ko-KR')
    });

    sendDrowsyData(randomLevel, state);
  };

  const getStatusColor = () => {
    switch (drowsyStatus.state) {
      case 'DROWSY': return '#FF3B30';
      case 'WARNING': return '#FF9500';
      default: return '#34C759';
    }
  };

  const getStatusEmoji = () => {
    switch (drowsyStatus.state) {
      case 'DROWSY': return '😴';
      case 'WARNING': return '😐';
      default: return '😊';
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={onBack}>
          <Text style={styles.backButtonText}>← 모드 변경</Text>
        </TouchableOpacity>
        <View style={styles.headerContent}>
          <Text style={styles.modeTag}>☀️ 비수면 모드</Text>
          <Text style={styles.headerTitle}>졸음 감지 시스템</Text>
        </View>
      </View>

      <View style={styles.statusContainer}>
        <Animated.View 
          style={[
            styles.statusCircle,
            { 
              backgroundColor: getStatusColor(),
              transform: [{ scale: isMonitoring ? pulseAnim : 1 }]
            }
          ]}
        >
          <Text style={styles.statusEmoji}>{getStatusEmoji()}</Text>
          <Text style={styles.statusPercentage}>
            {(drowsyStatus.level * 100).toFixed(0)}%
          </Text>
        </Animated.View>
        
        <Text style={styles.statusMessage}>
          {drowsyStatus.state === 'DROWSY' ? '졸음 감지됨' : 
           drowsyStatus.state === 'WARNING' ? '주의가 필요해요' : '정상 상태'}
        </Text>
        {drowsyStatus.timestamp && (
          <Text style={styles.timestampText}>
            마지막 측정: {drowsyStatus.timestamp}
          </Text>
        )}
      </View>

      <View style={styles.controlSection}>
        <TouchableOpacity
          style={[
            styles.mainButton,
            { backgroundColor: isMonitoring ? '#FF3B30' : '#007AFF' }
          ]}
          onPress={() => {
            setIsMonitoring(!isMonitoring);
            if (!isMonitoring) simulateDrowsyDetection();
          }}
        >
          <Text style={styles.mainButtonText}>
            {isMonitoring ? '⏹ 모니터링 중지' : '▶️ 모니터링 시작'}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.testButton}
          onPress={simulateDrowsyDetection}
        >
          <Text style={styles.testButtonText}>🧪 테스트</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.indicatorSection}>
        <View style={styles.indicatorRow}>
          <View style={[styles.indicatorDot, { backgroundColor: '#34C759' }]} />
          <Text style={styles.indicatorLabel}>정상</Text>
          <Text style={styles.indicatorRange}>0-40%</Text>
        </View>
        <View style={styles.indicatorRow}>
          <View style={[styles.indicatorDot, { backgroundColor: '#FF9500' }]} />
          <Text style={styles.indicatorLabel}>주의</Text>
          <Text style={styles.indicatorRange}>40-70%</Text>
        </View>
        <View style={styles.indicatorRow}>
          <View style={[styles.indicatorDot, { backgroundColor: '#FF3B30' }]} />
          <Text style={styles.indicatorLabel}>졸음</Text>
          <Text style={styles.indicatorRange}>70-100%</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f2f2f7',
  },
  header: {
    backgroundColor: '#2d5f7a',
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  backButton: {
    marginBottom: 20,
  },
  backButtonText: {
    color: '#ffffff',
    fontSize: 16,
    opacity: 0.8,
  },
  headerContent: {
    alignItems: 'center',
  },
  modeTag: {
    fontSize: 14,
    color: '#ffffff',
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginBottom: 8,
    overflow: 'hidden',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  statusContainer: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  statusCircle: {
    width: 200,
    height: 200,
    borderRadius: 100,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 12,
  },
  statusEmoji: {
    fontSize: 60,
    marginBottom: 10,
  },
  statusPercentage: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  statusMessage: {
    fontSize: 24,
    fontWeight: '600',
    color: '#1c1c1e',
    marginTop: 24,
  },
  timestampText: {
    fontSize: 14,
    color: '#8e8e93',
    marginTop: 8,
  },
  controlSection: {
    paddingHorizontal: 20,
    marginTop: 20,
  },
  mainButton: {
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 6,
  },
  mainButtonText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  testButton: {
    backgroundColor: '#5856d6',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    marginTop: 12,
  },
  testButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
  indicatorSection: {
    backgroundColor: '#ffffff',
    margin: 20,
    padding: 20,
    borderRadius: 16,
    marginBottom: 40,
  },
  indicatorRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  indicatorDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 12,
  },
  indicatorLabel: {
    fontSize: 16,
    color: '#1c1c1e',
    fontWeight: '600',
    flex: 1,
  },
  indicatorRange: {
    fontSize: 14,
    color: '#8e8e93',
  },
});