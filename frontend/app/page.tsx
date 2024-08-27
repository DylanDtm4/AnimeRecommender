"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";

interface Genre {
	ord_id: number;
	name: string;
}

function Page() {
	const [genres, setGenres] = useState<Genre[]>([]);
	const [selectedGenres, setSelectedGenres] = useState<string[]>([]);

	useEffect(() => {
		fetch("https://anime-api-livid.vercel.app/genres")
			.then((response) => response.json())
			.then((responseData) => {
				const data = responseData.data;
				setGenres(data);
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
		localStorage.setItem("selectedGenres", JSON.stringify(selectedGenres));
	};

	return (
		<div>
			<h1>Select Genres</h1>
			<ul>
				{genres.map((genre) => (
					<div key={genre.ord_id}>
						<label htmlFor={genre.name}>{genre.name}</label>
						<input
							type="checkbox"
							id={genre.name}
							name="genre"
							value={genre.name}
							checked={isSelected(genre.name)}
							onChange={handleCheckboxChange}
						/>
					</div>
				))}
			</ul>
			<Link href="/animes" onClick={handleClick}>
				Go to Animes
			</Link>
		</div>
	);
}

export default Page;
