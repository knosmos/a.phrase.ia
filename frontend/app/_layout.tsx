import {
  Inter_300Light,
  Inter_600SemiBold,
  useFonts,
} from "@expo-google-fonts/inter";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import "react-native-reanimated";
import { router } from "expo-router";

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded] = useFonts({
    Inter_300Light,
    Inter_600SemiBold,
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();

      // TODO: Load the initial screen based on the user's authentication status.
      router.navigate("/auth");
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return (
    <Stack>
      <Stack.Screen name="auth" options={{ headerShown: false }} />
      <Stack.Screen name="(home)" options={{ headerShown: false }} />
    </Stack>
  );
}
