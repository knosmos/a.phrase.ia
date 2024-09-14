import { ThemedText } from "@/components/ThemedText";
import { Link } from "expo-router";
import { SafeAreaView } from "react-native";

// TODO: Clerk
export default function Auth() {
  return (
    <SafeAreaView>
      <Link href="/(home)/">
        <ThemedText>Test</ThemedText>
      </Link>
    </SafeAreaView>
  );
}
