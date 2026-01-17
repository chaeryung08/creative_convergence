import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import SleepModeScreen from '../App_sleep/screens/sleep_mode_screen';
import NonSleepModeScreen from '../App_sleep/screens/NonSleepModeScreen';

export default function Page() {
  const [mode, setMode] = useState<'sleep' | 'nonsleep' | null>(null);

  // 모드별 화면 렌더링
  if (mode === 'sleep') {
    return <SleepModeScreen onBack={() => setMode(null)} />;
  }

  if (mode === 'nonsleep') {
    return <NonSleepModeScreen onBack={() => setMode(null)} />;
  }

  // 모드 선택 화면
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>모드를 선택하세요</Text>
        <Text style={styles.subtitle}>운전 환경에 맞는 모드를 선택해주세요</Text>
      </View>

      <TouchableOpacity
        style={[styles.card, styles.sleepCard]}
        onPress={() => setMode('sleep')}
        activeOpacity={0.8}
      >
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>🌙</Text>
        </View>
        <Text style={styles.cardTitle}>수면 모드</Text>
        <Text style={styles.cardDesc}>
          낮잠 타이머 제공{'\n'}하루 최대 30분
        </Text>
        <View style={styles.features}>
          <Text style={styles.featureText}>• 낮잠 타이머</Text>
          <Text style={styles.featureText}>• 알람 및 진동</Text>
          <Text style={styles.featureText}>• 하루 30분 제한</Text>
        </View>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.card, styles.nonsleepCard]}
        onPress={() => setMode('nonsleep')}
        activeOpacity={0.8}
      >
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>☀️</Text>
        </View>
        <Text style={styles.cardTitle}>비수면 모드</Text>
        <Text style={styles.cardDesc}>
          실시간 졸음 감지{'\n'}상태 모니터링
        </Text>
        <View style={styles.features}>
          <Text style={styles.featureText}>• 실시간 모니터링</Text>
          <Text style={styles.featureText}>• 상태 기록</Text>
          <Text style={styles.featureText}>• 통계 제공</Text>
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0e1a',
    padding: 20,
    paddingTop: 60,
  },
  header: {
    marginBottom: 40,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#8e8e93',
  },
  card: {
    borderRadius: 20,
    padding: 30,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  sleepCard: {
    backgroundColor: '#1a1f3a',
  },
  nonsleepCard: {
    backgroundColor: '#2d5f7a',
  },
  iconContainer: {
    width: 80,
    height: 80,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  icon: {
    fontSize: 40,
  },
  cardTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  cardDesc: {
    fontSize: 16,
    color: '#c7c7cc',
    marginBottom: 20,
    lineHeight: 24,
  },
  features: {
    marginTop: 10,
  },
  featureText: {
    fontSize: 14,
    color: '#8e8e93',
    marginBottom: 6,
  },
});