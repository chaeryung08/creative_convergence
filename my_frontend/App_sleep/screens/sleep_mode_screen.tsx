import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert, TextInput, Modal, Animated } from 'react-native';
// @ts-ignore - react-native-svg 타입 오류 무시
import Svg, { Circle, Line } from 'react-native-svg';

interface Props {
  onBack: () => void;
}

interface SleepRecord {
  time: string;
  duration: number;
}

// 원형 프로그레스 바 + 아날로그 시계 컴포넌트
const ClockWithProgress = ({ angle, progress }: { angle: number; progress: number }) => {
  const radius = 110;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress);

  return (
    <View style={{ position: 'relative', alignItems: 'center' }}>
      <Svg width="240" height="240" style={{ margin: 20 }}>
        {/* 배경 원 (회색) */}
        <Circle
          cx="120"
          cy="120"
          r="110"
          stroke="#E0E0E0"
          strokeWidth="15"
          fill="none"
        />
        
        {/* 프로그레스 원 (파란색) */}
        <Circle
          cx="120"
          cy="120"
          r="110"
          stroke="#4A90E2"
          strokeWidth="15"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          rotation="-90"
          origin="120, 120"
        />
        
        {/* 시계 테두리 */}
        <Circle
          cx="120"
          cy="120"
          r="85"
          stroke="#333"
          strokeWidth="3"
          fill="#F5F7FA"
        />
        
        {/* 12시 표시 */}
        <Line
          x1="120"
          y1="40"
          x2="120"
          y2="50"
          stroke="#333"
          strokeWidth="3"
        />
        
        {/* 시계 바늘 */}
        <Line
          x1="120"
          y1="120"
          x2={120 + 60 * Math.sin((angle * Math.PI) / 180)}
          y2={120 - 60 * Math.cos((angle * Math.PI) / 180)}
          stroke="#E74C3C"
          strokeWidth="4"
          strokeLinecap="round"
        />
        
        {/* 중심점 */}
        <Circle cx="120" cy="120" r="8" fill="#333" />
      </Svg>
      
      {/* 진행률 텍스트 */}
      <Text style={styles.progressText}>
        {Math.round(progress * 100)}%
      </Text>
    </View>
  );
};

// 알림 모달 컴포넌트
const WakeUpModal = ({ 
  visible, 
  onConfirm, 
  onSnooze, 
  onTimeout 
}: { 
  visible: boolean; 
  onConfirm: () => void; 
  onSnooze: () => void; 
  onTimeout: () => void;
}) => {
  const [countdown, setCountdown] = useState(60);

  useEffect(() => {
    if (visible) {
      setCountdown(60);
      
      const interval = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(interval);
            onTimeout();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [visible, onTimeout]);

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <Text style={styles.modalTitle}>일어날 시각입니다!</Text>
          
          <View style={styles.modalButtons}>
            <TouchableOpacity
              style={styles.modalButton}
              onPress={onConfirm}
              activeOpacity={0.8}
            >
              <Text style={styles.modalButtonText}>확인</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.modalButton}
              onPress={onSnooze}
              activeOpacity={0.8}
            >
              <Text style={styles.modalButtonText}>5분 더</Text>
            </TouchableOpacity>
          </View>

          <Text style={styles.modalCountdown}>
            {countdown}초 후에 비수면 모드로 전환됩니다
          </Text>
        </View>
      </View>
    </Modal>
  );
};

// 수면 기록 컴포넌트
const SleepHistory = ({ history }: { history: SleepRecord[] }) => {
  if (history.length === 0) {
    return (
      <View style={styles.historyContainer}>
        <Text style={styles.historyEmptyText}>
          아직 수면 기록이 없습니다
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.historyContainer}>
      <Text style={styles.historyTitle}>최근 수면 기록</Text>
      <ScrollView style={styles.historyScroll}>
        {history.slice(-5).reverse().map((record, index) => (
          <View 
            key={index} 
            style={[
              styles.historyItem,
              index < Math.min(4, history.length - 1) && styles.historyItemBorder
            ]}
          >
            <Text style={styles.historyTime}>{record.time}</Text>
            <Text style={styles.historyDuration}>
              {Math.floor(record.duration / 60)}분 {record.duration % 60}초
            </Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

// 메인 화면
export default function SleepModeScreen({ onBack }: Props) {
  const [maxTime, setMaxTime] = useState(1800);
  const [timeLeft, setTimeLeft] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isSleepMode, setIsSleepMode] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [usedTime, setUsedTime] = useState(0);
  const [startTime, setStartTime] = useState(0);
  const [sleepHistory, setSleepHistory] = useState<SleepRecord[]>([]);
  const [inputMinutes, setInputMinutes] = useState(30);
  const [inputSeconds, setInputSeconds] = useState(0);
  
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 컴포넌트 마운트 시 페이드인
  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  // 타이머 로직
  useEffect(() => {
    if (isRunning && timeLeft > 0) {
      intervalRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            if (intervalRef.current) clearInterval(intervalRef.current);
            setIsRunning(false);
            setShowModal(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning, timeLeft]);

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const getClockAngle = () => {
    const progress = 1 - (timeLeft / maxTime);
    return progress * 360;
  };

  const getProgress = () => {
    return 1 - (timeLeft / maxTime);
  };

  const getRemainingTotal = () => {
    if (isSleepMode && isRunning) {
      const elapsed = startTime - timeLeft;
      return 1800 - usedTime - elapsed;
    }
    return 1800 - usedTime;
  };

  // 수면 기록 저장
  const saveSleepRecord = (duration: number) => {
    const now = new Date();
    const timeStr = `${now.getMonth() + 1}/${now.getDate()} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const newRecord = { time: timeStr, duration };
    setSleepHistory([...sleepHistory, newRecord]);
  };

  const startSleepMode = () => {
    const totalSeconds = inputMinutes * 60 + inputSeconds;
    
    if (totalSeconds <= 0) {
      Alert.alert('알림', '시간을 0보다 크게 설정해주세요!');
      return;
    }
    
    const remaining = 1800 - usedTime;
    if (remaining <= 0) {
      Alert.alert('알림', '오늘의 수면 시간 30분을 모두 사용했습니다.');
      return;
    }
    
    const finalTime = Math.min(totalSeconds, remaining);
    setMaxTime(finalTime);
    setTimeLeft(finalTime);
    setStartTime(finalTime);
    setIsSleepMode(true);
    setIsRunning(true);
  };

  const stopSleep = () => {
    setIsRunning(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    const elapsed = startTime - timeLeft;
    setUsedTime((prev) => prev + elapsed);
    saveSleepRecord(elapsed);
    
    setIsSleepMode(false);
    setTimeLeft(0);
    Alert.alert('수면 종료', `${Math.floor(elapsed / 60)}분 ${elapsed % 60}초 사용했습니다.`);
  };

  const handleConfirm = () => {
    setShowModal(false);
    setIsRunning(false);
    const elapsed = startTime - timeLeft;
    setUsedTime((prev) => prev + elapsed);
    saveSleepRecord(elapsed);
    Alert.alert('알림', '정상적으로 기상했습니다.');
    setIsSleepMode(false);
  };

  const handleSnooze = () => {
    setShowModal(false);
    const remaining = 1800 - usedTime - (startTime - timeLeft);
    const snoozeTime = Math.min(300, remaining);
    
    if (snoozeTime <= 0) {
      Alert.alert('알림', '오늘의 수면 시간을 모두 사용했습니다.');
      handleConfirm();
      return;
    }
    
    setMaxTime(snoozeTime);
    setTimeLeft(snoozeTime);
    setStartTime(snoozeTime);
    setIsRunning(true);
    Alert.alert('알림', `${Math.floor(snoozeTime / 60)}분 ${snoozeTime % 60}초 더 잡니다 😴`);
  };

  const handleTimeout = () => {
    setShowModal(false);
    setIsRunning(false);
    const elapsed = startTime - timeLeft;
    setUsedTime((prev) => prev + elapsed);
    saveSleepRecord(elapsed);
    Alert.alert('알림', '사용자가 깨어나지 못해\n비수면 모드로 전환되었습니다.');
    setIsSleepMode(false);
  };

  const remainingTotal = getRemainingTotal();

  return (
    <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <TouchableOpacity style={styles.backButton} onPress={onBack}>
          <Text style={styles.backButtonText}>← 뒤로</Text>
        </TouchableOpacity>

        <Text style={styles.title}>수면 모드</Text>

        <Text style={styles.remainingInfo}>
          오늘 남은 수면 시간: {Math.floor(Math.max(0, remainingTotal) / 60)}분 {Math.max(0, remainingTotal) % 60}초
        </Text>

        {!isSleepMode && (
          <View style={styles.settingCard}>
            <Text style={styles.settingTitle}>수면 시간 설정</Text>
            
            <View style={styles.timeInputContainer}>
              <View style={styles.inputWrapper}>
                <TextInput
                  style={styles.timeInput}
                  value={String(inputMinutes)}
                  onChangeText={(text) => {
                    const num = parseInt(text) || 0;
                    setInputMinutes(Math.max(0, Math.min(30, num)));
                  }}
                  keyboardType="number-pad"
                  maxLength={2}
                />
                <Text style={styles.inputLabel}>분</Text>
              </View>
              
              <Text style={styles.timeSeparator}>:</Text>
              
              <View style={styles.inputWrapper}>
                <TextInput
                  style={styles.timeInput}
                  value={String(inputSeconds)}
                  onChangeText={(text) => {
                    const num = parseInt(text) || 0;
                    setInputSeconds(Math.max(0, Math.min(59, num)));
                  }}
                  keyboardType="number-pad"
                  maxLength={2}
                />
                <Text style={styles.inputLabel}>초</Text>
              </View>
            </View>
          </View>
        )}

        {isSleepMode && (
          <View style={styles.clockContainer}>
            <ClockWithProgress angle={getClockAngle()} progress={getProgress()} />
            <Text style={styles.timeDisplay}>{formatTime(timeLeft)}</Text>
          </View>
        )}

        {isSleepMode && (
          <TouchableOpacity
            style={styles.stopButton}
            onPress={stopSleep}
            activeOpacity={0.8}
          >
            <Text style={styles.stopButtonText}>정지</Text>
          </TouchableOpacity>
        )}

        {!isSleepMode && (
          <TouchableOpacity
            style={styles.startButton}
            onPress={startSleepMode}
            activeOpacity={0.8}
          >
            <Text style={styles.startButtonText}>수면 모드 시작</Text>
          </TouchableOpacity>
        )}

        {!isSleepMode && <SleepHistory history={sleepHistory} />}
      </ScrollView>

      <WakeUpModal
        visible={showModal}
        onConfirm={handleConfirm}
        onSnooze={handleSnooze}
        onTimeout={handleTimeout}
      />
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1d3a',
  },
  scrollContent: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  backButton: {
    alignSelf: 'flex-start',
    marginTop: 50,
    marginBottom: 20,
  },
  backButtonText: {
    color: '#ffffff',
    fontSize: 16,
    opacity: 0.8,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 20,
  },
  remainingInfo: {
    fontSize: 16,
    color: '#b8c5d6',
    marginBottom: 30,
    textAlign: 'center',
  },
  settingCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    padding: 30,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    width: '100%',
    maxWidth: 320,
    marginBottom: 20,
  },
  settingTitle: {
    fontSize: 18,
    color: '#ffffff',
    marginBottom: 20,
    textAlign: 'center',
  },
  timeInputContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 15,
  },
  inputWrapper: {
    alignItems: 'center',
  },
  timeInput: {
    width: 80,
    fontSize: 24,
    textAlign: 'center',
    padding: 10,
    borderWidth: 2,
    borderColor: '#5a9fd4',
    borderRadius: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    color: '#1a1d3a',
  },
  inputLabel: {
    fontSize: 14,
    color: '#b8c5d6',
    marginTop: 5,
  },
  timeSeparator: {
    fontSize: 24,
    color: '#ffffff',
    fontWeight: 'bold',
  },
  clockContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  progressText: {
    position: 'absolute',
    bottom: 40,
    fontSize: 14,
    color: '#5a9fd4',
    fontWeight: 'bold',
  },
  timeDisplay: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 10,
  },
  stopButton: {
    backgroundColor: '#5a7ea1',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 25,
    marginBottom: 20,
  },
  stopButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '600',
  },
  startButton: {
    backgroundColor: '#5a9fd4',
    paddingVertical: 18,
    paddingHorizontal: 50,
    borderRadius: 30,
    marginBottom: 20,
  },
  startButtonText: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '600',
  },
  historyContainer: {
    backgroundColor: '#ffffff',
    padding: 20,
    borderRadius: 15,
    marginTop: 20,
    width: '100%',
    maxWidth: 350,
    maxHeight: 200,
  },
  historyEmptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  historyTitle: {
    fontSize: 18,
    color: '#333',
    marginBottom: 15,
    fontWeight: 'bold',
  },
  historyScroll: {
    maxHeight: 150,
  },
  historyItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 10,
  },
  historyItemBorder: {
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  historyTime: {
    fontSize: 14,
    color: '#666',
  },
  historyDuration: {
    fontSize: 14,
    color: '#5a9fd4',
    fontWeight: 'bold',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 30,
    alignItems: 'center',
    minWidth: 300,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 30,
  },
  modalButtons: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 20,
  },
  modalButton: {
    backgroundColor: '#5a9fd4',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
  },
  modalButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '600',
  },
  modalCountdown: {
    fontSize: 12,
    color: '#999',
  },
});