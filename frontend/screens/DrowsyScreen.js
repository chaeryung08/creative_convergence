import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";

export default function DrowsyScreen() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      const res = await fetch("http://127.0.0.1:8001/drowsy"); 
      const json = await res.json();
      setData(json);
    };

    loadData();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>졸음 상태</Text>

      {data ? (
        <>
          <Text>시간: {data.timestamp}</Text>
          <Text>졸음 지수: {data.drowsy_level}</Text>
          <Text>상태: {data.state}</Text>
        </>
      ) : (
        <Text>불러오는중...</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center" },
  title: { fontSize: 28, fontWeight: "bold", marginBottom: 20 }
});
