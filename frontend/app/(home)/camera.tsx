import { CameraView, useCameraPermissions } from "expo-camera";
import {
  Button,
  SafeAreaView,
  StyleSheet,
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

  if (!permission || !permission.granted) {
    return (
      <SafeAreaView>
        <Button onPress={requestPermission} title="grant permission" />
      </SafeAreaView>
    );
  }

  function handleTakePicture() {
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
            router.navigate("/(home)/");
          });
      });
  }

  return (
    <View style={styles.container}>
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
});
