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
import Ionicons from "@expo/vector-icons/Ionicons";
import config from "@/config.json";
import { Link, router } from "expo-router";
import * as Speech from "expo-speech";
import AsyncStorage from "@react-native-async-storage/async-storage";
import FontAwesome6 from "@expo/vector-icons/FontAwesome6";
import FontAwesome from "@expo/vector-icons/FontAwesome";

export default function Home() {
  const [emojis, setEmojis] = useState<string[]>([]);
  const [recs, setRecs] = useState<string[]>([]);
  const [std, setStd] = useState<string[]>([]);

  const handleDelete = () => {
    const temp = emojis.slice(0, -1);
    setEmojis(temp);
  };

  const handleLoadMore = () => {
    //TODO: Load more
  };

  useEffect(() => {
    // TODO: Load recommendations
    setStd(["❓", "❗", "😊", "💀", "😔", "🎉", "🫵"]);
    const i = setInterval(() => {
      AsyncStorage.getItem("emojis").then((data) => {
        if (data) {
          setEmojis(JSON.parse(data));
          AsyncStorage.removeItem("emojis");
        }
      });

      AsyncStorage.getItem("emoji").then((data) => {
        if (data) {
          let x = JSON.parse(data);
          setEmojis([`b64|${x.emoji}|${x.short}`, ...emojis]);

          AsyncStorage.removeItem("emoji");
        }
      });
    }, 500);

    handleRecommendation();

    return () => clearInterval(i);
  }, []);

  function handleSentenceGen() {
    fetch(config.API_URL + "/sentence-gen", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: "1",
        emoji_seq: emojis.map((x) =>
          x.startsWith("b64") ? x.split("|")[2] : x
        ),
      }),
    })
      .then((res) => res.json())
      .then((data) => Speech.speak(data, { language: "en" }));
  }

  async function handleRecommendation() {
    fetch(config.API_URL + "/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: "1",
        emoji_seq: emojis.map((x) =>
          x.startsWith("b64") ? x.split("|")[2] : x
        ),
      }),
    })
      .then((res) => res.json())
      .then(async (data) => {
        const storedEmojis = await AsyncStorage.getItem("emojis");
        console.log(storedEmojis);
        if (storedEmojis && storedEmojis.length > 0) {
          setRecs([JSON.parse(storedEmojis), ...data]);
        } else {
          setRecs(data);
        }
      });
  }

  async function handleCamera() {
    const storedEmojis = await AsyncStorage.getItem("emojis");
    const updatedEmojis = storedEmojis ? JSON.parse(storedEmojis) : [];
    await AsyncStorage.setItem("emojis", JSON.stringify(updatedEmojis));
    router.navigate("/(home)/camera");
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.emojicontainer}>
          <ScrollView horizontal style={styles.emojis}>
            {emojis.length > 0 ? (
              emojis.map((emoji, i) => <Emoji key={i} size={80} data={emoji} />)
            ) : (
              <Emoji muted size={40} data="..." />
            )}
          </ScrollView>
        </View>
        <View style={styles.go}>
          <TouchableOpacity onPress={handleSentenceGen}>
            <FontAwesome name="send" size={24} color="black" />
          </TouchableOpacity>
        </View>
        <View style={styles.delete}>
          <TouchableOpacity onPress={handleDelete}>
            <FontAwesome6 name="delete-left" size={24} color="black" />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.grid}>
        <FlatList
          style={styles.flatList}
          horizontal
          data={[std]}
          renderItem={({ item }) => (
            <View style={styles.row}>
              {item.map((x, i) => (
                <TouchableOpacity
                  key={i}
                  onPress={() => {
                    handleRecommendation();
                    setEmojis([...emojis, x]);
                  }}
                >
                  <EmojiRec item={x} />
                </TouchableOpacity>
              ))}
            </View>
          )}
        />
      </View>

      <View style={styles.gridForRecs}>
        <FlatList
          style={styles.flatList}
          data={[recs.slice(2)]}
          renderItem={({ item }) => (
            <View style={styles.recRow}>
              {item.map((x, i) => (
                <TouchableOpacity
                  key={i}
                  onPress={() => {
                    handleRecommendation();
                    setEmojis([...emojis, x]);
                  }}
                >
                  <EmojiRec item={x} />
                </TouchableOpacity>
              ))}
              <View style={styles.spacer} />
            </View>
          )}
        />
      </View>
      <View style={styles.footBar}>
        <View style={styles.row}>
          <TouchableOpacity onPress={handleCamera}>
            <AntDesign name="camera" size={36} color="black" />
          </TouchableOpacity>
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
    backgroundColor: "#fc731e", // redish orange
  },
  header: {
    flex: 0,
    alignItems: "center",
    justifyContent: "space-between",
    flexDirection: "row",
    paddingHorizontal: 16,
    gap: 16,
    margin: 30,
    marginBottom: 0,
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
    padding: 0,
  },
  row: {
    flexDirection: "row",
    justifyContent: "flex-start",
    gap: 40,
    flexWrap: "wrap",
  },
  recRow: {
    flexDirection: "row",
    justifyContent: "flex-start",
    gap: 40,
    flexWrap: "wrap",
    marginBottom: 200,
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
    borderColor: "#c9550c",
    borderWidth: 1,
    borderStyle: "solid",
  },
  emojis: {
    gap: 2,
  },
  grid: {
    width: "auto",
    padding: 16,
    margin: 30,
    height: "22%",
    marginBottom: 0,
    borderColor: "#c9550c",
    backgroundColor: "#c9550c",
    borderWidth: 4,
  },
  gridForRecs: {
    width: "100%",
    padding: 16,
    margin: 30,
    height: "100%",
    marginBottom: 40,
    paddingBottom: 40,
  },

  go: {
    position: "absolute",
    right: 30,
    backgroundColor: "#fff",
  },
  delete: {
    position: "absolute",
    right: 80,
    backgroundColor: "#fff",
  },
  footBar: {
    position: "absolute",
    padding: 16,
    width: "100%",
    bottom: 0,
    backgroundColor: "#fff",
    alignItems: "center",
  },
  flatList: {
    margin: 0,
    padding: 0,
  },
  spacer: {
    height: 300,
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
// x button, remove emoji after go
// actual authentication
// fix recommendation
// video and script
