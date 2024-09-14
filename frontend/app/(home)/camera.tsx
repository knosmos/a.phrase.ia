import { CameraView, useCameraPermissions } from "expo-camera";
import {
  Button,
  SafeAreaView,
  StyleSheet,
  TouchableOpacity,
  View,
} from "react-native";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

export default function Home() {
  const [permission, requestPermission] = useCameraPermissions();

  if (!permission || !permission.granted) {
    return (
      <SafeAreaView>
        <Button onPress={requestPermission} title="grant permission" />
      </SafeAreaView>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing="back">
        <View style={styles.btn}>
          <TouchableOpacity>
            <MaterialCommunityIcons
              name="camera-iris"
              size={60}
              color="white"
            />
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
  },
  camera: {
    flex: 1,
    position: "relative",
  },
  btn: {
    position: "absolute",
    bottom: 40,
    flex: 1,
    width: "100%",
    flexDirection: "row",
    justifyContent: "center",
  },
});
