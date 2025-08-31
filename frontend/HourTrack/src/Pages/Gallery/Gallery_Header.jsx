import React from "react";

const GalleryHeader = () => {
  return (
    <div style={styles.headerContainer}>
      <h1 style={styles.title}>Projekty</h1>
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
};

export default GalleryHeader;
