import Product from "@/components/product"

const API_URL = process.env.API_URL ?? 'http://localhost:8000';

async function getData(id) {
  const res = await fetch(`${API_URL}/products/${id}`, { cache: 'no-store' });

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

export default async function page({ params }) {
  const data = await getData(params.slug);

  return (
    <Product product={data} />
  )
}
