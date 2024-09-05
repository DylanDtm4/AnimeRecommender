"use client";
import { useEffect, useState } from "react";

const AnimesPage = () => {
  const [genres, setGenres] = useState<string[]>([]);

  useEffect(() => {
    const storedGenres = localStorage.getItem("selectedGenres");
    if (storedGenres) {
      setGenres(JSON.parse(storedGenres));
    }
  }, []);

  return (
    <div>
      <h1>Selected Genres</h1>
      <ul>
        {genres.map((genre: string, index: number) => (
          <li key={index}>{genre}</li>
        ))}
      </ul>
    </div>
  );
};

export default AnimesPage;
