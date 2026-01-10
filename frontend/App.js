import { Text, View } from 'react-native';
import mockData from './data/mock_data';

export default function App() {
  return (
    <View>
      <Text>{mockData.title}</Text>
    </View>
  );
}
