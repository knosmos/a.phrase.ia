import Emoji from "@/components/emoji";
import { useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  Button,
  View,
  TouchableOpacity,
  FlatList,
} from "react-native";
import AntDesign from "@expo/vector-icons/AntDesign";
import config from "@/config.json";
import { Link } from "expo-router";
import * as Speech from "expo-speech";

const handleLoadMore = () => {
  //TODO: Load more
};

export default function Home() {
  const [emojis, setEmojis] = useState<string[]>([]);
  const [recs, setRecs] = useState<string[]>([]);

  useEffect(() => {
    // TODO: Load recommendations
    setRecs([
      "❓",
      "❗",
      "🍕",
      "🍔",
      "🍟",
      "🍦",
      "🍩",
      "🍪",
      "🍫",
      "🍬",
      "🍭",
      "🍮",
    ]);
  }, []);

  function handleSentenceGen() {
    fetch(config.API_URL + "/sentence-gen", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: "1",
        emoji_seq: [...emojis],
      }),
    })
      .then((res) => res.json())
      .then((data) => Speech.speak(data, { language: "en" }));
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.emojicontainer}>
          <ScrollView horizontal style={styles.emojis}>
            {emojis.length > 0 ? (
              emojis.map((emoji, i) => <Emoji key={i} size={40} data={emoji} />)
            ) : (
              <Emoji muted size={40} data="..." />
            )}
          </ScrollView>
        </View>
        <View style={styles.go}>
          <Button onPress={handleSentenceGen} title="Go" />
        </View>
      </View>

      <View style={styles.grid}>
        <FlatList
          data={[recs]}
          renderItem={({ item }) => (
            <View style={styles.row}>
              {item.map((x, i) => (
                <TouchableOpacity
                  key={i}
                  onPress={() => setEmojis([...emojis, x])}
                >
                  <EmojiRec item={x} />
                </TouchableOpacity>
              ))}
            </View>
          )}
        />
      </View>
      <View style={styles.footBar}>
        <View style={styles.row}>
          <Link href="/(home)/camera">
            <AntDesign name="camera" size={36} color="black" />
          </Link>
          <Button onPress={handleLoadMore} title="Load More"></Button>
        </View>
      </View>
    </SafeAreaView>
  );
}

function EmojiRec({ item }: { item: string }) {
  return (
    <View style={styles.reccontainer}>
      <Emoji size={120} data={item} />
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
    padding: 10,
  },
  row: {
    flexDirection: "row",
    justifyContent: "flex-start",
    marginBottom: 16,
    gap: 20,
    flexWrap: "wrap",
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
    padding: 0,
  },
  emojis: {
    gap: 2,
  },
  grid: {
    flex: 7,
    width: "100%",
    padding: 16,
  },
  go: {
    position: "absolute",
    right: 30,
  },
  footBar: {
    position: "absolute",
    padding: 16,
    width: "100%",
    bottom: 0,
    backgroundColor: "#fff",
    alignItems: "center",
  },
});

// sides aligned with search bar
// emojis bigger
// spacing smaller
// make padding within emoji container smaller
// Set emojis on top bar
// Recommended emojis in bottom
// Sing button
// Go button
// Speak button
// Load more button
// Camera button
// x button
