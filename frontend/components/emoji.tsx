import { Image } from "expo-image";
import { StyleSheet, Text, View } from "react-native";

const blurhash =
  "|rF?hV%2WCj[ayj[a|j[az_NaeWBj@ayfRayfQfQM{M|azj[azf6fQfQfQIpWXofj[ayj[j[fQayWCoeoeaya}j[ayfQa{oLj?j[WVj[ayayj[fQoff7azayj[ayj[j[ayofayayayj[fQj[ayayj[ayfjj[j[ayjuayj[";

export default function Emoji({
  data,
  size,
  muted,
}: {
  data: string;
  size: number;
  muted?: boolean;
}) {
  if (data.startsWith("https://")) {
    return (
      <View
        style={{
          ...styles.container,
          opacity: muted ? 0.4 : 1,
          height: size,
          width: size,
        }}
      >
        <Image
          style={styles.image}
          source="https://picsum.photos/seed/696/3000/2000"
          placeholder={{ blurhash }}
          contentFit="cover"
          transition={1000}
        />
      </View>
    );
  }

  return (
    <View
      style={{
        ...styles.container,
        opacity: muted ? 0.4 : 1,
        height: size,
        width: size,
      }}
    >
      <Text style={{ fontSize: size / 2 - 2 }}>{data}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "center",
  },
  image: {
    width: "100%",
    height: "100%",
  },
});
