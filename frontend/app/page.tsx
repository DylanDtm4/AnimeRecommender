"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";

interface Genre {
  ord_id: number;
  name: string;
}

// Skeleton Loader Component
const SkeletonLoader = () => (
  <div>Loading genres...</div> // You can style this as needed
);

function Page() {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("https://anime-api-livid.vercel.app/genres")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((responseData) => {
        const data = responseData.data;
        setGenres(data);
      })
      .catch((error) => {
        setError("Failed to load genres.");
        console.error("Error fetching genres:", error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedGenres([...selectedGenres, value]);
    } else {
      setSelectedGenres(selectedGenres.filter((genre) => genre !== value));
    }
  };

  const isSelected = (name: string) => selectedGenres.includes(name);

  const handleClick = () => {
    // You can perform any actions here before navigating
    console.log("Selected genres:", selectedGenres);
  };

  if (isLoading) {
    return <SkeletonLoader />;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Select Genres</h1>
      <ul>
        {genres.map((genre) => (
          <li key={genre.ord_id}>
            <label htmlFor={genre.name}>{genre.name}</label>
            <input
              type="checkbox"
              id={genre.name}
              name="genre"
              value={genre.name}
              checked={isSelected(genre.name)}
              onChange={handleCheckboxChange}
            />
          </li>
        ))}
      </ul>
      <Link href="/animes" onClick={handleClick}>
        Go to Animes
      </Link>
    </div>
  );
}

export default Page;
