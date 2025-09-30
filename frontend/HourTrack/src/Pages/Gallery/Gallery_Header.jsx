import React from "react";
import PemesLogo from "../../assets/Pemes_logo.png";

const GalleryHeader = ({ result_count }) => {
  return (
    <div
      style={styles.headerContainer}
      className="flex items-center justify-between w-full max-w-[1500px] mx-auto px-4"
    >
      <div className="flex items-center gap-4">
        <h1 style={styles.title}>Projekty</h1>
        <img
          src={PemesLogo}
          alt="Pemes logo"
          style={{ height: 90, marginLeft: -14, marginTop: 20 }}
        />
      </div>
      <span style={styles.count} className="text-right">
        Liczba projektów: {result_count}
      </span>
    </div>
  );
};

const styles = {
  headerContainer: {
    marginBottom: "20px",
  },
  title: {
    fontSize: "50px",
    fontWeight: "bold",
    color: "#333",
  },
  count: {
    fontSize: "21px",
    fontWeight: 500,
    color: "#333",
    marginLeft: "auto",
  },
};

export default GalleryHeader;
