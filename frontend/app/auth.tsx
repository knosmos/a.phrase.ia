import { useSignIn, useSignUp } from "@clerk/clerk-expo";
import { Link, router } from "expo-router";
import { useState } from "react";
import {
  Button,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

// TODO: Clerk
export default function Auth() {
  const { signIn, setActive: signInSetActive } = useSignIn();
  const { signUp, setActive: signUpSetActive } = useSignUp();
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    let signInAttempt = await signIn?.create({
      identifier: emailAddress,
      password,
    });

    if (signInAttempt?.status === "complete" && !!signInSetActive) {
      await signInSetActive({ session: signInAttempt.createdSessionId });
      router.replace("/");
    }
  }

  async function handleSignup() {
    // await signUp?.create({
    //   emailAddress,
    //   password,
    // });

    // For demo, we'll just sign in
    router.replace("/");
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={{ fontFamily: "Inter_600SemiBold", fontSize: 48 }}>
          Aphrasia
        </Text>
        <Text style={{ fontFamily: "Inter_300Light", fontSize: 24 }}>auth</Text>
      </View>

      <View style={styles.boxes}>
        <View style={styles.lni}>
          <Text style={{ fontFamily: "Inter_300Light", fontSize: 16 }}>
            Email
          </Text>
          <TextInput
            style={styles.input}
            value={emailAddress}
            onChangeText={setEmailAddress}
          />
        </View>
        <View style={styles.lni}>
          <Text style={{ fontFamily: "Inter_300Light", fontSize: 16 }}>
            Password
          </Text>
          <TextInput
            secureTextEntry
            style={styles.input}
            value={password}
            onChangeText={setPassword}
          />
        </View>
      </View>

      <View style={styles.btnwrap}>
        <TouchableOpacity style={styles.btn1} onPress={handleLogin}>
          <Text
            style={{
              fontFamily: "Inter_600SemiBold",
              fontSize: 16,
              color: "#000",
            }}
          >
            Log In
          </Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.btn2} onPress={handleSignup}>
          <Text
            style={{
              fontFamily: "Inter_600SemiBold",
              fontSize: 16,
              color: "#fff",
            }}
          >
            Sign Up
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    gap: 26,
  },
  header: {
    flexDirection: "row",
    alignItems: "baseline",
    gap: 6,
  },
  boxes: {
    gap: 10,
  },
  lni: {
    gap: 3,
  },
  input: {
    padding: 10,
    backgroundColor: "#f0f0f0",
    width: 300,
    borderRadius: 8,
    color: "#000",
  },
  btn1: {
    backgroundColor: "#fff",
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  btn2: {
    backgroundColor: "#000",
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  btnwrap: {
    flexDirection: "row",
    gap: 10,
    marginTop: 16,
  },
});
