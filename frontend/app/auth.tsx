import { Link } from "expo-router";
import { SafeAreaView, Text } from "react-native";

// TODO: Clerk
export default function Auth() {
  return (
    <SafeAreaView>
      <Link href="/(home)/">
        <Text>Test</Text>
      </Link>
    </SafeAreaView>
  );
}
