import Emoji from "@/components/emoji";
import { useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  FlatList,
} from "react-native";
import AntDesign from "@expo/vector-icons/AntDesign";

const chunks = (a: any[], size: number) =>
  Array.from(new Array(Math.ceil(a.length / size)), (_, i) =>
    a.slice(i * size, i * size + size)
  );

export default function Home() {
  const [emojis, setEmojis] = useState<string[]>([]);
  const [recs, setRecs] = useState<string[]>([]);

  useEffect(() => {
    // TODO: Load recommendations
    setRecs(["🍕", "🍔", "🍟", "🍦", "🍩", "🍪", "🍫", "🍬", "🍭", "🍮"]);
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.emojicontainer}>
          <ScrollView horizontal style={styles.emojis}>
            {emojis.length > 0 ? (
              emojis.map((emoji) => <Emoji size={40} data={emoji} />)
            ) : (
              <Emoji muted size={40} data="..." />
            )}
          </ScrollView>
        </View>
        <TouchableOpacity>
          <AntDesign name="rightcircleo" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <View style={styles.grid}>
        <FlatList
          data={chunks(recs, 5)}
          renderItem={({ item }) => (
            <View key={item[0]} style={styles.row}>
              {item.map((x) => (
                <TouchableOpacity onPress={() => setEmojis([...emojis, x])}>
                  <EmojiRec item={x} />
                </TouchableOpacity>
              ))}
            </View>
          )}
        />
      </View>
    </SafeAreaView>
  );
}

function EmojiRec({ item }: { item: string }) {
  return (
    <View style={styles.reccontainer}>
      <Emoji size={60} data={item} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#e1e1e1",
  },
  header: {
    flex: 1,
    alignItems: "center",
    justifyContent: "space-between",
    flexDirection: "row",
    paddingHorizontal: 16,
    gap: 16,
  },
  emojicontainer: {
    backgroundColor: "#fff",
    flex: 1,
    borderRadius: 8,
    flexDirection: "row",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    padding: 4,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    marginBottom: 16,
  },
  reccontainer: {
    backgroundColor: "#fff",
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    padding: 4,
  },
  emojis: {
    gap: 2,
  },
  grid: {
    flex: 7,
  },
});
