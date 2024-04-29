'use client'

import Image from "next/image"
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";

const api = 'http://localhost:8000/analyze';

export default function Product({ product }) {
  product = product[0];
  const [history, setHistory] = useState([]);
  const [value, setValue] = useState('');

  const handleInputChange = (event) => {
    setValue(event.target.value);
  };

  const askGemini = async () => {
    const url = `${api}?question=${value}`;

    let body;

    if (history.length > 0) {
      body = {
        history
      }
    } else {
      body = {
        product
      }
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    setHistory(data);
    setValue('');
  }

  return (
    <div className="h-screen text-wrap">
      <main className="h-2/3 overflow-y-auto">
        <Image src={product.image} alt={product.name} width={200} height={200} />
        <h1>{product.name}</h1>
        <p>${product.price}</p>
        <p>Category: {product.category}</p>
        <p>About: {product.about}</p>
        <p>Weight: {product.weight}</p>
        <p>Specifications: {product.specifications}</p>
        <p>Details: {product.details}</p>
      </main>
      <div className="h-1/3">
        <div className="h-2/3 overflow-y-auto">
          <ul>
            {history.slice(2).map((item, index) => (
              <li key={index}>
                <p>{item.role === "model" ? "Gemini" : "User"}: {item.parts[0]}</p>
              </li>
            ))}
          </ul>
        </div>
        <div className="h-1/3">
          <Input placeholder="Ask Gemini about this product" value={value} onChange={handleInputChange} />
          <Button onClick={askGemini}>Send</Button>
        </div>
      </div>
    </div>
  )
}
