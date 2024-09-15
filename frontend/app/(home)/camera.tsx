import { CameraView, useCameraPermissions } from "expo-camera";
import {
  ActivityIndicator,
  Button,
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import { useEffect, useRef, useState } from "react";
import config from "@/config.json";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from "expo-router";

export default function Home() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);
  const [loading, setLoading] = useState(false);

  if (!permission || !permission.granted) {
    return (
      <SafeAreaView>
        <Button onPress={requestPermission} title="grant permission" />
      </SafeAreaView>
    );
  }

  function handleTakePicture() {
    setLoading(true);
    cameraRef.current
      ?.takePictureAsync({ base64: true, quality: 0 })
      .then((data) => {
        fetch(config.API_URL + "/image-description", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_id: "1", b64_image: data?.base64 }),
        })
          .then((res) => res.json())
          .then((data) => {
            AsyncStorage.setItem("emoji", JSON.stringify(data));
          })
          .finally(() => {
            setLoading(false);
            router.navigate("/(home)/");
          });
      });
  }

  return (
    <View style={styles.container}>
      {loading && (
        <View style={styles.circular}>
          <ActivityIndicator size="large" />
          <Text style={{ color: "white" }}>Processing...</Text>
        </View>
      )}

      <CameraView style={styles.camera} facing="back" ref={cameraRef}>
        <View style={styles.btn}>
          <TouchableOpacity onPress={handleTakePicture}>
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
  circular: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "column",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    zIndex: 20,
  },
});
