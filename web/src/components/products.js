'use client'

import Image from "next/image"
import Link from "next/link"
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button"

export default function Products({ data, api }) {
  const store = data;
  const [products, setProducts] = useState(store);
  const [value, setValue] = useState("");

  const handleInputChange = (event) => {
    setValue(event.target.value);
  };

  const searchProducts = async () => {
    const response = await fetch(`${api}/search?query=${value}`, {
      method: "POST"
    });

    const data = await response.json();

    setProducts(data);
  }

  const clearSearch = () => {
    setValue("");
    setProducts(store);
  }

  return (
    <div>
      <div>
        <Input placeholder="Search with Gemini..." value={value} onChange={handleInputChange} />
        <Button onClick={searchProducts}>Search</Button>
        <Button onClick={clearSearch}>Clear</Button>
      </div>
      <ul>
        {products.map(product => (
          <Link href={`/products/${product.id}`} >
            <li key={product.id}>
              <Image src={product.image} alt={product.name} width={200} height={200} />
              <h2>{product.name}</h2>
              <p>${product.price}</p>
            </li>
          </Link>
        ))}
      </ul>
    </div>
  )
}
